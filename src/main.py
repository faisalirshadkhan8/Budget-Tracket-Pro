import argparse
import sys
import os

# Add src directory to Python path
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def main():
    parser = argparse.ArgumentParser(description="Budget Tracker Pro")
    parser.add_argument('--version', action='version', version='Budget Tracker Pro 4.0 - Production Ready')
    parser.add_argument('--gui', action='store_true', help='Launch classic GUI version')
    parser.add_argument('--modern', action='store_true', help='Launch modern GUI version')
    parser.add_argument('--cli', action='store_true', help='Launch CLI version')
    parser.add_argument('--launcher', action='store_true', help='Launch GUI selector')
    
    # Parse known args to handle CLI subcommands
    args, unknown = parser.parse_known_args()
    
    # If no specific mode is chosen, default to launcher
    if not any([args.cli, args.gui, args.modern, args.launcher]):
        args.launcher = True
    
    if args.launcher:
        try:
            # Add parent directory to path to import launcher
            parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_path not in sys.path:
                sys.path.insert(0, parent_path)
            
            from launcher import main as launcher_main
            print("Launching GUI Selector...")
            launcher_main()
        except ImportError as e:
            print(f"Error launching GUI selector: {e}")
            print("Falling back to classic GUI...")
            args.gui = True
    
    if args.gui:
        try:
            from gui_app import main as gui_main
            print("Launching Budget Tracker Classic GUI...")
            gui_main()
        except ImportError as e:
            print(f"Error launching GUI: {e}")
            print("Please ensure all required modules are installed.")
    
    elif args.modern:
        try:
            from modern_gui_app import main as modern_gui_main
            print("Launching Budget Tracker Modern GUI...")
            modern_gui_main()
        except ImportError as e:
            print(f"Error launching modern GUI: {e}")
            print("Please ensure all required modules are installed.")
            sys.exit(1)
    elif args.cli:
        try:
            # Set up sys.argv for CLI module
            sys.argv = ['cli'] + unknown
            from commands.cli import main as cli_main
            print("Launching Budget Tracker CLI...")
            cli_main()
        except ImportError as e:
            print(f"Error launching CLI: {e}")
            print("Please ensure all required modules are installed.")
            sys.exit(1)

if __name__ == "__main__":
    main()