"""
VibeDoc 多 format guideout管managedevice
support Ma# PDF guideout
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# advancedPDFguideout - removeweasyprintdependency，usereportlab
WEASYPRINT_AVAILABLE = FalseF format documentation guideout
"""

import os
import io
import re
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, Tuple, Optional, Any
import logging

# 核心 dependency
import markdown
import html2text

# Word guideout
try:
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# PDF guideout
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# advancedPDFguideout（备useplan） - removeweasyprintdependency
WEASYPRINT_AVAILABLE = False

logger = logging.getLogger(__name__)

class ExportManager:
    """多 format guideout管managedevice"""
    
    def __init__(self):
        self.supported_formats = ['markdown', 'html']
        
        # check can select dependency
        if DOCX_AVAILABLE:
            self.supported_formats.append('docx')
        if PDF_AVAILABLE:
            self.supported_formats.append('pdf')
            
        logger.info(f"📄 ExportManager initial始transform complete ， support format: {', '.join(self.supported_formats)}")
    
    def get_supported_formats(self) -> list:
        """get support guideout format"""
        return self.supported_formats.copy()
    
    def export_to_markdown(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        export as Markdown format（清manage and optimize）
        
        Args:
            content: original始 content
            metadata: metadata information
            
        Returns:
            str: optimize after Markdown content
        """
        try:
            # add documentation 头部 information
            if metadata:
                header = f"""---
title: {metadata.get('title', 'VibeDoc Development Plan')}
author: {metadata.get('author', 'VibeDoc AI Agent')}
date: {metadata.get('date', datetime.now().strftime('%Y-%m-%d'))}
generator: VibeDoc AI Agent v1.0
---

"""
                content = header + content
            
            # 清manage and optimize content
            content = self._clean_markdown_content(content)
            
            logger.info("✅ Markdown guideout success")
            return content
            
        except Exception as e:
            logger.error(f"❌ Markdown guideout failure: {e}")
            return content  # 返回original始 content
    
    def export_to_html(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        export as HTML format（带样式）
        
        Args:
            content: Markdown content
            metadata: metadata information
            
        Returns:
            str: complete HTML content
        """
        try:
            # configuration Markdown 扩expand
            md = markdown.Markdown(
                extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                    'markdown.extensions.tables'
                ],
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'use_pygments': False
                    },
                    'toc': {
                        'title': 'directory'
                    }
                }
            )
            
            # convert Markdown to HTML
            html_content = md.convert(content)
            
            # generate complete HTML text档
            title = metadata.get('title', 'VibeDoc Development Plan') if metadata else 'VibeDoc Development Plan'
            author = metadata.get('author', 'VibeDoc AI Agent') if metadata else 'VibeDoc AI Agent'
            date = metadata.get('date', datetime.now().strftime('%Y-%m-%d')) if metadata else datetime.now().strftime('%Y-%m-%d')
            
            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="author" content="{author}">
    <meta name="generator" content="VibeDoc AI Agent">
    <style>
        {self._get_html_styles()}
    </style>
    <!-- Mermaid support -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            mermaid.initialize({{ 
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
                flowchart: {{ useMaxWidth: true }}
            }});
        }});
    </script>
</head>
<body>
    <div class="container">
        <header class="document-header">
            <h1>{title}</h1>
            <div class="meta-info">
                <span class="author">📝 {author}</span>
                <span class="date">📅 {date}</span>
                <span class="generator">🤖 Generated by VibeDoc AI Agent</span>
            </div>
        </header>
        
        <main class="content">
            {html_content}
        </main>
        
        <footer class="document-footer">
            <p>This document is generated by <strong>VibeDoc AI Agent</strong> generate | generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>"""
            
            logger.info("✅ HTML guideout success")
            return full_html
            
        except Exception as e:
            logger.error(f"❌ HTML guideout failure: {e}")
            # simple HTML 备useplan
            return f"""<!DOCTYPE html>
<html><head><title>VibeDoc Development Plan</title></head>
<body><pre>{content}</pre></body></html>"""
    
    def export_to_docx(self, content: str, metadata: Optional[Dict] = None) -> bytes:
        """
        export as Word documentation format
        
        Args:
            content: Markdown content
            metadata: metadata information
            
        Returns:
            bytes: Word documentation 二进make data
        """
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx not yet安装，无法guideout Word format")
        
        try:
            # create 新 documentation
            doc = Document()
            
            # setting documentation property
            properties = doc.core_properties
            properties.title = metadata.get('title', 'VibeDoc Development Plan') if metadata else 'VibeDoc Development Plan'
            properties.author = metadata.get('author', 'VibeDoc AI Agent') if metadata else 'VibeDoc AI Agent'
            properties.subject = 'AI驱动 intelligent Development Plan'
            properties.comments = 'Generated by VibeDoc AI Agent'
            
            # add title
            title = doc.add_heading(properties.title, 0)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # add meta information
            doc.add_paragraph()
            meta_para = doc.add_paragraph()
            meta_para.add_run(f"📝 work者: {properties.author}").bold = True
            meta_para.add_run("\n")
            meta_para.add_run(f"📅 generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").bold = True
            meta_para.add_run("\n")
            meta_para.add_run("🤖 generate tool: VibeDoc AI Agent").bold = True
            
            doc.add_paragraph()
            doc.add_paragraph("─" * 50)
            doc.add_paragraph()
            
            # parse and add content
            self._parse_markdown_to_docx(doc, content)
            
            # add 页脚
            doc.add_paragraph()
            doc.add_paragraph("─" * 50)
            footer_para = doc.add_paragraph()
            footer_para.add_run("This document is generated by VibeDoc AI Agent 自动generate").italic = True
            footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # save to internal存
            doc_stream = io.BytesIO()
            doc.save(doc_stream)
            doc_stream.seek(0)
            
            logger.info("✅ Word documentation guideout success")
            return doc_stream.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Word guideout failure: {e}")
            raise
    
    def export_to_pdf(self, content: str, metadata: Optional[Dict] = None) -> bytes:
        """
        export as PDF format
        
        Args:
            content: Markdown content  
            metadata: metadata information
            
        Returns:
            bytes: PDF documentation 二进make data
        """
        if PDF_AVAILABLE:
            return self._export_pdf_reportlab(content, metadata)
        else:
            raise ImportError("PDF guideout dependency not yet安装")
    
    def create_multi_format_export(self, content: str, formats: list = None, metadata: Optional[Dict] = None) -> bytes:
        """
        create 多 format guideout ZIP package
        
        Args:
            content: original始 content
            formats: want guideout format list ，默认 for all have support format
            metadata: metadata information
            
        Returns:
            bytes: ZIP file 二进make data
        """
        if formats is None:
            formats = self.supported_formats
        
        # verify format
        invalid_formats = set(formats) - set(self.supported_formats)
        if invalid_formats:
            raise ValueError(f"not supported format: {', '.join(invalid_formats)}")
        
        try:
            # create internal存 in ZIP textitem
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # generate 基础 file name
                base_name = metadata.get('title', 'vibedoc_plan') if metadata else 'vibedoc_plan'
                base_name = re.sub(r'[^\w\-_\.]', '_', base_name)  # 清manage file name
                
                # guideout各种 format
                for fmt in formats:
                    try:
                        if fmt == 'markdown':
                            file_content = self.export_to_markdown(content, metadata)
                            zip_file.writestr(f"{base_name}.md", file_content.encode('utf-8'))
                            
                        elif fmt == 'html':
                            file_content = self.export_to_html(content, metadata)
                            zip_file.writestr(f"{base_name}.html", file_content.encode('utf-8'))
                            
                        elif fmt == 'docx' and DOCX_AVAILABLE:
                            file_content = self.export_to_docx(content, metadata)
                            zip_file.writestr(f"{base_name}.docx", file_content)
                            
                        elif fmt == 'pdf' and PDF_AVAILABLE:
                            file_content = self.export_to_pdf(content, metadata)
                            zip_file.writestr(f"{base_name}.pdf", file_content)
                            
                    except Exception as e:
                        logger.warning(f"⚠️ format {fmt} guideout failure: {e}")
                        # in ZIP 中adderror informationtextitem
                        error_msg = f"format {fmt} guideout failure:\n{str(e)}\n\npleasecheck相关dependency是nocorrect确安装。"
                        zip_file.writestr(f"ERROR_{fmt}.txt", error_msg.encode('utf-8'))
                
                # add description file
                readme_content = f"""# VibeDoc guideout file package

## 📋 file description
this 压缩package include 您 Development Plan 多种 format guideout：

### 📄 support format ：
- **Markdown (.md)**: original始 format ， support all have Markdown 语法
- **HTML (.html)**: 网页 format ， include 样式 and Mermaid diagram tablesupport
- **Word (.docx)**: Microsoft Word documentation format
- **PDF (.pdf)**: convenient携式 documentation format

### 🤖 generate information ：
- generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- generate tool: VibeDoc AI Agent v1.0
- project address: https://github.com/JasonRobertDestiny/VibeDocs

### 💡 use recommendation ：
1. excellentfirst use HTML formatcheck看，support最佳的view觉效result
2. use Markdown format进行进一步edit
3. use Word format进行correct式text档process
4. use PDF format进行divide享和hit印

---
感谢 use VibeDoc AI Agent！
"""
                zip_file.writestr("README.md", readme_content.encode('utf-8'))
            
            zip_buffer.seek(0)
            logger.info(f"✅ 多 format guideout success ， include {len(formats)} 种format")
            return zip_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ 多 format guideout failure: {e}")
            raise
    
    def _clean_markdown_content(self, content: str) -> str:
        """清manage and optimize Markdown content"""
        # fix 常见 format issue
        content = re.sub(r'\n{3,}', '\n\n', content)  # remove 多余空行
        content = re.sub(r'(?m)^[ \t]+$', '', content)  # remove 只 have 空format行
        content = content.strip()
        
        return content
    
    def _get_html_styles(self) -> str:
        """get HTML 样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8fafc;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 8px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        
        .document-header {
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .document-header h1 {
            color: #667eea;
            font-size: 2.2em;
            margin-bottom: 15px;
        }
        
        .meta-info {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            color: #666;
            font-size: 0.9em;
        }
        
        .content h1, .content h2, .content h3, .content h4 {
            color: #2d3748;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        
        .content h1 { border-bottom: 2px solid #667eea; padding-bottom: 0.5em; }
        .content h2 { border-bottom: 1px solid #e2e8f0; padding-bottom: 0.3em; }
        
        .content p {
            margin-bottom: 1em;
            text-align: justify;
        }
        
        .content ul, .content ol {
            margin-bottom: 1em;
            padding-left: 2em;
        }
        
        .content li {
            margin-bottom: 0.5em;
        }
        
        .content pre {
            background: #2d3748;
            color: #e2e8f0;
            padding: 1em;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1em 0;
        }
        
        .content code {
            background: #f7fafc;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, monospace;
        }
        
        .content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
        }
        
        .content th, .content td {
            border: 1px solid #e2e8f0;
            padding: 0.75em;
            text-align: left;
        }
        
        .content th {
            background: #f7fafc;
            font-weight: 600;
        }
        
        .content blockquote {
            border-left: 4px solid #667eea;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
            font-style: italic;
        }
        
        .mermaid {
            text-align: center;
            margin: 2em 0;
        }
        
        .document-footer {
            margin-top: 3em;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                padding: 15px;
            }
            
            .meta-info {
                flex-direction: column;
                gap: 10px;
            }
        }
        """
    
    def _parse_markdown_to_docx(self, doc: "Document", content: str):
        """parse Markdown content并addto Word text档"""
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
                
            # title process
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title_text = line.lstrip('#').strip()
                if level <= 6:
                    doc.add_heading(title_text, level)
                    continue
            
            # code 块 process （ simplify ）
            if line.startswith('```'):
                continue
                
            # list process
            if line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                para = doc.add_paragraph(text, style='List Bullet')
                continue
                
            if re.match(r'^\d+\.', line):
                text = re.sub(r'^\d+\.\s*', '', line)
                para = doc.add_paragraph(text, style='List Number')
                continue
            
            # 普通 paragraph
            if line:
                # simple 粗body and 斜body process
                line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # remove 粗bodymark，Word 中后续canwith手动set置
                line = re.sub(r'\*(.*?)\*', r'\1', line)      # remove 斜bodymark
                doc.add_paragraph(line)
    
    def _export_pdf_reportlab(self, content: str, metadata: Optional[Dict] = None) -> bytes:
        """use ReportLab guideout PDF"""
        try:
            buffer = io.BytesIO()
            
            # create PDF text档
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                topMargin=1*inch,
                bottomMargin=1*inch,
                leftMargin=1*inch,
                rightMargin=1*inch
            )
            
            # 样式 setting
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=20,
                spaceAfter=30,
                alignment=1  # 居 in
            )
            
            # construct建 content
            story = []
            
            # add title
            title = metadata.get('title', 'VibeDoc Development Plan') if metadata else 'VibeDoc Development Plan'
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # add meta information
            meta_text = f"""
            work者: {metadata.get('author', 'VibeDoc AI Agent') if metadata else 'VibeDoc AI Agent'}<br/>
            generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            generate tool: VibeDoc AI Agent
            """
            story.append(Paragraph(meta_text, styles['Normal']))
            story.append(Spacer(1, 30))
            
            # simple process Markdown content（基础版本）
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 12))
                    continue
                    
                if line.startswith('#'):
                    # title
                    level = len(line) - len(line.lstrip('#'))
                    title_text = line.lstrip('#').strip()
                    if level == 1:
                        story.append(Paragraph(title_text, styles['Heading1']))
                    elif level == 2:
                        story.append(Paragraph(title_text, styles['Heading2']))
                    else:
                        story.append(Paragraph(title_text, styles['Heading3']))
                else:
                    # 普通 paragraph
                    story.append(Paragraph(line, styles['Normal']))
                    
                story.append(Spacer(1, 6))
            
            # generate PDF
            doc.build(story)
            buffer.seek(0)
            
            logger.info("✅ PDF guideout success （ReportLab）")
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ ReportLab PDF guideout failure: {e}")
            raise

# 全局guideout管managedevice example
export_manager = ExportManager()