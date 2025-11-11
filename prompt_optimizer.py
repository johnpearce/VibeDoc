"""
prompt optimize 器 module
useAIoptimize user input 创意 description，提升generate报告的质量
"""

import requests
import json
import logging
from typing import Tuple, Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)

class PromptOptimizer:
    """user input prompt optimize 器"""
    
    def __init__(self):
        self.api_key = config.ai_model.api_key
        self.api_url = config.ai_model.api_url
        self.model_name = config.ai_model.model_name
        
    def optimize_user_input(self, user_idea: str) -> Tuple[bool, str, str]:
        """
        optimize user input 创意 description
        
        Args:
            user_idea: user 原始 input
            
        Returns:
            Tuple[bool, str, str]: (success status, optimize after description, optimizerecommendation)
        """
        if not self.api_key:
            return False, user_idea, "API密钥未 configuration ，无法 optimize description"
        
        if not user_idea or len(user_idea.strip()) < 5:
            return False, user_idea, "input content 过短，无法 optimize"
        
        try:
            # 构建 optimize prompt
            optimization_prompt = self._build_optimization_prompt(user_idea)
            
            # callAIoptimize
            response = self._call_ai_service(optimization_prompt)
            
            if response['success']:
                result = self._parse_optimization_result(response['data'])
                return True, result['optimized_idea'], result['suggestions']
            else:
                logger.error(f"AIoptimize failure: {response['error']}")
                return False, user_idea, f"optimize failure: {response['error']}"
                
        except Exception as e:
            logger.error(f"prompt optimize exception: {e}")
            return False, user_idea, f"optimize procedure 出错: {str(e)}"
    
    def _build_optimization_prompt(self, user_idea: str) -> str:
        """构建 optimize prompt"""
        return f"""你 is 一个专业 Product Manager and 技术顾问，擅长 will user simple 想法 extension for detailed 产品 description 。

user 原始 input ：
{user_idea}

Please help optimize this creative description to make it more detailed, specific and professional. The optimized description should contain the following elements:

1. **core function**：明确产品的main function和价值
2. **目标 user**：定义产品的目标 user群体
3. **use 场景**：description产品的典型use 场景
4. **技术特点**：提及可能需要的key 技术特性
5. **商业价 value**：阐述产品的市场价值和竞争优势

请按 with 下JSONformat输出：
{{
    "optimized_idea": "optimize after detailed 产品 description",
    "key_improvements": [
        "改进点1",
        "改进点2",
        "改进点3"
    ],
    "suggestions": "进一步 optimize recommendation"
}}

requirement ：
- 保持原始创意核心思想
- use 专业但易懂语言
- 长度控制 in200-400字之间
- 突出产品创新性 and actual 用性"""

    def _call_ai_service(self, prompt: str) -> Dict[str, Any]:
        """callAIservice"""
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
                timeout=300  # Optimization: Creative description optimization timeout is300秒（5分钟）
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                return {"success": True, "data": content}
            else:
                return {"success": False, "error": f"APIcall failed: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _parse_optimization_result(self, ai_response: str) -> Dict[str, Any]:
        """parseAIoptimize结果"""
        try:
            # try parseJSON
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
                # such as 果无法 parseJSON，直接返回原始响应
                return {
                    "optimized_idea": ai_response,
                    "suggestions": "AIReturned optimization suggestions, but format needs adjustment",
                    "key_improvements": []
                }
                
        except json.JSONDecodeError:
            # JSONparse failure ，返回原始 response should
            return {
                "optimized_idea": ai_response,
                "suggestions": "AIReturned optimization suggestions, but format needs adjustment",
                "key_improvements": []
            }
    
    def get_optimization_examples(self) -> list:
        """get optimize example"""
        return [
            {
                "original": "我想做一个购物 website",
                "optimized": "Develop an intelligent shopping platform for young consumers, integratingAI推荐系统、社交分享功能和个性化user experience。平台将提供多品类商品展示、智能搜索、用户评价系统和便捷的移动支付功能，旨in为用户提供个性化的购物体验和高质量的商品推荐service。",
                "improvements": ["明确目标 user", "定义core function", "突出技术特色"]
            },
            {
                "original": "想搞个学习 system",
                "optimized": "Build aAI的个性化online学习管理系统，support多媒体content展示、学习进度跟踪、智能题库管理和师生互动功能。系统将为教育机构和个人学习者提供complete数字化学习solution，包括课程管理、作业批改、学习分析和成绩评估等功能。",
                "improvements": ["extension function description", "明确application场景", "增加技术亮点"]
            }
        ]

# 全局 optimize 器 example
prompt_optimizer = PromptOptimizer()