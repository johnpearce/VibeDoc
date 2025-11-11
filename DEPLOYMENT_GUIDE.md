# 🚀 VibeDoc ModelScope deployment guide

## 📋 deployment 准备清单

### ✅ file check
ensure with 下 file 已准备 complete ：
- `app.py` - 主 application 程序
- `requirements.txt` - dependency 清单
- `README.md` - project description （ includeModelScope前言）
- `config.py` - configuration 管理
- `mcp_manager.py` - MCPservice 管理
- `prompt_optimizer.py` - prompt optimize 器
- `explanation_manager.py` - AIcan 解释性 component
- `streaming_manager.py` - 流式 response should 管理

### ✅ environment variable 准备
必需 environment variable ：
- `SILICONFLOW_API_KEY` - Silicon Flow APIKey (required)
- `PORT` - application 端口（默认3000）

can 选MCPservice变量：
- `DEEPWIKI_SSE_URL` - DeepWiki MCPserviceURL
- `FETCH_SSE_URL` - Fetch MCPserviceURL

## 🏗️ ModelScopedeployment Step

### 第1步：create新的创空间

1. access [ModelScope创空间](https://www.modelscope.cn/studios)
2. click"create新的创空间"
3. 填写 basic information ：
   - **空 time name 称**: `Vibedocs`
   - **空 time 标识**: `your-username/Vibedocs`
   - **can 见性**: 公开
   - **SDK**: Gradio
   - **硬件**: CPU Basic (免费)

### 第2步：上传项目文件

method1：Git仓库关联
```bash
# such as 果 haveGitHub仓库
git clone https://github.com/your-username/Vibedocs.git
cd Vibedocs
git push origin main
```

method2：文件上传
1. in 创空 time interface click"文件"
2. 逐一上传 all havePython文件
3. ensure file 结构正确

### 第3步：Configure environment variables

1. in 创空 time setting in select"环境变量"
2. add 必需 environment variable ：

```env
# 必填项
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
PORT=3000

# can option （ such as 果 haveMCPservice）
DEEPWIKI_SSE_URL=your_deepwiki_service_url
FETCH_SSE_URL=your_fetch_service_url  
DOUBAO_SSE_URL=your_doubao_service_url
DOUBAO_API_KEY=your_doubao_api_key
```

### 第4步：deploymentconfiguration

ensure`README.md`文件顶部包含正确configuration：

```yaml
---
title: VibeDoc - AI驱动 Development Plan generate 器
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

### 第5步：启动 deployment

1. click"deployment"按钮
2. system 会自动安装 dependency 并启动 application
3. waiting deployment complete （通常需 want2-5分钟）

## 🔧 常见 issue 排查

### Q1: deployment failure ， prompt dependency 安装 error
**solution**：
1. check`requirements.txt`format是否正确
2. ensure all have dependency version 兼容
3. 查看 deployment log 解具体 error

### Q2: application 启动 after display configuration error
**solution**：
1. check environment variable is 否正确 setting
2. confirm`SILICONFLOW_API_KEY`已configuration
3. checkAPI密钥是否have 效

### Q3: MCPservice 连接 failure
**solution**：
1. checkMCPserviceURL是否可access
2. confirmAPI密钥configuration正确
3. 查看 application log 定位 issue

### Q4: page load 缓慢
**solution**：
1. check 网络连接
2. try refresh page
3. 查看 is 否 have 资源 load issue

## 🎯 deployment after verify

### function test 清单

1. **基础 function**：
   - [ ] page 正常 load
   - [ ] input 框 can 正常 use
   - [ ] example button 工作正常

2. **AIgenerate function**：
   - [ ] 创意 input verify
   - [ ] AIoptimize function
   - [ ] Development Plan generate
   - [ ] programming prompts generate

3. **交互 function**：
   - [ ] 复制 button 工作
   - [ ] edit prompt function
   - [ ] download function
   - [ ] process procedure 查看

4. **MCPservice**：
   - [ ] reference link process
   - [ ] 外部 knowledge acquisition
   - [ ] service status monitoring

## 📊 performance optimize recommendation

### 1. 减少启动 when time
- optimize 导入语句
- 减少 not 必 want 初始化操作
- use 懒 load 机制

### 2. improve response should 速度
- 启用缓存机制
- optimizeAPIcall
- 减少 not 必 want 计算

### 3. 资源管理
- monitoring 内存 use
- optimize fileI/O操作
- 管理临 when file

## 🔐 security note 事项

1. **API密钥管理**：
   - not want in code in hardcodeAPI密钥
   - use environment variable 存储敏感 information
   - 定期更换API密钥

2. **input verify**：
   - verify user input format
   - 防止恶意 input
   - 限制 input 长度

3. **error process**：
   - not want expose 内部 error information
   - 提供友好 error prompt
   - 记录 error log 便于排查

## 📈 monitoring and 维护

### log monitoring
```python
# application 已 configuration log system
import logging
logger = logging.getLogger(__name__)

# 查看 application log
logger.info("application 启动 success")
logger.error("error information")
```

### performance monitoring
- monitoring response time
- 追踪 error 率
- 观察资源 use 情况

### 定期维护
- update dependency version
- optimize code performance
- 备份 important data

## 🎉 deployment success ！

deployment complete after ，您VibeDocapplication将in以下地址可用：
`https://www.modelscope.cn/studios/your-username/Vibedocs`

### Next Steps:
1. 分享您创空 time link
2. 收集 user 反馈
3. 持续 optimize function
4. 参加 ModelScopeMCP&Agent挑战赛

---

**技术 support**：
- such as 遇 issue ，请查看ModelScope文档
- or submitIssue到项目仓库
- 联系 development 者 get 帮助

**祝您 deployment success ！🚀**