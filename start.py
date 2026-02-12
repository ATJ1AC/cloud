import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "asyncpg",
        "aiosqlite",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "requests"
    ]
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}")

def main():
    # Install requirements
    print("Installing requirements...")
    install_requirements()
    
    # Start the FastAPI application
    print("Starting Sh7omyLab API server...")
    try:
        import uvicorn
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("Could not start server. Please make sure all dependencies are installed.")
        sys.exit(1)

if __name__ == "__main__":
    main()