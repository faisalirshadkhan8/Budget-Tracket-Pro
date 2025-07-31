#!/usr/bin/env python3
"""
Modern GUI Test Script
Test the new professional, production-ready interface
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_modern_gui():
    """Test the modern GUI interface"""
    print("🎨 Testing Modern Budget Tracker GUI")
    print("=" * 50)
    
    try:
        # Test import
        print("Testing import...")
        from modern_gui_app import ModernBudgetTrackerGUI
        print("✅ Modern GUI module imported successfully")
        
        # Test GUI launch
        print("\nLaunching Modern GUI...")
        print("🚀 Modern interface should open in a new window")
        print("\n✨ Features to test in the Modern GUI:")
        print("   • Professional dashboard layout")
        print("   • Modern color scheme and typography")
        print("   • Card-based interface design")
        print("   • Enhanced data visualization")
        print("   • Responsive and professional styling")
        print("   • Modern input forms and buttons")
        print("   • Professional charts and analytics")
        print("   • Dark/light theme toggle")
        
        # Launch GUI
        import tkinter as tk
        root = tk.Tk()
        app = ModernBudgetTrackerGUI(root)
        
        print("\n📋 Test Checklist:")
        print("   □ Interface looks professional and modern")
        print("   □ Color scheme is appealing and consistent")
        print("   □ Cards and sections are well-organized")
        print("   □ Buttons and inputs have modern styling")
        print("   □ Charts look professional")
        print("   □ Theme toggle works smoothly")
        print("   □ All functionality from original GUI works")
        print("   □ Interface is production-ready")
        
        print("\n🎯 Running Modern GUI...")
        print("Close the window to end the test.")
        
        root.mainloop()
        
        print("\n✅ Modern GUI test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("   • tkinter")
        print("   • matplotlib")
        print("   • tkcalendar")
        print("   • numpy")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        print("Check the error message above for details.")

def test_launcher():
    """Test the GUI launcher"""
    print("\n🚀 Testing GUI Launcher")
    print("=" * 30)
    
    try:
        print("Launching GUI selector...")
        print("Choose between Original and Modern interfaces")
        
        # Launch launcher
        import tkinter as tk
        root = tk.Tk()
        
        # Import launcher
        sys.path.insert(0, os.path.dirname(__file__))
        from launcher import GUILauncher
        
        launcher = GUILauncher(root)
        root.mainloop()
        
        print("✅ Launcher test completed!")
        
    except Exception as e:
        print(f"❌ Launcher error: {e}")

if __name__ == "__main__":
    print("🎨 Budget Tracker - Modern GUI Testing")
    print("=" * 60)
    
    choice = input("\nChoose test option:\n1. Test Modern GUI directly\n2. Test GUI Launcher\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_modern_gui()
    elif choice == "2":
        test_launcher()
    else:
        print("Invalid choice. Testing Modern GUI directly...")
        test_modern_gui()
    
    print("\n🎉 Testing complete!")
    print("=" * 60)
