"""
AIcan solveexplain性管managedevice
提provide process 链条transparentdegree and 结合SOP的cansolveexplain性功能
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class ProcessingStage(Enum):
    """process phase 枚举"""
    INPUT_VALIDATION = "input_validation"
    PROMPT_OPTIMIZATION = "prompt_optimization"
    KNOWLEDGE_RETRIEVAL = "knowledge_retrieval"
    AI_GENERATION = "ai_generation"
    QUALITY_ASSESSMENT = "quality_assessment"
    CONTENT_FORMATTING = "content_formatting"
    RESULT_VALIDATION = "result_validation"

@dataclass
class ProcessingStep:
    """process Step data 结construct"""
    stage: ProcessingStage
    title: str
    description: str
    timestamp: str
    duration: float
    success: bool
    details: Dict[str, Any]
    quality_score: Optional[float] = None
    evidence: Optional[str] = None

class ExplanationManager:
    """AIcan solveexplain性管managedevice"""
    
    def __init__(self):
        self.processing_steps: List[ProcessingStep] = []
        self.sop_guidelines = self._load_sop_guidelines()
        self.quality_metrics = {}
        
    def start_processing(self):
        """start process procedure"""
        self.processing_steps.clear()
        self.quality_metrics.clear()
        logger.info("🔄 start process 链条track")
    
    def add_processing_step(self, 
                          stage: ProcessingStage,
                          title: str,
                          description: str,
                          success: bool,
                          details: Dict[str, Any],
                          duration: float = 0.0,
                          quality_score: Optional[float] = None,
                          evidence: Optional[str] = None):
        """add process Step"""
        step = ProcessingStep(
            stage=stage,
            title=title,
            description=description,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            duration=duration,
            success=success,
            details=details,
            quality_score=quality_score,
            evidence=evidence
        )
        
        self.processing_steps.append(step)
        logger.info(f"📝 记录 process Step: {title} - {'✅' if success else '❌'}")
    
    def get_processing_explanation(self) -> str:
        """get process procedure detailed description"""
        if not self.processing_steps:
            return "temporarily无 process 记录"
        
        explanation = self._generate_explanation_header()
        explanation += self._generate_sop_compliance_report()
        explanation += self._generate_processing_steps_report()
        explanation += self._generate_quality_metrics_report()
        explanation += self._generate_evidence_summary()
        
        return explanation
    
    def _generate_explanation_header(self) -> str:
        """generate description 头部"""
        total_steps = len(self.processing_steps)
        successful_steps = sum(1 for step in self.processing_steps if step.success)
        success_rate = (successful_steps / total_steps * 100) if total_steps > 0 else 0
        
        return f"""
# 🔍 AIgenerate procedure detailed description

## 📊 process generalbrowse
- **total process Step**: {total_steps}
- **success Step**: {successful_steps}
- **success 率**: {success_rate:.1f}%
- **process when time**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
    
    def _generate_sop_compliance_report(self) -> str:
        """generateSOP合规报notify"""
        return f"""
## 📋 SOP (mark准operate程序) 合规报notify

### 🎯 quality 保证mark准
{self._format_sop_guidelines()}

### ✅ 合规性 check
- **input verify**: {'✅ 通过' if self._check_sop_compliance('input_validation') else '❌ not yet通过'}
- **knowledge acquisition**: {'✅ 通过' if self._check_sop_compliance('knowledge_retrieval') else '❌ not yet通过'}
- **AIgenerate**: {'✅ 通过' if self._check_sop_compliance('ai_generation') else '❌ not yet通过'}
- **quality assessment**: {'✅ 通过' if self._check_sop_compliance('quality_assessment') else '❌ not yet通过'}
- **content formatting**: {'✅ 通过' if self._check_sop_compliance('content_formatting') else '❌ not yet通过'}

---

"""
    
    def _generate_processing_steps_report(self) -> str:
        """generate process Step 报notify"""
        report = "## 🔄 detailed process Step\n\n"
        
        for i, step in enumerate(self.processing_steps, 1):
            status_icon = "✅" if step.success else "❌"
            quality_info = f" (quality divide: {step.quality_score:.1f})" if step.quality_score else ""
            
            report += f"""
### Step {i}: {step.title} {status_icon}

- **phase**: {self._get_stage_name(step.stage)}
- **when time**: {step.timestamp}
- **consume when**: {step.duration:.2f}seconds{quality_info}
- **description**: {step.description}

**detailed information**:
{self._format_step_details(step.details)}

"""
            
            if step.evidence:
                report += f"**证data**: {step.evidence}\n\n"
        
        return report + "---\n\n"
    
    def _generate_quality_metrics_report(self) -> str:
        """generate quality pointmark报notify"""
        if not self.quality_metrics:
            return ""
        
        report = "## 📈 quality pointmark详情\n\n"
        
        for metric_name, metric_value in self.quality_metrics.items():
            report += f"- **{metric_name}**: {metric_value}\n"
        
        return report + "\n---\n\n"
    
    def _generate_evidence_summary(self) -> str:
        """generate 证data summary"""
        evidence_steps = [step for step in self.processing_steps if step.evidence]
        
        if not evidence_steps:
            return ""
        
        report = "## 🧾 证data summary\n\n"
        
        for i, step in enumerate(evidence_steps, 1):
            report += f"**{i}. {step.title}**\n{step.evidence}\n\n"
        
        return report
    
    def _load_sop_guidelines(self) -> Dict[str, Any]:
        """loadSOPpointguideoriginal则"""
        return {
            "input_validation": {
                "title": "input verify mark准",
                "requirements": [
                    "user input 长degree >= 10字symbol",
                    "input content include 产品 description",
                    "无恶意 content and 敏感 information"
                ]
            },
            "knowledge_retrieval": {
                "title": "外部 knowledge acquisition",
                "requirements": [
                    "MCPservice 连connect status check",
                    "reference link have 效性 verify",
                    "knowledge content 相关性 assessment"
                ]
            },
            "ai_generation": {
                "title": "AIcontent generate",
                "requirements": [
                    "use 专业 system prompt",
                    "generate content 结construct complete",
                    "include 必 want 技technique细section"
                ]
            },
            "quality_assessment": {
                "title": "quality assessment mark准",
                "requirements": [
                    "content complete 性 check",
                    "Mermaiddiagram table语法 verify",
                    "link have 效性 check",
                    "date准确性 verify"
                ]
            },
            "content_formatting": {
                "title": "content formatting",
                "requirements": [
                    "Markdownformat 规范",
                    "add when time 戳 and meta information",
                    "enhanced prompt display 效result"
                ]
            }
        }
    
    def _format_sop_guidelines(self) -> str:
        """formattingSOPpointguideoriginal则"""
        formatted = ""
        for key, guideline in self.sop_guidelines.items():
            formatted += f"**{guideline['title']}**:\n"
            for requirement in guideline['requirements']:
                formatted += f"- {requirement}\n"
            formatted += "\n"
        return formatted
    
    def _check_sop_compliance(self, stage_name: str) -> bool:
        """checkSOP合规性"""
        relevant_steps = [step for step in self.processing_steps 
                         if step.stage.value == stage_name]
        return len(relevant_steps) > 0 and all(step.success for step in relevant_steps)
    
    def _get_stage_name(self, stage: ProcessingStage) -> str:
        """get phase name called"""
        stage_names = {
            ProcessingStage.INPUT_VALIDATION: "input verify",
            ProcessingStage.PROMPT_OPTIMIZATION: "prompt optimize",
            ProcessingStage.KNOWLEDGE_RETRIEVAL: "knowledge acquisition",
            ProcessingStage.AI_GENERATION: "AIgenerate",
            ProcessingStage.QUALITY_ASSESSMENT: "quality assessment",
            ProcessingStage.CONTENT_FORMATTING: "content formatting",
            ProcessingStage.RESULT_VALIDATION: "结result verify"
        }
        return stage_names.get(stage, stage.value)
    
    def _format_step_details(self, details: Dict[str, Any]) -> str:
        """formatting Step 详情"""
        formatted = ""
        for key, value in details.items():
            if isinstance(value, dict):
                formatted += f"  - **{key}**: {self._format_nested_dict(value)}\n"
            elif isinstance(value, list):
                formatted += f"  - **{key}**: {', '.join(str(item) for item in value)}\n"
            else:
                formatted += f"  - **{key}**: {value}\n"
        return formatted
    
    def _format_nested_dict(self, nested_dict: Dict[str, Any]) -> str:
        """formatting 嵌套字典"""
        items = []
        for key, value in nested_dict.items():
            items.append(f"{key}={value}")
        return f"{{{', '.join(items)}}}"
    
    def update_quality_metrics(self, metrics: Dict[str, Any]):
        """update quality pointmark"""
        self.quality_metrics.update(metrics)
        
    def get_trust_score(self) -> float:
        """calculatetrust任divide数"""
        if not self.processing_steps:
            return 0.0
        
        # 基于 success 率 and quality divide数calculatetrust任divide数
        success_rate = sum(1 for step in self.processing_steps if step.success) / len(self.processing_steps)
        
        quality_scores = [step.quality_score for step in self.processing_steps if step.quality_score]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        # trust任divide数 = success 率 * 0.6 + 平均quality divide数 * 0.4
        trust_score = success_rate * 0.6 + (avg_quality / 100) * 0.4
        
        return round(trust_score * 100, 1)

# 全局 can solveexplain性管managedevice example
explanation_manager = ExplanationManager()