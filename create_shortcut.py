import os
import sys
import win32com.client
import pythoncom

def create_desktop_shortcut():
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path to the batch file
        batch_file = os.path.join(current_dir, 'start.bat')
        
        # Desktop path
        desktop = win32com.client.Dispatch("WScript.Shell").SpecialFolders("Desktop")
        
        # Create shortcut
        shortcut_path = os.path.join(desktop, "Mathruseva Foundation.lnk")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        shortcut.Targetpath = batch_file
        shortcut.WorkingDirectory = current_dir
        shortcut.IconLocation = shell.SpecialFolders("Programs")
        shortcut.Description = "Mathruseva Foundation NGO Management System"
        
        # Try to use a system icon if available
        icon_path = os.path.join(current_dir, 'static', 'favicon.ico')
        if os.path.exists(icon_path):
            shortcut.IconLocation = icon_path
        
        shortcut.save()
        
        print("✅ Desktop shortcut created successfully!")
        print(f"Shortcut location: {shortcut_path}")
        
    except Exception as e:
        print(f"❌ Error creating desktop shortcut: {e}")
        print("You can still run the application by double-clicking 'start.bat'")

if __name__ == "__main__":
    create_desktop_shortcut()
