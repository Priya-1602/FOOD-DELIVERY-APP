
"""
Setup script for Restaurant Ordering System
This script helps users set up the application quickly
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "static/uploads",
        "static/css",
        "static/js",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("🔧 Creating .env file...")
        env_content = """# Restaurant Ordering System Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=mysql://root:password@localhost/restaurant_ordering
FLASK_ENV=development
FLASK_DEBUG=1
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please update the .env file with your actual configuration")
    else:
        print("✅ .env file already exists")

def check_database():
    """Check database connection"""
    print("🗄️  Checking database connection...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("⚠️  Please make sure MySQL is running and configured correctly")
        print("⚠️  Update the DATABASE_URL in config.py or .env file")

def run_sample_data():
    """Run sample data initialization"""
    print("📊 Initializing sample data...")
    try:
        subprocess.check_call([sys.executable, "init_data.py"])
        print("✅ Sample data initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing sample data: {e}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your email configuration")
    print("2. Configure your MySQL database connection")
    print("3. Run the application: python app.py")
    print("4. Open your browser and go to: http://localhost:5000")
    print("\n👥 Sample login credentials:")
    print("   Admin: admin@restaurant.com / admin123")
    print("   Restaurant: owner@pizzapalace.com / owner123")
    print("   Customer: john@example.com / customer123")
    print("\n📚 For more information, see README.md")

def main():
    """Main setup function"""
    print("🚀 Restaurant Ordering System Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check database
    check_database()
    
    # Initialize sample data
    run_sample_data()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 