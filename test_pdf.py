import subprocess
import sys

def test_pdf_generation():
    try:
        result = subprocess.run([sys.executable, "-c", 
            "from app import app; print('Testing PDF generation import...')"], 
            capture_output=True, text=True, cwd="C:\\Users\\nehaj\\CascadeProjects\\mathruseva_foundation")
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        print("Return code:", result.returncode)
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_pdf_generation()
