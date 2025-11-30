"""
Report generation service
Exports analysis results as PDF, JSON, or Markdown
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import json
import os
from datetime import datetime
from typing import Dict
import markdown

def generate_pdf_report(media_data: Dict, analysis: Dict, chat_history: list, output_path: str) -> str:
    """
    Generate a PDF report of media analysis
    
    Args:
        media_data: Media metadata
        analysis: Analysis results
        chat_history: Conversation history
        output_path: Where to save PDF
    
    Returns:
        Path to generated PDF
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6A4AFF'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#8A5AFF'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Title
    story.append(Paragraph("Multi-Modal AI Analysis Report", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Metadata Section
    story.append(Paragraph("Media Information", heading_style))
    
    metadata_data = [
        ["Filename:", media_data.get('filename', 'N/A')],
        ["Type:", media_data.get('media_type', 'N/A')],
        ["Size:", f"{media_data.get('size_bytes', 0) / 1024 / 1024:.2f} MB"],
        ["Uploaded:", media_data.get('uploaded_at', 'N/A')[:19]],
    ]
    
    if media_data.get('duration'):
        metadata_data.append(["Duration:", f"{media_data['duration']:.1f} seconds"])
    
    if media_data.get('width') and media_data.get('height'):
        metadata_data.append(["Dimensions:", f"{media_data['width']} × {media_data['height']}"])
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Analysis Results
    story.append(Paragraph("Analysis Results", heading_style))
    
    if analysis.get('caption'):
        story.append(Paragraph(f"<b>Caption:</b> {analysis['caption']}", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
    
    if analysis.get('transcript'):
        story.append(Paragraph("<b>Transcript:</b>", styles['Normal']))
        # Truncate if too long
        transcript = analysis['transcript']
        if len(transcript) > 1000:
            transcript = transcript[:1000] + "... (truncated)"
        story.append(Paragraph(transcript, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
    
    if analysis.get('sentiment'):
        sent = analysis['sentiment']
        story.append(Paragraph(
            f"<b>Sentiment:</b> {sent.get('label', 'N/A')} "
            f"(Confidence: {sent.get('score', 0) * 100:.1f}%)",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.1 * inch))
    
    if analysis.get('language'):
        story.append(Paragraph(f"<b>Language:</b> {analysis['language']}", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
    
    if analysis.get('object_detection'):
        obj_detect = analysis['object_detection']
        story.append(Paragraph(
            f"<b>Objects Detected:</b> {obj_detect.get('total_objects', 0)} objects",
            styles['Normal']
        ))
        
        if obj_detect.get('object_counts'):
            counts_text = ", ".join([f"{k}: {v}" for k, v in obj_detect['object_counts'].items()])
            story.append(Paragraph(counts_text, styles['Normal']))
        
        story.append(Spacer(1, 0.1 * inch))
    
    if analysis.get('visual_summary'):
        story.append(Paragraph(f"<b>Visual Summary:</b> {analysis['visual_summary']}", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
    
    # Chat History (if available)
    if chat_history and len(chat_history) > 0:
        story.append(PageBreak())
        story.append(Paragraph("Conversation History", heading_style))
        
        for msg in chat_history[:20]:  # Limit to 20 messages
            role = msg.get('role', 'user')
            message = msg.get('message', '')
            
            role_label = "👤 You:" if role == 'user' else "🤖 Assistant:"
            story.append(Paragraph(f"<b>{role_label}</b>", styles['Normal']))
            story.append(Paragraph(message, styles['Normal']))
            story.append(Spacer(1, 0.15 * inch))
    
    # Footer
    story.append(Spacer(1, 0.5 * inch))
    footer_text = f"Generated by Multi-Modal AI Inspector on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    return output_path

def generate_json_report(media_data: Dict, analysis: Dict, chat_history: list) -> str:
    """
    Generate JSON export of all data
    
    Returns:
        JSON string
    """
    report = {
        "generated_at": datetime.now().isoformat(),
        "media": media_data,
        "analysis": analysis,
        "chat_history": chat_history,
        "version": "1.0"
    }
    
    return json.dumps(report, indent=2, ensure_ascii=False)

def generate_markdown_report(media_data: Dict, analysis: Dict, chat_history: list) -> str:
    """
    Generate Markdown report
    
    Returns:
        Markdown string
    """
    md_lines = [
        "# Multi-Modal AI Analysis Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Media Information",
        "",
        f"- **Filename:** {media_data.get('filename', 'N/A')}",
        f"- **Type:** {media_data.get('media_type', 'N/A')}",
        f"- **Size:** {media_data.get('size_bytes', 0) / 1024 / 1024:.2f} MB",
        f"- **Uploaded:** {media_data.get('uploaded_at', 'N/A')[:19]}",
    ]
    
    if media_data.get('duration'):
        md_lines.append(f"- **Duration:** {media_data['duration']:.1f} seconds")
    
    if media_data.get('width') and media_data.get('height'):
        md_lines.append(f"- **Dimensions:** {media_data['width']} × {media_data['height']}")
    
    md_lines.extend(["", "## Analysis Results", ""])
    
    if analysis.get('caption'):
        md_lines.append(f"**Caption:** {analysis['caption']}")
        md_lines.append("")
    
    if analysis.get('transcript'):
        md_lines.append("**Transcript:**")
        md_lines.append("")
        md_lines.append(analysis['transcript'])
        md_lines.append("")
    
    if analysis.get('sentiment'):
        sent = analysis['sentiment']
        md_lines.append(f"**Sentiment:** {sent.get('label', 'N/A')} (Confidence: {sent.get('score', 0) * 100:.1f}%)")
        md_lines.append("")
    
    if analysis.get('language'):
        md_lines.append(f"**Language:** {analysis['language']}")
        md_lines.append("")
    
    if analysis.get('object_detection'):
        obj_detect = analysis['object_detection']
        md_lines.append(f"**Objects Detected:** {obj_detect.get('total_objects', 0)}")
        md_lines.append("")
        
        if obj_detect.get('object_counts'):
            md_lines.append("Object counts:")
            for obj, count in obj_detect['object_counts'].items():
                md_lines.append(f"- {obj}: {count}")
            md_lines.append("")
    
    if analysis.get('visual_summary'):
        md_lines.append(f"**Visual Summary:** {analysis['visual_summary']}")
        md_lines.append("")
    
    if chat_history and len(chat_history) > 0:
        md_lines.extend(["## Conversation History", ""])
        
        for msg in chat_history:
            role = msg.get('role', 'user')
            message = msg.get('message', '')
            
            if role == 'user':
                md_lines.append(f"### 👤 You")
            else:
                md_lines.append(f"### 🤖 Assistant")
            
            md_lines.append("")
            md_lines.append(message)
            md_lines.append("")
    
    md_lines.append("---")
    md_lines.append("*Generated by Multi-Modal AI Inspector*")
    
    return "\n".join(md_lines)
