# 🚀 VibeDoc: Your PersonalAIProduct Manager与架构师

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-5.34.1-orange)](https://gradio.app/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<div align="center">

**60-180秒， will 创意转化 for complete development plan**

Your PersonalAIProduct Manager与架构师，智能generatetechnical documentation、architecture diagram表和AIprogramming prompts

[🌐 online experience](https://modelscope.cn/studios/JasonRobert/Vibedocs) | [🎬 演示视频](https://www.bilibili.com/video/BV1ieagzQEAC/) | [🤝 参 with 贡献](./CONTRIBUTING.md) | [💬 讨论社区](https://github.com/JasonRobertDestiny/VibeDoc/discussions) | [English](./README.md)

</div>

---

## ✨ why select VibeDoc？

As a developer, product manager or entrepreneur, have you encountered these problems:

- 💭 **Have good ideas but don't know how to plan?** 想法很多，但不知道如何转化为可执行的Development Plan
- ⏰ **documentation 编写 consume when 太长？** 写Technical Solution、架构文档要花费大量when time
- 🤖 **AIDon't know how to use tools?** 想用AI辅助 programming，但不知道如何写好prompt词
- 📊 **Missing professional charts?** 需要architecture diagram、流程图、甘特 diagram，但不熟悉画图tool

**VibeDoc One-stop solution!**

![VibeDoc主 interface](./image/vibedoc.png)

## 🎯 core function

### 📋 intelligent Development Plan generate

input 产品创意，AIin60-180秒内自动generatecomplete Development Plan：

- **Product Overview** - 项目背景、目标 user、核心价值
- **Technical Solution** - tech stack选型、architecture design、技术对比
- **Development Plan** - 分phase实施计划、when time安排、人力configuration
- **deployment plan** - environment configuration、CI/CD流程、运维监控
- **promotion strategy** - 市场定位、运营recommendation、增长策略

### 🤖 AIprogramming prompts generate

for 每个 function module generate can 直接 useAIprogramming prompts，support：

- ✅ **Claude** - code generate 、 architecture design
- ✅ **GitHub Copilot** - intelligent code 补全
- ✅ **ChatGPT** - 技术咨询、 code optimize
- ✅ **Cursor** - AI辅助 programming

![AIprogramming prompts](./image/1.png)

### 📊 can 视化 diagram 表自动 generate

use Mermaid 自动generate专业diagram 表：

- 🏗️ **system architecture diagram** - 清晰展示系统组件关系
- 📈 **business process diagram** - 可视化业务逻辑
- 📅 **甘特 diagram** - 项目when time规划一目了然
- 📊 **技术 to 比表** - 技术选型决策reference

### 📁 多 format documentation 导出

One-click export to meet different scenario needs:

- **Markdown** (.md) - 适合 version 控制、GitHub展示
- **Word** (.docx) - 商务 documentation 、 project 汇报
- **PDF** (.pdf) - official 提案、打印归档
- **HTML** (.html) - 网页展示、 online 分享

![generate example](./image/2.png)

## 💡 真 actual 案例展示

### input 创意
```
development 一款AR手语翻译application，能够实时将手语翻译成语音和文字，
At the same time, it can translate voice and text into sign language actions, inAR形式展示
```

### generate 结果

**📄 [查看 complete Development Plan](./HandVoice_Development_Plan.md)** (1万+字)

AIgenerate complete plan including ：

#### 1. **Product Overview**
- Target users (deaf and mute people, medical workers, educators)
- Core functions (real-time translation, multi-language support,AR可视化）
- 市场定位 and 竞品分析

#### 2. **技术 architecture**
complete system architecture diagram ， including ：
- user interface component
- backend service
- machine learning model integration
- database design
- AR渲染管 line

#### 3. **tech stack**
- **frontend**：React Native（跨平台）
- **backend**：Node.js + Express
- **machine learning**：TensorFlow 手语识别 model
- **Natural Language Processing**：spaCy
- **ARdisplay**：ARKit (iOS) / ARCore (Android)
- **database**：MongoDB

#### 4. **development when time 表**
6个月计划，分3个主要里程碑：
- **第1-2月**：核心识别与翻译引擎
- **第3-4月**：ARintegration与UI开发
- **第5-6月**：test、optimize与deployment

#### 5. **12+个AIprogramming prompts**
每个 function moduleready-to-useprompt词。示例：

```
function ：手势识别 model

Context:
构建 actual when 手势识别 system 用于手语翻译。
需 want 检测 and 分 class 手部 location 、动作 and 面部表情。

requirement ：
- process30+ FPS的视频帧
- 识别500+种手语手势
- support 连续手势序列
- process not 同光照条件

tech stack ：
- TensorFlow/Keras model training
- MediaPipe 手部 key 点检测
- OpenCV diagram 像预 process

constraint 条件：
- 必须 in 移动设备运行 (iOS/Android)
- model 大小 < 50MB 用于移动deployment
- inference when time < 100ms 每帧

期望 output ：
- model architecture code
- training 管道
- data 预 process function
- 移动端 optimize 策略
```

## 🚀 快速 start

### 🌐 online experience （推荐）

**👉 [立即 experience VibeDoc](https://modelscope.cn/studios/JasonRobert/Vibedocs)** - 无需安装，打开即用！

experience complete function ：
1. input 您产品创意（ for example ："开发一个智能健身APP"）
2. can 选填写 reference link （帮助AIget更多上下文）
3. click generate ， waiting60-180秒
4. 查看 complete development plan andAIprogramming prompts
5. One-click export asMarkdown/Word/PDF/HTMLformat

### 💻 this 地 deployment

#### environment requirement

- Python 3.11+
- pip 包管理器
- [SiliconFlow API Key](https://siliconflow.cn) (免费 get)

#### 安装 Step

```bash
# 1. clone project
git clone https://github.com/JasonRobertDestiny/VibeDoc.git
cd VibeDoc

# 2. create 虚拟 environment （推荐）
python -m venv venv

# 激活虚拟 environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装 dependency
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# edit .env 文件，add你的 API Key
```

### configuration description

in `.env` 文件中configuration：

```env
# 必填：SiliconFlow API Key（免费注册get）
SILICONFLOW_API_KEY=your_api_key_here

# Optional: advanced configuration
API_TIMEOUT=300
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### 运行 application

```bash
python app.py
```

application will in with 下 address 启动：
- this 地 access: http://localhost:7860
- 网络 access: http://0.0.0.0:7860

### 🐳 Docker deployment （ can 选）

```bash
# 构建镜像
docker build -t vibedoc .

# 运行容器
docker run -p 7860:7860 \
  -e SILICONFLOW_API_KEY=your_key \
  vibedoc
```

## 🏗️ 技术 architecture

VibeDoc 采用 module 化 architecture design ：

```
┌─────────────────────────────────────────┐
│         Gradio Web Interface            │
│  (user 交互 + UI渲染 + 文件导出)           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       核心 process 引擎 (app.py)              │
├─────────────────────────────────────────┤
│  • input verify with optimize                        │
│  • AIgenerate 协调                           │
│  • content quality 控制                          │
│  • 多 format 导出                            │
└──┬────────┬──────────┬─────────┬────────┘
   │        │          │         │
   ▼        ▼          ▼         ▼
┌──────┐ ┌────────┐ ┌──────┐ ┌──────────┐
│AImodel│ │prompt词  │ │content  │ │导出      │
│integration  │ │optimize器  │ │verify  │ │管理器    │
└──────┘ └────────┘ └──────┘ └──────────┘
```

### 核心 tech stack

- **frontend interface**: Gradio 5.34.1 - 快速构建AIapplication界面
- **AImodel**: Qwen2.5-72B-Instruct - 阿里云通义千问大model
- **diagram 表渲染**: Mermaid.js - 代码化generate专业diagram 表
- **documentation 导出**: python-docx, reportlab - 多formatsupport
- **asynchronous process**: asyncio, aiofiles - 高性能asynchronous process

## 📊 performance 指标

| 指标 | 表现 |
|------|------|
| **generate 速度** | 60-180秒完成complete plan |
| **success 率** | >95% generatesuccess 率 |
| **content quality** | 平均quality 分 85/100 |
| **support format** | 4种专业documentation format |

## 🎨 use 场景

### 👨‍💻 development 者
- ✅ 快速 verify Technical Solution can 行性
- ✅ generate project technical documentation
- ✅ getAI编程辅助prompt词
- ✅ 学习最佳 architecture actual 践

### 📊 Product Manager
- ✅ will requirement 转化 for Technical Solution
- ✅ generate project 规划 documentation
- ✅ 估算 development 周期 and 资源
- ✅ 制作 project 提案PPT

### 🎓 学生 & 学习者
- ✅ 学习软件 development 最佳 actual 践
- ✅ 解技术 architecture design
- ✅ 准备技术面试
- ✅ complete 毕业 design 规划

### 🚀 创业者
- ✅ 快速 verify 产品创意
- ✅ generate Technical Solution 给投资人
- ✅ 规划MVP开发路线
- ✅ assessment 技术 implementation 成 this

## 🤝 参 with 贡献

我们欢迎 all have 形式贡献！无论 is ：

- 🐛 报告 Bug
- 💡 提出新 function recommendation
- 📝 改进 documentation
- 🔧 submit code

### 贡献 Step

1. Fork this project
2. create 特性分支 (`git checkout -b feature/AmazingFeature`)
3. submit 更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送 to 分支 (`git push origin feature/AmazingFeature`)
5. submit Pull Request

detailed guide 请查看 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📝 development documentation

- [user guide](./USER_GUIDE.md) - 详细Usage Instructions
- [technical documentation](./CLAUDE.md) - 代码架构和开发指南
- [deployment guide](./DEPLOYMENT.md) - 生产环境deployment
- [security 策略](./SECURITY.md) - 安全最佳实践

## 🎯 路 line diagram

### v2.1 (计划 in)
- [ ] support 更多AImodel（GPT-4, Claude等）
- [ ] 团队协作 function
- [ ] plan version 管理
- [ ] online edit 器

### v2.2 (计划 in)
- [ ] 移动端适配
- [ ] 多语言 support （英文、日文）
- [ ] template 市场
- [ ] APIinterface

## 🙏 致谢

- **Qwen2.5-72B-Instruct** by Alibaba Cloud - 强大AI能力
- **Gradio** - 优秀Web框架
- **SiliconFlow** - 稳定APIservice
- all have 贡献者 and user ❤️

## 📄 开源协议

this project 采用 [MIT License](LICENSE) 开源协议

## 📞 联系 method

- **issue 反馈**: [GitHub Issues](https://github.com/JasonRobertDestiny/VibeDoc/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/JasonRobertDestiny/VibeDoc/discussions)
- **邮箱**: johnrobertdestiny@gmail.com
- **演示视频**: [Bilibili](https://www.bilibili.com/video/BV1ieagzQEAC/)

## ⭐ Star History

such as 果这个 project to 您 have 帮助，请给我们一个 Star ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=JasonRobertDestiny/VibeDoc&type=Date)](https://star-history.com/#JasonRobertDestiny/VibeDoc&Date)

---

<div align="center">

**🚀 用AI赋能每一个创意**

Made with ❤️ by the VibeDoc Team

</div>
