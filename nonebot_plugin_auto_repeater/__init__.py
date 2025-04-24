import time
from difflib import SequenceMatcher
from importlib.metadata import version

from nonebot import logger, require
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_message, on_notice

try:
    from nonebot.adapters.onebot.v11 import (
        Bot,
        GroupMessageEvent,
        GroupRecallNoticeEvent,
        Message,
    )
    from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER

except ModuleNotFoundError as _:
    try:
        from nonebot.adapters.cqhttp import (  # type: ignore
            Bot,
            GroupMessageEvent,
            GroupRecallNoticeEvent,
            Message,
        )
        from nonebot.adapters.cqhttp.permission import (  # type: ignore
            GROUP_ADMIN,
            GROUP_OWNER,
        )
    except ModuleNotFoundError as _:
        raise ImportError("No support adapter find! Abort load!")

from nonebot.plugin import PluginMetadata

from .config import Config
from .data_source import Repeater

try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except RuntimeError:
    logger.error("Not find nonebot_plugin_apscheduler!Please install it!Abort Load!")
    raise ModuleNotFoundError

try:
    __version__ = version("nonebot_plugin_auto_repeater")
except Exception:
    __version__ = "0.0.0"

repeater = Repeater()

__plugin_meta__ = PluginMetadata(
    name="自动复读",
    description="自动复读",
    usage="连续两条一样的消息将自动复读",
    config=Config,
    extra={
        "author": "MaxCrazy1101",
        "version": __version__,
    },
)

on_repeater_config = on_command(
    "自动+1设置",
    aliases={"自动复读", "自动复读设置"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
)


MESSAGE_OPTIONS = ["关闭", "开启"]


@on_repeater_config.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text()
    group_id = event.group_id
    now_state = 1 if repeater.is_enable(group_id) else 0
    now_mode = MESSAGE_OPTIONS[now_state]
    if not text or text not in MESSAGE_OPTIONS:
        await on_repeater_config.finish(
            f"没有输入需要设置的模式或输入有误！当前模式为{now_mode}!"
        )
    new_index = MESSAGE_OPTIONS.index(text)
    if new_index == now_state:
        await on_repeater_config.finish(f"当前模式已经为{now_mode}")
    repeater.set_mode(group_id, True if new_index == 1 else False)
    await on_repeater_config.finish(
        f"设置成功！设置自动复读功能为：{MESSAGE_OPTIONS[new_index]}"
    )


message_list: dict[int, list] = {}
repeat_after_message: list[dict] = []
sender_message_detail: dict[int, dict] = {}

auto_repeat = on_message(block=False, priority=99)


@auto_repeat.handle()
async def _(event: GroupMessageEvent):
    global message_list, repeat_after_message, sender_message_detail
    group_id = event.group_id
    if not repeater.is_enable(group_id):
        await auto_repeat.finish()

    event_msg = event.get_message()

    # 将当前消息与历史复读比较
    for msg in repeat_after_message:
        if msg["group_id"] == group_id:
            if check_similarity(event_msg, msg["msg"]):
                return

    for msg in event_msg:  # msg 是 MessageSegment
        if msg.type not in ["text", "image", "face"]:
            logger.info("Other Type Message Ignore!")
            return

    # --------- 消息匹配处理 ----------
    if group_id not in message_list:
        message_list[group_id] = []

    if len(message_list[group_id]) < 1:
        message_list[group_id].append(event_msg)
    else:  # 判断是否需要复读
        # 对不同消息类型应用不同的相似度比较方法
        message_list[group_id].append(event_msg)
        last_msg = message_list[group_id][0]

        if check_similarity(event_msg, last_msg):  # 复读
            repeater_msg = Message(str(event_msg))
            repeat_after_message.append(
                {"group_id": group_id, "msg": repeater_msg, "time": time.time()}
            )
            message_list[group_id] = []

            try:
                msg_id = await auto_repeat.send(repeater_msg)
            except Exception as e:
                logger.error("复读失败！" + str(e))
            if event.message_id not in sender_message_detail:
                sender_message_detail[event.message_id] = {
                    "message_id": msg_id["message_id"],
                    "time": time.time(),
                }
        else:
            message_list[group_id].pop(0)

    await auto_repeat.finish()


def check_similarity(event_msg: Message, last_msg: Message):
    f_sim = True
    if len(event_msg) == len(last_msg):
        for e_msg, l_msg in zip(event_msg, last_msg):
            if e_msg.type != l_msg.type:
                f_sim = False
                break
            if e_msg.type == "text" or e_msg.type == "face":
                match_ratio = SequenceMatcher(None, str(e_msg), str(l_msg)).quick_ratio()
                if match_ratio < 0.90:
                    f_sim = False
                    break
            elif e_msg.type == "image":
                # TODO:优化图片比较方式
                if e_msg.data["filename"] != l_msg.data["filename"]:
                    f_sim = False
                    break
    else:
        f_sim = False
    return f_sim


recall = on_notice(block=True)  # 跟随撤回


@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    global sender_message_detail
    if event.message_id in sender_message_detail:
        if abs(sender_message_detail[event.message_id]["time"] - time.time()) < (60 + 59):
            try:
                await bot.delete_msg(
                    message_id=sender_message_detail[event.message_id]["message_id"]
                )
            except Exception as e:
                logger.error(f"复读自动跟随撤回失败||{e}")
        sender_message_detail.pop(event.message_id)
    await recall.finish()


@scheduler.scheduled_job("interval", seconds=30, jitter=5, id="repeater_cleaner")
async def _():
    global repeat_after_message, sender_message_detail
    for repeat_msg in repeat_after_message:
        if abs(int(time.time() - repeat_msg["time"])) > repeater.repeat_interval:
            repeat_after_message.remove(repeat_msg)
    temp = []
    for key, values in sender_message_detail.items():
        if abs(int(time.time() - values["time"])) > 179:
            temp.append(key)
    for key in temp:
        sender_message_detail.pop(key)
    return
