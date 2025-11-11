# 🚀 VibeDoc: Your PersonalAIProduct Managerandarchitect

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-5.34.1-orange)](https://gradio.app/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<div align="center">

**60-180seconds， will 创意转transform for complete development plan**

Your PersonalAIProduct Managerandarchitect，智能generatetechnical documentation、architecture diagramtable和AIprogramming prompts

[🌐 online experience](https://modelscope.cn/studios/JasonRobert/Vibedocs) | [🎬 演示view频](https://www.bilibili.com/video/BV1ieagzQEAC/) | [🤝 参 with 贡献](./CONTRIBUTING.md) | [💬 讨论社区](https://github.com/JasonRobertDestiny/VibeDoc/discussions) | [English](./README.md)

</div>

---

## ✨ why select VibeDoc？

As a developer, product manager or entrepreneur, have you encountered these problems:

- 💭 **Have good ideas but don't know how to plan?** 想法很多，但not知道如what转transform为can执行的Development Plan
- ⏰ **documentation 编写 consume when 太长？** 写Technical Solution、architecturetext档important花费大quantitywhen time
- 🤖 **AIDon't know how to use tools?** 想useAI辅助 programming，但not知道如what写好prompt词
- 📊 **Missing professional charts?** 需importantarchitecture diagram、流程图、gan特 diagram，但not熟悉画图tool

**VibeDoc One-stop solution!**

![VibeDoc主 interface](./image/vibedoc.png)

## 🎯 core function

### 📋 intelligent Development Plan generate

input 产品创意，AIin60-180secondsinternal自动generatecomplete Development Plan：

- **Product Overview** - 项目背scene、目mark user、核心价值
- **Technical Solution** - tech stackselect型、architecture design、技technique对比
- **Development Plan** - dividephase实施calculate划、when time安排、人力configuration
- **deployment plan** - environment configuration、CI/CD流程、运维监控
- **promotion strategy** - 市场定位、运营recommendation、增长策略

### 🤖 AIprogramming prompts generate

for 每个 function module generate can direct useAIprogramming prompts，support：

- ✅ **Claude** - code generate 、 architecture design
- ✅ **GitHub Copilot** - intelligent code 补全
- ✅ **ChatGPT** - 技technique咨询、 code optimize
- ✅ **Cursor** - AI辅助 programming

![AIprogramming prompts](./image/1.png)

### 📊 can viewtransform diagram table自动 generate

use Mermaid 自动generate专业diagram table：

- 🏗️ **system architecture diagram** - 清晰expand示系统groupitem关系
- 📈 **business process diagram** - canviewtransform业务逻辑
- 📅 **gan特 diagram** - 项目when time规划一目了然
- 📊 **技technique to 比table** - 技techniqueselect型决策reference

### 📁 多 format documentation guideout

One-click export to meet different scenario needs:

- **Markdown** (.md) - 适合 version 控make、GitHubexpand示
- **Word** (.docx) - 商务 documentation 、 project 汇报
- **PDF** (.pdf) - official 提plan、hit印归档
- **HTML** (.html) - 网页expand示、 online divide享

![generate example](./image/2.png)

## 💡 真 actual caseexpand示

### input 创意
```
development 一款AR手语翻译application，能够实timewill手语翻译成语音和text字，
At the same time, it can translate voice and text into sign language actions, inAR形式expand示
```

### generate 结result

**📄 [check看 complete Development Plan](./HandVoice_Development_Plan.md)** (1万+字)

AIgenerate complete plan including ：

#### 1. **Product Overview**
- Target users (deaf and mute people, medical workers, educators)
- Core functions (real-time translation, multi-language support,ARcanviewtransform）
- 市场定位 and 竞品analyze

#### 2. **技technique architecture**
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

#### 4. **development when time table**
6个月calculate划，divide3个主important里程碑：
- **第1-2月**：核心识别and翻译引擎
- **第3-4月**：ARintegrationandUIdevelopment
- **第5-6月**：test、optimizeanddeployment

#### 5. **12+个AIprogramming prompts**
每个 function moduleready-to-useprompt词。示例：

```
function ：手trend识别 model

Context:
construct建 actual when 手trend识别 system use于手语翻译。
需 want detect and divide class 手部 location 、动work and 面部table情。

requirement ：
- process30+ FPS的view频帧
- 识别500+种手语手trend
- support 连续手trend序列
- process not 同光照条item

tech stack ：
- TensorFlow/Keras model training
- MediaPipe 手部 key 点detect
- OpenCV diagram 像预 process

constraint 条item：
- 必须 in 移动set备运行 (iOS/Android)
- model 大small < 50MB use于移动deployment
- inference when time < 100ms 每帧

期望 output ：
- model architecture code
- training 管道
- data 预 process function
- 移动端 optimize 策略
```

## 🚀 快速 start

### 🌐 online experience （push荐）

**👉 [立即 experience VibeDoc](https://modelscope.cn/studios/JasonRobert/Vibedocs)** - 无需安装，hitopen即use！

experience complete function ：
1. input 您产品创意（ for example ："development一个智能健身APP"）
2. can select填写 reference link （帮助AIget更多上下text）
3. click generate ， waiting60-180seconds
4. check看 complete development plan andAIprogramming prompts
5. One-click export asMarkdown/Word/PDF/HTMLformat

### 💻 this 地 deployment

#### environment requirement

- Python 3.11+
- pip package管managedevice
- [SiliconFlow API Key](https://siliconflow.cn) (free get)

#### 安装 Step

```bash
# 1. clone project
git clone https://github.com/JasonRobertDestiny/VibeDoc.git
cd VibeDoc

# 2. create 虚拟 environment （push荐）
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
# edit .env textitem，add你的 API Key
```

### configuration description

in `.env` textitem中configuration：

```env
# 必填：SiliconFlow API Key（free注册get）
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

application will in with 下 address start：
- this 地 access: http://localhost:7860
- 网络 access: http://0.0.0.0:7860

### 🐳 Docker deployment （ can select）

```bash
# construct建镜像
docker build -t vibedoc .

# 运行容device
docker run -p 7860:7860 \
  -e SILICONFLOW_API_KEY=your_key \
  vibedoc
```

## 🏗️ 技technique architecture

VibeDoc 采use module transform architecture design ：

```
┌─────────────────────────────────────────┐
│         Gradio Web Interface            │
│  (user exchange互 + UI渲染 + textitemguideout)           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       核心 process 引擎 (app.py)              │
├─────────────────────────────────────────┤
│  • input verify with optimize                        │
│  • AIgenerate 协调                           │
│  • content quality 控make                          │
│  • 多 format guideout                            │
└──┬────────┬──────────┬─────────┬────────┘
   │        │          │         │
   ▼        ▼          ▼         ▼
┌──────┐ ┌────────┐ ┌──────┐ ┌──────────┐
│AImodel│ │prompt词  │ │content  │ │guideout      │
│integration  │ │optimizedevice  │ │verify  │ │管managedevice    │
└──────┘ └────────┘ └──────┘ └──────────┘
```

### 核心 tech stack

- **frontend interface**: Gradio 5.34.1 - 快速construct建AIapplication界面
- **AImodel**: Qwen2.5-72B-Instruct - 阿里云通义千问大model
- **diagram table渲染**: Mermaid.js - 代码transformgenerate专业diagram table
- **documentation guideout**: python-docx, reportlab - 多formatsupport
- **asynchronous process**: asyncio, aiofiles - 高性能asynchronous process

## 📊 performance pointmark

| pointmark | table现 |
|------|------|
| **generate 速degree** | 60-180secondscompletecomplete plan |
| **success 率** | >95% generatesuccess 率 |
| **content quality** | 平均quality divide 85/100 |
| **support format** | 4种专业documentation format |

## 🎨 use 场scene

### 👨‍💻 development 者
- ✅ 快速 verify Technical Solution can 行性
- ✅ generate project technical documentation
- ✅ getAI编程辅助prompt词
- ✅ learn习最佳 architecture actual 践

### 📊 Product Manager
- ✅ will requirement 转transform for Technical Solution
- ✅ generate project 规划 documentation
- ✅ 估calculate development 周期 and 资源
- ✅ makework project 提planPPT

### 🎓 learn生 & learn习者
- ✅ learn习软item development 最佳 actual 践
- ✅ solve技technique architecture design
- ✅ 准备技technique面试
- ✅ complete 毕业 design 规划

### 🚀 创业者
- ✅ 快速 verify 产品创意
- ✅ generate Technical Solution 给投资人
- ✅ 规划MVPdevelopment路线
- ✅ assessment 技technique implementation 成 this

## 🤝 参 with 贡献

我们欢迎 all have 形式贡献！无论 is ：

- 🐛 报notify Bug
- 💡 提out新 function recommendation
- 📝 改进 documentation
- 🔧 submit code

### 贡献 Step

1. Fork this project
2. create 特性divide支 (`git checkout -b feature/AmazingFeature`)
3. submit 更改 (`git commit -m 'Add some AmazingFeature'`)
4. push送 to divide支 (`git push origin feature/AmazingFeature`)
5. submit Pull Request

detailed guide pleasecheck看 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📝 development documentation

- [user guide](./USER_GUIDE.md) - 详细Usage Instructions
- [technical documentation](./CLAUDE.md) - 代码architecture和developmentpoint南
- [deployment guide](./DEPLOYMENT.md) - 生产environmentdeployment
- [security 策略](./SECURITY.md) - 安全最佳实践

## 🎯 路 line diagram

### v2.1 (calculate划 in)
- [ ] support 更多AImodel（GPT-4, Claude等）
- [ ] 团队协work function
- [ ] plan version 管manage
- [ ] online edit device

### v2.2 (calculate划 in)
- [ ] 移动端适配
- [ ] 多语言 support （英text、daytext）
- [ ] template 市场
- [ ] APIinterface

## 🙏 致谢

- **Qwen2.5-72B-Instruct** by Alibaba Cloud - 强大AI能力
- **Gradio** - excellent秀Web框架
- **SiliconFlow** - 稳定APIservice
- all have 贡献者 and user ❤️

## 📄 open源协议

this project 采use [MIT License](LICENSE) open源协议

## 📞 联系 method

- **issue 反馈**: [GitHub Issues](https://github.com/JasonRobertDestiny/VibeDoc/issues)
- **讨论exchange流**: [GitHub Discussions](https://github.com/JasonRobertDestiny/VibeDoc/discussions)
- **邮箱**: johnrobertdestiny@gmail.com
- **演示view频**: [Bilibili](https://www.bilibili.com/video/BV1ieagzQEAC/)

## ⭐ Star History

such as result这个 project to 您 have 帮助，please给我们一个 Star ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=JasonRobertDestiny/VibeDoc&type=Date)](https://star-history.com/#JasonRobertDestiny/VibeDoc&Date)

---

<div align="center">

**🚀 useAI赋能每一个创意**

Made with ❤️ by the VibeDoc Team

</div>
