"""
tip词Optimize器module
使用AIOptimizeuserEnter的Idea Description，提升Generate报告的质量
"""

import requests
import json
import logging
from typing import Tuple, Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)

class PromptOptimizer:
    """userEntertip词Optimize器"""
    
    def __init__(self):
        self.api_key = config.ai_model.api_key
        self.api_url = config.ai_model.api_url
        self.model_name = config.ai_model.model_name
        
    def optimize_user_input(self, user_idea: str) -> Tuple[bool, str, str]:
        """
        OptimizeuserEnter的Idea Description
        
        Args:
            user_idea: user原始Enter
            
        Returns:
            Tuple[bool, str, str]: (successfulstatus, Optimize后的description, Optimizesuggestions)
        """
        if not self.api_key:
            return False, user_idea, "API密钥未configuration，unable toOptimizedescription"
        
        if not user_idea or len(user_idea.strip()) < 5:
            return False, user_idea, "Entercontenttoo short，unable toOptimize"
        
        try:
            # 构建Optimizetip词
            optimization_prompt = self._build_optimization_prompt(user_idea)
            
            # CallAIOptimize
            response = self._call_ai_service(optimization_prompt)
            
            if response['success']:
                result = self._parse_optimization_result(response['data'])
                return True, result['optimized_idea'], result['suggestions']
            else:
                logger.error(f"AIOptimizefailed: {response['error']}")
                return False, user_idea, f"Optimizefailed: {response['error']}"
                
        except Exception as e:
            logger.error(f"tip词Optimize异常: {e}")
            return False, user_idea, f"Optimize过程出错: {str(e)}"
    
    def _build_optimization_prompt(self, user_idea: str) -> str:
        """构建Optimizetip词"""
        return f"""你是一个专业的产品经理和技术顾问，擅长将user的简单想法扩展为详细的产品description。

user原始Enter：
{user_idea}

请帮助Optimize这个Idea Description，使其更加详细、具体和专业。Optimize后的description应该包含以下要素：

1. **Core Features**：明确产品的主要feature和价值
2. **目标user**：定义产品的目标user群体
3. **使用场景**：description产品的典型使用场景
4. **技术特点**：提及可能需要的关键技术特性
5. **商业价值**：阐述产品的市场价值和竞争优势

请按以下JSONformatoutput：
{{
    "optimized_idea": "Optimize后的详细产品description",
    "key_improvements": [
        "改进点1",
        "改进点2",
        "改进点3"
    ],
    "suggestions": "进一步Optimizesuggestions"
}}

要求：
- 保持原始创意的核心思想
- 使用专业但易懂的语言
- length控制在200-400字之间
- 突出产品的创新性和实用性"""

    def _call_ai_service(self, prompt: str) -> Dict[str, Any]:
        """CallAIservice"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=300  # Optimize：Idea DescriptionOptimizeTimeout duration为300s（5min）
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                return {"success": True, "data": content}
            else:
                return {"success": False, "error": f"APICallfailed: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _parse_optimization_result(self, ai_response: str) -> Dict[str, Any]:
        """ParseAIOptimizeresult"""
        try:
            # 尝试ParseJSON
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                result = json.loads(json_str)
                
                return {
                    "optimized_idea": result.get("optimized_idea", ""),
                    "suggestions": result.get("suggestions", ""),
                    "key_improvements": result.get("key_improvements", [])
                }
            else:
                # 如果unable toParseJSON，直接返回原始响应
                return {
                    "optimized_idea": ai_response,
                    "suggestions": "AI返回了Optimizesuggestions，但format需要调整",
                    "key_improvements": []
                }
                
        except json.JSONDecodeError:
            # JSONParsefailed，返回原始响应
            return {
                "optimized_idea": ai_response,
                "suggestions": "AI返回了Optimizesuggestions，但format需要调整",
                "key_improvements": []
            }
    
    def get_optimization_examples(self) -> list:
        """GetOptimizeexample"""
        return [
            {
                "original": "我想做一个购物网站",
                "optimized": "开发一个面向y轻消费者的智能购物平台，集成AI推荐系统、社交分享feature和个性化user体验。平台将提供多品类商品展示、智能Search、user评价系统和便捷的移动支付feature，旨在为user提供个性化的购物体验和高质量的商品推荐service。",
                "improvements": ["明确目标user", "定义Core Features", "突出技术特色"]
            },
            {
                "original": "想搞个学习系统",
                "optimized": "构建一个基于AI的个性化Online学习管理系统，支持多媒体content展示、学习进度跟踪、智能题库管理和师生互动feature。系统将为教育机构和个人学习者提供完整的数字化学习解决方案，包括课程管理、作业批改、学习分析和成绩评估等feature。",
                "improvements": ["扩展featuredescription", "明确Apply场景", "增加技术亮点"]
            }
        ]

# 全局Optimize器实例
prompt_optimizer = PromptOptimizer()