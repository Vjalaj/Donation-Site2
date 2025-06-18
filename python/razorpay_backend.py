"""
Razorpay Payment Integration for Seva Connect
Handles payment processing for donations and memberships
"""

import os
import razorpay
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import hashlib
import hmac
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Razorpay client
try:
    razorpay_client = razorpay.Client(auth=(
        os.getenv('RAZORPAY_KEY_ID'),
        os.getenv('RAZORPAY_KEY_SECRET')
    ))
except Exception as e:
    print(f"Razorpay initialization error: {e}")
    razorpay_client = None

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'seva_connect')
    )

def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify Razorpay payment signature"""
    try:
        key_secret = os.getenv('RAZORPAY_KEY_SECRET')
        body = razorpay_order_id + "|" + razorpay_payment_id
        
        expected_signature = hmac.new(
            key_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, razorpay_signature)
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False

@app.route('/create-order', methods=['POST'])
def create_order():
    """Create Razorpay order for payment"""
    try:
        if not razorpay_client:
            return jsonify({'success': False, 'message': 'Payment gateway not configured'}), 500
        
        data = request.get_json()
        amount = float(data.get('amount', 0))
        currency = data.get('currency', 'INR')
        payment_type = data.get('type', 'donation')  # donation or membership
        
        # Convert amount to paisa (smallest currency unit)
        amount_in_paisa = int(amount * 100)
        
        # Create order
        order_data = {
            'amount': amount_in_paisa,
            'currency': currency,
            'payment_capture': 1
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        # Store order in database
        db = get_db_connection()
        cursor = db.cursor()
        
        insert_query = """
        INSERT INTO payment_orders (
            razorpay_order_id, amount, currency, payment_type, status, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            order['id'],
            amount,
            currency,
            payment_type,
            'created',
            datetime.now()
        ))
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'amount': amount_in_paisa,
            'currency': currency,
            'key': os.getenv('RAZORPAY_KEY_ID')
        })
        
    except Exception as e:
        print(f"Order creation error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    """Verify payment and update database"""
    try:
        data = request.get_json()
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        # Verify signature
        if not verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
            return jsonify({'success': False, 'message': 'Invalid payment signature'}), 400
        
        # Get payment details from Razorpay
        payment = razorpay_client.payment.fetch(razorpay_payment_id)
        
        # Update database
        db = get_db_connection()
        cursor = db.cursor()
        
        # Update payment order status
        update_order_query = """
        UPDATE payment_orders 
        SET razorpay_payment_id = %s, status = %s, verified_at = %s 
        WHERE razorpay_order_id = %s
        """
        
        cursor.execute(update_order_query, (
            razorpay_payment_id,
            'verified',
            datetime.now(),
            razorpay_order_id
        ))
        
        # Get order details
        order_query = "SELECT * FROM payment_orders WHERE razorpay_order_id = %s"
        cursor.execute(order_query, (razorpay_order_id,))
        order = cursor.fetchone()
        
        if order:
            # Process based on payment type
            if order[4] == 'membership':  # payment_type
                # Update membership payment status
                membership_query = """
                UPDATE members 
                SET payment_status = 'completed', razorpay_payment_id = %s, updated_at = %s
                WHERE razorpay_order_id = %s
                """
                cursor.execute(membership_query, (
                    razorpay_payment_id,
                    datetime.now(),
                    razorpay_order_id
                ))
            else:
                # Update donation payment status
                donation_query = """
                UPDATE donations 
                SET payment_status = 'completed', razorpay_payment_id = %s, updated_at = %s
                WHERE razorpay_order_id = %s
                """
                cursor.execute(donation_query, (
                    razorpay_payment_id,
                    datetime.now(),
                    razorpay_order_id
                ))
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'payment_id': razorpay_payment_id
        })
        
    except Exception as e:
        print(f"Payment verification error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/payment-webhook', methods=['POST'])
def payment_webhook():
    """Handle Razorpay webhooks"""
    try:
        # Verify webhook signature
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        webhook_secret = os.getenv('RAZORPAY_WEBHOOK_SECRET')
        
        if webhook_secret:
            body = request.get_data()
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                body,
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, webhook_signature):
                return jsonify({'success': False, 'message': 'Invalid webhook signature'}), 400
        
        # Process webhook event
        event = request.get_json()
        event_type = event.get('event')
        
        if event_type == 'payment.captured':
            payment_data = event.get('payload', {}).get('payment', {}).get('entity', {})
            # Handle successful payment
            print(f"Payment captured: {payment_data.get('id')}")
            
        elif event_type == 'payment.failed':
            payment_data = event.get('payload', {}).get('payment', {}).get('entity', {})
            # Handle failed payment
            print(f"Payment failed: {payment_data.get('id')}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/refund-payment', methods=['POST'])
def refund_payment():
    """Initiate refund for a payment"""
    try:
        if not razorpay_client:
            return jsonify({'success': False, 'message': 'Payment gateway not configured'}), 500
        
        data = request.get_json()
        payment_id = data.get('payment_id')
        amount = data.get('amount')  # Optional, for partial refunds
        
        refund_data = {'payment_id': payment_id}
        if amount:
            refund_data['amount'] = int(float(amount) * 100)  # Convert to paisa
        
        refund = razorpay_client.payment.refund(payment_id, refund_data)
        
        # Update database
        db = get_db_connection()
        cursor = db.cursor()
        
        # Record refund
        refund_query = """
        INSERT INTO payment_refunds (
            razorpay_refund_id, razorpay_payment_id, amount, status, created_at
        ) VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(refund_query, (
            refund['id'],
            payment_id,
            refund.get('amount', 0) / 100,  # Convert back to rupees
            refund.get('status'),
            datetime.now()
        ))
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True,
            'refund_id': refund['id'],
            'status': refund.get('status')
        })
        
    except Exception as e:
        print(f"Refund error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/payment-status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Get payment status from Razorpay"""
    try:
        if not razorpay_client:
            return jsonify({'success': False, 'message': 'Payment gateway not configured'}), 500
        
        payment = razorpay_client.payment.fetch(payment_id)
        
        return jsonify({
            'success': True,
            'payment': {
                'id': payment['id'],
                'amount': payment['amount'] / 100,  # Convert to rupees
                'currency': payment['currency'],
                'status': payment['status'],
                'method': payment.get('method'),
                'created_at': payment['created_at']
            }
        })
        
    except Exception as e:
        print(f"Payment status error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Create necessary database tables if they don't exist
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Payment orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            razorpay_order_id VARCHAR(255) UNIQUE NOT NULL,
            razorpay_payment_id VARCHAR(255),
            amount DECIMAL(10,2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'INR',
            payment_type ENUM('donation', 'membership') NOT NULL,
            status ENUM('created', 'verified', 'failed') DEFAULT 'created',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified_at TIMESTAMP NULL
        )
        """)
        
        # Payment refunds table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_refunds (
            id INT AUTO_INCREMENT PRIMARY KEY,
            razorpay_refund_id VARCHAR(255) UNIQUE NOT NULL,
            razorpay_payment_id VARCHAR(255) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        db.commit()
        cursor.close()
        db.close()
        
        print("Database tables created successfully")
        
    except Exception as e:
        print(f"Database setup error: {e}")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
