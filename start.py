#!/usr/bin/env python3
"""
Plant Catalogue Launcher
Starts both frontend and backend servers and opens the browser.
Cross-platform (Windows, macOS, Linux)
"""

import subprocess
import webbrowser
import time
import sys
import os
import signal
from pathlib import Path

# Configuration
FRONTEND_PORT = 8000
BACKEND_PORT = 8001
FRONTEND_URL = f"http://localhost:{FRONTEND_PORT}"

# Store process references for cleanup
processes = []

def cleanup(signum=None, frame=None):
    """Clean up processes on exit"""
    print("\n🛑 Shutting down servers...")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except:
            proc.kill()
    print("✅ Servers stopped")
    sys.exit(0)

# Register cleanup handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🌱 Starting Plant Catalogue...")
    print("=" * 50)
    
    # Determine Python executable
    if sys.platform == "win32":
        python_exe = "venv\\Scripts\\python.exe"
    else:
        python_exe = "./venv/bin/python3"
    
    # Check if venv exists
    if not Path(python_exe).exists():
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv")
        print("Then: pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        # Start Backend (FastAPI)
        print(f"🔧 Starting backend on port {BACKEND_PORT}...")
        backend_proc = subprocess.Popen(
            [python_exe, "-m", "backend.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processes.append(backend_proc)
        
        # Start Frontend (HTTP Server)
        print(f"🌐 Starting frontend on port {FRONTEND_PORT}...")
        frontend_proc = subprocess.Popen(
            [python_exe, "-m", "http.server", str(FRONTEND_PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processes.append(frontend_proc)
        
        # Wait for servers to start
        print("⏳ Waiting for servers to initialize...")
        time.sleep(3)
        
        # Check if processes are still running
        if backend_proc.poll() is not None:
            print("❌ Backend failed to start!")
            cleanup()
        
        if frontend_proc.poll() is not None:
            print("❌ Frontend failed to start!")
            cleanup()
        
        # Open browser
        print(f"🚀 Opening browser at {FRONTEND_URL}")
        webbrowser.open(FRONTEND_URL)
        
        print("=" * 50)
        print("✅ Plant Catalogue is running!")
        print(f"   Frontend: {FRONTEND_URL}")
        print(f"   Backend:  http://localhost:{BACKEND_PORT}")
        print("\nPress Ctrl+C to stop")
        print("=" * 50)
        
        # Keep script running
        try:
            while True:
                time.sleep(1)
                # Check if processes died
                if backend_proc.poll() is not None or frontend_proc.poll() is not None:
                    print("\n⚠️  A server process stopped unexpectedly")
                    cleanup()
        except KeyboardInterrupt:
            cleanup()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        cleanup()

if __name__ == "__main__":
    main()
