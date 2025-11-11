# 🚀 VibeDoc deployment guide

## 📋 directory
- [快速 deployment](#快速 deployment)
- [ModelScopeModelScopedeployment](#ModelScopemodelscopedeployment)
- [Dockerdeployment](#dockerdeployment)
- [this 地 development](#this 地 development)
- [environment configuration](#environment configuration)
- [故障排除](#故障排除)

## 🚀 快速 deployment

### method1：ModelScopeModelScope一键deployment（push荐）

1. **登录 ModelScopeModelScope**
   - access [ModelScope](https://modelscope.cn)
   - 注册并登录账户

2. **guide入 project**
   ```
   仓 library address: https://github.com/JasonRobertDestiny/VibeDocs.git
   divide支: modelscope
   SDK: Gradio
   ```

3. **Configure environment variables**
   ```bash
   SILICONFLOW_API_KEY=your_api_key_here
   NODE_ENV=production
   PORT=3000
   ```

4. **start deployment**
   - click"start"press钮
   - waiting construct建 complete

### method2：本地快速start

```bash
# clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# 切换 to correct确divide支
git checkout modelscope

# 安装 dependency
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# edit .env textitem，add你的API密key

# start application
python app.py
```

## 🌟 ModelScopeModelScopedeployment

### complete deployment configuration

**project information ：**
- **仓 library address ：** `https://github.com/JasonRobertDestiny/VibeDocs.git`
- **divide支：** `modelscope`
- **SDK：** `Gradio`
- **Pythonversion ：** `3.11`

**environment variable configuration ：**

| variable name | 值 | description | 必填 |
|--------|----|----|------|
| `SILICONFLOW_API_KEY` | `your_api_key` | Silicon Flow API密key | ✅ |
| `NODE_ENV` | `production` | 运行 environment | ✅ |
| `PORT` | `3000` | application 端口 | ✅ |
| `DEEPWIKI_SSE_URL` | `http://localhost:8080` | DeepWiki MCPservice | ❌ |
| `FETCH_SSE_URL` | `http://localhost:8081` | 通use抓取MCPservice | ❌ |
| `DOUBAO_SSE_URL` | `http://localhost:8082` | diagram 像 generateMCPservice | ❌ |
| `DOUBAO_API_KEY` | `your_doubao_key` | Doubao API密key | ❌ |

### deployment Step 详solve

1. **准备API密key**
   - access [Silicon Flow](https://siliconflow.cn) 注册账户
   - get freeAPI密key

2. **create 创空 time**
   - inModelScope中create新的创空间
   - select"从Git仓库guide入"

3. **configuration project setting**
   ```yaml
   title: "VibeDoc AI Agent - Agentapplication development 赛道"
   emoji: "🤖"
   sdk: gradio
   sdk_version: 5.34.1
   app_file: app.py
   ```

4. **setting environment variable**
   - in 创空 time setting in add environment variable
   - ensure `SILICONFLOW_API_KEY` correct确configuration

5. **construct建 and deployment**
   - click"construct建"press钮
   - waiting construct建 complete
   - test application function

### 常见 issue solve

**issue1：construct建failure**
- ensure use `modelscope` divide支
- check `requirements.txt` textitem是no存in
- verifyPython版本兼容性

**issue2：APIcall failed**
- check `SILICONFLOW_API_KEY` 是nocorrect确
- verifyAPI密key是nohave 效
- confirm 网络连connectcorrect常

**issue3：MCPservicenotcanuse**
- MCPservice is can select， not 影 response core function
- such as result not use 外部 link parse ， can with 忽略相关 error

## 🐳 Dockerdeployment

### useDocker Compose（push荐）

```bash
# clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# Configure environment variables
cp .env.example .env
# edit .env textitem

# start service
docker-compose up -d

# check看 log
docker-compose logs -f vibedoc
```

### useDockerdirectconstruct建

```bash
# construct建镜像
docker build -t vibedoc .

# 运行容device
docker run -d \
  --name vibedoc \
  -p 3000:3000 \
  -e SILICONFLOW_API_KEY=your_api_key \
  -e NODE_ENV=production \
  vibedoc
```

## 💻 this 地 development

### environment requirement
- Python 3.11+
- pip or pipenv
- Git

### development environment setting

```bash
# 1. clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# 2. create 虚拟 environment （ can select）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装 dependency
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# edit .env textitem，add 必 wantconfiguration

# 5. start development server
python app.py
```

### development tool push荐

- **IDE：** VS Code, PyCharm
- **Pythonplugin ：** Python Extension Pack
- **code formatting ：** Black, isort
- **type check ：** mypy
- **test framework ：** pytest

## ⚙️ environment configuration

### 必填 configuration

```bash
# Silicon Flow APIKey (required)
SILICONFLOW_API_KEY=your_siliconflow_api_key

# application configuration
NODE_ENV=production
PORT=3000
```

### can select configuration

```bash
# MCPservice configuration （ can select）
DEEPWIKI_SSE_URL=http://localhost:8080
FETCH_SSE_URL=http://localhost:8081
DOUBAO_SSE_URL=http://localhost:8082
DOUBAO_API_KEY=your_doubao_api_key

# 调试 configuration
DEBUG=false
LOG_LEVEL=INFO
API_TIMEOUT=120
MCP_TIMEOUT=30
```

### configuration file description

- `.env.example`: environment variable template
- `app_config.yaml`: ModelScope deployment configuration
- `requirements.txt`: Pythondependency
- `Dockerfile`: Docker镜像 configuration
- `docker-compose.yml`: 容device编排 configuration

## 🛠️ 故障排除

### 常见 error and solution

**error1：`ModuleNotFoundError`**
```bash
# solution ：重新安装 dependency
pip install -r requirements.txt
```

**error2：API密keyerror**
```bash
# check environment variable
echo $SILICONFLOW_API_KEY

# verify 密key format
# should 该 with "sk-" open头
```

**error3：端口占use**
```bash
# find 占use端口进程
lsof -i :3000

# 杀死进程
kill -9 <PID>

# or 者更改端口
export PORT=3001
```

**error4：网络连connectissue**
```bash
# test 网络连connect
curl -I https://api.siliconflow.cn/v1/chat/completions

# check 防火墙 setting
# ensure 端口3000canwithaccess
```

### log 调试

```bash
# check看 application log
tail -f /var/log/vibedoc.log

# Dockerlog
docker logs vibedoc

# actual when log
docker logs -f vibedoc
```

### performance optimize

1. **internal存 optimize**
   - 增加容deviceinternal存limit
   - use 更高效Python版本

2. **网络 optimize**
   - configurationCDN加速
   - use 负载均衡

3. **缓存 optimize**
   - startuseRedis缓存
   - configurationHTTP缓存头

## 📞 技technique support

such as result遇 to issue ，please：

1. check this documentation 故障排除部divide
2. check看 projectIssues页面
3. submit 新Issue并提provide：
   - error information
   - system environment
   - configuration information
   - 复现 Step

## 🔄 update 升级

```bash
# 拉取最新 code
git pull origin modelscope

# update dependency
pip install -r requirements.txt --upgrade

# 重start application
docker-compose restart vibedoc
```

---

**🎯 Note:** recommendationexcellentfirst useModelScopeModelScopedeployment，这是最简单且稳定method。this 地 developmenttimeuseDockercanwithensureenvironment一致性。