# 🚀 VibeDoc deployment guide

## 📋 directory
- [快速 deployment](#快速 deployment)
- [ModelScopeModelScopedeployment](#ModelScopemodelscopedeployment)
- [Dockerdeployment](#dockerdeployment)
- [this 地 development](#this 地 development)
- [environment configuration](#environment configuration)
- [故障排除](#故障排除)

## 🚀 快速 deployment

### method1：ModelScopeModelScope一键deployment（推荐）

1. **登录 ModelScopeModelScope**
   - access [ModelScope](https://modelscope.cn)
   - 注册并登录账户

2. **导入 project**
   ```
   仓 library address: https://github.com/JasonRobertDestiny/VibeDocs.git
   分支: modelscope
   SDK: Gradio
   ```

3. **Configure environment variables**
   ```bash
   SILICONFLOW_API_KEY=your_api_key_here
   NODE_ENV=production
   PORT=3000
   ```

4. **启动 deployment**
   - click"启动"按钮
   - waiting 构建 complete

### method2：本地快速启动

```bash
# clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# 切换 to 正确分支
git checkout modelscope

# 安装 dependency
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# edit .env 文件，add你的API密钥

# 启动 application
python app.py
```

## 🌟 ModelScopeModelScopedeployment

### complete deployment configuration

**project information ：**
- **仓 library address ：** `https://github.com/JasonRobertDestiny/VibeDocs.git`
- **分支：** `modelscope`
- **SDK：** `Gradio`
- **Pythonversion ：** `3.11`

**environment variable configuration ：**

| variable name | 值 | description | 必填 |
|--------|----|----|------|
| `SILICONFLOW_API_KEY` | `your_api_key` | Silicon Flow API密钥 | ✅ |
| `NODE_ENV` | `production` | 运行 environment | ✅ |
| `PORT` | `3000` | application 端口 | ✅ |
| `DEEPWIKI_SSE_URL` | `http://localhost:8080` | DeepWiki MCPservice | ❌ |
| `FETCH_SSE_URL` | `http://localhost:8081` | 通用抓取MCPservice | ❌ |
| `DOUBAO_SSE_URL` | `http://localhost:8082` | diagram 像 generateMCPservice | ❌ |
| `DOUBAO_API_KEY` | `your_doubao_key` | Doubao API密钥 | ❌ |

### deployment Step 详解

1. **准备API密钥**
   - access [Silicon Flow](https://siliconflow.cn) 注册账户
   - get 免费API密钥

2. **create 创空 time**
   - inModelScope中create新的创空间
   - select"从Git仓库导入"

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
   - ensure `SILICONFLOW_API_KEY` 正确configuration

5. **构建 and deployment**
   - click"构建"按钮
   - waiting 构建 complete
   - test application function

### 常见 issue 解决

**issue1：构建失败**
- ensure use `modelscope` 分支
- check `requirements.txt` 文件是否存in
- verifyPython版本兼容性

**issue2：APIcall failed**
- check `SILICONFLOW_API_KEY` 是否正确
- verifyAPI密钥是否have 效
- confirm 网络连接正常

**issue3：MCPservice不可用**
- MCPservice is can 选， not 影 response core function
- such as 果 not use 外部 link parse ， can with 忽略相关 error

## 🐳 Dockerdeployment

### useDocker Compose（推荐）

```bash
# clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# Configure environment variables
cp .env.example .env
# edit .env 文件

# 启动 service
docker-compose up -d

# 查看 log
docker-compose logs -f vibedoc
```

### useDocker直接构建

```bash
# 构建镜像
docker build -t vibedoc .

# 运行容器
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

# 2. create 虚拟 environment （ can 选）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装 dependency
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# edit .env 文件，add 必 wantconfiguration

# 5. 启动 development server
python app.py
```

### development tool 推荐

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

### can 选 configuration

```bash
# MCPservice configuration （ can 选）
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
- `docker-compose.yml`: 容器编排 configuration

## 🛠️ 故障排除

### 常见 error and solution

**error1：`ModuleNotFoundError`**
```bash
# solution ：重新安装 dependency
pip install -r requirements.txt
```

**error2：API密钥error**
```bash
# check environment variable
echo $SILICONFLOW_API_KEY

# verify 密钥 format
# should 该 with "sk-" 开头
```

**error3：端口占用**
```bash
# find 占用端口进程
lsof -i :3000

# 杀死进程
kill -9 <PID>

# or 者更改端口
export PORT=3001
```

**error4：网络连接issue**
```bash
# test 网络连接
curl -I https://api.siliconflow.cn/v1/chat/completions

# check 防火墙 setting
# ensure 端口3000可以access
```

### log 调试

```bash
# 查看 application log
tail -f /var/log/vibedoc.log

# Dockerlog
docker logs vibedoc

# actual when log
docker logs -f vibedoc
```

### performance optimize

1. **内存 optimize**
   - 增加容器内存限制
   - use 更高效Python版本

2. **网络 optimize**
   - configurationCDN加速
   - use 负载均衡

3. **缓存 optimize**
   - 启用Redis缓存
   - configurationHTTP缓存头

## 📞 技术 support

such as 果遇 to issue ，请：

1. check this documentation 故障排除部分
2. 查看 projectIssues页面
3. submit 新Issue并提供：
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

# 重启 application
docker-compose restart vibedoc
```

---

**🎯 Note:** recommendation优先 useModelScopeModelScopedeployment，这是最简单且稳定method。this 地 development时useDocker可以ensure环境一致性。