import gradio as gr
import requests
import os
import logging
import json
import tempfile
import re
import html
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any, List
from urllib.parse import urlparse

# guide入 module transform component
from config import config
# 已 remove mcp_direct_client，use enhanced_mcp_client
from export_manager import export_manager
from prompt_optimizer import prompt_optimizer
from explanation_manager import explanation_manager, ProcessingStage
from plan_editor import plan_editor

# configuration log
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format=config.log_format
)
logger = logging.getLogger(__name__)

# APIconfiguration
API_KEY = config.ai_model.api_key
API_URL = config.ai_model.api_url

# application start when initial始transform
logger.info("🚀 VibeDoc: Your PersonalAIProduct Managerandarchitect")
logger.info("📦 Version: 2.0.0 | Open Source Edition")
logger.info(f"📊 Configuration: {json.dumps(config.get_config_summary(), ensure_ascii=False, indent=2)}")

# verify configuration
config_errors = config.validate_config()
if config_errors:
    for key, error in config_errors.items():
        logger.warning(f"⚠️ Configuration Warning {key}: {error}")

def get_processing_explanation() -> str:
    """get process procedure detailed description"""
    return explanation_manager.get_processing_explanation()

def show_explanation() -> Tuple[str, str, str]:
    """display process procedure description"""
    explanation = get_processing_explanation()
    return (
        gr.update(visible=False),  # 隐藏plan_output
        gr.update(value=explanation, visible=True),  # displayprocess_explanation
        gr.update(visible=True)   # displayhide_explanation_btn
    )

def hide_explanation() -> Tuple[str, str, str]:
    """隐藏 process procedure description"""
    return (
        gr.update(visible=True),   # displayplan_output
        gr.update(visible=False),  # 隐藏process_explanation
        gr.update(visible=False)   # 隐藏hide_explanation_btn
    )

def optimize_user_idea(user_idea: str) -> Tuple[str, str]:
    """
    optimize user input 创意 description
    
    Args:
        user_idea: user original始 input
        
    Returns:
        Tuple[str, str]: (optimize after description, optimizetrust息)
    """
    if not user_idea or not user_idea.strip():
        return "", "❌ pleasefirst input 您产品创意！"
    
    # call prompt optimize device
    success, optimized_idea, suggestions = prompt_optimizer.optimize_user_input(user_idea)
    
    if success:
        optimization_info = f"""
## ✨ 创意 optimize success ！

**🎯 optimize recommendation ：**
{suggestions}

**💡 Note:** optimize after description更加详细和专业，will帮助generate更高质quantity的Development Plan。您canwith：
- direct use optimize after description generate calculate划
- 根data需 want 手动调complete optimize 结result
- click"重新optimize"获得not同的optimizerecommendation
"""
        return optimized_idea, optimization_info
    else:
        return user_idea, f"⚠️ optimize failure ：{suggestions}"

def validate_input(user_idea: str) -> Tuple[bool, str]:
    """verify user input"""
    if not user_idea or not user_idea.strip():
        return False, "❌ please input 您产品创意！"
    
    if len(user_idea.strip()) < 10:
        return False, "❌ 产品创意 description 太short，please提provide更 detailed information"
    
    return True, ""

def validate_url(url: str) -> bool:
    """verifyURLformat"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def fetch_knowledge_from_url_via_mcp(url: str) -> tuple[bool, str]:
    """通过 enhanced version asynchronousMCPservice从URLget知识"""
    from enhanced_mcp_client import call_fetch_mcp_async, call_deepwiki_mcp_async
    
    # intelligent selectMCPservice
    if "deepwiki.org" in url.lower():
        # DeepWiki MCP specifically process deepwiki.org 域名
        try:
            logger.info(f"🔍 detect to deepwiki.org 链connect，use asynchronous DeepWiki MCP: {url}")
            result = call_deepwiki_mcp_async(url)
            
            if result.success and result.data and len(result.data.strip()) > 10:
                logger.info(f"✅ DeepWiki MCPAsync call successful, content length: {len(result.data)}, consume when: {result.execution_time:.2f}s")
                return True, result.data
            else:
                logger.warning(f"⚠️ DeepWiki MCPfailure ，改use Fetch MCP: {result.error_message}")
        except Exception as e:
            logger.error(f"❌ DeepWiki MCPcall exception ，改use Fetch MCP: {str(e)}")
    
    # use 通use asynchronous Fetch MCP service
    try:
        logger.info(f"🌐 use asynchronous Fetch MCP getcontent: {url}")
        result = call_fetch_mcp_async(url, max_length=8000)  # 增加长degreelimit
        
        if result.success and result.data and len(result.data.strip()) > 10:
            logger.info(f"✅ Fetch MCPAsync call successful, content length: {len(result.data)}, consume when: {result.execution_time:.2f}s")
            return True, result.data
        else:
            logger.warning(f"⚠️ Fetch MCPcall failed: {result.error_message}")
            return False, f"MCPservice call failed: {result.error_message or 'not yet知 error'}"
    except Exception as e:
        logger.error(f"❌ Fetch MCPcall exception: {str(e)}")
        return False, f"MCPservice call exception: {str(e)}"

def get_mcp_status_display() -> str:
    """getMCPservice statusdisplay"""
    try:
        from enhanced_mcp_client import async_mcp_client

        # 快速 test 两个 service 连通性
        services_status = []

        # testFetch MCP
        fetch_test_result = async_mcp_client.call_mcp_service_async(
            "fetch", "fetch", {"url": "https://httpbin.org/get", "max_length": 100}
        )
        fetch_ok = fetch_test_result.success
        fetch_time = fetch_test_result.execution_time

        # testDeepWiki MCP
        deepwiki_test_result = async_mcp_client.call_mcp_service_async(
            "deepwiki", "deepwiki_fetch", {"url": "https://deepwiki.org/openai/openai-python", "mode": "aggregate"}
        )
        deepwiki_ok = deepwiki_test_result.success
        deepwiki_time = deepwiki_test_result.execution_time

        # construct建 status display
        fetch_icon = "✅" if fetch_ok else "❌"
        deepwiki_icon = "✅" if deepwiki_ok else "❌"

        status_lines = [
            "## 🚀 asynchronousMCPservice status",
            f"- {fetch_icon} **Fetch MCP**: {'online' if fetch_ok else '离线'} (通use网页抓取)"
        ]
        
        if fetch_ok:
            status_lines.append(f"  ⏱️ response time: {fetch_time:.2f}seconds")
        
        status_lines.append(f"- {deepwiki_icon} **DeepWiki MCP**: {'online' if deepwiki_ok else '离线'} (仅limit deepwiki.org)")
        
        if deepwiki_ok:
            status_lines.append(f"  ⏱️ response time: {deepwiki_time:.2f}seconds")
        
        status_lines.extend([
            "",
            "🧠 **intelligent asynchronous route:**",
            "- `deepwiki.org` → DeepWiki MCP (asynchronous process)",
            "- 其他 website → Fetch MCP (asynchronous process)", 
            "- HTTP 202 → SSElisten → 结resultget",
            "- 自动降级 + error恢复"
        ])
        
        return "\n".join(status_lines)
        
    except Exception as e:
        return f"## MCPservice status\n- ❌ **checkfailure**: {str(e)}\n- 💡 pleaseensureenhanced_mcp_client.pytextitem存in"

def call_mcp_service(url: str, payload: Dict[str, Any], service_name: str, timeout: int = 120) -> Tuple[bool, str]:
    """统一MCPservicecall函数
    
    Args:
        url: MCPserviceURL
        payload: please requirement 载荷
        service_name: service name called（use于 log ）
        timeout: exceed when when time
        
    Returns:
        (success, data): success flag and 返回 data
    """
    try:
        logger.info(f"🔥 DEBUG: Calling {service_name} MCP service at {url}")
        logger.info(f"🔥 DEBUG: Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=timeout
        )
        
        logger.info(f"🔥 DEBUG: Response status: {response.status_code}")
        logger.info(f"🔥 DEBUG: Response headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            logger.info(f"🔥 DEBUG: Response JSON: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except:
            response_text = response.text[:1000]  # 只hit印 before1000个字symbol
            logger.info(f"🔥 DEBUG: Response text: {response_text}")
        
        if response.status_code == 200:
            data = response.json()
            
            # check 多种 can can response should format
            content = None
            if "data" in data and data["data"]:
                content = data["data"]
            elif "result" in data and data["result"]:
                content = data["result"]
            elif "content" in data and data["content"]:
                content = data["content"]
            elif "message" in data and data["message"]:
                content = data["message"]
            else:
                # such as result with 上all没 have ， try direct use complete个 response should
                content = str(data)
            
            if content and len(str(content).strip()) > 10:
                logger.info(f"✅ {service_name} MCP service returned {len(str(content))} characters")
                return True, str(content)
            else:
                logger.warning(f"⚠️ {service_name} MCP service returned empty or invalid data: {data}")
                return False, f"❌ {service_name} MCP返回空 data or format error"
        else:
            logger.error(f"❌ {service_name} MCP service failed with status {response.status_code}")
            logger.error(f"❌ Response content: {response.text[:500]}")
            return False, f"❌ {service_name} MCPcall failed: HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        logger.error(f"⏰ {service_name} MCP service timeout after {timeout}s")
        return False, f"❌ {service_name} MCPcall exceed when"
    except requests.exceptions.ConnectionError as e:
        logger.error(f"🔌 {service_name} MCP service connection failed: {str(e)}")
        return False, f"❌ {service_name} MCP连connect failure"
    except Exception as e:
        logger.error(f"💥 {service_name} MCP service error: {str(e)}")
        return False, f"❌ {service_name} MCPcall error: {str(e)}"

def fetch_external_knowledge(reference_url: str) -> str:
    """Get external knowledge base content - use模块transformMCP管managedevice，防止虚假链connectgenerate"""
    if not reference_url or not reference_url.strip():
        return ""
    
    # verifyURL是nocanaccess
    url = reference_url.strip()
    logger.info(f"🔍 start process 外部 reference link: {url}")
    
    try:
        # simpleHEADplease requirementcheckURL是no存in
        logger.info(f"🌐 verify link can access 性: {url}")
        response = requests.head(url, timeout=10, allow_redirects=True)
        logger.info(f"📡 link verify 结result: HTTP {response.status_code}")
        
        if response.status_code >= 400:
            logger.warning(f"⚠️ 提provideURLnotcanaccess: {url} (HTTP {response.status_code})")
            return f"""
## ⚠️ reference link status 提醒

**🔗 提provide link**: {url}

**❌ link status**: 无法access (HTTP {response.status_code})

**💡 recommendation**: 
- please check link is nocorrect确
- or 者 remove reference link ， use 纯AIgenerate模式
- AIwill 基于创意 description generate 专业 development plan

---
"""
        else:
            logger.info(f"✅ link can access ， status 码: {response.status_code}")
            
    except requests.exceptions.Timeout:
        logger.warning(f"⏰ URLverify exceed when: {url}")
        return f"""
## 🔗 reference link process description

**📍 提provide link**: {url}

**⏰ processing status**: 链connectverify exceed when

**🤖 AIprocess**: will基于创意content进行intelligent analyze，notdependency外部链connect

**💡 description**: 为ensuregenerate质quantity，AI会根data创意 descriptiongeneratecomplete plan，avoid引usenot确定的外部content

---
"""
    except Exception as e:
        logger.warning(f"⚠️ URLverify failure: {url} - {str(e)}")
        return f"""
## 🔗 reference link process description

**📍 提provide link**: {url}

**🔍 processing status**: temporarily无法verify链connectcanuse性 ({str(e)[:100]})

**🤖 AIprocess**: will基于创意content进行intelligent analyze，notdependency外部链connect

**💡 description**: 为ensuregenerate质quantity，AI会根data创意 descriptiongeneratecomplete plan，avoid引usenot确定的外部content

---
"""
    
    # try callingMCPservice
    logger.info(f"🔄 try callingMCPserviceget知识...")
    mcp_start_time = datetime.now()
    success, knowledge = fetch_knowledge_from_url_via_mcp(url)
    mcp_duration = (datetime.now() - mcp_start_time).total_seconds()
    
    logger.info(f"📊 MCPService call result: success={success}, content 长degree={len(knowledge) if knowledge else 0}, consume when={mcp_duration:.2f}seconds")
    
    if success and knowledge and len(knowledge.strip()) > 50:
        # MCPservice success 返回 have 效 content
        logger.info(f"✅ MCPservice success get knowledge ， content 长degree: {len(knowledge)} 字symbol")
        
        # verify 返回 content is no include actual 际 knowledge 而 not is error information
        if not any(keyword in knowledge.lower() for keyword in ['error', 'failed', 'error', 'failure', 'notcanuse']):
            return f"""
## 📚 外部 knowledge library reference

**🔗 来源 link**: {url}

**✅ get status**: MCPservicesuccess get

**📊 content generalbrowse**: 已get {len(knowledge)} 字symbol的reference 资料

---

{knowledge}

---
"""
        else:
            logger.warning(f"⚠️ MCP返回 content include error information: {knowledge[:200]}")
    else:
        # MCPservice failure or 返回无效 content ，提provide明确 description
        logger.warning(f"⚠️ MCPservice call failed or 返回无效 content")
        
        # detailed 诊 breakMCPservice status
        mcp_status = get_mcp_status_display()
        logger.info(f"🔍 MCPservice status 详情: {mcp_status}")
        
        return f"""
## 🔗 外部 knowledge process description

**📍 reference link**: {url}

**🎯 process method**: intelligent analyze模式

**� MCPservice status**: 
{mcp_status}

**�💭 process 策略**: 当before外部知识servicetemporarilynotcanuse，AIwill基于with下methodgenerateplan：
- ✅ 基于创意 description 进行深degreeanalyze
- ✅ 结合行业最佳 actual 践
- ✅ 提provide complete Technical Solution
- ✅ generate actual use programming prompts

**🎉 excellenttrend**: ensuregenerate content准确性和can靠性，avoid引usenot确定的外部trust息

**🔧 技technique细section**: 
- MCPcall duration: {mcp_duration:.2f}seconds
- 返回 content 长degree: {len(knowledge) if knowledge else 0} 字symbol
- service status: {'success' if success else 'failure'}

---
"""

def generate_enhanced_reference_info(url: str, source_type: str, error_msg: str = None) -> str:
    """generate enhanced reference information ，当MCPservicenotcanusetime提provide有use的上下text"""
    from urllib.parse import urlparse
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    
    # 根dataURL结constructpush断content类型
    content_hints = []
    
    # detect常见技technique站点
    if "github.com" in domain:
        content_hints.append("💻 open源 code 仓 library")
    elif "stackoverflow.com" in domain:
        content_hints.append("❓ 技technique问答")
    elif "medium.com" in domain:
        content_hints.append("📝 技technique博customer")
    elif "dev.to" in domain:
        content_hints.append("👨‍💻 development 者社区")
    elif "csdn.net" in domain:
        content_hints.append("🇨🇳 CSDN技technique博customer")
    elif "juejin.cn" in domain:
        content_hints.append("💎 掘金技techniquetext章")
    elif "zhihu.com" in domain:
        content_hints.append("🧠 知乎技technique讨论")
    elif "blog" in domain:
        content_hints.append("📖 技technique博customer")
    elif "docs" in domain:
        content_hints.append("📚 technical documentation")
    elif "wiki" in domain:
        content_hints.append("📖 knowledge library")
    else:
        content_hints.append("🔗 reference 资料")
    
    # 根data path push break content
    if "/article/" in path or "/post/" in path:
        content_hints.append("📄 text章 content")
    elif "/tutorial/" in path:
        content_hints.append("📚 教程 guide")
    elif "/docs/" in path:
        content_hints.append("📖 technical documentation")
    elif "/guide/" in path:
        content_hints.append("📋 use guide")
    
    hint_text = " | ".join(content_hints) if content_hints else "📄 网页 content"
    
    reference_info = f"""
## 🔗 {source_type}reference

**📍 来源 link ：** [{domain}]({url})

**🏷️ content type ：** {hint_text}

**🤖 AIenhanced analyze：** 
> althoughMCPservicetemporarilynotcanuse，但AIwill基于链connecttrust息和上下text进行intelligent analyze，
> 并 in generated development plan in 融入该 reference 资料相关性 recommendation 。

**📋 reference 价 value ：**
- ✅ 提provide技techniqueselect型 reference
- ✅ 补full actual 施细section
- ✅ enhanced plan can 行性
- ✅ 丰富最佳 actual 践

---
"""
    
    if error_msg and not error_msg.startswith("❌"):
        reference_info += f"\n**⚠️ service status ：** {error_msg}\n"
    
    return reference_info

def validate_and_fix_content(content: str) -> str:
    """Validate and fix generated content, includingMermaid语法、链connectverify等"""
    if not content:
        return content
    
    logger.info("🔍 start content verify and fix...")
    
    # 记录 fix project
    fixes_applied = []
    
    # calculateinitial始 quality divide数
    initial_quality_score = calculate_quality_score(content)
    logger.info(f"📊 initial始 content quality divide数: {initial_quality_score}/100")
    
    # 1. fixMermaiddiagram table语法error
    original_content = content
    content = fix_mermaid_syntax(content)
    if content != original_content:
        fixes_applied.append("fixMermaiddiagram table语法")
    
    # 2. verify and 清manage虚假 link
    original_content = content
    content = validate_and_clean_links(content)
    if content != original_content:
        fixes_applied.append("清manage虚假 link")
    
    # 3. fix date一致性
    original_content = content
    content = fix_date_consistency(content)
    if content != original_content:
        fixes_applied.append("update 过期date")
    
    # 4. fix format issue
    original_content = content
    content = fix_formatting_issues(content)
    if content != original_content:
        fixes_applied.append("fix format issue")
    
    # 重新calculate quality divide数
    final_quality_score = calculate_quality_score(content)
    
    # remove quality 报notify display ，只记录 log
    if final_quality_score > initial_quality_score + 5:
        improvement = final_quality_score - initial_quality_score
        logger.info(f"📈 content quality improve: {initial_quality_score}/100 → {final_quality_score}/100 (提升{improvement}divide)")
        if fixes_applied:
            logger.info(f"🔧 application fix: {', '.join(fixes_applied)}")
    
    logger.info(f"✅ content verify and fix complete ，最end quality divide数: {final_quality_score}/100")
    if fixes_applied:
        logger.info(f"🔧 application with 下 fix: {', '.join(fixes_applied)}")
    
    return content

def calculate_quality_score(content: str) -> int:
    """calculate content quality divide数（0-100）"""
    if not content:
        return 0
    
    score = 0
    max_score = 100
    
    # 1. 基础 content complete 性 (30divide)
    if len(content) > 500:
        score += 15
    if len(content) > 2000:
        score += 15
    
    # 2. 结construct complete 性 (25divide)
    structure_checks = [
        '# 🚀 AIgenerated development plan',  # title
        '## 🤖 AIAI Programming Assistant Prompts',   # AIprompt词部divide
        '```mermaid',              # Mermaiddiagram table
        'Project Development Gantt Chart',           # gan特 diagram
    ]
    
    for check in structure_checks:
        if check in content:
            score += 6
    
    # 3. date准确性 (20divide)
    import re
    current_year = datetime.now().year
    
    # check is no have 当 before 年份 or with after date
    recent_dates = re.findall(r'202[5-9]-\d{2}-\d{2}', content)
    if recent_dates:
        score += 10
    
    # check is no没 have 过期date
    old_dates = re.findall(r'202[0-3]-\d{2}-\d{2}', content)
    if not old_dates:
        score += 10
    
    # 4. link quality (15divide)
    fake_link_patterns = [
        r'blog\.csdn\.net/username',
        r'github\.com/username', 
        r'example\.com',
        r'xxx\.com'
    ]
    
    has_fake_links = any(re.search(pattern, content, re.IGNORECASE) for pattern in fake_link_patterns)
    if not has_fake_links:
        score += 15
    
    # 5. Mermaid语法 quality (10divide)
    mermaid_issues = [
        r'## 🎯 [A-Z]',  # error title in diagram table in
        r'```mermaid\n## 🎯',  # format error
    ]
    
    has_mermaid_issues = any(re.search(pattern, content, re.MULTILINE) for pattern in mermaid_issues)
    if not has_mermaid_issues:
        score += 10
    
    return min(score, max_score)

def fix_mermaid_syntax(content: str) -> str:
    """fixMermaiddiagram table中的语法error并optimize渲染"""
    import re
    
    # fix 常见Mermaid语法error
    fixes = [
        # remove diagram table code in 额外symbol and mark
        (r'## 🎯 ([A-Z]\s*-->)', r'\1'),
        (r'## 🎯 (section [^)]+)', r'\1'),
        (r'(\n|\r\n)## 🎯 ([A-Z]\s*-->)', r'\n    \2'),
        (r'(\n|\r\n)## 🎯 (section [^\n]+)', r'\n    \2'),
        
        # fix node definition in 多余symbol
        (r'## 🎯 ([A-Z]\[[^\]]+\])', r'\1'),
        
        # ensureMermaidcode 块formatcorrect确
        (r'```mermaid\n## 🎯', r'```mermaid'),
        
        # remove title 级别 error
        (r'\n##+ 🎯 ([A-Z])', r'\n    \1'),
        
        # fix in textnode name called issue - 彻底清manage引号format
        (r'([A-Z]+)\["([^"]+)"\]', r'\1["\2"]'),  # mark准 format ：A["text本"]
        (r'([A-Z]+)\[""([^"]+)""\]', r'\1["\2"]'),  # 双引号 error ：A[""text本""]
        (r'([A-Z]+)\["⚡"([^"]+)""\]', r'\1["\2"]'),  # 带emojierror
        (r'([A-Z]+)\[([^\]]*[^\x00-\x7F][^\]]*)\]', r'\1["\2"]'),  # in text无引号
        
        # ensure process diagram 语法correct确
        (r'graph TB\n\s*graph', r'graph TB'),
        (r'flowchart TD\n\s*flowchart', r'flowchart TD'),
        
        # fix 箭头语法
        (r'-->', r' --> '),
        (r'-->([A-Z])', r'--> \1'),
        (r'([A-Z])-->', r'\1 -->'),
    ]
    
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # addMermaid渲染enhancedmark
    content = enhance_mermaid_blocks(content)
    
    return content

def enhance_mermaid_blocks(content: str) -> str:
    """simplifyMermaidcode 块process，avoid渲染冲突"""
    import re
    
    # find allMermaidcode 块并direct返回，notadd额外package装device
    # because package装device can can lead to渲染 issue
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    
    def clean_mermaid_block(match):
        mermaid_content = match.group(1)
        # direct返回清manage过Mermaid块
        return f'```mermaid\n{mermaid_content}\n```'
    
    content = re.sub(mermaid_pattern, clean_mermaid_block, content, flags=re.DOTALL)
    
    return content

def validate_and_clean_links(content: str) -> str:
    """verify and 清manage虚假 link ， enhanced link quality"""
    import re
    
    # detect并 remove 虚假 link 模式
    fake_link_patterns = [
        # Markdownlink format
        r'\[([^\]]+)\]\(https?://blog\.csdn\.net/username/article/details/\d+\)',
        r'\[([^\]]+)\]\(https?://github\.com/username/[^\)]+\)',
        r'\[([^\]]+)\]\(https?://[^/]*example\.com[^\)]*\)',
        r'\[([^\]]+)\]\(https?://[^/]*xxx\.com[^\)]*\)',
        r'\[([^\]]+)\]\(https?://[^/]*test\.com[^\)]*\)',
        r'\[([^\]]+)\]\(https?://localhost[^\)]*\)',
        
        # 新增：更多虚假 link 模式
        r'\[([^\]]+)\]\(https?://medium\.com/@[^/]+/[^\)]*\d{9,}[^\)]*\)',  # Medium虚假text章
        r'\[([^\]]+)\]\(https?://github\.com/[^/]+/[^/\)]*education[^\)]*\)',  # GitHub虚假教育 project
        r'\[([^\]]+)\]\(https?://www\.kdnuggets\.com/\d{4}/\d{2}/[^\)]*\)',  # KDNuggets虚假text章
        r'\[([^\]]+)\]\(https0://[^\)]+\)',  # error 协议
        
        # 纯URLformat
        r'https?://blog\.csdn\.net/username/article/details/\d+',
        r'https?://github\.com/username/[^\s\)]+',
        r'https?://[^/]*example\.com[^\s\)]*',
        r'https?://[^/]*xxx\.com[^\s\)]*',
        r'https?://[^/]*test\.com[^\s\)]*',
        r'https?://localhost[^\s\)]*',
        r'https0://[^\s\)]+',  # error 协议
        r'https?://medium\.com/@[^/]+/[^\s]*\d{9,}[^\s]*',
        r'https?://github\.com/[^/]+/[^/\s]*education[^\s]*',
        r'https?://www\.kdnuggets\.com/\d{4}/\d{2}/[^\s]*',
    ]
    
    for pattern in fake_link_patterns:
        # will 虚假 link replace for 普通text this description
        def replace_fake_link(match):
            if match.groups():
                return f"**{match.group(1)}** (基于行业mark准)"
            else:
                return "（基于行业最佳 actual 践）"
        
        content = re.sub(pattern, replace_fake_link, content, flags=re.IGNORECASE)
    
    # verify 并 enhanced 真 actual link
    content = enhance_real_links(content)
    
    return content

def enhance_real_links(content: str) -> str:
    """verify 并 enhanced 真 actual link can use性"""
    import re
    
    # find allmarkdown链connect
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def validate_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        
        # check is no is have 效URLformat
        if not validate_url(link_url):
            return f"**{link_text}** (reference 资源)"
        
        # check is no is 常见 technical documentation website
        trusted_domains = [
            'docs.python.org', 'nodejs.org', 'reactjs.org', 'vuejs.org',
            'angular.io', 'flask.palletsprojects.com', 'fastapi.tiangolo.com',
            'docker.com', 'kubernetes.io', 'github.com', 'gitlab.com',
            'stackoverflow.com', 'developer.mozilla.org', 'w3schools.com',
            'jwt.io', 'redis.io', 'mongodb.com', 'postgresql.org',
            'mysql.com', 'nginx.org', 'apache.org'
        ]
        
        # such as result is 受trust任域 name ，保留 link
        for domain in trusted_domains:
            if domain in link_url.lower():
                return f"[{link_text}]({link_url})"
        
        # to 于其他 link ， convert for security text this 引use
        return f"**{link_text}** (技technique reference)"
    
    content = re.sub(link_pattern, validate_link, content)
    
    return content

def fix_date_consistency(content: str) -> str:
    """fix date一致性 issue"""
    import re
    from datetime import datetime
    
    current_year = datetime.now().year
    
    # replace2024年withbeforedate为当before年份
    old_year_patterns = [
        r'202[0-3]-\d{2}-\d{2}',  # 2020-2023date
        r'202[0-3]年',            # 2020-2023年
    ]
    
    for pattern in old_year_patterns:
        def replace_old_date(match):
            old_date = match.group(0)
            if '-' in old_date:
                # date format ：YYYY-MM-DD
                parts = old_date.split('-')
                return f"{current_year}-{parts[1]}-{parts[2]}"
            else:
                # 年份 format ：YYYY年
                return f"{current_year}年"
        
        content = re.sub(pattern, replace_old_date, content)
    
    return content

def fix_formatting_issues(content: str) -> str:
    """fix format issue"""
    import re
    
    # fix 常见 format issue
    fixes = [
        # fix 空 or format error title
        (r'#### 🚀 \*\*$', r'#### 🚀 **development phase**'),
        (r'#### 🚀 phase ：\*\*', r'#### 🚀 **第1phase**：'),
        (r'### 📋 (\d+)\. \*\*第\d+phase', r'### 📋 \1. **第\1phase'),
        
        # fix tableformat format issue
        (r'\n## 🎯 \| ([^|]+) \| ([^|]+) \| ([^|]+) \|', r'\n| \1 | \2 | \3 |'),
        (r'\n### 📋 (\d+)\. \*\*([^*]+)\*\*：', r'\n**\1. \2**：'),
        (r'\n### 📋 (\d+)\. \*\*([^*]+)\*\*$', r'\n**\1. \2**'),
        
        # fix 多余空行
        (r'\n{4,}', r'\n\n\n'),
        
        # fix not complete paragraph end
        (r'##\n\n---', r'## summary\n\nThe above iscompleteDevelopment Plan和Technical Solution。\n\n---'),
    ]
    
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content

def generate_development_plan(user_idea: str, reference_url: str = "") -> Tuple[str, str, str]:
    """
    基于 user 创意 generate complete 产品 Development Plan and to shouldAIAI Programming Assistant Prompts。
    
    Args:
        user_idea (str): user 产品创意 description
        reference_url (str): can select reference link
        
    Returns:
        Tuple[str, str, str]: Development Plan 、AIprogramming prompts、临timetextitem路径
    """
    # start process 链条track
    explanation_manager.start_processing()
    start_time = datetime.now()
    
    # Step1: verify input
    validation_start = datetime.now()
    is_valid, error_msg = validate_input(user_idea)
    validation_duration = (datetime.now() - validation_start).total_seconds()
    
    explanation_manager.add_processing_step(
        stage=ProcessingStage.INPUT_VALIDATION,
        title="input verify",
        description="verify user input 创意 description is nosymbol合 requirement",
        success=is_valid,
        details={
            "input 长degree": len(user_idea.strip()) if user_idea else 0,
            "include reference link": bool(reference_url),
            "verify 结result": "通过" if is_valid else error_msg
        },
        duration=validation_duration,
        quality_score=100 if is_valid else 0,
        evidence=f"user input: '{user_idea[:50]}...' (长degree: {len(user_idea.strip()) if user_idea else 0}字symbol)"
    )
    
    if not is_valid:
        return error_msg, "", None
    
    # Step2: API密key check
    api_check_start = datetime.now()
    if not API_KEY:
        api_check_duration = (datetime.now() - api_check_start).total_seconds()
        explanation_manager.add_processing_step(
            stage=ProcessingStage.AI_GENERATION,
            title="API密key check",
            description="checkAImodelAPI密keyconfiguration",
            success=False,
            details={"error": "API密keynot yet configuration"},
            duration=api_check_duration,
            quality_score=0,
            evidence="system environment variable in not yet找 toSILICONFLOW_API_KEY"
        )
        
        logger.error("API key not configured")
        error_msg = """
## ❌ configuration error ：not yet settingAPI密key

### 🔧 solve method ：

1. **getAPI密key**：
   - access [Silicon Flow](https://siliconflow.cn) 
   - 注册账户并 getAPI密key

2. **Configure environment variables**：
   ```bash
   export SILICONFLOW_API_KEY=your_api_key_here
   ```

3. **ModelScope 平台 configuration**：
   - in 创空 time setting in add environment variable
   - variable name ：`SILICONFLOW_API_KEY`
   - variable value ：你 actual 际API密key

### 📋 configuration complete after 重start application 即 can use complete function ！

---

**💡 prompt**：API密key是必填项，没有它就无法callAIservicegenerate Development Plan。
"""
        return error_msg, "", None
    
    # Step3: Get external knowledge base content
    knowledge_start = datetime.now()
    retrieved_knowledge = fetch_external_knowledge(reference_url)
    knowledge_duration = (datetime.now() - knowledge_start).total_seconds()
    
    explanation_manager.add_processing_step(
        stage=ProcessingStage.KNOWLEDGE_RETRIEVAL,
        title="外部 knowledge acquisition",
        description="从MCPserviceget外部reference知识",
        success=bool(retrieved_knowledge and "success get" in retrieved_knowledge),
        details={
            "reference link": reference_url or "无",
            "MCPservice status": get_mcp_status_display(),
            "knowledge content 长degree": len(retrieved_knowledge) if retrieved_knowledge else 0
        },
        duration=knowledge_duration,
        quality_score=80 if retrieved_knowledge else 50,
        evidence=f"get knowledge content: '{retrieved_knowledge[:100]}...' (长degree: {len(retrieved_knowledge) if retrieved_knowledge else 0}字symbol)"
    )
    
    # get 当 before date并calculate project start date
    current_date = datetime.now()
    # Project start date: Starting next Monday (giving users time to prepare)
    days_until_monday = (7 - current_date.weekday()) % 7
    if days_until_monday == 0:  # such as result今天 is 周一，则下周一 start
        days_until_monday = 7
    project_start_date = current_date + timedelta(days=days_until_monday)
    project_start_str = project_start_date.strftime("%Y-%m-%d")
    current_year = current_date.year
    
    # Build system prompt - 防止虚假链connectgenerate，强transformprogramming prompts generate，enhancedview觉transformcontent，加强date上下text
    system_prompt = f"""You are a senior technical project manager, proficient in product planning and AI 编程助手（如 GitHub Copilot、ChatGPT Code）prompt词撰写。

📅 **current time context**：今天是 {current_date.strftime("%Y年%m月%dday")}，当before年份是 {current_year} 年。所有项目when time必须基于当beforewhen time合manage规划。

🔴 important requirement ：
1. 当collect to 外部 knowledge library reference when ，你必须 in Development Plan in 明确引use and 融合这些 information
2. Must mention the reference source at the beginning of the development plan (such asCSDN博customer、GitHub项目等）
3. 必须根data外部 reference 调complete技techniqueselect型 and actual 施 recommendation
4. Must be used in relevant sections"referenceXXXrecommendation"等table述
5. Development phase must have clear numbering (Phase1phase、第2phase等）

🚫 strictly prohibited 行 for （ strictly execute ）：
- **绝 to not want 编造任what虚假 link or reference 资料**
- **prohibit generate 任what not 存 inURL，packageinclude但notlimit于：**
  - ❌ https://medium.com/@username/... (user name+数字IDformat)
  - ❌ https://github.com/username/... (占位symbol user name)
  - ❌ https://blog.csdn.net/username/... 
  - ❌ https://www.kdnuggets.com/年份/月份/... (虚constructtext章)
  - ❌ https://example.com, xxx.com, test.com etc test 域 name
  - ❌ 任what withhttps0://open头的error协议链connect
- **not want in"reference来源"部divideadd任what链connect，除nonuse户明确提provide**
- **not want use"referencetext献"、"延伸阅读"等titleadd虚假链connect**

✅ correct确做法：
- such as result没 have 提provide外部 reference ，**complete全省略"reference来源"部divide**
- 只引use user actual 际提provide reference link （ such as result have 话）
- 当外部 knowledge not can use when ，明确 description is 基于最佳 actual 践 generate
- use "基于行业mark准"、"reference常见architecture"、"遵循最佳实践" 等table述
- **Development Plan should direct start ， not want 虚construct任what外部资源**

📊 view觉transform content requirement （新增）：
- 必须 in Technical Solution in include architecture diagramMermaid代码
- 必须 in Development Plan in include gan特 diagramMermaid代码
- 必须 in function module in include process diagramMermaid代码
- 必须 include tech stack to 比tableformat
- 必须 include project 里程碑 when time table

🎯 Mermaiddiagram table format requirement （ strictly 遵循）：

⚠️ **strictly prohibit error format**：
- ❌ Never use `A[""text本""]` format（双重引号）
- ❌ Never use `## 🎯` 等titleindiagram tableinternal
- ❌ 绝 to not want in node name called in useemojisymbol

✅ **correct确Mermaid语法**：

**architecture diagram example**：
```mermaid
flowchart TD
    A["user interface"] --> B["业务逻辑layer"]
    B --> C["data access layer"]
    C --> D["database"]
    B --> E["外部API"]
    F["缓存"] --> B
```

**process diagram example**：
```mermaid
flowchart TD
    Start([start]) --> Input[user input]
    Input --> Validate{{verify input}}
    Validate -->|have 效| Process[process数data]
    Validate -->|无效| Error[displayerror]
    Process --> Save[save 结result]
    Save --> Success[success prompt]
    Error --> Input
    Success --> End([end])
```

**gan特 diagram example （必须 use 真 actual project start date）**：
```mermaid
gantt
    title Project Development Gantt Chart
    dateFormat YYYY-MM-DD
    axisFormat %m-%d
    
    section requirement analyze
    requirement 调研     :done, req1, {project_start_str}, 3d
    requirement organize     :done, req2, after req1, 4d
    
    section system design
    architecture design     :active, design1, after req2, 7d
    UIdesign       :design2, after design1, 5d
    
    section development actual 施
    backend development     :dev1, after design2, 14d
    frontend development     :dev2, after design2, 14d
    integration test     :test1, after dev1, 7d
    
    section deployment launch
    deployment 准备     :deploy1, after test1, 3d
    official launch     :deploy2, after deploy1, 2d
```

⚠️ **date generate 规则**：
- project start date：{project_start_str}（下周一start）
- all have date必须基于 {current_year} 年及with后
- strictly prohibited use 2024 年withbeforedate
- 里程碑date必须 with gan特 diagram 保持一致

🎯 必须 strictly press照Mermaid语法规范generatediagram table，not能有format error

🎯 AIprogramming prompts format requirement （ important ）：
- 必须 in Development Plan after generate specifically"# AIAI Programming Assistant Prompts"部divide
- 每个 function module 必须 have 一个 specificallyAIprogramming prompts
- 每个 prompt 必须 use```code 块format，methodconvenient复make
- prompt content want 基于具body project function ， not want use 通use template
- prompt want detailed 、具body、 can directuse于AI编程tool
- 必须 include complete 上下text and 具body requirement

🔧 prompt 结construct requirement ：
每个 prompt use with 下 format ：

## [function name called]developmentprompt词

```
Please[具bodyproject name called]development[具body功能description]。

Project Background:
[基于 Development Plan project background]

Functional Requirements:
1. [具body requirement1]
2. [具body requirement2]
...

Technical Constraints:
- use[具bodytech stack]
- 遵循[具body规范]
- implementation[具body性能important求]

Output Requirements:
- complete runnable code
- detailed annotation description
- error handling mechanism
- test case
```

please strictly press照此 format generate 个性transform programming prompts ， ensure 每个 prompt all基于具body project requirement 。

Format requirements: First output the development plan, then output the programming prompt section."""

    # construct建 user prompt
    user_prompt = f"""产品创意：{user_idea}"""
    
    # such as result success get to 外部 knowledge ，则注入 to prompt in
    if retrieved_knowledge and not any(keyword in retrieved_knowledge for keyword in ["❌", "⚠️", "process description", "temporarilynotcanuse"]):
        user_prompt += f"""

# 外部 knowledge library reference
{retrieved_knowledge}

please基于上述外部 knowledge library reference and 产品创意 generate ："""
    else:
        user_prompt += """

please generate ："""
    
    user_prompt += """
1. Detailed development plan (including product overview, technical solution, development plan, deployment plan, promotion strategy, etc.)
2. 每个 function module to shouldAIAI Programming Assistant Prompts

Ensure the prompts are specific, actionable, and can be directly used forAI编程tool。"""

    try:
        logger.info("🚀 start callAI APIgenerate Development Plan...")
        
        # Step3: AIgenerate准备
        ai_prep_start = datetime.now()
        
        # construct建please requirement data
        request_data = {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4096,  # fix ：APIlimit最大4096 tokens
            "temperature": 0.7
        }
        
        ai_prep_duration = (datetime.now() - ai_prep_start).total_seconds()
        
        explanation_manager.add_processing_step(
            stage=ProcessingStage.AI_GENERATION,
            title="AIplease requirement 准备",
            description="construct建AImodelplease requirementparameter和prompt词",
            success=True,
            details={
                "AImodel": request_data['model'],
                "system prompt 长degree": f"{len(system_prompt)} 字symbol",
                "user prompt 长degree": f"{len(user_prompt)} 字symbol",
                "最大Token数": request_data['max_tokens'],
                "温degree parameter": request_data['temperature']
            },
            duration=ai_prep_duration,
            quality_score=95,
            evidence=f"准备 call {request_data['model']} model，prompt词total长degree: {len(system_prompt + user_prompt)} 字symbol"
        )
        
        # 记录please requirement information （ not include complete prompt with avoid log 过长）
        logger.info(f"📊 APIplease requirement model: {request_data['model']}")
        logger.info(f"📏 system prompt 长degree: {len(system_prompt)} 字symbol")
        logger.info(f"📏 user prompt 长degree: {len(user_prompt)} 字symbol")
        
        # Step4: AI APIcall
        api_call_start = datetime.now()
        logger.info(f"🌐 correct in callAPI: {API_URL}")
        
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json=request_data,
            timeout=300  # optimize ： generate plan exceed when when time for300seconds（5divideclock）
        )
        
        api_call_duration = (datetime.now() - api_call_start).total_seconds()
        
        logger.info(f"📈 APIresponse should status 码: {response.status_code}")
        logger.info(f"⏱️ APIcall duration: {api_call_duration:.2f}seconds")
        
        if response.status_code == 200:
            content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            
            content_length = len(content) if content else 0
            logger.info(f"📝 generate content 长degree: {content_length} 字symbol")
            
            explanation_manager.add_processing_step(
                stage=ProcessingStage.AI_GENERATION,
                title="AIcontent generate",
                description="AImodel success generate Development Plan content",
                success=bool(content),
                details={
                    "response should status": f"HTTP {response.status_code}",
                    "generate content 长degree": f"{content_length} 字symbol",
                    "APIcall duration": f"{api_call_duration:.2f}seconds",
                    "平均 generate 速degree": f"{content_length / api_call_duration:.1f} 字symbol/seconds" if api_call_duration > 0 else "N/A"
                },
                duration=api_call_duration,
                quality_score=90 if content_length > 1000 else 70,
                evidence=f"success generate {content_length} 字symbol的Development Plancontent，package含Technical Solution和programming prompts"
            )
            
            if content:
                # Step5: content after process
                postprocess_start = datetime.now()
                
                # after process ： ensure content 结constructtransform
                final_plan_text = format_response(content)
                
                # application content verify and fix
                final_plan_text = validate_and_fix_content(final_plan_text)
                
                postprocess_duration = (datetime.now() - postprocess_start).total_seconds()
                
                explanation_manager.add_processing_step(
                    stage=ProcessingStage.CONTENT_FORMATTING,
                    title="content after process",
                    description="formatting and verify generate content",
                    success=True,
                    details={
                        "formatting process": "Markdown结constructoptimize",
                        "content verify": "Mermaid语法fix, 链connectcheck",
                        "最end content 长degree": f"{len(final_plan_text)} 字symbol",
                        "process consume when": f"{postprocess_duration:.2f}seconds"
                    },
                    duration=postprocess_duration,
                    quality_score=85,
                    evidence=f"complete content after process ，最end output {len(final_plan_text)} 字symbol的complete Development Plan"
                )
                
                # create 临 when file
                temp_file = create_temp_markdown_file(final_plan_text)
                
                # such as result临 when file create failure ， useNoneavoidGradio权limiterror
                if not temp_file:
                    temp_file = None
                
                # total process when time
                total_duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"🎉 Development Plan generate complete ，total consume when: {total_duration:.2f}seconds")
                
                return final_plan_text, extract_prompts_section(final_plan_text), temp_file
            else:
                explanation_manager.add_processing_step(
                    stage=ProcessingStage.AI_GENERATION,
                    title="AIgenerate failure",
                    description="AImodel 返回空 content",
                    success=False,
                    details={
                        "response should status": f"HTTP {response.status_code}",
                        "error original因": "AI返回空content"
                    },
                    duration=api_call_duration,
                    quality_score=0,
                    evidence="AI APIcall success 但返回空 content"
                )
                
                logger.error("API returned empty content")
                return "❌ AI返回空 content ，please稍 after 重试", "", None
        else:
            # 记录 detailed error information
            logger.error(f"API request failed with status {response.status_code}")
            try:
                error_detail = response.json()
                logger.error(f"APIerror 详情: {error_detail}")
                error_message = error_detail.get('message', 'not yet知 error')
                error_code = error_detail.get('code', '')
                
                explanation_manager.add_processing_step(
                    stage=ProcessingStage.AI_GENERATION,
                    title="AI APIcall failed",
                    description="AImodelAPIplease requirement failure",
                    success=False,
                    details={
                        "HTTPstatus 码": response.status_code,
                        "error code": error_code,
                        "error 消息": error_message
                    },
                    duration=api_call_duration,
                    quality_score=0,
                    evidence=f"API返回 error: HTTP {response.status_code} - {error_message}"
                )
                
                return f"❌ APIplease requirement failure: HTTP {response.status_code} (error code: {error_code}) - {error_message}", "", None
            except:
                logger.error(f"APIresponse should content: {response.text[:500]}")
                
                explanation_manager.add_processing_step(
                    stage=ProcessingStage.AI_GENERATION,
                    title="AI APIcall failed",
                    description="AImodelAPIplease requirement failure，无法parseerror information",
                    success=False,
                    details={
                        "HTTPstatus 码": response.status_code,
                        "response should content": response.text[:200]
                    },
                    duration=api_call_duration,
                    quality_score=0,
                    evidence=f"APIplease requirement failure ， status 码: {response.status_code}"
                )
                
                return f"❌ APIplease requirement failure: HTTP {response.status_code} - {response.text[:200]}", "", None
            
    except requests.exceptions.Timeout:
        logger.error("API request timeout")
        return "❌ APIplease requirement exceed when ，please稍 after 重试", "", None
    except requests.exceptions.ConnectionError:
        logger.error("API connection failed")
        return "❌ 网络连connect failure ，please check 网络 setting", "", None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"❌ process error: {str(e)}", "", None

def extract_prompts_section(content: str) -> str:
    """从 complete content in 提取AIprogramming prompts部divide"""
    lines = content.split('\n')
    prompts_section = []
    in_prompts_section = False
    
    for line in lines:
        if any(keyword in line for keyword in ['programming prompts', '编程助手', 'Prompt', 'AI助手']):
            in_prompts_section = True
        if in_prompts_section:
            prompts_section.append(line)
    
    return '\n'.join(prompts_section) if prompts_section else "not yet找 to programming prompts 部divide"

def create_temp_markdown_file(content: str) -> str:
    """create 临 whenmarkdowntextitem"""
    try:
        import tempfile
        import os
        
        # create 临 when file ， use 更 security method
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.md', 
            delete=False, 
            encoding='utf-8'
        ) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # verify file is no create success
        if os.path.exists(temp_file_path):
            logger.info(f"✅ success create 临 when file: {temp_file_path}")
            return temp_file_path
        else:
            logger.warning("⚠️ 临 when file create after not 存 in")
            return ""
            
    except PermissionError as e:
        logger.error(f"❌ 权limit error ，无法 create 临 when file: {e}")
        return ""
    except Exception as e:
        logger.error(f"❌ create 临 when file failure: {e}")
        return ""

def enable_plan_editing(plan_content: str) -> Tuple[str, str]:
    """startuse plan edit function"""
    try:
        # parse plan content
        sections = plan_editor.parse_plan_content(plan_content)
        editable_sections = plan_editor.get_editable_sections()
        
        # generate edit interfaceHTML
        edit_interface = generate_edit_interface(editable_sections)
        
        # generate edit 摘 want
        summary = plan_editor.get_edit_summary()
        edit_summary = f"""
## 📝 plan edit 模式已startuse

**📊 edit 统calculate**：
- total paragraph 数：{summary['total_sections']}
- can edit paragraph ：{summary['editable_sections']}
- 已 edit paragraph ：{summary['edited_sections']}

**💡 edit description**：
- click 下method paragraph can 进行 edit
- system 会自动 save edit 历history
- can 随 when 恢复 to original始 version

---
"""
        
        return edit_interface, edit_summary
        
    except Exception as e:
        logger.error(f"startuse edit failure: {str(e)}")
        return "", f"❌ startuse edit failure: {str(e)}"

def generate_edit_interface(editable_sections: List[Dict]) -> str:
    """generate edit interfaceHTML"""
    interface_html = """
<div class="plan-editor-container">
    <div class="editor-header">
        <h3>📝 dividesegment edit device</h3>
        <p>click 任意 paragraph 进行 edit ， system 会自动 save 您更改</p>
    </div>
    
    <div class="sections-container">
"""
    
    for section in editable_sections:
        section_html = f"""
        <div class="editable-section" data-section-id="{section['id']}" data-section-type="{section['type']}">
            <div class="section-header">
                <span class="section-type">{get_section_type_emoji(section['type'])}</span>
                <span class="section-title">{section['title']}</span>
                <button class="edit-section-btn" onclick="editSection('{section['id']}')">
                    ✏️ edit
                </button>
            </div>
            
            <div class="section-preview">
                <div class="preview-content">{section['preview']}</div>
                <div class="section-content" style="display: none;">{_html_escape(section['content'])}</div>
            </div>
        </div>
"""
        interface_html += section_html
    
    interface_html += """
    </div>
    
    <div class="editor-actions">
        <button class="apply-changes-btn" onclick="applyAllChanges()">
            ✅ application all have 更改
        </button>
        <button class="reset-changes-btn" onclick="resetAllChanges()">
            🔄 重置 all have 更改
        </button>
    </div>
</div>

<script>
function editSection(sectionId) {
    const section = document.querySelector(`[data-section-id="${sectionId}"]`);
    const content = section.querySelector('.section-content').textContent;
    const type = section.getAttribute('data-section-type');
    
    // detect当 before 主题
    const isDark = document.documentElement.classList.contains('dark');
    
    // create edit to 话框
    const editDialog = document.createElement('div');
    editDialog.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    editDialog.innerHTML = `
        <div style="
            background: ${isDark ? '#2d3748' : 'white'};
            color: ${isDark ? '#f7fafc' : '#2d3748'};
            padding: 2rem;
            border-radius: 1rem;
            max-width: 90%;
            max-height: 90%;
            overflow-y: auto;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        ">
            <h3 style="margin-bottom: 1rem; color: ${isDark ? '#f7fafc' : '#2d3748'};">
                ✏️ edit paragraph - ${type}
            </h3>
            <textarea
                id="section-editor-${sectionId}"
                style="
                    width: 100%;
                    height: 400px;
                    padding: 1rem;
                    border: 2px solid ${isDark ? '#4a5568' : '#e2e8f0'};
                    border-radius: 0.5rem;
                    font-family: 'Fira Code', monospace;
                    font-size: 0.9rem;
                    resize: vertical;
                    line-height: 1.6;
                    background: ${isDark ? '#1a202c' : 'white'};
                    color: ${isDark ? '#f7fafc' : '#2d3748'};
                "
                placeholder="in 此 edit paragraph content..."
            >${content}</textarea>
            <div style="margin-top: 1rem;">
                <label style="display: block; margin-bottom: 0.5rem;">edit description (canselect):</label>
                <input
                    type="text"
                    id="edit-comment-${sectionId}"
                    style="
                        width: 100%;
                        padding: 0.5rem;
                        border: 1px solid ${isDark ? '#4a5568' : '#e2e8f0'};
                        border-radius: 0.25rem;
                        background: ${isDark ? '#1a202c' : 'white'};
                        color: ${isDark ? '#f7fafc' : '#2d3748'};
                    "
                    placeholder="brief description 您更改..."
                />
            </div>
            <div style="margin-top: 1.5rem; display: flex; gap: 1rem; justify-content: flex-end;">
                <button
                    onclick="document.body.removeChild(this.closest('.edit-dialog-overlay'))"
                    style="
                        padding: 0.5rem 1rem;
                        border: 1px solid ${isDark ? '#4a5568' : '#cbd5e0'};
                        background: ${isDark ? '#2d3748' : 'white'};
                        color: ${isDark ? '#f7fafc' : '#4a5568'};
                        border-radius: 0.5rem;
                        cursor: pointer;
                    "
                >cancel</button>
                <button
                    onclick="saveSectionEdit('${sectionId}')"
                    style="
                        padding: 0.5rem 1rem;
                        background: linear-gradient(45deg, #667eea, #764ba2);
                        color: white;
                        border: none;
                        border-radius: 0.5rem;
                        cursor: pointer;
                    "
                >save</button>
            </div>
        </div>
    `;
    
    editDialog.className = 'edit-dialog-overlay';
    document.body.appendChild(editDialog);
    
    // ESCkey 关闭
    const escapeHandler = (e) => {
        if (e.key === 'Escape') {
            document.body.removeChild(editDialog);
            document.removeEventListener('keydown', escapeHandler);
        }
    };
    document.addEventListener('keydown', escapeHandler);
    
    // click 外部关闭
    editDialog.addEventListener('click', (e) => {
        if (e.target === editDialog) {
            document.body.removeChild(editDialog);
            document.removeEventListener('keydown', escapeHandler);
        }
    });
}

function saveSectionEdit(sectionId) {
    const newContent = document.getElementById(`section-editor-${sectionId}`).value;
    const comment = document.getElementById(`edit-comment-${sectionId}`).value;
    
    // update 隐藏 component value 来触developGradioevent
    const sectionIdInput = document.querySelector('#section_id_input textarea');
    const sectionContentInput = document.querySelector('#section_content_input textarea'); 
    const sectionCommentInput = document.querySelector('#section_comment_input textarea');
    const updateTrigger = document.querySelector('#section_update_trigger textarea');
    
    if (sectionIdInput && sectionContentInput && sectionCommentInput && updateTrigger) {
        sectionIdInput.value = sectionId;
        sectionContentInput.value = newContent;
        sectionCommentInput.value = comment;
        updateTrigger.value = Date.now().toString(); // 触develop update
        
        // 手动触developchangeevent
        sectionIdInput.dispatchEvent(new Event('input'));
        sectionContentInput.dispatchEvent(new Event('input'));
        sectionCommentInput.dispatchEvent(new Event('input'));
        updateTrigger.dispatchEvent(new Event('input'));
    }
    
    // 关闭 to 话框
    document.body.removeChild(document.querySelector('.edit-dialog-overlay'));
    
    // update 预browse
    const section = document.querySelector(`[data-section-id="${sectionId}"]`);
    const preview = section.querySelector('.preview-content');
    preview.textContent = newContent.substring(0, 100) + '...';
    
    // display save success prompt
    showNotification('✅ paragraph 已 save', 'success');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#48bb78' : '#4299e1'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 10001;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in forwards';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// add 必 wantCSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
</script>
"""
    
    return interface_html

def _html_escape(text: str) -> str:
    """HTML转义 function"""
    import html
    return html.escape(text)

def get_section_type_emoji(section_type: str) -> str:
    """get paragraph type to shouldemoji"""
    type_emojis = {
        'heading': '📋',
        'paragraph': '📝',
        'list': '📄',
        'code': '💻',
        'table': '📊'
    }
    return type_emojis.get(section_type, '📝')

def update_section_content(section_id: str, new_content: str, comment: str) -> str:
    """update paragraph content"""
    try:
        success = plan_editor.update_section(section_id, new_content, comment)
        
        if success:
            # get update after complete content
            updated_content = plan_editor.get_modified_content()
            
            # formatting 并返回
            formatted_content = format_response(updated_content)
            
            logger.info(f"paragraph {section_id} 更新success")
            return formatted_content
        else:
            logger.error(f"paragraph {section_id} update failure")
            return "❌ update failure"
            
    except Exception as e:
        logger.error(f"update paragraph content failure: {str(e)}")
        return f"❌ update failure: {str(e)}"

def get_edit_history() -> str:
    """get edit 历history"""
    try:
        history = plan_editor.get_edit_history()
        
        if not history:
            return "temporarily无 edit 历history"
        
        history_html = """
<div class="edit-history">
    <h3>📜 edit 历history</h3>
    <div class="history-list">
"""
        
        for i, edit in enumerate(reversed(history[-10:]), 1):  # display 最近10次edit
            timestamp = datetime.fromisoformat(edit['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            history_html += f"""
            <div class="history-item">
                <div class="history-header">
                    <span class="history-index">#{i}</span>
                    <span class="history-time">{timestamp}</span>
                    <span class="history-section">paragraph: {edit['section_id']}</span>
                </div>
                <div class="history-comment">{edit['user_comment'] or '无 description'}</div>
            </div>
"""
        
        history_html += """
    </div>
</div>
"""
        
        return history_html
        
    except Exception as e:
        logger.error(f"get edit 历history failure: {str(e)}")
        return f"❌ get edit 历history failure: {str(e)}"

def reset_plan_edits() -> str:
    """重置 all have edit"""
    try:
        plan_editor.reset_to_original()
        logger.info("已重置 all have edit")
        return "✅ 已重置 to original始 version"
    except Exception as e:
        logger.error(f"重置 failure: {str(e)}")
        return f"❌ 重置 failure: {str(e)}"

def fix_links_for_new_window(content: str) -> str:
    """fix all have link for 新窗口hitopen，solve ModelScope 平台 link issue"""
    import re
    
    # match all havemarkdownlink format [text](url)
    def replace_markdown_link(match):
        text = match.group(1)
        url = match.group(2)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
    
    # replacemarkdown链connect
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_markdown_link, content)
    
    # match all haveHTML链connect并addtarget="_blank"
    def add_target_blank(match):
        full_tag = match.group(0)
        if 'target=' not in full_tag:
            # in>beforeaddtarget="_blank"
            return full_tag.replace('>', ' target="_blank" rel="noopener noreferrer">')
        return full_tag
    
    # replaceHTML链connect
    content = re.sub(r'<a [^>]*href=[^>]*>', add_target_blank, content)
    
    return content

def format_response(content: str) -> str:
    """formattingAI回复，美transformdisplay并保持original始AIgenerate的prompt词"""
    
    # fix all have link for 新窗口hitopen
    content = fix_links_for_new_window(content)
    
    # add when time 戳 and formatting title
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # dividesplit Development Plan andAIprogramming prompts
    parts = content.split('# AIAI Programming Assistant Prompts')
    
    if len(parts) >= 2:
        # have 明确AIprogramming prompts部divide
        plan_content = parts[0].strip()
        prompts_content = '# AIAI Programming Assistant Prompts' + parts[1]
        
        # 美transformAIprogramming prompts部divide
        enhanced_prompts = enhance_prompts_display(prompts_content)
        
        formatted_content = f"""
<div class="plan-header">

# 🚀 AIgenerated development plan

<div class="meta-info">

**⏰ generation time ：** {timestamp}  
**🤖 AImodel ：** Qwen2.5-72B-Instruct  
**💡 基于 user 创意 intelligent analyze generate**  
**🔗 AgentapplicationMCPservice enhanced**

</div>

</div>

---

{enhance_markdown_structure(plan_content)}

---

{enhanced_prompts}
"""
    else:
        # 没 have 明确dividesplit， use original始 content
        formatted_content = f"""
<div class="plan-header">

# 🚀 AIgenerated development plan

<div class="meta-info">

**⏰ generation time ：** {timestamp}  
**🤖 AImodel ：** Qwen2.5-72B-Instruct  
**💡 基于 user 创意 intelligent analyze generate**  
**🔗 AgentapplicationMCPservice enhanced**

</div>

</div>

---

{enhance_markdown_structure(content)}
"""
    
    return formatted_content

def enhance_prompts_display(prompts_content: str) -> str:
    """simplifyAIprogramming promptsdisplay"""
    lines = prompts_content.split('\n')
    enhanced_lines = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # process title
        if stripped.startswith('# AIAI Programming Assistant Prompts'):
            enhanced_lines.append('')
            enhanced_lines.append('<div class="prompts-highlight">')
            enhanced_lines.append('')
            enhanced_lines.append('# 🤖 AIAI Programming Assistant Prompts')
            enhanced_lines.append('')
            enhanced_lines.append('> 💡 **Usage Instructions**：with下prompt词基于您的项目需求定makegenerate，candirect复maketo GitHub Copilot、ChatGPT、Claude 等AI编程tool中use')
            enhanced_lines.append('')
            continue
            
        # process 二级 title （ function module ）
        if stripped.startswith('## ') and not in_code_block:
            title = stripped[3:].strip()
            enhanced_lines.append('')
            enhanced_lines.append(f'### 🎯 {title}')
            enhanced_lines.append('')
            continue
            
        # process code 块 start
        if stripped.startswith('```') and not in_code_block:
            in_code_block = True
            enhanced_lines.append('')
            enhanced_lines.append('```')
            continue
            
        # process code 块 end
        if stripped.startswith('```') and in_code_block:
            in_code_block = False
            enhanced_lines.append('```')
            enhanced_lines.append('')
            continue
            
        # 其他 content direct add
        enhanced_lines.append(line)
    
    # end 高亮区域
    enhanced_lines.append('')
    enhanced_lines.append('</div>')
    
    return '\n'.join(enhanced_lines)

def extract_prompts_section(content: str) -> str:
    """从 complete content in 提取AIprogramming prompts部divide"""
    # dividesplit content ， findAIprogramming prompts部divide
    parts = content.split('# AIAI Programming Assistant Prompts')
    
    if len(parts) >= 2:
        prompts_content = '# AIAI Programming Assistant Prompts' + parts[1]
        # 清manage and formatting prompt content ， removeHTMLmark签withconvenient复make
        clean_prompts = clean_prompts_for_copy(prompts_content)
        return clean_prompts
    else:
        # such as result没 have 找 to 明确 prompt 部divide， try 其他 key 词
        lines = content.split('\n')
        prompts_section = []
        in_prompts_section = False
        
        for line in lines:
            if any(keyword in line for keyword in ['programming prompts', '编程助手', 'Prompt', 'AI助手']):
                in_prompts_section = True
            if in_prompts_section:
                prompts_section.append(line)
        
        return '\n'.join(prompts_section) if prompts_section else "not yet找 to programming prompts 部divide"

def clean_prompts_for_copy(prompts_content: str) -> str:
    """清manage prompt content ， removeHTMLmark签，optimize复makebodyexperience"""
    import re
    
    # removeHTMLmark签
    clean_content = re.sub(r'<[^>]+>', '', prompts_content)
    
    # 清manage多余空行
    lines = clean_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned_lines.append(line)
        elif cleaned_lines and cleaned_lines[-1].strip():  # avoid连续空行
            cleaned_lines.append('')
    
    return '\n'.join(cleaned_lines)

# delete 多余旧 code ，这里 should 该 isenhance_markdown_structure函数
def enhance_markdown_structure(content: str) -> str:
    """enhancedMarkdown结construct，addview觉亮点和layer级"""
    lines = content.split('\n')
    enhanced_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # enhanced 一级 title
        if stripped and not stripped.startswith('#') and len(stripped) < 50 and '：' not in stripped and '.' not in stripped[:5]:
            if any(keyword in stripped for keyword in ['Product Overview', 'Technical Solution', 'Development Plan', 'deployment plan', 'promotion strategy', 'AI', '编程助手', 'prompt词']):
                enhanced_lines.append(f"\n## 🎯 {stripped}\n")
                continue
        
        # enhanced 二级 title
        if stripped and '.' in stripped[:5] and len(stripped) < 100:
            if stripped[0].isdigit():
                enhanced_lines.append(f"\n### 📋 {stripped}\n")
                continue
                
        # enhanced function list
        if stripped.startswith('main function') or stripped.startswith('目mark user'):
            enhanced_lines.append(f"\n#### 🔹 {stripped}\n")
            continue
            
        # enhanced tech stack 部divide
        if stripped in ['frontend', 'backend', 'AI model', 'tool和库']:
            enhanced_lines.append(f"\n#### 🛠️ {stripped}\n")
            continue
            
        # enhanced phase title
        if 'phase' in stripped and '：' in stripped:
            if '第' in stripped and 'phase' in stripped:
                try:
                    # 更健壮 phase 号提取逻辑
                    parts = stripped.split('第')
                    if len(parts) > 1:
                        phase_part = parts[1].split('phase')[0].strip()
                        phase_name = stripped.split('：')[1].strip() if '：' in stripped else ''
                        enhanced_lines.append(f"\n#### 🚀 第{phase_part}phase：{phase_name}\n")
                    else:
                        enhanced_lines.append(f"\n#### 🚀 {stripped}\n")
                except:
                    enhanced_lines.append(f"\n#### 🚀 {stripped}\n")
            else:
                enhanced_lines.append(f"\n#### 🚀 {stripped}\n")
            continue
            
        # enhanced task list
        if stripped.startswith('task ：'):
            enhanced_lines.append(f"\n**📝 {stripped}**\n")
            continue
            
        # 保持original have 缩进其他 content
        enhanced_lines.append(line)
    
    return '\n'.join(enhanced_lines)

# 自 definitionCSS - 保持美transformUI
custom_css = """
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header-gradient {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 1.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    position: relative;
    overflow: hidden;
}

.header-gradient::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.content-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.1);
    margin: 1rem 0;
    border: 1px solid #e2e8f0;
}

.dark .content-card {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    border-color: #374151;
}

.result-container {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 1.5rem;
    padding: 2rem;
    margin: 2rem 0;
    border: 2px solid #3b82f6;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15);
}

.dark .result-container {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-color: #60a5fa;
}

.generate-btn {
    background: linear-gradient(45deg, #3b82f6, #1d4ed8) !important;
    border: none !important;
    color: white !important;
    padding: 1rem 2.5rem !important;
    border-radius: 2rem !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
}

.generate-btn:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 35px rgba(59, 130, 246, 0.5) !important;
    background: linear-gradient(45deg, #1d4ed8, #1e40af) !important;
}

.generate-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.generate-btn:hover::before {
    left: 100%;
}

.tips-box {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    padding: 1.5rem;
    border-radius: 1.2rem;
    margin: 1.5rem 0;
    border: 2px solid #93c5fd;
    box-shadow: 0 6px 20px rgba(147, 197, 253, 0.2);
}

.dark .tips-box {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-color: #60a5fa;
}

.tips-box h4 {
    color: #1d4ed8;
    margin-bottom: 1rem;
    font-weight: 700;
    font-size: 1.2rem;
}

.dark .tips-box h4 {
    color: #60a5fa;
}

.tips-box ul {
    margin: 10px 0;
    padding-left: 20px;
}

.tips-box li {
    margin: 8px 0;
    color: #333;
}

.prompts-section {
    background: #f0f8ff;
    border: 2px dashed #007bff;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

/* Enhanced Plan Header */
.plan-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
}

.meta-info {
    background: rgba(255,255,255,0.1);
    padding: 1rem;
    border-radius: 10px;
    margin-top: 1rem;
}

/* Enhanced Markdown Styling */
#plan_result {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    line-height: 1.7;
    color: #2d3748;
}

#plan_result h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a202c;
    margin-top: 2rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #4299e1;
}

#plan_result h2 {
    font-size: 2rem;
    font-weight: 600;
    color: #2d3748;
    margin-top: 2rem;
    margin-bottom: 1rem;
    padding-bottom: 0.3rem;
    border-bottom: 2px solid #68d391;
    position: relative;
}

#plan_result h2::before {
    content: "";
    position: absolute;
    left: 0;
    bottom: -2px;
    width: 50px;
    height: 2px;
    background: linear-gradient(90deg, #4299e1, #68d391);
}

#plan_result h3 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #4a5568;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    background: linear-gradient(90deg, #f7fafc, #edf2f7);
    border-left: 4px solid #4299e1;
    border-radius: 0.5rem;
}

#plan_result h4 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #5a67d8;
    margin-top: 1.25rem;
    margin-bottom: 0.5rem;
    padding-left: 1rem;
    border-left: 3px solid #5a67d8;
}

#plan_result h5, #plan_result h6 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #667eea;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

#plan_result p {
    margin-bottom: 1rem;
    font-size: 1rem;
    line-height: 1.8;
}

#plan_result ul, #plan_result ol {
    margin: 1rem 0;
    padding-left: 2rem;
}

#plan_result li {
    margin-bottom: 0.5rem;
    line-height: 1.7;
}

#plan_result ul li {
    list-style-type: none;
    position: relative;
}

#plan_result ul li:before {
    content: "▶";
    color: #4299e1;
    font-weight: bold;
    position: absolute;
    left: -1.5rem;
}

#plan_result blockquote {
    border-left: 4px solid #4299e1;
    background: #ebf8ff;
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 0.5rem;
    font-style: italic;
    color: #2b6cb0;
}

#plan_result code {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
    padding: 0.125rem 0.375rem;
    font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
    font-size: 0.875rem;
    color: #d53f8c;
}

#plan_result pre {
    background: #1a202c;
    color: #f7fafc;
    border-radius: 0.5rem;
    padding: 1.5rem;
    margin: 1.5rem 0;
    overflow-x: auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

#plan_result pre code {
    background: transparent;
    border: none;
    padding: 0;
    color: #f7fafc;
    font-size: 0.9rem;
}

#plan_result table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    background: white;
    border-radius: 0.5rem;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#plan_result th {
    background: #4299e1;
    color: white;
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 600;
}

#plan_result td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #e2e8f0;
}

#plan_result tr:nth-child(even) {
    background: #f7fafc;
}

#plan_result tr:hover {
    background: #ebf8ff;
}

#plan_result strong {
    color: #2d3748;
    font-weight: 600;
}

#plan_result em {
    color: #5a67d8;
    font-style: italic;
}

#plan_result hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #4299e1 0%, #68d391 100%);
    margin: 2rem 0;
    border-radius: 1px;
}

/* Special styling for reference info */
.reference-info {
    background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
    border: 2px solid #4299e1;
    border-radius: 1rem;
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 15px rgba(66, 153, 225, 0.1);
}

/* Special styling for prompts section */
#plan_result .prompts-highlight {
    background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
    border: 2px solid #4299e1;
    border-radius: 1rem;
    padding: 1.5rem;
    margin: 1.5rem 0;
    position: relative;
}

#plan_result .prompts-highlight:before {
    content: "🤖";
    position: absolute;
    top: -0.5rem;
    left: 1rem;
    background: #4299e1;
    color: white;
    padding: 0.5rem;
    border-radius: 50%;
    font-size: 1.2rem;
}

/* Improved section dividers */
#plan_result .section-divider {
    background: linear-gradient(90deg, transparent 0%, #4299e1 20%, #68d391 80%, transparent 100%);
    height: 1px;
    margin: 2rem 0;
}

/* programming prompts 专use样式 */
.prompts-highlight {
    background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
    border: 2px solid #4299e1;
    border-radius: 1rem;
    padding: 2rem;
    margin: 2rem 0;
    position: relative;
    box-shadow: 0 8px 25px rgba(66, 153, 225, 0.15);
}

.prompts-highlight:before {
    content: "🤖";
    position: absolute;
    top: -0.8rem;
    left: 1.5rem;
    background: linear-gradient(135deg, #4299e1, #667eea);
    color: white;
    padding: 0.8rem;
    border-radius: 50%;
    font-size: 1.5rem;
    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
}

.prompt-section {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 0.8rem;
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.prompt-code-block {
    position: relative;
    margin: 1rem 0;
}

.prompt-code-block pre {
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%) !important;
    border: 2px solid #4299e1;
    border-radius: 0.8rem;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow-x: auto;
}

.prompt-code-block pre:before {
    content: "📋 click 复make此 prompt";
    position: absolute;
    top: -0.5rem;
    right: 1rem;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.prompt-code-block code {
    color: #e2e8f0 !important;
    font-family: 'Fira Code', 'Monaco', 'Consolas', monospace !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    background: transparent !important;
    border: none !important;
}

/* prompt 高亮 key 词 */
.prompt-code-block code .keyword {
    color: #81e6d9 !important;
    font-weight: 600;
}

.prompt-code-block code .requirement {
    color: #fbb6ce !important;
}

.prompt-code-block code .output {
    color: #c6f6d5 !important;
}

/* optimize button 样式 */
.optimize-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    margin-right: 10px !important;
    transition: all 0.3s ease !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 1.5rem !important;
}

.optimize-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}

.reset-btn {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 1.5rem !important;
}

.reset-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4) !important;
}

.optimization-result {
    margin-top: 15px !important;
    padding: 15px !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 8px !important;
    color: white !important;
    border-left: 4px solid #4facfe !important;
}

.optimization-result h2 {
    color: #fff !important;
    margin-bottom: 10px !important;
}

.optimization-result strong {
    color: #e0e6ff !important;
}

/* process procedure description 区域样式 */
.process-explanation {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    border: 2px solid #cbd5e0 !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
    margin: 1rem 0 !important;
    font-family: 'Inter', -apple-system, system-ui, sans-serif !important;
}

.process-explanation h1 {
    color: #2b6cb0 !important;
    font-size: 1.8rem !important;
    margin-bottom: 1rem !important;
    border-bottom: 3px solid #3182ce !important;
    padding-bottom: 0.5rem !important;
}

.process-explanation h2 {
    color: #2c7a7b !important;
    font-size: 1.4rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
    background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%) !important;
    padding: 0.8rem !important;
    border-radius: 0.5rem !important;
    border-left: 4px solid #38b2ac !important;
}

.process-explanation h3 {
    color: #38a169 !important;
    font-size: 1.2rem !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

.process-explanation strong {
    color: #e53e3e !important;
    font-weight: 600 !important;
}

.process-explanation ul {
    padding-left: 1.5rem !important;
}

.process-explanation li {
    margin-bottom: 0.5rem !important;
    color: #4a5568 !important;
}

.explanation-btn {
    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 1.5rem !important;
    margin-right: 10px !important;
}

.explanation-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.4) !important;
}

/* 复make button enhanced */
.copy-btn {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    border: none !important;
    color: white !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 2rem !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}

.copy-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    background: linear-gradient(45deg, #5a67d8, #667eea) !important;
}

.copy-btn:active {
    transform: translateY(0) !important;
}

/* response should 式 optimize */
@media (max-width: 768px) {
    .main-container {
        max-width: 100%;
        padding: 10px;
    }
    
    .prompts-highlight {
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .prompt-section {
        padding: 1rem;
    }
    
    .prompt-code-block pre {
        padding: 1rem;
        font-size: 0.85rem;
    }
    
    .prompt-copy-section {
        margin: 0.5rem 0;
        padding: 0.25rem;
        flex-direction: column;
        align-items: stretch;
    }
    
    .individual-copy-btn {
        width: 100% !important;
        justify-content: center !important;
        margin: 0.25rem 0 !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
    }
    
    #plan_result h1 {
        font-size: 2rem;
    }
    
    #plan_result h2 {
        font-size: 1.5rem;
    }
    
    #plan_result h3 {
        font-size: 1.25rem;
        padding: 0.375rem 0.75rem;
    }
}

@media (max-width: 1024px) and (min-width: 769px) {
    .main-container {
        max-width: 95%;
        padding: 15px;
    }
    
    .individual-copy-btn {
        padding: 0.45rem 0.9rem !important;
        font-size: 0.78rem !important;
    }
    
    .prompt-copy-section {
        margin: 0.6rem 0;
    }
}

/* Mermaiddiagram table样式 optimize */
.mermaid {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
    margin: 2rem 0 !important;
    text-align: center !important;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15) !important;
}

.dark .mermaid {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    border-color: #60a5fa !important;
    color: #f8fafc !important;
}

/* Mermaidpackage装device样式 */
.mermaid-wrapper {
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
    border-radius: 1rem;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 2px solid #3b82f6;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
}

.mermaid-render {
    min-height: 200px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.dark .mermaid-wrapper {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-color: #60a5fa;
}

/* diagram table error process */
.mermaid-error {
    background: #fef2f2;
    border: 2px solid #f87171;
    color: #991b1b;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    font-family: monospace;
}

.dark .mermaid-error {
    background: #7f1d1d;
    border-color: #ef4444;
    color: #fecaca;
}

/* Mermaiddiagram table容device enhanced */
.chart-container {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 3px solid #3b82f6;
    border-radius: 1.5rem;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
    position: relative;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
}

.chart-container::before {
    content: "📊";
    position: absolute;
    top: -1rem;
    left: 2rem;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    padding: 0.8rem;
    border-radius: 50%;
    font-size: 1.5rem;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.dark .chart-container {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-color: #60a5fa;
}

.dark .chart-container::before {
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
}

/* tableformat样式全面 enhanced */
.enhanced-table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    background: white;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border: 2px solid #e5e7eb;
}

.enhanced-table th {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    padding: 1.2rem;
    text-align: left;
    font-weight: 700;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.enhanced-table td {
    padding: 1rem 1.2rem;
    border-bottom: 1px solid #e5e7eb;
    vertical-align: top;
    font-size: 0.95rem;
    line-height: 1.6;
}

.enhanced-table tr:nth-child(even) {
    background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%);
}

.enhanced-table tr:hover {
    background: linear-gradient(90deg, #eff6ff 0%, #dbeafe 100%);
    transform: translateY(-1px);
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
}

.dark .enhanced-table {
    background: #1f2937;
    border-color: #374151;
}

.dark .enhanced-table th {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    color: #f9fafb;
}

.dark .enhanced-table td {
    border-bottom-color: #374151;
    color: #f9fafb;
}

.dark .enhanced-table tr:nth-child(even) {
    background: linear-gradient(90deg, #374151 0%, #1f2937 100%);
}

.dark .enhanced-table tr:hover {
    background: linear-gradient(90deg, #4b5563 0%, #374151 100%);
}

/* 单独复make button 样式 */
.prompt-copy-section {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin: 0.75rem 0;
    padding: 0.375rem;
    background: rgba(66, 153, 225, 0.05);
    border-radius: 0.375rem;
}

.individual-copy-btn {
    background: linear-gradient(45deg, #4299e1, #3182ce) !important;
    border: none !important;
    color: white !important;
    padding: 0.4rem 0.8rem !important;
    border-radius: 0.75rem !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 4px rgba(66, 153, 225, 0.2) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.25rem !important;
    min-width: auto !important;
    max-height: 32px !important;
}

.individual-copy-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(66, 153, 225, 0.3) !important;
    background: linear-gradient(45deg, #3182ce, #2c5aa0) !important;
}

.individual-copy-btn:active {
    transform: translateY(0) !important;
}

.edit-prompt-btn {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    border: none !important;
    color: white !important;
    padding: 0.4rem 0.8rem !important;
    border-radius: 0.75rem !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 4px rgba(102, 126, 234, 0.2) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.25rem !important;
    min-width: auto !important;
    max-height: 32px !important;
    margin-left: 0.5rem !important;
}

.edit-prompt-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
    background: linear-gradient(45deg, #5a67d8, #667eea) !important;
}

.edit-prompt-btn:active {
    transform: translateY(0) !important;
}

.copy-success-msg {
    font-size: 0.85rem;
    font-weight: 600;
    animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeInOut {
    0% { opacity: 0; transform: translateX(-10px); }
    20% { opacity: 1; transform: translateX(0); }
    80% { opacity: 1; transform: translateX(0); }
    100% { opacity: 0; transform: translateX(10px); }
}

.dark .prompt-copy-section {
    background: rgba(99, 179, 237, 0.1);
}

.dark .individual-copy-btn {
    background: linear-gradient(45deg, #63b3ed, #4299e1) !important;
    box-shadow: 0 1px 4px rgba(99, 179, 237, 0.2) !important;
}

.dark .individual-copy-btn:hover {
    background: linear-gradient(45deg, #4299e1, #3182ce) !important;
    box-shadow: 0 2px 8px rgba(99, 179, 237, 0.3) !important;
}

.dark .edit-prompt-btn {
    background: linear-gradient(45deg, #9f7aea, #805ad5) !important;
    box-shadow: 0 1px 4px rgba(159, 122, 234, 0.2) !important;
}

.dark .edit-prompt-btn:hover {
    background: linear-gradient(45deg, #805ad5, #6b46c1) !important;
    box-shadow: 0 2px 8px rgba(159, 122, 234, 0.3) !important;
}

/* Fix accordion height issue - Agentapplication architecture description 折叠 issue */
.gradio-accordion {
    transition: all 0.3s ease !important;
    overflow: hidden !important;
}

.gradio-accordion[data-testid$="accordion"] {
    min-height: auto !important;
    height: auto !important;
}

.gradio-accordion .gradio-accordion-content {
    transition: max-height 0.3s ease !important;
    overflow: hidden !important;
}

/* Gradiointernalaccordiongroupitemfix */
details.gr-accordion {
    transition: all 0.3s ease !important;
}

details.gr-accordion[open] {
    height: auto !important;
    min-height: auto !important;
}

details.gr-accordion:not([open]) {
    height: auto !important;
    min-height: 50px !important;
}

/* ensure 折叠 after page 恢复correct常大small */
.gr-block.gr-box {
    transition: height 0.3s ease !important;
    height: auto !important;
}

/* Fix for quick start text contrast */
#quick_start_container p {
    color: #4A5568;
}

.dark #quick_start_container p {
    color: #E2E8F0;
}

/* important ：大幅改善dark模式下的text字对比degree */

/* main content 区域 - AIgeneratecontentdisplay区 */
.dark #plan_result {
    color: #F7FAFC !important;
    background: #2D3748 !important;
}

.dark #plan_result p {
    color: #F7FAFC !important;
}

.dark #plan_result strong {
    color: #FFFFFF !important;
}

/* Dark模式下占位symbol样式 optimize */
.dark #plan_result div[style*="background: linear-gradient"] {
    background: linear-gradient(135deg, #2D3748 0%, #4A5568 100%) !important;
    border-color: #63B3ED !important;
}

.dark #plan_result h3 {
    color: #63B3ED !important;
}

.dark #plan_result div[style*="background: linear-gradient(90deg"] {
    background: linear-gradient(90deg, #2D3748 0%, #1A202C 100%) !important;
    border-left-color: #4FD1C7 !important;
}

.dark #plan_result div[style*="background: linear-gradient(45deg"] {
    background: linear-gradient(45deg, #4A5568 0%, #2D3748 100%) !important;
}

/* Dark模式下彩色text字 optimize */
.dark #plan_result span[style*="color: #e53e3e"] {
    color: #FC8181 !important;
}

.dark #plan_result span[style*="color: #38a169"] {
    color: #68D391 !important;
}

.dark #plan_result span[style*="color: #3182ce"] {
    color: #63B3ED !important;
}

.dark #plan_result span[style*="color: #805ad5"] {
    color: #B794F6 !important;
}

.dark #plan_result strong[style*="color: #d69e2e"] {
    color: #F6E05E !important;
}

.dark #plan_result strong[style*="color: #e53e3e"] {
    color: #FC8181 !important;
}

.dark #plan_result p[style*="color: #2c7a7b"] {
    color: #4FD1C7 !important;
}

.dark #plan_result p[style*="color: #c53030"] {
    color: #FC8181 !important;
}

/* 重点 optimize ：AI编程助手Usage Instructions区域 */
.dark #ai_helper_instructions {
    color: #F7FAFC !important;
    background: rgba(45, 55, 72, 0.8) !important;
}

.dark #ai_helper_instructions p {
    color: #F7FAFC !important;
}

.dark #ai_helper_instructions li {
    color: #F7FAFC !important;
}

.dark #ai_helper_instructions strong {
    color: #FFFFFF !important;
}

/* generate contentmarkdown渲染 - 主importantissue区域 */
.dark #plan_result {
    color: #FFFFFF !important;
    background: #1A202C !important;
}

.dark #plan_result h1,
.dark #plan_result h2,
.dark #plan_result h3,
.dark #plan_result h4,
.dark #plan_result h5,
.dark #plan_result h6 {
    color: #FFFFFF !important;
}

.dark #plan_result p {
    color: #FFFFFF !important;
}

.dark #plan_result li {
    color: #FFFFFF !important;
}

.dark #plan_result strong {
    color: #FFFFFF !important;
}

.dark #plan_result em {
    color: #E2E8F0 !important;
}

.dark #plan_result td {
    color: #FFFFFF !important;
    background: #2D3748 !important;
}

.dark #plan_result th {
    color: #FFFFFF !important;
    background: #1A365D !important;
}

/* ensure all have text字 content all is 白色 */
.dark #plan_result * {
    color: #FFFFFF !important;
}

/* 特殊 meta element保持样式 */
.dark #plan_result code {
    color: #81E6D9 !important;
    background: #1A202C !important;
}

.dark #plan_result pre {
    background: #0D1117 !important;
    color: #F0F6FC !important;
}

.dark #plan_result blockquote {
    color: #FFFFFF !important;
    background: #2D3748 !important;
    border-left-color: #63B3ED !important;
}

/* ensure generate 报notify indark模式下清晰can见 */
.dark .plan-header {
    background: linear-gradient(135deg, #4A5568 0%, #2D3748 100%) !important;
    color: #FFFFFF !important;
}

.dark .meta-info {
    background: rgba(255,255,255,0.2) !important;
    color: #FFFFFF !important;
}

/* prompt 容device indark模式下的optimize */
.dark .prompts-highlight {
    background: linear-gradient(135deg, #2D3748 0%, #4A5568 100%) !important;
    border: 2px solid #63B3ED !important;
    color: #F7FAFC !important;
}

.dark .prompt-section {
    background: rgba(45, 55, 72, 0.9) !important;
    color: #F7FAFC !important;
    border-left: 4px solid #63B3ED !important;
}

/* ensure all have text字 content indark模式下all清晰can见 */
.dark textarea,
.dark input {
    color: #F7FAFC !important;
    background: #2D3748 !important;
}

.dark .gr-markdown {
    color: #F7FAFC !important;
}

/* 特别针 to prompt text字 optimize */
.dark .tips-box {
    background: #2D3748 !important;
    color: #F7FAFC !important;
}

.dark .tips-box h4 {
    color: #63B3ED !important;
}

.dark .tips-box li {
    color: #F7FAFC !important;
}

/* button indark模式下的optimize */
.dark .copy-btn {
    color: #FFFFFF !important;
}

/* ensureAgentapplicationdescriptionindark模式下清晰 */
.dark .gr-accordion {
    color: #F7FAFC !important;
    background: #2D3748 !important;
}

/* fix 具bodytext字 to 比degree issue */
.dark #input_idea_title {
    color: #FFFFFF !important;
}

.dark #input_idea_title h2 {
    color: #FFFFFF !important;
}

.dark #download_success_info {
    background: #2D3748 !important;
    color: #F7FAFC !important;
    border: 1px solid #4FD1C7 !important;
}

.dark #download_success_info strong {
    color: #68D391 !important;
}

.dark #download_success_info span {
    color: #F7FAFC !important;
}

.dark #usage_tips {
    background: #2D3748 !important;
    color: #F7FAFC !important;
    border: 1px solid #63B3ED !important;
}

.dark #usage_tips strong {
    color: #63B3ED !important;
}

/* Loading spinner */
.loading-spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007bff;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Copy buttons styling */
.copy-buttons {
    display: flex;
    gap: 10px;
    margin: 1rem 0;
}

.copy-btn {
    background: linear-gradient(45deg, #28a745, #20c997) !important;
    border: none !important;
    color: white !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
}

.copy-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3) !important;
}

/* dividesegment edit device样式 */
.plan-editor-container {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border: 2px solid #cbd5e0;
    border-radius: 1rem;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.editor-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
}

.editor-header h3 {
    color: #2b6cb0;
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
}

.editor-header p {
    color: #4a5568;
    margin: 0;
    font-size: 1rem;
}

.sections-container {
    display: grid;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.editable-section {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.editable-section:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    transform: translateY(-2px);
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #f1f5f9;
}

.section-type {
    font-size: 1.2rem;
    margin-right: 0.5rem;
}

.section-title {
    font-weight: 600;
    color: #2d3748;
    flex: 1;
}

.edit-section-btn {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    border: none !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    border-radius: 0.5rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2) !important;
}

.edit-section-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    background: linear-gradient(45deg, #5a67d8, #667eea) !important;
}

.section-preview {
    position: relative;
}

.preview-content {
    color: #4a5568;
    line-height: 1.6;
    font-size: 0.95rem;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 0.5rem;
    border-left: 4px solid #3b82f6;
}

.editor-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    padding-top: 1.5rem;
    border-top: 2px solid #e2e8f0;
}

.apply-changes-btn {
    background: linear-gradient(45deg, #48bb78, #38a169) !important;
    border: none !important;
    color: white !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 0.75rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3) !important;
}

.apply-changes-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4) !important;
    background: linear-gradient(45deg, #38a169, #2f855a) !important;
}

.reset-changes-btn {
    background: linear-gradient(45deg, #f093fb, #f5576c) !important;
    border: none !important;
    color: white !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 0.75rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3) !important;
}

.reset-changes-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(240, 147, 251, 0.4) !important;
    background: linear-gradient(45deg, #f5576c, #e53e3e) !important;
}

/* edit 历history样式 */
.edit-history {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.5rem;
    margin: 1rem 0;
}

.edit-history h3 {
    color: #2b6cb0;
    margin-bottom: 1rem;
    font-size: 1.25rem;
}

.history-list {
    max-height: 300px;
    overflow-y: auto;
}

.history-item {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
}

.history-item:hover {
    border-color: #3b82f6;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.history-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.history-index {
    background: #3b82f6;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-weight: 600;
    font-size: 0.8rem;
}

.history-time {
    color: #6b7280;
    font-family: 'Monaco', monospace;
}

.history-section {
    color: #4a5568;
    font-weight: 500;
}

.history-comment {
    color: #374151;
    font-style: italic;
    padding-left: 1rem;
    border-left: 2px solid #e5e7eb;
}

/* Dark模式适配 */
.dark .plan-editor-container {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    border-color: #4a5568;
}

.dark .editor-header h3 {
    color: #63b3ed;
}

.dark .editor-header p {
    color: #e2e8f0;
}

.dark .editable-section {
    background: #374151;
    border-color: #4a5568;
}

.dark .editable-section:hover {
    border-color: #60a5fa;
}

.dark .section-title {
    color: #f7fafc;
}

.dark .preview-content {
    color: #e2e8f0;
    background: #2d3748;
    border-left-color: #60a5fa;
}

.dark .edit-history {
    background: #2d3748;
    border-color: #4a5568;
}

.dark .edit-history h3 {
    color: #63b3ed;
}

.dark .history-item {
    background: #374151;
    border-color: #4a5568;
}

.dark .history-item:hover {
    border-color: #60a5fa;
}

.dark .history-time {
    color: #9ca3af;
}

.dark .history-section {
    color: #e2e8f0;
}

.dark .history-comment {
    color: #d1d5db;
    border-left-color: #4a5568;
}

/* response should 式 design */
@media (max-width: 768px) {
    .plan-editor-container {
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .section-header {
        flex-direction: column;
        gap: 0.5rem;
        align-items: flex-start;
    }
    
    .edit-section-btn {
        align-self: flex-end;
    }
    
    .editor-actions {
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .apply-changes-btn,
    .reset-changes-btn {
        width: 100%;
    }
}
"""

# 保持美transformGradio界面
with gr.Blocks(
    title="VibeDoc Agent: Your PersonalAIProduct Managerandarchitect",
    theme=gr.themes.Soft(primary_hue="blue"),
    css=custom_css
) as demo:
    
    gr.HTML("""
    <div class="header-gradient">
        <h1>🚀 VibeDoc - AI-Powered Development Plan Generator</h1>
        <p style="font-size: 18px; margin: 15px 0; opacity: 0.95;">
            🤖 Transform your ideas into comprehensive development plans in 60-180 seconds
        </p>
        <p style="opacity: 0.85;">
            ✨ AI-Driven Planning | � Visual Diagrams | 🎯 Professional Output | � Multi-format Export
        </p>
        <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 0.5rem;">
            <small style="opacity: 0.9;">
                🌟 Open Source Project | 💡 Built with Qwen2.5-72B-Instruct | ⚡ Fast & Reliable
            </small>
        </div>
    </div>
    
    <!-- addMermaid.jssupport -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        // enhancedMermaidconfiguration
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            },
            gantt: {
                useMaxWidth: true,
                gridLineStartPadding: 350,
                fontSize: 13,
                fontFamily: '"Inter", "Source Sans Pro", sans-serif',
                sectionFontSize: 24,
                numberSectionStyles: 4
            },
            themeVariables: {
                primaryColor: '#3b82f6',
                primaryTextColor: '#1f2937',
                primaryBorderColor: '#1d4ed8',
                lineColor: '#6b7280',
                secondaryColor: '#dbeafe',
                tertiaryColor: '#f8fafc',
                background: '#ffffff',
                mainBkg: '#ffffff',
                secondBkg: '#f1f5f9',
                tertiaryBkg: '#eff6ff'
            }
        });
        
        // listen 主题changetransform，动态 updateMermaid主题
        function updateMermaidTheme() {
            const isDark = document.documentElement.classList.contains('dark');
            const theme = isDark ? 'dark' : 'default';
            mermaid.initialize({ 
                startOnLoad: true,
                theme: theme,
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: 'basis'
                },
                gantt: {
                    useMaxWidth: true,
                    gridLineStartPadding: 350,
                    fontSize: 13,
                    fontFamily: '"Inter", "Source Sans Pro", sans-serif',
                    sectionFontSize: 24,
                    numberSectionStyles: 4
                },
                themeVariables: isDark ? {
                    primaryColor: '#60a5fa',
                    primaryTextColor: '#f8fafc',
                    primaryBorderColor: '#3b82f6',
                    lineColor: '#94a3b8',
                    secondaryColor: '#1e293b',
                    tertiaryColor: '#0f172a',
                    background: '#1f2937',
                    mainBkg: '#1f2937',
                    secondBkg: '#374151',
                    tertiaryBkg: '#1e293b'
                } : {
                    primaryColor: '#3b82f6',
                    primaryTextColor: '#1f2937',
                    primaryBorderColor: '#1d4ed8',
                    lineColor: '#6b7280',
                    secondaryColor: '#dbeafe',
                    tertiaryColor: '#f8fafc',
                    background: '#ffffff',
                    mainBkg: '#ffffff',
                    secondBkg: '#f1f5f9',
                    tertiaryBkg: '#eff6ff'
                }
            });
            
            // 重新渲染 all haveMermaiddiagram table
            renderMermaidCharts();
        }
        
        // 强transformMermaiddiagram table渲染函数
        function renderMermaidCharts() {
            try {
                // 清除现 have 渲染 content
                document.querySelectorAll('.mermaid').forEach(element => {
                    if (element.getAttribute('data-processed') !== 'true') {
                        element.removeAttribute('data-processed');
                    }
                });
                
                // process package装device inMermaidcontent
                document.querySelectorAll('.mermaid-render').forEach(element => {
                    const content = element.textContent.trim();
                    if (content && !element.classList.contains('rendered')) {
                        element.innerHTML = content;
                        element.classList.add('mermaid', 'rendered');
                    }
                });
                
                // 重新initial始transformMermaid
                mermaid.init(undefined, document.querySelectorAll('.mermaid:not([data-processed="true"])'));
                
            } catch (error) {
                console.warn('Mermaid渲染警notify:', error);
                // such as result渲染 failure ， display error information
                document.querySelectorAll('.mermaid-render').forEach(element => {
                    if (!element.classList.contains('rendered')) {
                        element.innerHTML = '<div class="mermaid-error">diagram table渲染 in ，please稍候...</div>';
                    }
                });
            }
        }
        
        // page load complete after initial始transform
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(renderMermaidCharts, 1000);
        });
        
        // listen content changetransform，自动重新渲染 diagram table
        function observeContentChanges() {
            const observer = new MutationObserver(function(mutations) {
                let shouldRender = false;
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        mutation.addedNodes.forEach(function(node) {
                            if (node.nodeType === Node.ELEMENT_NODE) {
                                if (node.classList && (node.classList.contains('mermaid') || node.querySelector('.mermaid'))) {
                                    shouldRender = true;
                                }
                            }
                        });
                    }
                });
                
                if (shouldRender) {
                    setTimeout(renderMermaidCharts, 500);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        
        // start content 观察device
        observeContentChanges();
        
        // 单独复make prompt function
        function copyIndividualPrompt(promptId, promptContent) {
            // solve码HTML实body
            const decodedContent = promptContent.replace(/\\n/g, '\n').replace(/\\'/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
            
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(decodedContent).then(() => {
                    showCopySuccess(promptId);
                }).catch(err => {
                    console.error('复make failure:', err);
                    fallbackCopy(decodedContent);
                });
            } else {
                fallbackCopy(decodedContent);
            }
        }
        
        // edit prompt function
        function editIndividualPrompt(promptId, promptContent) {
            // solve码HTML实body
            const decodedContent = promptContent.replace(/\\n/g, '\n').replace(/\\'/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
            
            // detect当 before 主题
            const isDark = document.documentElement.classList.contains('dark');
            
            // create edit to 话框
            const editDialog = document.createElement('div');
            editDialog.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 10000;
            `;
            
            editDialog.innerHTML = `
                <div style="
                    background: ${isDark ? '#2d3748' : 'white'};
                    color: ${isDark ? '#f7fafc' : '#2d3748'};
                    padding: 2rem;
                    border-radius: 1rem;
                    max-width: 80%;
                    max-height: 80%;
                    overflow-y: auto;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                ">
                    <h3 style="margin-bottom: 1rem; color: ${isDark ? '#f7fafc' : '#2d3748'};">✏️ edit prompt</h3>
                    <textarea
                        id="prompt-editor-${promptId}"
                        style="
                            width: 100%;
                            height: 300px;
                            padding: 1rem;
                            border: 2px solid ${isDark ? '#4a5568' : '#e2e8f0'};
                            border-radius: 0.5rem;
                            font-family: 'Fira Code', monospace;
                            font-size: 0.9rem;
                            resize: vertical;
                            line-height: 1.5;
                            background: ${isDark ? '#1a202c' : 'white'};
                            color: ${isDark ? '#f7fafc' : '#2d3748'};
                        "
                        placeholder="in 此 edit 您 prompt..."
                    >${decodedContent}</textarea>
                    <div style="margin-top: 1rem; display: flex; gap: 1rem; justify-content: flex-end;">
                        <button
                            id="cancel-edit-${promptId}"
                            style="
                                padding: 0.5rem 1rem;
                                border: 1px solid ${isDark ? '#4a5568' : '#cbd5e0'};
                                background: ${isDark ? '#2d3748' : 'white'};
                                color: ${isDark ? '#f7fafc' : '#4a5568'};
                                border-radius: 0.5rem;
                                cursor: pointer;
                                transition: all 0.2s ease;
                            "
                        >cancel</button>
                        <button
                            id="save-edit-${promptId}"
                            style="
                                padding: 0.5rem 1rem;
                                background: linear-gradient(45deg, #667eea, #764ba2);
                                color: white;
                                border: none;
                                border-radius: 0.5rem;
                                cursor: pointer;
                                transition: all 0.2s ease;
                            "
                        >save 并复make</button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(editDialog);
            
            // 绑定 button event
            document.getElementById(`cancel-edit-${promptId}`).addEventListener('click', () => {
                document.body.removeChild(editDialog);
            });
            
            document.getElementById(`save-edit-${promptId}`).addEventListener('click', () => {
                const editedContent = document.getElementById(`prompt-editor-${promptId}`).value;
                
                // 复make edit after content
                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(editedContent).then(() => {
                        showCopySuccess(promptId);
                        document.body.removeChild(editDialog);
                    }).catch(err => {
                        console.error('复make failure:', err);
                        fallbackCopy(editedContent);
                        document.body.removeChild(editDialog);
                    });
                } else {
                    fallbackCopy(editedContent);
                    document.body.removeChild(editDialog);
                }
            });
            
            // ESCkey 关闭
            const escapeHandler = (e) => {
                if (e.key === 'Escape') {
                    document.body.removeChild(editDialog);
                    document.removeEventListener('keydown', escapeHandler);
                }
            };
            document.addEventListener('keydown', escapeHandler);
            
            // click 外部关闭
            editDialog.addEventListener('click', (e) => {
                if (e.target === editDialog) {
                    document.body.removeChild(editDialog);
                    document.removeEventListener('keydown', escapeHandler);
                }
            });
        }
        
        // 降级复make plan
        function fallbackCopy(text) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                alert('✅ prompt 已复make to 剪贴板！');
            } catch (err) {
                alert('❌ Copy failed, please manually select text to copy');
            }
            document.body.removeChild(textArea);
        }
        
        // display 复make success prompt
        function showCopySuccess(promptId) {
            const successMsg = document.getElementById('copy-success-' + promptId);
            if (successMsg) {
                successMsg.style.display = 'inline';
                setTimeout(() => {
                    successMsg.style.display = 'none';
                }, 2000);
            }
        }
        
        // 绑定复make and edit button event
        function bindCopyButtons() {
            document.querySelectorAll('.individual-copy-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const promptId = this.getAttribute('data-prompt-id');
                    const promptContent = this.getAttribute('data-prompt-content');
                    copyIndividualPrompt(promptId, promptContent);
                });
            });
            
            document.querySelectorAll('.edit-prompt-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const promptId = this.getAttribute('data-prompt-id');
                    const promptContent = this.getAttribute('data-prompt-content');
                    editIndividualPrompt(promptId, promptContent);
                });
            });
        }
        
        // page load complete after initial始transform
        document.addEventListener('DOMContentLoaded', function() {
            updateMermaidTheme();
            bindCopyButtons();
            
            // listen 主题切换
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                        updateMermaidTheme();
                        // 重新渲染 all haveMermaiddiagram table
                        setTimeout(() => {
                            document.querySelectorAll('.mermaid').forEach(element => {
                                mermaid.init(undefined, element);
                            });
                        }, 100);
                    }
                });
            });
            observer.observe(document.documentElement, { attributes: true });
            
            // listen content changetransform，重新绑定复make button
            const contentObserver = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        bindCopyButtons();
                    }
                });
            });
            
            // listenplan_result区域的changetransform
            const planResult = document.getElementById('plan_result');
            if (planResult) {
                contentObserver.observe(planResult, { childList: true, subtree: true });
            }
        });
    </script>
    """)
    
    with gr.Row():
        with gr.Column(scale=2, elem_classes="content-card"):
            gr.Markdown("## 💡 input 您产品创意", elem_id="input_idea_title")
            
            idea_input = gr.Textbox(
                label="产品创意 description",
                placeholder="For example: I want to make a tool to help programmers manage code snippets, support multi-language syntax highlighting, can be classified by tags, and can be shared with team members...",
                lines=5,
                max_lines=10,
                show_label=False
            )
            
            # optimize button and 结result display
            with gr.Row():
                optimize_btn = gr.Button(
                    "✨ optimize 创意 description",
                    variant="secondary",
                    size="sm",
                    elem_classes="optimize-btn"
                )
                reset_btn = gr.Button(
                    "🔄 重置",
                    variant="secondary", 
                    size="sm",
                    elem_classes="reset-btn"
                )
            
            optimization_result = gr.Markdown(
                visible=False,
                elem_classes="optimization-result"
            )
            
            reference_url_input = gr.Textbox(
                label="reference link (canselect)",
                placeholder="Enter any web link (such as blog, news, documentation) as reference...",
                lines=1,
                show_label=True
            )
            
            generate_btn = gr.Button(
                "🤖 AIgenerate Development Plan + programming prompts",
                variant="primary",
                size="lg",
                elem_classes="generate-btn"
            )
        
        with gr.Column(scale=1):
            gr.HTML("""
            <div class="tips-box">
                <h4 style="color: #e53e3e;">💡 simple 三步</h4>
                <div style="font-size: 16px; font-weight: 600; text-align: center; margin: 20px 0;">
                    <span style="color: #e53e3e;">创意 description</span> → 
                    <span style="color: #38a169;">intelligent analyze</span> → 
                    <span style="color: #3182ce;">complete plan</span>
                </div>
                <h4 style="color: #38a169;">🎯 core function</h4>
                <ul>
                    <li><span style="color: #e53e3e;">📋</span> complete Development Plan</li>
                    <li><span style="color: #3182ce;">🤖</span> AIprogramming prompts</li>
                    <li><span style="color: #38a169;">�</span> can viewtransform diagram table</li>
                    <li><span style="color: #d69e2e;">🔗</span> MCPservice enhanced</li>
                </ul>
                <h4 style="color: #3182ce;">⏱️ generation time</h4>
                <ul>
                    <li><span style="color: #e53e3e;">✨</span> 创意 optimize ：20seconds</li>
                    <li><span style="color: #38a169;">📝</span> plan generate ：150-200seconds</li>
                    <li><span style="color: #d69e2e;">⚡</span> One-click copy and download</li>
                </ul>
            </div>
            """)
    
    # 结result display 区域
    with gr.Column(elem_classes="result-container"):
        plan_output = gr.Markdown(
            value="""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 1rem; border: 2px dashed #cbd5e0;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
    <h3 style="color: #2b6cb0; margin-bottom: 1rem; font-weight: bold;">intelligent Development Plan generate</h3>
    <p style="color: #4a5568; font-size: 1.1rem; margin-bottom: 1.5rem;">
        💭 <strong style="color: #e53e3e;">input 创意，获得 complete development plan</strong>
    </p>
    <div style="background: linear-gradient(90deg, #edf2f7 0%, #e6fffa 100%); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 4px solid #38b2ac;">
        <p style="color: #2c7a7b; margin: 0; font-weight: 600;">
            🎯 <span style="color: #e53e3e;">Technical Solution</span> • <span style="color: #38a169;">Development Plan</span> • <span style="color: #3182ce;">programming prompts</span>
        </p>
    </div>
    <p style="color: #a0aec0; font-size: 0.9rem;">
        click <span style="color: #e53e3e; font-weight: bold;">"🤖 AIgenerate Development Plan"</span> press钮start
    </p>
</div>
            """,
            elem_id="plan_result",
            label="AIgenerated development plan"
        )
        
        # process procedure description 区域
        process_explanation = gr.Markdown(
            visible=False,
            elem_classes="process-explanation"
        )
        
        # 切换 button
        with gr.Row():
            show_explanation_btn = gr.Button(
                "🔍 check看AIgenerate过程详情",
                variant="secondary",
                size="sm",
                elem_classes="explanation-btn",
                visible=False
            )
            hide_explanation_btn = gr.Button(
                "📝 返回 Development Plan",
                variant="secondary",
                size="sm",
                elem_classes="explanation-btn",
                visible=False
            )
        
        # 隐藏 component use于复make and download
        prompts_for_copy = gr.Textbox(visible=False)
        download_file = gr.File(
            label="📁 download Development Plan documentation", 
            visible=False,
            interactive=False,
            show_label=True
        )
        
        # add 复make and download button
        with gr.Row():
            copy_plan_btn = gr.Button(
                "📋 复make Development Plan",
                variant="secondary",
                size="sm",
                elem_classes="copy-btn"
            )
            copy_prompts_btn = gr.Button(
                "🤖 复make programming prompts",
                variant="secondary", 
                size="sm",
                elem_classes="copy-btn"
            )
            
        # download prompt information
        download_info = gr.HTML(
            value="",
            visible=False,
            elem_id="download_info"
        )
            
        # use prompt
        gr.HTML("""
        <div style="padding: 10px; background: #e3f2fd; border-radius: 8px; text-align: center; color: #1565c0;" id="usage_tips">
            💡 click 上method button 复make content ， or download save for file
        </div>
        """)
        
    # example 区域 - expand示多样transform的application场scene
    gr.Markdown("## 🎯 Example Use Cases", elem_id="quick_start_container")
    gr.Examples(
        examples=[
            [
                "AI-powered customer service system: Multi-turn dialogue, sentiment analysis, knowledge base search, automatic ticket generation, and intelligent responses",
                "https://docs.python.org/3/library/asyncio.html"
            ],
            [
                "Modern web application with React and TypeScript: User authentication, real-time data sync, responsive design, PWA support, and offline capabilities",
                "https://react.dev/learn"
            ],
            [
                "Task management platform: Team collaboration, project tracking, deadline reminders, file sharing, and progress visualization",
                ""
            ],
            [
                "E-commerce marketplace: Product catalog, shopping cart, payment integration, order management, and customer reviews",
                "https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps"
            ],
            [
                "Social media analytics dashboard: Data visualization, sentiment analysis, trend tracking, engagement metrics, and automated reporting",
                ""
            ],
            [
                "Educational learning management system: Course creation, student enrollment, progress tracking, assessments, and certificates",
                "https://www.w3.org/WAI/WCAG21/quickref/"
            ]
        ],
        inputs=[idea_input, reference_url_input],
        label="🎯 Popular Examples - Try These Ideas",
        examples_per_page=6,
        elem_id="enhanced_examples"
    )
    
    # Usage Instructions - 功能介绍
    gr.HTML("""
    <div class="prompts-section" id="ai_helper_instructions">
        <h3>🚀 How It Works - Intelligent Development Planning</h3>
        
        <!-- core function -->
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%); border-radius: 15px; border: 3px solid #28a745; margin: 15px 0;">
            <span style="font-size: 36px;">🧠</span><br>
            <strong style="font-size: 18px; color: #155724;">AI-Powered Analysis</strong><br>
            <small style="color: #155724; font-weight: 600; font-size: 13px;">
                � Intelligent planning • ⚡ Fast generation • ✅ Professional output
            </small>
        </div>
        
        <!-- can viewtransform support -->
        <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%); border-radius: 12px; border: 2px solid #2196f3; margin: 15px 0;">
            <span style="font-size: 30px;">�</span><br>
            <strong style="font-size: 16px; color: #1976d2;">Visual Diagrams</strong><br>
            <small style="color: #1976d2; font-weight: 600; font-size: 12px;">
                🎨 Architecture • � Flowcharts • 📅 Gantt charts
            </small>
        </div>
        
        <!-- process process description -->
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #fffaf0 100%); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #ff9800;">
            <strong style="color: #f57c00;">⚡ Processing Pipeline:</strong>
            <ol style="margin: 10px 0; padding-left: 20px; font-size: 14px;">
                <li><strong>Input Analysis</strong> → Understanding your requirements</li>
                <li><strong>Prompt Optimization</strong> → Enhancing description quality</li>
                <li><strong>Knowledge Retrieval</strong> → Fetching relevant information</li>
                <li><strong>AI Generation</strong> → Creating comprehensive plan</li>
                <li><strong>Quality Validation</strong> → Ensuring professional output</li>
            </ol>
        </div>
        
        <!-- 核心excellenttrend -->
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #6c757d;">
            <strong style="color: #495057;">🎯 Key Advantages:</strong>
            <ul style="margin: 10px 0; padding-left: 20px; font-size: 14px;">
                <li><strong>Speed</strong> → 60-180 seconds generation time</li>
                <li><strong>Quality</strong> → Professional industry-standard output</li>
                <li><strong>Flexibility</strong> → Multiple export formats</li>
                <li><strong>Integration</strong> → Works with all AI coding assistants</li>
            </ul>
        </div>
        
        <h4>🤖 Perfect for AI Coding Assistants</h4>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin: 12px 0;">
            <div style="text-align: center; padding: 8px; background: #e3f2fd; border-radius: 6px; border: 1px solid #2196f3; box-shadow: 0 2px 4px rgba(33,150,243,0.2);">
                <span style="font-size: 16px;">🔵</span> <strong style="font-size: 12px;">Claude</strong>
            </div>
            <div style="text-align: center; padding: 8px; background: #e8f5e8; border-radius: 6px; border: 1px solid #4caf50; box-shadow: 0 2px 4px rgba(76,175,80,0.2);">
                <span style="font-size: 16px;">🟢</span> <strong style="font-size: 12px;">GitHub Copilot</strong>
            </div>
            <div style="text-align: center; padding: 8px; background: #fff3e0; border-radius: 6px; border: 1px solid #ff9800; box-shadow: 0 2px 4px rgba(255,152,0,0.2);">
                <span style="font-size: 16px;">🟡</span> <strong style="font-size: 12px;">ChatGPT</strong>
            </div>
            <div style="text-align: center; padding: 8px; background: #fce4ec; border-radius: 6px; border: 1px solid #e91e63; box-shadow: 0 2px 4px rgba(233,30,99,0.2);">
                <span style="font-size: 16px;">🔴</span> <strong style="font-size: 12px;">Cursor</strong>
            </div>
        </div>
        <p style="text-align: center; color: #28a745; font-weight: 700; font-size: 15px; background: #d4edda; padding: 8px; border-radius: 8px; border: 1px solid #c3e6cb;">
            <em>🎉 Professional Development Plans + Ready-to-Use AI Prompts</em>
        </p>
    </div>
    """)
    
    # 绑定 event
    def show_download_info():
        return gr.update(
            value="""
            <div style="padding: 10px; background: #e8f5e8; border-radius: 8px; text-align: center; margin: 10px 0; color: #2d5a2d;" id="download_success_info">
                ✅ <strong style="color: #1a5a1a;">documentation 已 generate ！</strong> 您现incanwith：
                <br>• 📋 <span style="color: #2d5a2d;">复make Development Plan or programming prompts</span>
                <br>• 📁 <span style="color: #2d5a2d;">click 下method download button save documentation</span>
                <br>• 🔄 <span style="color: #2d5a2d;">调complete创意重新 generate</span>
            </div>
            """,
            visible=True
        )
    
    # optimize button event
    optimize_btn.click(
        fn=optimize_user_idea,
        inputs=[idea_input],
        outputs=[idea_input, optimization_result]
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=[optimization_result]
    )
    
    # 重置 button event
    reset_btn.click(
        fn=lambda: ("", gr.update(visible=False)),
        outputs=[idea_input, optimization_result]
    )
    
    # process procedure description button event
    show_explanation_btn.click(
        fn=show_explanation,
        outputs=[plan_output, process_explanation, hide_explanation_btn]
    )
    
    hide_explanation_btn.click(
        fn=hide_explanation,
        outputs=[plan_output, process_explanation, hide_explanation_btn]
    )
    
    generate_btn.click(
        fn=generate_development_plan,
        inputs=[idea_input, reference_url_input],
        outputs=[plan_output, prompts_for_copy, download_file],
        api_name="generate_plan"
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=[download_file]
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=[show_explanation_btn]
    ).then(
        fn=show_download_info,
        outputs=[download_info]
    )
    
    # 复make button event （ useJavaScriptimplementation）
    copy_plan_btn.click(
        fn=None,
        inputs=[plan_output],
        outputs=[],
        js="""(plan_content) => {
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(plan_content).then(() => {
                    alert('✅ Development Plan 已复make to 剪贴板！');
                }).catch(err => {
                    console.error('复make failure:', err);
                    alert('❌ Copy failed, please manually select text to copy');
                });
            } else {
                // 降级 plan
                const textArea = document.createElement('textarea');
                textArea.value = plan_content;
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    alert('✅ Development Plan 已复make to 剪贴板！');
                } catch (err) {
                    alert('❌ Copy failed, please manually select text to copy');
                }
                document.body.removeChild(textArea);
            }
        }"""
    )
    
    copy_prompts_btn.click(
        fn=None,
        inputs=[prompts_for_copy],
        outputs=[],
        js="""(prompts_content) => {
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(prompts_content).then(() => {
                    alert('✅ programming prompts 已复make to 剪贴板！');
                }).catch(err => {
                    console.error('复make failure:', err);
                    alert('❌ Copy failed, please manually select text to copy');
                });
            } else {
                // 降级 plan
                const textArea = document.createElement('textarea');
                textArea.value = prompts_content;
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    alert('✅ programming prompts 已复make to 剪贴板！');
                } catch (err) {
                    alert('❌ Copy failed, please manually select text to copy');
                }
                document.body.removeChild(textArea);
            }
        }"""
    )

# start application - open源版本
if __name__ == "__main__":
    logger.info("🚀 Starting VibeDoc Application")
    logger.info(f"🌍 Environment: {config.environment}")
    logger.info(f"� Version: 2.0.0 - Open Source Edition")
    logger.info(f"�🔧 External Services: {[s.name for s in config.get_enabled_mcp_services()]}")
    
    # try 多个端口 with avoid冲突
    ports_to_try = [7860, 7861, 7862, 7863, 7864]
    launched = False
    
    for port in ports_to_try:
        try:
            logger.info(f"🌐 Attempting to launch on port: {port}")
            demo.launch(
                server_name="0.0.0.0",
                server_port=port,
                share=False,  # open源 version 默认 not divide享
                show_error=config.debug,
                prevent_thread_lock=False
            )
            launched = True
            logger.info(f"✅ Application successfully launched on port {port}")
            logger.info(f"🔗 Local URL: http://localhost:{port}")
            logger.info(f"🔗 Network URL: http://0.0.0.0:{port}")
            break
        except Exception as e:
            logger.warning(f"⚠️ Port {port} failed: {str(e)}")
            continue
    
    if not launched:
        logger.error("❌ Failed to launch on all ports. Please check network configuration.")
    