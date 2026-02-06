import sys
import importlib

def check_import(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False

def main():
    print(f"Python version: {sys.version}")
    required_modules = ['cv2', 'mediapipe', 'numpy', 'pandas', 'matplotlib']
    
    all_passed = True
    for module in required_modules:
        if not check_import(module):
            all_passed = False
            
    if all_passed:
        print("\n🎉 Environment validation passed!")
        sys.exit(0)
    else:
        print("\n⚠️ Environment validation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
