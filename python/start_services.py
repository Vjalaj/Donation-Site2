#!/usr/bin/env python3
"""
Startup script for all Seva Connect Python services
"""

import os
import sys
import subprocess
import time
import signal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Service configurations
SERVICES = [
    {
        'name': 'Certificate API',
        'file': 'certificate_api.py',
        'port': 5002,
        'description': 'Certificate generation and download service'
    },
    {
        'name': 'Razorpay Backend',
        'file': 'razorpay_backend.py',
        'port': 5000,
        'description': 'Payment processing service'
    },
    {
        'name': 'OAuth Backend',
        'file': 'oauth_backend.py',
        'port': 5001,
        'description': 'Google/Microsoft authentication service'
    }
]

class ServiceManager:
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def start_service(self, service):
        """Start a single service"""
        try:
            print(f"Starting {service['name']} on port {service['port']}...")
            
            process = subprocess.Popen([
                sys.executable, service['file']
            ], cwd=os.path.dirname(__file__))
            
            self.processes[service['name']] = process
            print(f"✓ {service['name']} started (PID: {process.pid})")
            
        except Exception as e:
            print(f"✗ Failed to start {service['name']}: {e}")
    
    def start_all_services(self):
        """Start all services"""
        print("🚀 Starting Seva Connect Python Services...\n")
        
        # Check if required packages are installed
        self.check_dependencies()
        
        # Start all services
        for service in SERVICES:
            self.start_service(service)
            time.sleep(2)  # Wait between starts
        
        self.running = True
        print(f"\n✅ All services started successfully!")
        print("\nService URLs:")
        for service in SERVICES:
            print(f"  • {service['name']}: http://localhost:{service['port']}")
        
        print(f"\nPress Ctrl+C to stop all services...")
        
        # Keep the script running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all_services()
    
    def stop_all_services(self):
        """Stop all services"""
        print(f"\n🛑 Stopping all services...")
        
        for name, process in self.processes.items():
            try:
                print(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✓ {name} stopped")
            except subprocess.TimeoutExpired:
                print(f"Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"Error stopping {name}: {e}")
        
        self.running = False
        print("✅ All services stopped")
    
    def check_dependencies(self):
        """Check if required Python packages are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            'flask', 'flask_cors', 'PIL', 'mysql.connector', 
            'python-dotenv', 'razorpay', 'jwt', 'msal'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'PIL':
                    import PIL
                elif package == 'mysql.connector':
                    import mysql.connector
                elif package == 'python-dotenv':
                    import dotenv
                elif package == 'flask_cors':
                    import flask_cors
                else:
                    __import__(package)
                    
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print(f"💡 Install them with: pip install {' '.join(missing_packages)}")
            print(f"   Or run: pip install -r requirements.txt")
            sys.exit(1)
        else:
            print("✅ All dependencies installed")
    
    def status(self):
        """Check status of all services"""
        print("📊 Service Status:")
        
        for service in SERVICES:
            try:
                import requests
                response = requests.get(f"http://localhost:{service['port']}/health", timeout=2)
                if response.status_code == 200:
                    print(f"  ✅ {service['name']} - Running")
                else:
                    print(f"  ❌ {service['name']} - Not responding")
            except:
                print(f"  ❌ {service['name']} - Offline")

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        manager = ServiceManager()
        
        if command == 'start':
            manager.start_all_services()
        elif command == 'status':
            manager.status()
        elif command == 'install':
            print("📦 Installing Python dependencies...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed")
        else:
            print("❓ Unknown command. Use: start, status, or install")
    else:
        # Default to start
        manager = ServiceManager()
        manager.start_all_services()

if __name__ == '__main__':
    print("🌟 Seva Connect Python Services Manager")
    print("=" * 50)
    main()
