"""
VibeDoc AgentApplyconfigurationfile
Support multiple environments、多MCPserviceconfiguration
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load环境变量
load_dotenv()

@dataclass
class MCPServiceConfig:
    """MCPserviceconfiguration"""
    name: str
    url: Optional[str]
    api_key: Optional[str] = None
    timeout: int = 30
    enabled: bool = True
    health_check_path: str = "/health"

@dataclass
class AIModelConfig:
    """AI模型configuration"""
    provider: str = "siliconflow"
    model_name: str = "Qwen/Qwen2.5-72B-Instruct"
    api_key: str = ""
    api_url: str = "https://api.siliconflow.cn/v1/chat/completions"
    max_tokens: int = 8000
    temperature: float = 0.7
    timeout: int = 300  # 增加到300s（5min）解决timeoutproblem

class AppConfig:
    """Apply总configuration类"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.port = int(os.getenv("PORT", "7860"))
        
        # AI模型configuration
        self.ai_model = AIModelConfig(
            api_key=os.getenv("SILICONFLOW_API_KEY", ""),
            timeout=int(os.getenv("API_TIMEOUT", "300"))
        )
        
        # 简化MCPserviceconfiguration - Use built-in directlyURL，避免环境变量复杂性
        self.mcp_services = {
            "deepwiki": MCPServiceConfig(
                name="DeepWiki MCP",
                url="https://mcp.api-inference.modelscope.net/d4ed08072d2846/sse",
                timeout=int(os.getenv("MCP_TIMEOUT", "60")),
                enabled=True  # 默认启用，简化configuration
            ),
            "fetch": MCPServiceConfig(
                name="Fetch MCP", 
                url="https://mcp.api-inference.modelscope.net/6ec508e067dc41/sse",
                timeout=int(os.getenv("MCP_TIMEOUT", "60")),
                enabled=True  # 默认启用，简化configuration
            )
        }
        
        # Applyfeatureconfiguration
        self.features = {
            "external_knowledge": any(service.enabled for service in self.mcp_services.values()),
            "multi_mcp_fusion": sum(service.enabled for service in self.mcp_services.values()) > 1
        }
        
        # logconfiguration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    def get_enabled_mcp_services(self) -> List[MCPServiceConfig]:
        """Get已启用的MCPservice列table"""
        return [service for service in self.mcp_services.values() if service.enabled]
    
    def get_mcp_service(self, service_key: str) -> Optional[MCPServiceConfig]:
        """GetspecifiedMCPserviceconfiguration"""
        return self.mcp_services.get(service_key)
    
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.environment == "production"
    
    def validate_config(self) -> Dict[str, str]:
        """Validateconfigurationcompleteness"""
        errors = {}
        
        # ValidateAI模型configuration
        if not self.ai_model.api_key:
            errors["ai_model"] = "SILICONFLOW_API_KEY 未configuration"
        
        # ValidateMCPserviceconfiguration
        enabled_services = self.get_enabled_mcp_services()
        if not enabled_services:
            errors["mcp_services"] = "未configuration任何MCPservice，somefeature将受限"
        
        return errors
    
    def get_config_summary(self) -> Dict:
        """Getconfigurationsummaryinformation"""
        enabled_services = self.get_enabled_mcp_services()
        
        return {
            "environment": self.environment,
            "debug": self.debug,
            "port": self.port,
            "ai_model": {
                "provider": self.ai_model.provider,
                "model": self.ai_model.model_name,
                "configured": bool(self.ai_model.api_key)
            },
            "mcp_services": {
                "total": len(self.mcp_services),
                "enabled": len(enabled_services),
                "services": [service.name for service in enabled_services]
            },
            "features": self.features
        }

# 全局configuration实例
config = AppConfig()

# 常用configurationconstants
EXAMPLE_CONFIGURATIONS = {
    "web_applications": {
        "description": "Web Application Development Examples",
        "examples": [
            {
                "idea": "E-commerce platform with product catalog, shopping cart, and payment integration",
                "reference_url": "https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps",
                "category": "web"
            },
            {
                "idea": "Social networking platform with user profiles, posts, comments, and real-time chat",
                "reference_url": "https://react.dev/learn",
                "category": "web"
            }
        ]
    },
    "mobile_apps": {
        "description": "Mobile Application Examples",
        "examples": [
            {
                "idea": "Fitness tracking app with workout plans, nutrition tracking, and progress analytics",
                "reference_url": "",
                "category": "mobile"
            },
            {
                "idea": "Language learning app with gamification, speech recognition, and personalized lessons",
                "reference_url": "",
                "category": "mobile"
            }
        ]
    },
    "data_science": {
        "description": "Data Science & AI Project Examples",
        "examples": [
            {
                "idea": "Customer sentiment analysis system using NLP and machine learning",
                "reference_url": "https://scikit-learn.org/stable/",
                "category": "data_science"
            },
            {
                "idea": "Predictive maintenance platform for industrial equipment using IoT sensors",
                "reference_url": "",
                "category": "data_science"
            }
        ]
    }
}