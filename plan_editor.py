"""
user方案Edit器
允许user对AIGenerate的Development Plan进行分段Edit和修改
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class EditableSection:
    """可Editplan sections"""
    section_id: str
    title: str
    content: str
    section_type: str  # 'heading', 'paragraph', 'list', 'code', 'table'
    level: int  # 1-6 for headings, 0 for others
    start_line: int
    end_line: int
    is_editable: bool = True

class PlanEditor:
    """Development PlanEdit器"""
    
    def __init__(self):
        self.sections: List[EditableSection] = []
        self.original_content = ""
        self.modified_content = ""
        self.edit_history: List[Dict] = []
    
    def parse_plan_content(self, content: str) -> List[EditableSection]:
        """ParseDevelopment Plancontentas availableEdit段落"""
        self.original_content = content
        self.sections = []
        
        lines = content.split('\n')
        current_section = None
        section_counter = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 检测title（# ## ### 等）
            if line.startswith('#') and not line.startswith('```'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:  # 有效的title级别
                    title = line.lstrip('#').strip()
                    
                    # Save上一个段落
                    if current_section and current_section.content.strip():
                        self.sections.append(current_section)
                    
                    # Create新的title段落
                    section_counter += 1
                    current_section = EditableSection(
                        section_id=f"section_{section_counter}",
                        title=title,
                        content=line,
                        section_type='heading',
                        level=level,
                        start_line=i,
                        end_line=i,
                        is_editable=self._is_section_editable(title)
                    )
                    i += 1
                    continue
            
            # 检测代码块
            if line.startswith('```'):
                if current_section and current_section.content.strip():
                    self.sections.append(current_section)
                
                # 收集整个代码块
                code_content = [line]
                i += 1
                start_line = i - 1
                
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_content.append(lines[i])
                    i += 1
                
                if i < len(lines):  # addend的```
                    code_content.append(lines[i])
                    i += 1
                
                section_counter += 1
                code_section = EditableSection(
                    section_id=f"code_{section_counter}",
                    title="代码块",
                    content='\n'.join(code_content),
                    section_type='code',
                    level=0,
                    start_line=start_line,
                    end_line=i - 1,
                    is_editable=True
                )
                self.sections.append(code_section)
                current_section = None
                continue
            
            # 检测table格
            if '|' in line and line.count('|') >= 2:
                if current_section and current_section.content.strip():
                    self.sections.append(current_section)
                
                # 收集整个table格
                table_content = [line]
                start_line = i
                i += 1
                
                while i < len(lines) and '|' in lines[i] and lines[i].count('|') >= 2:
                    table_content.append(lines[i])
                    i += 1
                
                section_counter += 1
                table_section = EditableSection(
                    section_id=f"table_{section_counter}",
                    title="table格",
                    content='\n'.join(table_content),
                    section_type='table',
                    level=0,
                    start_line=start_line,
                    end_line=i - 1,
                    is_editable=True
                )
                self.sections.append(table_section)
                current_section = None
                continue
            
            # 检测列table
            if line.startswith(('-', '*', '+')) or re.match(r'^\d+\.', line):
                if current_section and current_section.section_type != 'list':
                    if current_section.content.strip():
                        self.sections.append(current_section)
                    
                    section_counter += 1
                    current_section = EditableSection(
                        section_id=f"list_{section_counter}",
                        title="列table",
                        content=line,
                        section_type='list',
                        level=0,
                        start_line=i,
                        end_line=i,
                        is_editable=True
                    )
                elif current_section and current_section.section_type == 'list':
                    current_section.content += '\n' + line
                    current_section.end_line = i
                else:
                    section_counter += 1
                    current_section = EditableSection(
                        section_id=f"list_{section_counter}",
                        title="列table",
                        content=line,
                        section_type='list',
                        level=0,
                        start_line=i,
                        end_line=i,
                        is_editable=True
                    )
                i += 1
                continue
            
            # normal paragraph
            if line:
                if current_section and current_section.section_type == 'paragraph':
                    current_section.content += '\n' + line
                    current_section.end_line = i
                elif current_section and current_section.section_type == 'heading':
                    # title后的第一个段落
                    section_counter += 1
                    new_section = EditableSection(
                        section_id=f"paragraph_{section_counter}",
                        title="段落",
                        content=line,
                        section_type='paragraph',
                        level=0,
                        start_line=i,
                        end_line=i,
                        is_editable=True
                    )
                    self.sections.append(current_section)
                    current_section = new_section
                else:
                    if current_section and current_section.content.strip():
                        self.sections.append(current_section)
                    
                    section_counter += 1
                    current_section = EditableSection(
                        section_id=f"paragraph_{section_counter}",
                        title="段落",
                        content=line,
                        section_type='paragraph',
                        level=0,
                        start_line=i,
                        end_line=i,
                        is_editable=True
                    )
            
            i += 1
        
        # Savelast paragraph
        if current_section and current_section.content.strip():
            self.sections.append(current_section)
        
        logger.info(f"Parsecompleted，共找到 {len(self.sections)} 个可Edit段落")
        return self.sections
    
    def _is_section_editable(self, title: str) -> bool:
        """判断段落是否可Edit"""
        non_editable_patterns = [
            r'Generation Time',
            r'AI模型',
            r'基于user创意',
            r'AgentApply',
            r'meta-info'
        ]
        
        title_lower = title.lower()
        return not any(re.search(pattern, title_lower) for pattern in non_editable_patterns)
    
    def get_editable_sections(self) -> List[Dict]:
        """Get可Edit段落列table（用于前端Show）"""
        editable_sections = []
        
        for section in self.sections:
            if section.is_editable:
                editable_sections.append({
                    'id': section.section_id,
                    'title': section.title,
                    'content': section.content,
                    'type': section.section_type,
                    'level': section.level,
                    'preview': self._get_section_preview(section.content)
                })
        
        return editable_sections
    
    def _get_section_preview(self, content: str, max_length: int = 100) -> str:
        """Get段落预览"""
        # 移除Markdownformat符号
        preview = re.sub(r'[#*`|]', '', content)
        preview = re.sub(r'\n+', ' ', preview).strip()
        
        if len(preview) > max_length:
            preview = preview[:max_length] + '...'
        
        return preview
    
    def update_section(self, section_id: str, new_content: str, user_comment: str = "") -> bool:
        """Update指定段落的content"""
        try:
            # 查找目标段落
            target_section = None
            for section in self.sections:
                if section.section_id == section_id:
                    target_section = section
                    break
            
            if not target_section:
                logger.error(f"not found段落 {section_id}")
                return False
            
            if not target_section.is_editable:
                logger.error(f"段落 {section_id} not可Edit")
                return False
            
            # 记录Edit历史
            self.edit_history.append({
                'timestamp': datetime.now().isoformat(),
                'section_id': section_id,
                'old_content': target_section.content,
                'new_content': new_content,
                'user_comment': user_comment
            })
            
            # Updatecontent
            target_section.content = new_content
            
            # 重新build完整content
            self._rebuild_content()
            
            logger.info(f"successfulUpdate段落 {section_id}")
            return True
            
        except Exception as e:
            logger.error(f"Update段落failed: {str(e)}")
            return False
    
    def _rebuild_content(self):
        """重新build完整content"""
        try:
            lines = self.original_content.split('\n')
            
            # by line numberSort段落
            sorted_sections = sorted(self.sections, key=lambda x: x.start_line)
            
            # 重新buildcontent
            new_lines = []
            current_line = 0
            
            for section in sorted_sections:
                # add段落前的空行
                while current_line < section.start_line:
                    new_lines.append(lines[current_line])
                    current_line += 1
                
                # addUpdate后的段落content
                new_lines.extend(section.content.split('\n'))
                
                # 跳过原始段落行
                current_line = section.end_line + 1
            
            # add剩余的行
            while current_line < len(lines):
                new_lines.append(lines[current_line])
                current_line += 1
            
            self.modified_content = '\n'.join(new_lines)
            
        except Exception as e:
            logger.error(f"重建contentfailed: {str(e)}")
            self.modified_content = self.original_content
    
    def get_modified_content(self) -> str:
        """Get修改后的完整content"""
        return self.modified_content if self.modified_content else self.original_content
    
    def get_edit_history(self) -> List[Dict]:
        """GetEdit历史"""
        return self.edit_history
    
    def get_edit_summary(self) -> Dict:
        """GetEditsummary"""
        return {
            'total_sections': len(self.sections),
            'editable_sections': len([s for s in self.sections if s.is_editable]),
            'edited_sections': len(self.edit_history),
            'last_edit_time': self.edit_history[-1]['timestamp'] if self.edit_history else None
        }
    
    def reset_to_original(self):
        """Reset到原始content"""
        self.modified_content = self.original_content
        self.edit_history = []
        # 重新Parse段落
        self.parse_plan_content(self.original_content)
        logger.info("已Reset到原始content")
    
    def export_edited_content(self, format_type: str = 'markdown') -> str:
        """ExportEdit后的content"""
        content = self.get_modified_content()
        
        if format_type == 'markdown':
            return content
        elif format_type == 'html':
            # 简单的Markdown到HTMLConvert
            import markdown
            return markdown.markdown(content)
        else:
            return content

# 全局Editinstance
plan_editor = PlanEditor()