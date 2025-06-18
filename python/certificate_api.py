"""
Certificate API for Seva Connect
Provides endpoints for certificate generation and download
"""

import os
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
from certificate_generator import CertificateGenerator
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'seva_connect')
    )

@app.route('/generate-certificate', methods=['POST'])
def generate_certificate():
    """Generate certificate for a member"""
    try:
        data = request.get_json()
        member_id = data.get('member_id')
        theme = data.get('theme', 'light')
        
        if not member_id:
            return jsonify({'success': False, 'message': 'Member ID is required'}), 400
        
        # Verify member exists
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM members WHERE id = %s", (member_id,))
        member = cursor.fetchone()
        cursor.close()
        db.close()
        
        if not member:
            return jsonify({'success': False, 'message': 'Member not found'}), 404
        
        # Generate certificate
        generator = CertificateGenerator()
        try:
            certificate_path = generator.create_certificate(member_id, theme)
            
            if certificate_path:
                # Convert to base64 for preview
                cert_base64 = generator.get_certificate_base64(certificate_path)
                
                return jsonify({
                    'success': True,
                    'message': 'Certificate generated successfully',
                    'certificate_path': certificate_path,
                    'certificate_base64': cert_base64,
                    'download_url': f'/download-certificate/{member_id}?theme={theme}'
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to generate certificate'}), 500
                
        finally:
            generator.close_connection()
        
    except Exception as e:
        print(f"Certificate generation error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download-certificate/<int:member_id>', methods=['GET'])
def download_certificate(member_id):
    """Download certificate file"""
    try:
        theme = request.args.get('theme', 'light')
        
        # Get certificate path from database
        db = get_db_connection()
        cursor = db.cursor()
        
        if theme == 'dark':
            cursor.execute("SELECT certificate_dark_path, name FROM members WHERE id = %s", (member_id,))
        else:
            cursor.execute("SELECT certificate_light_path, name FROM members WHERE id = %s", (member_id,))
        
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        if not result or not result[0]:
            return jsonify({'success': False, 'message': 'Certificate not found'}), 404
        
        certificate_path = result[0]
        member_name = result[1]
        
        # Check if file exists
        if not os.path.exists(certificate_path):
            return jsonify({'success': False, 'message': 'Certificate file not found'}), 404
        
        # Generate filename for download
        safe_name = "".join(c for c in member_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"Certificate_{safe_name}_{theme}.png"
        
        return send_file(
            certificate_path,
            as_attachment=True,
            download_name=filename,
            mimetype='image/png'
        )
        
    except Exception as e:
        print(f"Certificate download error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/certificate-preview/<int:member_id>', methods=['GET'])
def certificate_preview(member_id):
    """Get certificate as base64 for preview"""
    try:
        theme = request.args.get('theme', 'light')
        
        # Get certificate path from database
        db = get_db_connection()
        cursor = db.cursor()
        
        if theme == 'dark':
            cursor.execute("SELECT certificate_dark_path FROM members WHERE id = %s", (member_id,))
        else:
            cursor.execute("SELECT certificate_light_path FROM members WHERE id = %s", (member_id,))
        
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        if not result or not result[0]:
            # Generate certificate if it doesn't exist
            generator = CertificateGenerator()
            try:
                certificate_path = generator.create_certificate(member_id, theme)
                if not certificate_path:
                    return jsonify({'success': False, 'message': 'Failed to generate certificate'}), 500
            finally:
                generator.close_connection()
        else:
            certificate_path = result[0]
        
        # Convert to base64
        generator = CertificateGenerator()
        try:
            cert_base64 = generator.get_certificate_base64(certificate_path)
            
            if cert_base64:
                return jsonify({
                    'success': True,
                    'certificate_base64': cert_base64
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to convert certificate'}), 500
                
        finally:
            generator.close_connection()
        
    except Exception as e:
        print(f"Certificate preview error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/bulk-generate-certificates', methods=['POST'])
def bulk_generate_certificates():
    """Generate certificates for multiple members"""
    try:
        data = request.get_json()
        member_ids = data.get('member_ids', [])
        theme = data.get('theme', 'light')
        
        if not member_ids:
            return jsonify({'success': False, 'message': 'Member IDs are required'}), 400
        
        results = []
        generator = CertificateGenerator()
        
        try:
            for member_id in member_ids:
                try:
                    certificate_path = generator.create_certificate(member_id, theme)
                    if certificate_path:
                        results.append({
                            'member_id': member_id,
                            'success': True,
                            'certificate_path': certificate_path
                        })
                    else:
                        results.append({
                            'member_id': member_id,
                            'success': False,
                            'error': 'Failed to generate certificate'
                        })
                except Exception as e:
                    results.append({
                        'member_id': member_id,
                        'success': False,
                        'error': str(e)
                    })
            
            successful_count = sum(1 for r in results if r['success'])
            
            return jsonify({
                'success': True,
                'message': f'Generated {successful_count} out of {len(member_ids)} certificates',
                'results': results
            })
            
        finally:
            generator.close_connection()
        
    except Exception as e:
        print(f"Bulk certificate generation error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/certificate-stats', methods=['GET'])
def certificate_stats():
    """Get certificate generation statistics"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Get stats
        stats_query = """
        SELECT 
            COUNT(*) as total_members,
            COUNT(certificate_light_path) as light_certificates,
            COUNT(certificate_dark_path) as dark_certificates
        FROM members
        """
        
        cursor.execute(stats_query)
        stats = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_members': stats[0],
                'light_certificates': stats[1],
                'dark_certificates': stats[2],
                'completion_rate': round((stats[1] / stats[0] * 100) if stats[0] > 0 else 0, 2)
            }
        })
        
    except Exception as e:
        print(f"Certificate stats error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Certificate API is running',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Ensure certificates directory exists
    cert_dir = os.path.join(os.path.dirname(__file__), '..', 'certificates')
    os.makedirs(cert_dir, exist_ok=True)
    
    print("Certificate API starting...")
    print(f"Certificates will be saved to: {cert_dir}")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5002)
