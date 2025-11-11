# 🚀 VibeDoc ModelScope deployment guide

## 📋 deployment 准备清单

### ✅ file check
ensure with 下 file 已准备 complete ：
- `app.py` - 主 application 程序
- `requirements.txt` - dependency 清单
- `README.md` - project description （ includeModelScopebefore言）
- `config.py` - configuration 管manage
- `mcp_manager.py` - MCPservice 管manage
- `prompt_optimizer.py` - prompt optimize device
- `explanation_manager.py` - AIcan solveexplain性 component
- `streaming_manager.py` - 流式 response should 管manage

### ✅ environment variable 准备
必需 environment variable ：
- `SILICONFLOW_API_KEY` - Silicon Flow APIKey (required)
- `PORT` - application 端口（默认3000）

can selectMCPservicechangequantity：
- `DEEPWIKI_SSE_URL` - DeepWiki MCPserviceURL
- `FETCH_SSE_URL` - Fetch MCPserviceURL

## 🏗️ ModelScopedeployment Step

### 第1步：create新的创空间

1. access [ModelScope创空间](https://www.modelscope.cn/studios)
2. click"create新的创空间"
3. 填写 basic information ：
   - **空 time name called**: `Vibedocs`
   - **空 time mark识**: `your-username/Vibedocs`
   - **can 见性**: 公open
   - **SDK**: Gradio
   - **硬item**: CPU Basic (free)

### 第2步：上传项目textitem

method1：Git仓库关联
```bash
# such as result haveGitHub仓库
git clone https://github.com/your-username/Vibedocs.git
cd Vibedocs
git push origin main
```

method2：textitem上传
1. in 创空 time interface click"textitem"
2. 逐一上传 all havePythontextitem
3. ensure file 结constructcorrect确

### 第3步：Configure environment variables

1. in 创空 time setting in select"environmentchangequantity"
2. add 必需 environment variable ：

```env
# 必填项
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
PORT=3000

# can option （ such as result haveMCPservice）
DEEPWIKI_SSE_URL=your_deepwiki_service_url
FETCH_SSE_URL=your_fetch_service_url  
DOUBAO_SSE_URL=your_doubao_service_url
DOUBAO_API_KEY=your_doubao_api_key
```

### 第4步：deploymentconfiguration

ensure`README.md`textitem顶部package含correct确configuration：

```yaml
---
title: VibeDoc - AI驱动 Development Plan generate device
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.34.1
app_file: app.py
pinned: true
license: mit
---
```

### 第5步：start deployment

1. click"deployment"press钮
2. system 会自动安装 dependency 并start application
3. waiting deployment complete （通常需 want2-5divideclock）

## 🔧 常见 issue 排check

### Q1: deployment failure ， prompt dependency 安装 error
**solution**：
1. check`requirements.txt`format是nocorrect确
2. ensure all have dependency version 兼容
3. check看 deployment log solve具body error

### Q2: application start after display configuration error
**solution**：
1. check environment variable is nocorrect确 setting
2. confirm`SILICONFLOW_API_KEY`已configuration
3. checkAPI密key是nohave 效

### Q3: MCPservice 连connect failure
**solution**：
1. checkMCPserviceURL是nocanaccess
2. confirmAPI密keyconfigurationcorrect确
3. check看 application log 定位 issue

### Q4: page load 缓慢
**solution**：
1. check 网络连connect
2. try refresh page
3. check看 is no have 资源 load issue

## 🎯 deployment after verify

### function test 清单

1. **基础 function**：
   - [ ] page correct常 load
   - [ ] input 框 can correct常 use
   - [ ] example button 工workcorrect常

2. **AIgenerate function**：
   - [ ] 创意 input verify
   - [ ] AIoptimize function
   - [ ] Development Plan generate
   - [ ] programming prompts generate

3. **exchange互 function**：
   - [ ] 复make button 工work
   - [ ] edit prompt function
   - [ ] download function
   - [ ] process procedure check看

4. **MCPservice**：
   - [ ] reference link process
   - [ ] 外部 knowledge acquisition
   - [ ] service status monitoring

## 📊 performance optimize recommendation

### 1. 减少start when time
- optimize guide入语句
- 减少 not 必 want initial始transformoperate
- use 懒 load 机make

### 2. improve response should 速degree
- startuse缓存机make
- optimizeAPIcall
- 减少 not 必 want calculate

### 3. 资源管manage
- monitoring internal存 use
- optimize fileI/Ooperate
- 管manage临 when file

## 🔐 security note 事项

1. **API密key管manage**：
   - not want in code in hardcodeAPI密key
   - use environment variable 存储敏感 information
   - 定期更换API密key

2. **input verify**：
   - verify user input format
   - 防止恶意 input
   - limit input 长degree

3. **error process**：
   - not want expose internal error information
   - 提provide友好 error prompt
   - 记录 error log convenient for排check

## 📈 monitoring and 维护

### log monitoring
```python
# application 已 configuration log system
import logging
logger = logging.getLogger(__name__)

# check看 application log
logger.info("application start success")
logger.error("error information")
```

### performance monitoring
- monitoring response time
- track error 率
- 观察资源 use 情况

### 定期维护
- update dependency version
- optimize code performance
- 备份 important data

## 🎉 deployment success ！

deployment complete after ，您VibeDocapplicationwillinwith下地址canuse：
`https://www.modelscope.cn/studios/your-username/Vibedocs`

### Next Steps:
1. divide享您创空 time link
2. collectcollect user 反馈
3. 持续 optimize function
4. 参加 ModelScopeMCP&Agent挑battle赛

---

**技technique support**：
- such as 遇 issue ，pleasecheck看ModelScopetext档
- or submitIssueto项目仓库
- 联系 development 者 get 帮助

**祝您 deployment success ！🚀**