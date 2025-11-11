"""
User Plan Editor
Allow users toAIgenerated development plan进行分段edit和修改
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
    """editable plan paragraphs"""
    section_id: str
    title: str
    content: str
    section_type: str  # 'heading', 'paragraph', 'list', 'code', 'table'
    level: int  # 1-6 for headings, 0 for others
    start_line: int
    end_line: int
    is_editable: bool = True

class PlanEditor:
    """Development Plan Editor"""
    
    def __init__(self):
        self.sections: List[EditableSection] = []
        self.original_content = ""
        self.modified_content = ""
        self.edit_history: List[Dict] = []
    
    def parse_plan_content(self, content: str) -> List[EditableSection]:
        """Parse development plan content into editable paragraphs"""
        self.original_content = content
        self.sections = []
        
        lines = content.split('\n')
        current_section = None
        section_counter = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detect heading (# ## ### 等）
            if line.startswith('#') and not line.startswith('```'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:  # valid heading level
                    title = line.lstrip('#').strip()
                    
                    # save previous paragraph
                    if current_section and current_section.content.strip():
                        self.sections.append(current_section)
                    
                    # create new heading paragraph
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
            
            # detect code block
            if line.startswith('```'):
                if current_section and current_section.content.strip():
                    self.sections.append(current_section)
                
                # collect entire code block
                code_content = [line]
                i += 1
                start_line = i - 1
                
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_content.append(lines[i])
                    i += 1
                
                if i < len(lines):  # add end```
                    code_content.append(lines[i])
                    i += 1
                
                section_counter += 1
                code_section = EditableSection(
                    section_id=f"code_{section_counter}",
                    title="code 块",
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
            
            # 检测表格
            if '|' in line and line.count('|') >= 2:
                if current_section and current_section.content.strip():
                    self.sections.append(current_section)
                
                # 收集整个表格
                table_content = [line]
                start_line = i
                i += 1
                
                while i < len(lines) and '|' in lines[i] and lines[i].count('|') >= 2:
                    table_content.append(lines[i])
                    i += 1
                
                section_counter += 1
                table_section = EditableSection(
                    section_id=f"table_{section_counter}",
                    title="表格",
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
            
            # 检测 list
            if line.startswith(('-', '*', '+')) or re.match(r'^\d+\.', line):
                if current_section and current_section.section_type != 'list':
                    if current_section.content.strip():
                        self.sections.append(current_section)
                    
                    section_counter += 1
                    current_section = EditableSection(
                        section_id=f"list_{section_counter}",
                        title="list",
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
                        title="list",
                        content=line,
                        section_type='list',
                        level=0,
                        start_line=i,
                        end_line=i,
                        is_editable=True
                    )
                i += 1
                continue
            
            # 普通 paragraph
            if line:
                if current_section and current_section.section_type == 'paragraph':
                    current_section.content += '\n' + line
                    current_section.end_line = i
                elif current_section and current_section.section_type == 'heading':
                    # title after 一个 paragraph
                    section_counter += 1
                    new_section = EditableSection(
                        section_id=f"paragraph_{section_counter}",
                        title="paragraph",
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
                        title="paragraph",
                        content=line,
                        section_type='paragraph',
                        level=0,
                        start_line=i,
                        end_line=i,
                        is_editable=True
                    )
            
            i += 1
        
        # save finally 一个 paragraph
        if current_section and current_section.content.strip():
            self.sections.append(current_section)
        
        logger.info(f"parse complete ，共找 to {len(self.sections)} 个可edit paragraph")
        return self.sections
    
    def _is_section_editable(self, title: str) -> bool:
        """判 break paragraph is 否 can edit"""
        non_editable_patterns = [
            r'generation time',
            r'AImodel',
            r'基于 user 创意',
            r'Agentapplication',
            r'meta-info'
        ]
        
        title_lower = title.lower()
        return not any(re.search(pattern, title_lower) for pattern in non_editable_patterns)
    
    def get_editable_sections(self) -> List[Dict]:
        """Get editable paragraph list (for frontend display)"""
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
        """get paragraph 预览"""
        # removeMarkdownformat符号
        preview = re.sub(r'[#*`|]', '', content)
        preview = re.sub(r'\n+', ' ', preview).strip()
        
        if len(preview) > max_length:
            preview = preview[:max_length] + '...'
        
        return preview
    
    def update_section(self, section_id: str, new_content: str, user_comment: str = "") -> bool:
        """update 指定 paragraph content"""
        try:
            # find 目标 paragraph
            target_section = None
            for section in self.sections:
                if section.section_id == section_id:
                    target_section = section
                    break
            
            if not target_section:
                logger.error(f"未找 to paragraph {section_id}")
                return False
            
            if not target_section.is_editable:
                logger.error(f"paragraph {section_id} 不可edit")
                return False
            
            # 记录 edit 历史
            self.edit_history.append({
                'timestamp': datetime.now().isoformat(),
                'section_id': section_id,
                'old_content': target_section.content,
                'new_content': new_content,
                'user_comment': user_comment
            })
            
            # update content
            target_section.content = new_content
            
            # 重新构建 complete content
            self._rebuild_content()
            
            logger.info(f"success update paragraph {section_id}")
            return True
            
        except Exception as e:
            logger.error(f"update paragraph failure: {str(e)}")
            return False
    
    def _rebuild_content(self):
        """重新构建 complete content"""
        try:
            lines = self.original_content.split('\n')
            
            # 按行号 sort paragraph
            sorted_sections = sorted(self.sections, key=lambda x: x.start_line)
            
            # 重新构建 content
            new_lines = []
            current_line = 0
            
            for section in sorted_sections:
                # add paragraph before 空行
                while current_line < section.start_line:
                    new_lines.append(lines[current_line])
                    current_line += 1
                
                # add update after paragraph content
                new_lines.extend(section.content.split('\n'))
                
                # 跳过原始 paragraph 行
                current_line = section.end_line + 1
            
            # add 剩余行
            while current_line < len(lines):
                new_lines.append(lines[current_line])
                current_line += 1
            
            self.modified_content = '\n'.join(new_lines)
            
        except Exception as e:
            logger.error(f"重建 content failure: {str(e)}")
            self.modified_content = self.original_content
    
    def get_modified_content(self) -> str:
        """get modify after complete content"""
        return self.modified_content if self.modified_content else self.original_content
    
    def get_edit_history(self) -> List[Dict]:
        """get edit 历史"""
        return self.edit_history
    
    def get_edit_summary(self) -> Dict:
        """get edit 摘 want"""
        return {
            'total_sections': len(self.sections),
            'editable_sections': len([s for s in self.sections if s.is_editable]),
            'edited_sections': len(self.edit_history),
            'last_edit_time': self.edit_history[-1]['timestamp'] if self.edit_history else None
        }
    
    def reset_to_original(self):
        """重置 to 原始 content"""
        self.modified_content = self.original_content
        self.edit_history = []
        # 重新 parse paragraph
        self.parse_plan_content(self.original_content)
        logger.info("已重置 to 原始 content")
    
    def export_edited_content(self, format_type: str = 'markdown') -> str:
        """导出 edit after content"""
        content = self.get_modified_content()
        
        if format_type == 'markdown':
            return content
        elif format_type == 'html':
            # simpleMarkdown到HTMLconvert
            import markdown
            return markdown.markdown(content)
        else:
            return content

# 全局 edit 器 example
plan_editor = PlanEditor()