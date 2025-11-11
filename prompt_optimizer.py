"""
prompt optimize device module
useAIoptimize user input 创意 description，提升generate报notify的质quantity
"""

import requests
import json
import logging
from typing import Tuple, Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)

class PromptOptimizer:
    """user input prompt optimize device"""
    
    def __init__(self):
        self.api_key = config.ai_model.api_key
        self.api_url = config.ai_model.api_url
        self.model_name = config.ai_model.model_name
        
    def optimize_user_input(self, user_idea: str) -> Tuple[bool, str, str]:
        """
        optimize user input 创意 description
        
        Args:
            user_idea: user original始 input
            
        Returns:
            Tuple[bool, str, str]: (success status, optimize after description, optimizerecommendation)
        """
        if not self.api_key:
            return False, user_idea, "API密keynot yet configuration ，无法 optimize description"
        
        if not user_idea or len(user_idea.strip()) < 5:
            return False, user_idea, "input content 过short，无法 optimize"
        
        try:
            # construct建 optimize prompt
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
            return False, user_idea, f"optimize procedure out错: {str(e)}"
    
    def _build_optimization_prompt(self, user_idea: str) -> str:
        """construct建 optimize prompt"""
        return f"""你 is 一个专业 Product Manager and 技techniqueconsider问，擅长 will user simple 想法 extension for detailed 产品 description 。

user original始 input ：
{user_idea}

Please help optimize this creative description to make it more detailed, specific and professional. The optimized description should contain the following elements:

1. **core function**：明确产品的main function和价值
2. **目mark user**：定义产品的目mark user群body
3. **use 场scene**：description产品的典型use 场scene
4. **技technique特点**：提及can能需important的key 技technique特性
5. **商业价 value**：阐述产品的市场价值和竞争excellenttrend

pleasepress with 下JSONformat输out：
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
- 保持original始创意核心think想
- use 专业但易懂语言
- 长degree控make in200-400字of间
- 突out产品创新性 and actual use性"""

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
                timeout=300  # Optimization: Creative description optimization timeout is300seconds（5divideclock）
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
        """parseAIoptimize结result"""
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
                # such as result无法 parseJSON，direct返回original始响should
                return {
                    "optimized_idea": ai_response,
                    "suggestions": "AIReturned optimization suggestions, but format needs adjustment",
                    "key_improvements": []
                }
                
        except json.JSONDecodeError:
            # JSONparse failure ，返回original始 response should
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
                "optimized": "Develop an intelligent shopping platform for young consumers, integratingAIpush荐系统、社exchangedivide享功能和个性transformuser experience。平台will提provide多品类商品expand示、智能搜索、use户评价系统和convenient捷的移动支付功能，旨in为use户提provide个性transform的购物bodyexperience和高质quantity的商品push荐service。",
                "improvements": ["明确目mark user", "定义core function", "突out技technique特色"]
            },
            {
                "original": "想搞个learn习 system",
                "optimized": "Build aAI的个性transformonlinelearn习管manage系统，support多媒bodycontentexpand示、learn习进degree跟踪、智能题库管manage和expert生互动功能。系统will为教育机construct和个人learn习者提providecomplete数字transformlearn习solution，packageinclude课程管manage、work业批改、learn习analyze和成performance评估等功能。",
                "improvements": ["extension function description", "明确application场scene", "增加技technique亮点"]
            }
        ]

# 全局 optimize device example
prompt_optimizer = PromptOptimizer()