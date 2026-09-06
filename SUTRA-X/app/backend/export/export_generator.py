
"""
Export Generator - PDF, JSON, CSV
"""

import json
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class ExportGenerator:
    """Generate export reports in multiple formats"""
    
    @staticmethod
    def export_json(G):
        """Export as JSON"""
        from app.backend.graph_engine.graph_builder import (
            get_node_list, get_node_attributes, get_degree, get_edge_data
        )
        
        node_list = get_node_list(G)
        report = {
            'generated_at': datetime.now().isoformat(),
            'version': '3.0.0',
            'network_summary': {
                'total_entities': len(node_list),
                'entity_types': {}
            },
            'entities': [],
            'relationships': []
        }
        
        for node in node_list:
            attrs = get_node_attributes(G, node)
            etype = attrs.get('type', 'UNKNOWN')
            report['network_summary']['entity_types'][etype] = \
                report['network_summary']['entity_types'].get(etype, 0) + 1
            report['entities'].append({
                'id': node,
                'type': etype,
                'attributes': attrs,
                'degree': get_degree(G, node)
            })
        
        for u in node_list:
            for v in get_neighbors(G, u):
                if (u, v) not in [(e['source'], e['target']) for e in report['relationships']]:
                    edge_data = get_edge_data(G, u, v)
                    report['relationships'].append({
                        'source': u,
                        'target': v,
                        'type': edge_data.get('type', 'CONNECTED'),
                        'attributes': edge_data
                    })
        
        return json.dumps(report, indent=2)
    
    @staticmethod
    def export_csv(G):
        """Export as CSV"""
        from app.backend.graph_engine.graph_builder import (
            get_node_list, get_node_attributes, get_degree
        )
        
        node_list = get_node_list(G)
        data = []
        for node in node_list:
            attrs = get_node_attributes(G, node)
            data.append({
                'ID': node,
                'Type': attrs.get('type', 'UNKNOWN'),
                'Degree': get_degree(G, node),
                'Name': attrs.get('name', attrs.get('number', '')),
                **attrs
            })
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    @staticmethod
    def export_pdf(G):
        """Export as PDF (simplified)"""
        from app.backend.graph_engine.graph_builder import get_node_list, get_node_attributes
        
        node_list = get_node_list(G)
        
        # Create PDF
        doc = SimpleDocTemplate(
            "SUTRA-X_Report.pdf",
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        story.append(Paragraph("SUTRA-X Investigation Report", title_style))
        story.append(Spacer(1, 0.25 * inch))
        
        # Date
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.25 * inch))
        
        # Summary
        story.append(Paragraph(f"Total Entities: {len(node_list)}", styles['Normal']))
        story.append(Spacer(1, 0.25 * inch))
        
        # Entity table
        table_data = [['ID', 'Type', 'Name']]
        for node in node_list[:20]:  # Limit to 20
            attrs = get_node_attributes(G, node)
            table_data.append([
                node,
                attrs.get('type', 'UNKNOWN'),
                attrs.get('name', attrs.get('number', ''))
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        
        doc.build(story)
        return "SUTRA-X_Report.pdf"
