"""
OAuth Authentication for Seva Connect Admin Panel
Supports Google and Microsoft authentication (Free tier)
"""

import os
import jwt
from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import msal
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
CORS(app, supports_credentials=True)

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
MICROSOFT_CLIENT_ID = os.getenv('MICROSOFT_CLIENT_ID')
MICROSOFT_CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET')

REDIRECT_URI = os.getenv('APP_URL', 'http://localhost:8000') + '/auth/callback'

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'seva_connect')
    )

def create_admin_user_from_oauth(email, name, provider):
    """Create admin user from OAuth data"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM admin_users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return existing_user[0]
        
        # Create new admin user
        username = email.split('@')[0]  # Use part before @ as username
        insert_query = """
        INSERT INTO admin_users (username, email, oauth_provider, oauth_id, role, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            username,
            email,
            provider,
            email,  # Using email as oauth_id for simplicity
            'admin',
            'active',
            datetime.now()
        ))
        
        user_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        
        return user_id
        
    except Exception as e:
        print(f"Error creating OAuth user: {e}")
        return None

def generate_jwt_token(user_id, email):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    return jwt.encode(payload, app.secret_key, algorithm='HS256')

@app.route('/auth/google', methods=['GET'])
def google_auth():
    """Initiate Google OAuth flow"""
    try:
        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={GOOGLE_CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}/google&"
            f"scope=openid email profile&"
            f"response_type=code&"
            f"access_type=offline"
        )
        
        return jsonify({
            'success': True,
            'auth_url': google_auth_url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/auth/microsoft', methods=['GET'])
def microsoft_auth():
    """Initiate Microsoft OAuth flow"""
    try:
        msal_app = msal.ConfidentialClientApplication(
            MICROSOFT_CLIENT_ID,
            authority="https://login.microsoftonline.com/common",
            client_credential=MICROSOFT_CLIENT_SECRET
        )
        
        auth_url = msal_app.get_authorization_request_url(
            scopes=["User.Read"],
            redirect_uri=f"{REDIRECT_URI}/microsoft"
        )
        
        return jsonify({
            'success': True,
            'auth_url': auth_url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/auth/callback/google', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({'success': False, 'message': 'No authorization code received'}), 400
        
        # Exchange code for token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': f"{REDIRECT_URI}/google"
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'id_token' not in token_json:
            return jsonify({'success': False, 'message': 'Failed to get ID token'}), 400
        
        # Verify and decode ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                token_json['id_token'], 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            email = idinfo.get('email')
            name = idinfo.get('name')
            
            if not email:
                return jsonify({'success': False, 'message': 'Email not provided by Google'}), 400
            
            # Create or get user
            user_id = create_admin_user_from_oauth(email, name, 'google')
            if not user_id:
                return jsonify({'success': False, 'message': 'Failed to create user'}), 500
            
            # Generate JWT token
            jwt_token = generate_jwt_token(user_id, email)
            
            # Redirect to admin panel with token
            admin_url = f"{os.getenv('ADMIN_URL')}?token={jwt_token}"
            return redirect(admin_url)
            
        except ValueError as e:
            return jsonify({'success': False, 'message': 'Invalid ID token'}), 400
        
    except Exception as e:
        print(f"Google auth error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/auth/callback/microsoft', methods=['GET'])
def microsoft_callback():
    """Handle Microsoft OAuth callback"""
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({'success': False, 'message': 'No authorization code received'}), 400
        
        msal_app = msal.ConfidentialClientApplication(
            MICROSOFT_CLIENT_ID,
            authority="https://login.microsoftonline.com/common",
            client_credential=MICROSOFT_CLIENT_SECRET
        )
        
        # Exchange code for token
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=["User.Read"],
            redirect_uri=f"{REDIRECT_URI}/microsoft"
        )
        
        if "error" in result:
            return jsonify({'success': False, 'message': result.get('error_description')}), 400
        
        # Get user info
        access_token = result.get('access_token')
        user_response = requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        user_data = user_response.json()
        email = user_data.get('mail') or user_data.get('userPrincipalName')
        name = user_data.get('displayName')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email not provided by Microsoft'}), 400
        
        # Create or get user
        user_id = create_admin_user_from_oauth(email, name, 'microsoft')
        if not user_id:
            return jsonify({'success': False, 'message': 'Failed to create user'}), 500
        
        # Generate JWT token
        jwt_token = generate_jwt_token(user_id, email)
        
        # Redirect to admin panel with token
        admin_url = f"{os.getenv('ADMIN_URL')}?token={jwt_token}"
        return redirect(admin_url)
        
    except Exception as e:
        print(f"Microsoft auth error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/auth/verify', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'message': 'No token provided'}), 400
        
        # Decode JWT token
        try:
            payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            email = payload.get('email')
            
            # Verify user exists in database
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("SELECT username, role FROM admin_users WHERE id = %s AND status = 'active'", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user_id,
                    'email': email,
                    'username': user[0],
                    'role': user[1]
                }
            })
            
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Update database schema for OAuth support
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Add OAuth columns to admin_users table if they don't exist
        try:
            cursor.execute("ALTER TABLE admin_users ADD COLUMN oauth_provider VARCHAR(50) NULL")
        except:
            pass  # Column might already exist
            
        try:
            cursor.execute("ALTER TABLE admin_users ADD COLUMN oauth_id VARCHAR(255) NULL")
        except:
            pass  # Column might already exist
            
        # Make password_hash nullable for OAuth users
        try:
            cursor.execute("ALTER TABLE admin_users MODIFY password_hash VARCHAR(255) NULL")
        except:
            pass  # Modification might already be applied
        
        db.commit()
        cursor.close()
        db.close()
        
        print("Database schema updated for OAuth support")
        
    except Exception as e:
        print(f"Database schema update error: {e}")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)
