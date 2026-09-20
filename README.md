# Proteus Skills

**简体中文** | [English](README.en.md)

<p align="center">
  <img src="images/stm32-hold.gif" alt="按住点灯" width="31%" />
  <img src="images/stm32-toggle.gif" alt="单击切换" width="31%" />
  <img src="images/stm32-dual.gif" alt="双按键独立点灯" width="31%" />
</p>




[![MIT Licensed](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE)

让 AI Agent 通过 Python 创建、编辑和验证真实的 Proteus 电路工程。

本科生，尤其是EE的学生，很容易被Proteus仿真所苦恼，今天，我们带来Proteus的skill！这个skill可以让AI进行proteus的仿真。不要让繁琐的连线和布局困住脑袋里绝妙的想法！


Proteus Skills 提供原理图编辑、单片机仿真、按钮与开关控制、波形读取的工作流。Agent 根据任务调用 [proteus-automatic-api](https://github.com/kudoumakoto6523-design/Proteus_automatic_package)，交付可继续编辑的 `.pdsprj`、验证脚本及实际仿真结果。

本仓库维护 skill 的指令与参考示例；Python 库在独立仓库维护，首次使用时由 Agent 按工作流检查并从官方 GitHub 安装。两者不需要放在相邻目录。

这个库是我一个人完成的，能用，但是有诸多需要完善的地方。如果也有同样被仿真困扰，想要用AI解决，请联系： `kudoumakoto6523@gmail.com`或者微信
<p align="center">
<img src = "images\WechatQR.jpg" width="31%">
</p>

## 环境要求

- **Windows**，已安装 Proteus 及电路所需的器件模型。
- **Python 3.10+**，推荐 3.12；Agent 会检查解释器，缺少时协助安装。无需提前准备库源码或 wheel。
- **Codex/ClaudeCode**：下文提供 Codex 的 skill 安装和调用方式。

当前工作流已在 **Python 3.12 / Proteus 8.16 SP3（8.16.36097）** 上验证。定时仿真和交互控制有 Proteus DLL 版本限制，其他构建的兼容性尚未验证。Proteus 软件、模型、官方样例及第三方固件不随本技能分发；本仓库仅提供原创演示固件。


## 安装

### 1. 安装 skill

在 Codex/ClaudeCode 中发送：

```text
使用 $skill-installer 安装 https://github.com/kudoumakoto6523-design/proteus-skills
仓库根目录就是技能目录，安装名称使用 proteus-skills。
```

也可以手动下载本仓库，将 `SKILL.md`、`agents/`、`references/`、`scripts/` 和 `LICENSE` 放入同一个 `proteus-skills` 文件夹，再放到 Codex 的 `$CODEX_HOME/skills/` 下；默认位置为 `~/.codex/skills/proteus-skills/`。安装后，技能入口应位于 `proteus-skills/SKILL.md`。

### 2. 让 Agent 准备环境并开始任务

安装 skill 后，在下一轮对话中直接发送：

```text
使用 $proteus-skills。我只安装了 Proteus，请先检查 Python 和库环境，
需要时从技能指定的官方 GitHub 仓库安装 proteus-automatic-api，验证后继续任务。
帮我完成一个 STM32 按下按键点亮 LED、松开熄灭的工程。
```


## 使用前准备

向 Agent 提供任务所需的工程或模板、Proteus 程序位置、输出目录；涉及 MCU 时再提供固件和目标引脚。新建电路需要含相应器件定义的模板，例如电阻、电容示例使用官方 `Rescap.pdsprj`。

这些资源使用本机实际路径，输出写入你的工作目录。库的内置路径不会自动适配所有安装位置；路径参数和已知限制见 [SKILL.md](SKILL.md#环境与版本)。


## 能力范围

| 任务 | 支持的工作流 |
| --- | --- |
| 工程编辑 | 新建或打开受支持的 `.pdsprj`，修改元件、属性、位置、连线和端子，保存并重开验证 |
| 连接检查 | 查询器件和引脚，导出 Proteus 原生 SDF 网表，核对网络连接 |
| MCU 仿真 | 检查和加载 ELF / HEX 固件，启停、暂停、按时长运行，读取支持的 GPIO 日志 |
| 按钮与开关 | 绑定二态控件，执行按下、松开、切换，并继续仿真验证下游响应 |
| 波形读取 | 基于已有图表和探针导出 CSV，读取电压、电流和采样值 |



## 仓库内容

| 文件 | 用途 |
| --- | --- |
| [examples/stm32](examples/stm32) | 三个按钮与 LED 场景的原创固件源码、HEX 和构建脚本 |
| [images](images) | README 演示 GIF 的统一目录 |
| [scripts/ensure_library.py](scripts/ensure_library.py) | 自动检查、安装或更新库，返回后续任务使用的 Python 路径 |
| [SKILL.md](SKILL.md) | Agent 的技能入口、任务选择、操作顺序和验证要求 |
| [agents/openai.yaml](agents/openai.yaml) | Codex 中的显示名称和简短说明 |
| [references/api-workflows.md](references/api-workflows.md) | 工程编辑、网表、固件和测量示例 |
| [references/interactive-controls.md](references/interactive-controls.md) | 按钮与开关的绑定、时序和响应验证 |
| [references/distribution.md](references/distribution.md) | 库的安装、版本匹配、迁移和独立分发约定 |
| [references/evidence-contract.md](references/evidence-contract.md) | 区分结构验证、运行验证和阻断结果的证据约定 |

### 验证证据

SDF 或文件重开成功不等于仿真成功。交付前可以用
`py -3.12 scripts/validate_evidence.py verification.json` 检查证据清单；需要
真实运行结果时加上 `--require-runtime`。校验器会拒绝带运行时错误的
`runtime_verified` 声明，并保留 `blocked` / `not_run` 状态。

## 许可证

本仓库的原创技能文档和示例采用 [MIT License](LICENSE)。Python 库单独分发；Proteus 软件、器件模型、第三方样例和固件适用各自的许可证。
