#!/usr/bin/env python3
"""
Demo startup script for Bedrock Document Agent
Starts the Streamlit interface for testing without AWS credentials
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("="*60)
    print("🤖 AMAZON BEDROCK DOCUMENT AGENT - DEMO MODE")
    print("="*60)
    print("Starting the Streamlit interface...")
    print("This demo runs without AWS credentials for testing the UI.")
    print("="*60)

def start_streamlit():
    """Start Streamlit app"""
    try:
        # Change to project directory
        os.chdir('/home/ec2-user/hackatonaws')
        
        # Start Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_app.py',
            '--server.port=8502',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--browser.gatherUsageStats=false'
        ]
        
        print("🚀 Starting Streamlit on http://localhost:8501")
        print("📝 Note: AWS features will require valid credentials in .env file")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Print output in real-time
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Streamlit server...")
        if 'process' in locals():
            process.terminate()
            process.wait()
        print("✅ Server stopped successfully")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        return False
    
    return True

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit is not installed. Run: pip install streamlit")
        return False
    
    # Check if streamlit_app.py exists
    if not os.path.exists('streamlit_app.py'):
        print("❌ streamlit_app.py not found")
        return False
    else:
        print("✅ streamlit_app.py found")
    
    # Check if config is working
    try:
        sys.path.insert(0, '.')
        from config.settings import Config
        print("✅ Configuration loaded")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    print("✅ All requirements met\n")
    return True

def main():
    """Main function"""
    print_banner()
    
    if not check_requirements():
        print("\n❌ Requirements not met. Please fix the issues above.")
        return False
    
    print("🎯 Starting demo mode...")
    print("💡 To enable full functionality:")
    print("   1. Add your AWS credentials to .env file")
    print("   2. Ensure Bedrock model access is enabled")
    print("   3. Restart the application\n")
    
    return start_streamlit()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
