#!/usr/bin/env python3
"""
enhanced versionMCP直接客户端 - supportModelScope平台asynchronousMCPservice
processHTTP 202asynchronous响应，通过SSEget结果
"""

import requests
import json
import time
import threading
import queue
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

@dataclass
class AsyncMCPResult:
    """asynchronousMCPcall结果"""
    success: bool
    data: str
    service_name: str
    execution_time: float
    session_id: Optional[str] = None
    error_message: Optional[str] = None

class AsyncMCPClient:
    """asynchronousMCP客户端 - 专为ModelScope平台optimize"""
    
    def __init__(self):
        self.timeout = 60
        self.result_timeout = 30  # waiting asynchronous 结果超 when when time
        
        # ModelScopeMCPservice configuration
        self.mcp_services = {
            "fetch": {
                "url": "https://mcp.api-inference.modelscope.net/6ec508e067dc41/sse",
                "name": "Fetch MCP",
                "enabled": True,
                "tools": {
                    "fetch": {
                        "url": "string",
                        "max_length": "integer", 
                        "start_index": "integer",
                        "raw": "boolean"
                    }
                }
            },
            "deepwiki": {
                "url": "https://mcp.api-inference.modelscope.net/d4ed08072d2846/sse",
                "name": "DeepWiki MCP", 
                "enabled": True,
                "tools": {
                    "deepwiki_fetch": {
                        "url": "string",
                        "mode": "string",
                        "maxDepth": "integer"
                    }
                }
            }
        }
    
    def _get_sse_endpoint(self, service_url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """getSSE endpoint和session_id"""
        try:
            headers = {
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache"
            }
            
            logger.info(f"🔗 连接SSE: {service_url}")
            response = requests.get(service_url, headers=headers, timeout=15, stream=True)
            
            if response.status_code != 200:
                logger.error(f"❌ SSE连接 failure: HTTP {response.status_code}")
                return False, None, None
            
            # parseSSEevent
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    data = line[6:]  # 去掉 'data: ' 前缀
                    if '/messages/' in data and 'session_id=' in data:
                        session_id = data.split('session_id=')[1]
                        logger.info(f"✅ getsession_id: {session_id}")
                        response.close()
                        return True, data, session_id
                elif line == "":
                    break
            
            response.close()
            logger.error("❌ 未 get to have 效endpoint")
            return False, None, None
            
        except Exception as e:
            logger.error(f"💥 SSE连接 exception: {str(e)}")
            return False, None, None
    
    def _listen_for_result(self, service_url: str, session_id: str, result_queue: queue.Queue):
        """listenSSE流getasynchronous结果"""
        try:
            headers = {
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache"
            }
            
            logger.info(f"👂 start listen 结果...")
            response = requests.get(service_url, headers=headers, timeout=self.result_timeout, stream=True)
            
            if response.status_code != 200:
                result_queue.put(("error", f"listen 连接 failure: HTTP {response.status_code}"))
                return
            
            # listenSSEevent
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    data_str = line[6:]
                    try:
                        # try parseJSON数据
                        data = json.loads(data_str)
                        if isinstance(data, dict):
                            # check is 否 isMCP响应
                            if "result" in data or "error" in data:
                                logger.info("✅ 收 toMCP响应")
                                result_queue.put(("success", data))
                                break
                            elif "id" in data:  # can can isMCP响应
                                result_queue.put(("success", data))
                                break
                    except json.JSONDecodeError:
                        # 非JSON数据，can can is纯文本结果
                        if len(data_str.strip()) > 10:
                            logger.info("✅ 收 to 文 this response should")
                            result_queue.put(("success", {"result": {"text": data_str}}))
                            break
                elif line.startswith('event: '):
                    event_type = line[7:]
                    logger.debug(f"📨 SSEevent: {event_type}")
            
            response.close()
            
        except requests.exceptions.Timeout:
            logger.warning("⏰ 结果 listen 超 when")
            result_queue.put(("timeout", "waiting 结果超 when"))
        except Exception as e:
            logger.error(f"💥 listen exception: {str(e)}")
            result_queue.put(("error", f"listen exception: {str(e)}"))
    
    def call_mcp_service_async(
        self,
        service_key: str,
        tool_name: str,
        tool_args: Dict[str, Any]
    ) -> AsyncMCPResult:
        """async callMCPservice"""
        
        if service_key not in self.mcp_services:
            return AsyncMCPResult(
                success=False,
                data="",
                service_name=service_key,
                execution_time=0.0,
                error_message=f"未知 service: {service_key}"
            )
        
        service_config = self.mcp_services[service_key]
        service_url = service_config["url"]
        service_name = service_config["name"]
        
        start_time = time.time()
        
        logger.info(f"🚀 start call {service_name}")
        logger.info(f"📊 tool: {tool_name}")
        logger.info(f"📋 parameter: {json.dumps(tool_args, ensure_ascii=False)}")
        
        # Step1: getSSE endpoint
        success, endpoint_path, session_id = self._get_sse_endpoint(service_url)
        if not success:
            return AsyncMCPResult(
                success=False,
                data="",
                service_name=service_name,
                execution_time=time.time() - start_time,
                error_message="getendpoint失败"
            )
        
        # Step2: 启动结果listen器
        result_queue = queue.Queue()
        listener_thread = threading.Thread(
            target=self._listen_for_result,
            args=(service_url, session_id, result_queue)
        )
        listener_thread.daemon = True
        listener_thread.start()
        
        # waiting 一小段 when time ensure listener 就绪
        time.sleep(0.5)
        
        # Step3: 发送MCP请 requirement
        try:
            base_url = service_url.replace('/sse', '')
            full_endpoint = urljoin(base_url, endpoint_path)
            
            mcp_request = {
                "jsonrpc": "2.0",
                "id": int(time.time() * 1000),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": tool_args
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            logger.info(f"📤 发送请 requirement to: {full_endpoint}")
            response = requests.post(full_endpoint, json=mcp_request, headers=headers, timeout=10)
            
            logger.info(f"📊 请 requirement response should: HTTP {response.status_code}")
            
            if response.status_code == 202:  # Accepted - asynchronous process
                logger.info("✅ 请 requirement 已接受， waiting asynchronous 结果...")
                
                # Step4: 等待asynchronous结果
                try:
                    result_type, result_data = result_queue.get(timeout=self.result_timeout)
                    
                    execution_time = time.time() - start_time
                    
                    if result_type == "success":
                        # parse 结果 data
                        content = self._extract_content_from_response(result_data)
                        if content and len(content.strip()) > 10:
                            logger.info(f"✅ {service_name} async call success!")
                            return AsyncMCPResult(
                                success=True,
                                data=content,
                                service_name=service_name,
                                execution_time=execution_time,
                                session_id=session_id
                            )
                        else:
                            return AsyncMCPResult(
                                success=False,
                                data="",
                                service_name=service_name,
                                execution_time=execution_time,
                                session_id=session_id,
                                error_message="response should content for 空"
                            )
                    else:
                        return AsyncMCPResult(
                            success=False,
                            data="",
                            service_name=service_name,
                            execution_time=execution_time,
                            session_id=session_id,
                            error_message=str(result_data)
                        )
                        
                except queue.Empty:
                    return AsyncMCPResult(
                        success=False,
                        data="",
                        service_name=service_name,
                        execution_time=time.time() - start_time,
                        session_id=session_id,
                        error_message="waiting asynchronous 结果超 when"
                    )
            
            elif response.status_code == 200:
                # synchronous response should
                try:
                    data = response.json()
                    content = self._extract_content_from_response(data)
                    execution_time = time.time() - start_time
                    
                    return AsyncMCPResult(
                        success=bool(content and len(content.strip()) > 10),
                        data=content or "",
                        service_name=service_name,
                        execution_time=execution_time,
                        session_id=session_id,
                        error_message=None if content else "response should content for 空"
                    )
                except json.JSONDecodeError:
                    content = response.text
                    return AsyncMCPResult(
                        success=len(content.strip()) > 10,
                        data=content,
                        service_name=service_name,
                        execution_time=time.time() - start_time,
                        session_id=session_id
                    )
            else:
                return AsyncMCPResult(
                    success=False,
                    data="",
                    service_name=service_name,
                    execution_time=time.time() - start_time,
                    session_id=session_id,
                    error_message=f"HTTP {response.status_code}: {response.text[:200]}"
                )
                
        except Exception as e:
            return AsyncMCPResult(
                success=False,
                data="",
                service_name=service_name,
                execution_time=time.time() - start_time,
                session_id=session_id,
                error_message=f"请 requirement exception: {str(e)}"
            )
    
    def _extract_content_from_response(self, response_data: Any) -> Optional[str]:
        """从 response should in 提取 content"""
        try:
            if isinstance(response_data, str):
                return response_data
            
            if isinstance(response_data, dict):
                # check 标准MCP响应format
                if "result" in response_data:
                    result = response_data["result"]
                    
                    # checkcontent数组
                    if "content" in result and isinstance(result["content"], list):
                        contents = []
                        for item in result["content"]:
                            if isinstance(item, dict) and "text" in item:
                                contents.append(item["text"])
                            elif isinstance(item, str):
                                contents.append(item)
                        if contents:
                            return "\n".join(contents)
                    
                    # check 其他 field
                    for field in ["text", "data", "message"]:
                        if field in result and result[field]:
                            return str(result[field])
                    
                    # such as 果result本身是字符串
                    if isinstance(result, str):
                        return result
                
                # check error
                if "error" in response_data:
                    error = response_data["error"]
                    if isinstance(error, dict) and "message" in error:
                        return f"error: {error['message']}"
                    else:
                        return f"error: {str(error)}"
                
                # check 直接 field
                for field in ["content", "data", "text", "message", "response"]:
                    if field in response_data and response_data[field]:
                        content = response_data[field]
                        if isinstance(content, list):
                            return "\n".join(str(item) for item in content if item)
                        else:
                            return str(content)
            
            # such as 果都没 have 匹配，返回JSON字符串
            return json.dumps(response_data, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.warning(f"⚠️ content 提取 failure: {e}")
            return str(response_data) if response_data else None

# 全局 example
async_mcp_client = AsyncMCPClient()

# 便捷 function
def call_fetch_mcp_async(url: str, max_length: int = 5000) -> AsyncMCPResult:
    """async callFetch MCPservice"""
    return async_mcp_client.call_mcp_service_async(
        "fetch",
        "fetch",
        {"url": url, "max_length": max_length}
    )

def call_deepwiki_mcp_async(url: str, mode: str = "aggregate") -> AsyncMCPResult:
    """async callDeepWiki MCPservice"""
    return async_mcp_client.call_mcp_service_async(
        "deepwiki",
        "deepwiki_fetch", 
        {"url": url, "mode": mode}
    )

if __name__ == "__main__":
    # test asynchronousMCP客户端
    print("🧪 test asynchronousMCP客户端")
    print("=" * 50)
    
    # testFetch MCP
    print("testFetch MCP...")
    result = call_fetch_mcp_async("https://example.com")
    print(f"success: {result.success}")
    print(f"content 长度: {len(result.data) if result.data else 0}")
    print(f"execute when time: {result.execution_time:.2f}s")
    if result.error_message:
        print(f"error: {result.error_message}")
    
    print("\n" + "-" * 30)
    
    # testDeepWiki MCP
    print("testDeepWiki MCP...")
    result = call_deepwiki_mcp_async("https://deepwiki.org/openai/openai-python")
    print(f"success: {result.success}")
    print(f"content 长度: {len(result.data) if result.data else 0}")
    print(f"execute when time: {result.execution_time:.2f}s")
    if result.error_message:
        print(f"error: {result.error_message}")
    
    print("\n✅ asynchronousMCP客户端test完成")