"""
Certificate Generator for Seva Connect
Generates membership certificates with member details
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

class CertificateGenerator:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.setup_database()
        
    def setup_database(self):
        """Setup database connection"""
        try:
            self.db = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'seva_connect')
            )
            self.cursor = self.db.cursor(dictionary=True)
        except Exception as e:
            print(f"Database connection error: {e}")
            sys.exit(1)
    
    def create_certificate(self, member_id, theme='light'):
        """Generate certificate for a member"""
        try:
            # Get member details
            member = self.get_member_details(member_id)
            if not member:
                return None
                
            # Create certificate image
            if theme == 'dark':
                bg_color = '#1a1a2e'
                text_color = '#ffffff'
                accent_color = '#6366f1'
            else:
                bg_color = '#ffffff'
                text_color = '#1a1a2e'
                accent_color = '#6366f1'
            
            # Create image
            img = Image.new('RGB', (self.width, self.height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Draw certificate content
            self.draw_certificate_content(draw, member, text_color, accent_color, theme)
            
            # Save certificate
            certificate_path = self.save_certificate(img, member_id, theme)
            
            # Update database with certificate path
            self.update_member_certificate(member_id, certificate_path, theme)
            
            return certificate_path
            
        except Exception as e:
            print(f"Error creating certificate: {e}")
            return None
    
    def get_member_details(self, member_id):
        """Get member details from database"""
        query = "SELECT * FROM members WHERE id = %s"
        self.cursor.execute(query, (member_id,))
        return self.cursor.fetchone()
    
    def draw_certificate_content(self, draw, member, text_color, accent_color, theme):
        """Draw certificate content on image"""
        try:
            # Load fonts
            title_font = self.get_font(48)
            subtitle_font = self.get_font(24)
            name_font = self.get_font(36)
            text_font = self.get_font(18)
            
            # Draw border
            border_width = 10
            draw.rectangle([border_width, border_width, self.width-border_width, self.height-border_width], 
                          outline=accent_color, width=border_width)
            
            # Draw inner border
            inner_border = 30
            draw.rectangle([inner_border, inner_border, self.width-inner_border, self.height-inner_border], 
                          outline=accent_color, width=2)
            
            # Title
            title = "CERTIFICATE OF MEMBERSHIP"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (self.width - title_width) // 2
            draw.text((title_x, 80), title, fill=accent_color, font=title_font)
            
            # Subtitle
            subtitle = "SEVA CONNECT"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (self.width - subtitle_width) // 2
            draw.text((subtitle_x, 140), subtitle, fill=text_color, font=subtitle_font)
            
            # Certificate text
            cert_text = "This is to certify that"
            cert_bbox = draw.textbbox((0, 0), cert_text, font=text_font)
            cert_width = cert_bbox[2] - cert_bbox[0]
            cert_x = (self.width - cert_width) // 2
            draw.text((cert_x, 220), cert_text, fill=text_color, font=text_font)
            
            # Member name
            name = member['name'].upper()
            name_bbox = draw.textbbox((0, 0), name, font=name_font)
            name_width = name_bbox[2] - name_bbox[0]
            name_x = (self.width - name_width) // 2
            draw.text((name_x, 280), name, fill=accent_color, font=name_font)
            
            # Draw underline for name
            underline_y = 330
            underline_start_x = name_x - 20
            underline_end_x = name_x + name_width + 20
            draw.line([underline_start_x, underline_y, underline_end_x, underline_y], 
                     fill=accent_color, width=3)
            
            # Membership text
            membership_text = "is a valued member of Seva Connect"
            membership_bbox = draw.textbbox((0, 0), membership_text, font=text_font)
            membership_width = membership_bbox[2] - membership_bbox[0]
            membership_x = (self.width - membership_width) // 2
            draw.text((membership_x, 370), membership_text, fill=text_color, font=text_font)
            
            # Description
            description = "committed to serving humanity through compassionate giving"
            desc_bbox = draw.textbbox((0, 0), description, font=text_font)
            desc_width = desc_bbox[2] - desc_bbox[0]
            desc_x = (self.width - desc_width) // 2
            draw.text((desc_x, 410), description, fill=text_color, font=text_font)
            
            # Membership details
            membership_id = f"Membership ID: {member['membership_id']}"
            join_date = f"Member Since: {member['created_at'].strftime('%B %d, %Y')}"
            
            # Left side - Membership ID
            draw.text((100, 550), membership_id, fill=text_color, font=text_font)
            
            # Right side - Join date
            date_bbox = draw.textbbox((0, 0), join_date, font=text_font)
            date_width = date_bbox[2] - date_bbox[0]
            date_x = self.width - 100 - date_width
            draw.text((date_x, 550), join_date, fill=text_color, font=text_font)
            
            # Issue date
            issue_date = f"Certificate Issued: {datetime.now().strftime('%B %d, %Y')}"
            issue_bbox = draw.textbbox((0, 0), issue_date, font=text_font)
            issue_width = issue_bbox[2] - issue_bbox[0]
            issue_x = (self.width - issue_width) // 2
            draw.text((issue_x, 650), issue_date, fill=text_color, font=text_font)
            
            # Signature line
            signature_text = "Authorized Signature"
            sig_bbox = draw.textbbox((0, 0), signature_text, font=text_font)
            sig_width = sig_bbox[2] - sig_bbox[0]
            sig_x = self.width - 150 - sig_width
            draw.text((sig_x, 720), signature_text, fill=text_color, font=text_font)
            
            # Signature line
            line_y = 715
            line_start_x = sig_x - 20
            line_end_x = sig_x + sig_width + 20
            draw.line([line_start_x, line_y, line_end_x, line_y], fill=text_color, width=2)
            
        except Exception as e:
            print(f"Error drawing certificate content: {e}")
    
    def get_font(self, size):
        """Get font with fallback"""
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            try:
                return ImageFont.truetype("/Windows/Fonts/arial.ttf", size)
            except:
                return ImageFont.load_default()
    
    def save_certificate(self, img, member_id, theme):
        """Save certificate image"""
        # Create certificates directory if it doesn't exist
        cert_dir = os.path.join(os.path.dirname(__file__), '..', 'certificates')
        os.makedirs(cert_dir, exist_ok=True)
        
        # Generate filename
        filename = f"certificate_{member_id}_{theme}.png"
        filepath = os.path.join(cert_dir, filename)
        
        # Save image
        img.save(filepath, 'PNG', quality=95)
        
        return filepath
    
    def update_member_certificate(self, member_id, certificate_path, theme):
        """Update member record with certificate path"""
        if theme == 'dark':
            column = 'certificate_dark_path'
        else:
            column = 'certificate_light_path'
            
        query = f"UPDATE members SET {column} = %s WHERE id = %s"
        self.cursor.execute(query, (certificate_path, member_id))
        self.db.commit()
    
    def get_certificate_base64(self, certificate_path):
        """Convert certificate to base64 for web display"""
        try:
            with open(certificate_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error converting to base64: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'db'):
            self.db.close()

def generate_member_certificate(member_id, theme='light'):
    """Main function to generate certificate"""
    generator = CertificateGenerator()
    try:
        certificate_path = generator.create_certificate(member_id, theme)
        return certificate_path
    finally:
        generator.close_connection()

if __name__ == "__main__":
    # Test certificate generation
    if len(sys.argv) > 1:
        member_id = sys.argv[1]
        theme = sys.argv[2] if len(sys.argv) > 2 else 'light'
        
        certificate_path = generate_member_certificate(member_id, theme)
        if certificate_path:
            print(f"Certificate generated: {certificate_path}")
        else:
            print("Failed to generate certificate")
    else:
        print("Usage: python certificate_generator.py <member_id> [theme]")
