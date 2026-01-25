from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import mysql.connector
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        # Custom styles for the report
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
    
    def get_database_data(self):
        """Fetch data from database for the report"""
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)
            
            # Get summary statistics
            cursor.execute("SELECT COUNT(*) as total FROM volunteers")
            result = cursor.fetchone()
            total_volunteers = result['total'] if result else 0
            
            cursor.execute("SELECT COUNT(*) as total FROM camps")
            result = cursor.fetchone()
            total_camps = result['total'] if result else 0
            
            cursor.execute("SELECT SUM(total_patients) as total FROM medical_summary")
            result = cursor.fetchone()
            total_beneficiaries = result['total'] or 0
            
            cursor.execute("SELECT SUM(quantity) as total FROM donations")
            result = cursor.fetchone()
            total_donations = result['total'] or 0
            
            # Get camp type distribution
            cursor.execute("SELECT type, COUNT(*) as count FROM camps GROUP BY type")
            camp_types = cursor.fetchall()
            
            # Get recent camps
            cursor.execute("""
                SELECT name, type, location, camp_date, status 
                FROM camps 
                ORDER BY camp_date DESC 
                LIMIT 5
            """)
            recent_camps = cursor.fetchall()
            
            # Get donation summary
            cursor.execute("""
                SELECT donation_type, SUM(quantity) as total_quantity
                FROM donations 
                GROUP BY donation_type
            """)
            donation_summary = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'total_volunteers': total_volunteers,
                'total_camps': total_camps,
                'total_beneficiaries': total_beneficiaries,
                'total_donations': total_donations,
                'camp_types': camp_types if camp_types else [],
                'recent_camps': recent_camps if recent_camps else [],
                'donation_summary': donation_summary if donation_summary else []
            }
            
        except Exception as e:
            print(f"Database error: {e}")
            # Return default data if database fails
            return {
                'total_volunteers': 0,
                'total_camps': 0,
                'total_beneficiaries': 0,
                'total_donations': 0,
                'camp_types': [],
                'recent_camps': [],
                'donation_summary': []
            }
    
    def generate_impact_report(self, output_filename):
        """Generate comprehensive impact report"""
        data = self.get_database_data()
        if not data:
            return False
        
        doc = SimpleDocTemplate(output_filename, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("Mathruseva Foundation - Impact Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report generation date
        date_paragraph = Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal'])
        story.append(date_paragraph)
        story.append(Spacer(1, 30))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        
        summary_data = [
            ['Metric', 'Count'],
            ['Total Volunteers', str(data['total_volunteers'])],
            ['Total Camps Conducted', str(data['total_camps'])],
            ['Total Beneficiaries Served', str(data['total_beneficiaries'])],
            ['Total Items Donated', str(data['total_donations'])]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Camp Type Distribution
        story.append(Paragraph("Camp Type Distribution", self.styles['CustomHeading']))
        
        camp_data = [['Camp Type', 'Number of Camps']]
        if data['camp_types']:
            for camp_type in data['camp_types']:
                camp_data.append([camp_type['type'], str(camp_type['count'])])
        else:
            camp_data.append(['No camps found', '0'])
        
        camp_table = Table(camp_data, colWidths=[3*inch, 2*inch])
        camp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(camp_table)
        story.append(Spacer(1, 30))
        
        # Recent Camps
        story.append(Paragraph("Recent Camps", self.styles['CustomHeading']))
        
        recent_camps_data = [['Camp Name', 'Type', 'Location', 'Date', 'Status']]
        if data['recent_camps']:
            for camp in data['recent_camps']:
                recent_camps_data.append([
                    camp['name'],
                    camp['type'],
                    camp['location'],
                    camp['camp_date'].strftime('%Y-%m-%d') if camp['camp_date'] else 'N/A',
                    camp['status']
                ])
        else:
            recent_camps_data.append(['No camps found', '-', '-', '-', '-'])
        
        recent_table = Table(recent_camps_data, colWidths=[2*inch, 1*inch, 2*inch, 1*inch, 1*inch])
        recent_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(recent_table)
        story.append(Spacer(1, 30))
        
        # Donation Summary
        story.append(Paragraph("Donation Summary", self.styles['CustomHeading']))
        
        donation_data = [['Donation Type', 'Total Quantity']]
        if data['donation_summary']:
            for donation in data['donation_summary']:
                donation_data.append([donation['donation_type'], str(donation['total_quantity'])])
        else:
            donation_data.append(['No donations found', '0'])
        
        donation_table = Table(donation_data, colWidths=[3*inch, 2*inch])
        donation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(donation_table)
        story.append(Spacer(1, 30))
        
        # Footer message
        footer_text1 = Paragraph("This report demonstrates the impact of Mathruseva Foundation's work in underserved communities.", self.styles['Normal'])
        footer_text2 = Paragraph("Together with our dedicated volunteers and generous donors, we continue to make a difference in the lives of those who need it most.", self.styles['Normal'])
        footer_text3 = Paragraph("<b>Thank you for your support!</b>", self.styles['Normal'])
        
        story.append(Spacer(1, 20))
        story.append(footer_text1)
        story.append(Spacer(1, 12))
        story.append(footer_text2)
        story.append(Spacer(1, 20))
        story.append(footer_text3)
        
        # Build PDF
        doc.build(story)
        return True

# Flask route for PDF generation
def generate_pdf_report(mysql_config):
    """Generate PDF report and return file path"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"impact_report_{timestamp}.pdf"
    output_path = os.path.join('reports', filename)
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    generator = PDFReportGenerator(mysql_config)
    success = generator.generate_impact_report(output_path)
    
    if success:
        return output_path
    else:
        return None
