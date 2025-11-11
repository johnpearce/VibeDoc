# 🚀 VibeDoc Deployment Guide

## 📋 Table of Contents
- [Quick Deployment](#quick-deployment)
- [ModelScope Deployment](#modelscope-deployment)
- [Docker Deployment](#docker-deployment)
- [Local Development](#local-development)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Deployment

### Method 1: ModelScope One-Click Deployment (Recommended)

1. **Login to ModelScope**
   - Visit [ModelScope](https://modelscope.cn)
   - Register and login to your account

2. **Import Project**
   ```
   Repository URL: https://github.com/JasonRobertDestiny/VibeDocs.git
   Branch: modelscope
   SDK: Gradio
   ```

3. **Configure Environment Variables**
   ```bash
   SILICONFLOW_API_KEY=your_api_key_here
   NODE_ENV=production
   PORT=3000
   ```

4. **Start Deployment**
   - Click "Start" button
   - Wait for build to complete

### Method 2: Local Quick Start

```bash
# Clone the project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# Switch to correct branch
git checkout modelscope

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env file and add your API key

# Start application
python app.py
```

## 🌟 ModelScope Deployment

### Complete Deployment Configuration

**Project Information:**
- **Repository URL:** `https://github.com/JasonRobertDestiny/VibeDocs.git`
- **Branch:** `modelscope`
- **SDK:** `Gradio`
- **Python Version:** `3.11`

**Environment Variable Configuration:**

| Variable Name | Value | Description | Required |
|--------------|-------|-------------|----------|
| `SILICONFLOW_API_KEY` | `your_api_key` | Silicon Flow API Key | ✅ |
| `NODE_ENV` | `production` | Runtime Environment | ✅ |
| `PORT` | `3000` | Application Port | ✅ |
| `DEEPWIKI_SSE_URL` | `http://localhost:8080` | DeepWiki MCP Service | ❌ |
| `FETCH_SSE_URL` | `http://localhost:8081` | General Fetch MCP Service | ❌ |
| `DOUBAO_SSE_URL` | `http://localhost:8082` | Image Generation MCP Service | ❌ |
| `DOUBAO_API_KEY` | `your_doubao_key` | Doubao API Key | ❌ |

### Deployment Steps

1. **Prepare API Key**
   - Visit [Silicon Flow](https://siliconflow.cn) to register
   - Get free API key

2. **Create Space**
   - Create new space in ModelScope
   - Select "Import from Git repository"

3. **Configure Project Settings**
   ```yaml
   title: "VibeDoc AI Agent"
   emoji: "🤖"
   sdk: gradio
   sdk_version: 5.34.1
   app_file: app.py
   ```

4. **Set Environment Variables**
   - Add environment variables in space settings
   - Ensure `SILICONFLOW_API_KEY` is correctly configured

5. **Build and Deploy**
   - Click "Build" button
   - Wait for build completion
   - Test application functionality

### Common Issues

**Issue 1: Build Failure**
- Ensure using `modelscope` branch
- Check if `requirements.txt` file exists
- Verify Python version compatibility

**Issue 2: API Call Failure**
- Check if `SILICONFLOW_API_KEY` is correct
- Verify API key validity
- Confirm network connection

**Issue 3: MCP Service Unavailable**
- MCP services are optional, don't affect core functionality
- If not using external link parsing, can ignore related errors

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# Configure environment variables
cp .env.example .env
# Edit .env file

# Start services
docker-compose up -d

# View logs
docker-compose logs -f vibedoc
```

### Direct Docker Build

```bash
# Build image
docker build -t vibedoc .

# Run container
docker run -d \
  --name vibedoc \
  -p 3000:3000 \
  -e SILICONFLOW_API_KEY=your_api_key \
  -e NODE_ENV=production \
  vibedoc
```

## 💻 Local Development

### Requirements
- Python 3.11+
- pip or pipenv
- Git

### Development Environment Setup

```bash
# 1. Clone project
git clone https://github.com/JasonRobertDestiny/VibeDocs.git
cd VibeDocs

# 2. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env file with necessary configurations

# 5. Start development server
python app.py
```

### Recommended Development Tools

- **IDE:** VS Code, PyCharm
- **Python Plugins:** Python Extension Pack
- **Code Formatting:** Black, isort
- **Type Checking:** mypy
- **Testing Framework:** pytest

## ⚙️ Environment Configuration

### Required Configuration

```bash
# Silicon Flow API Key (Required)
SILICONFLOW_API_KEY=your_siliconflow_api_key

# Application Configuration
NODE_ENV=production
PORT=3000
```

### Optional Configuration

```bash
# MCP Service Configuration (Optional)
DEEPWIKI_SSE_URL=http://localhost:8080
FETCH_SSE_URL=http://localhost:8081
DOUBAO_SSE_URL=http://localhost:8082
DOUBAO_API_KEY=your_doubao_api_key

# Debug Configuration
DEBUG=false
LOG_LEVEL=INFO
API_TIMEOUT=120
MCP_TIMEOUT=30
```

### Configuration Files

- `.env.example`: Environment variable template
- `app_config.yaml`: ModelScope deployment config
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker image configuration
- `docker-compose.yml`: Container orchestration config

## 🛠️ Troubleshooting

### Common Errors and Solutions

**Error 1: `ModuleNotFoundError`**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Error 2: API Key Error**
```bash
# Check environment variable
echo $SILICONFLOW_API_KEY

# Verify key format
# Should start with "sk-"
```

**Error 3: Port Already in Use**
```bash
# Find process using port
lsof -i :3000

# Kill process
kill -9 <PID>

# Or change port
export PORT=3001
```

**Error 4: Network Connection Issues**
```bash
# Test network connection
curl -I https://api.siliconflow.cn/v1/chat/completions

# Check firewall settings
# Ensure port 3000 is accessible
```

### Log Debugging

```bash
# View application logs
tail -f /var/log/vibedoc.log

# Docker logs
docker logs vibedoc

# Real-time logs
docker logs -f vibedoc
```

### Performance Optimization

1. **Memory Optimization**
   - Increase container memory limit
   - Use more efficient Python version

2. **Network Optimization**
   - Configure CDN acceleration
   - Use load balancing

3. **Cache Optimization**
   - Enable Redis caching
   - Configure HTTP cache headers

## 📞 Technical Support

If you encounter problems:

1. Check troubleshooting section in this document
2. Review project Issues page
3. Submit new Issue with:
   - Error message
   - System environment
   - Configuration info
   - Steps to reproduce

## 🔄 Updates and Upgrades

```bash
# Pull latest code
git pull origin modelscope

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
docker-compose restart vibedoc
```

---

**🎯 Tip:** ModelScope deployment is recommended as the simplest and most stable method. For local development, Docker ensures environment consistency.
