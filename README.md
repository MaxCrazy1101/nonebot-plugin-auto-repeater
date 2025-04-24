<!-- markdownlint-disable MD033 MD036 MD041 MD046 -->
<div align="center">
<p align="center">
  <a><img src="./docs/logo.gif"></a>
</p>
</div>

<div align="center">

  # Auto Repeater
  ✨ 基于[NoneBot2](https://github.com/nonebot/nonebot2)的插件，群聊自动复读机 ✨


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/MaxCrazy1101/nonebot-plugin-auto-repeater.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-auto-repeater">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-auto-repeater.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<br>
<a href="https://results.pre-commit.ci/latest/github/MaxCrazy1101/nonebot-plugin-auto-repeater/main">
    <img src="https://results.pre-commit.ci/badge/github/MaxCrazy1101/nonebot-plugin-auto-repeater/main.svg" alt="pre-commit.ci status">
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-auto-repeater:nonebot_plugin_auto_repeater">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-example" alt="NoneBot Registry" />
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
<a href="https://github.com/astral-sh/ruff">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://www.codefactor.io/repository/github/MaxCrazy1101/nonebot-plugin-auto-repeater"><img src="https://www.codefactor.io/repository/github/MaxCrazy1101/nonebot-plugin-auto-repeater/badge" alt="CodeFactor" />
</a>
</div>

## 📖 介绍

连续发送2条相同消息，机器人就会自动+1。包括普通消息，QQ表情，还有图片（表情包）。支持图片夹文字和表情夹文字的消息!


参考于[nonebot-plugin-repeater](https://github.com/ninthseason/nonebot-plugin-repeater)插件。

使用字符串相似度判断是否自动+1，Maybe有BUG。

支持复读跟随撤回功能，防止有人使用机器人复读功能爆破账号。

## 💿 安装
依赖插件:

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-auto-repeater

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-auto-repeater
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-auto-repeater
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-auto-repeater
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-auto-repeater
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_auto_repeater"]

</details>

## ⚙️ 配置

### 配置表

在 nonebot2 项目的`.env`文件中修改配置项

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| repeat_interval | 否 | 无 | 相同消息相隔多久复读一次 |
| repeat_default_mode | 否 | True | 在群聊中是否默认启用 |


## 🎉 使用

> [!NOTE]
> 记得使用[命令前缀](https://nonebot.dev/docs/appendices/config#command-start-%E5%92%8C-command-separator)哦

### 🪧 指令表

| 指令 | 权限 | 参数 | 说明 |
|:-----:|:----:|:----:|:----:|
| 自动复读 | 管理员、群主和Superuser | "开启"/"关闭" | 控制机器人在当前群是否进行复读 |


***
## 等待实现
- 多条消息复读
- Recall功能开关
- 图片使用hash比较,提高准确性
***
