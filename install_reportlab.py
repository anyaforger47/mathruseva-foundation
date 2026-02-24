import subprocess
import sys

def check_and_install_reportlab():
    try:
        import reportlab
        print("✅ ReportLab is already installed")
        return True
    except ImportError:
        print("❌ ReportLab not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
            print("✅ ReportLab installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install ReportLab: {e}")
            return False

if __name__ == "__main__":
    check_and_install_reportlab()
