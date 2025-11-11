#!/usr/bin/env python3
"""
Local testing script for Weekend Trunk Shifts application
Run this before deploying to verify everything works
"""

import os
import sys
import json

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} MISSING: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description} MISSING: {dirpath}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    required = ['flask', 'werkzeug', 'openpyxl']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def check_files():
    """Check if all required files exist"""
    print("\n" + "="*60)
    print("CHECKING FILES")
    print("="*60)
    
    files = [
        ('app.py', 'Main application'),
        ('requirements.txt', 'Dependencies file'),
        ('render.yaml', 'Render config'),
        ('README.md', 'Documentation'),
        ('DEPLOYMENT_GUIDE.md', 'Deployment guide'),
        ('.gitignore', 'Git ignore file'),
        ('templates/login.html', 'Login template'),
        ('templates/employee_dashboard.html', 'Employee dashboard'),
        ('templates/manager_dashboard.html', 'Manager dashboard'),
    ]
    
    all_exist = True
    for filepath, description in files:
        if not check_file(filepath, description):
            all_exist = False
    
    return all_exist

def test_app_import():
    """Test if app can be imported"""
    print("\n" + "="*60)
    print("TESTING APP IMPORT")
    print("="*60)
    
    try:
        import app
        print("✓ App imported successfully")
        
        # Check if Flask app exists
        if hasattr(app, 'app'):
            print("✓ Flask app object exists")
        else:
            print("✗ Flask app object not found")
            return False
        
        # Check if shifts were generated
        if hasattr(app, 'SHIFTS'):
            shift_count = len(app.SHIFTS)
            print(f"✓ Shifts generated: {shift_count} shifts")
            if shift_count == 60:
                print("✓ Correct number of shifts (60)")
            else:
                print(f"✗ Expected 60 shifts, got {shift_count}")
                return False
        else:
            print("✗ SHIFTS not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed to import app: {e}")
        return False

def check_data_structure():
    """Check if data directory structure is correct"""
    print("\n" + "="*60)
    print("CHECKING DATA STRUCTURE")
    print("="*60)
    
    # Import app to trigger data file creation
    try:
        import app
        
        data_files = [
            'data/employees.json',
            'data/preferences.json',
            'data/settings.json',
            'data/assignments.json'
        ]
        
        all_exist = True
        for filepath in data_files:
            if check_file(filepath, f"Data file"):
                # Verify JSON is valid
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    print(f"  → Valid JSON with {len(data)} items")
                except json.JSONDecodeError:
                    print(f"  → ERROR: Invalid JSON")
                    all_exist = False
            else:
                all_exist = False
        
        # Check employee count
        try:
            with open('data/employees.json', 'r') as f:
                employees = json.load(f)
            
            non_managers = [e for e in employees.values() if not e.get('is_manager')]
            print(f"\n✓ Found {len(non_managers)} employee accounts (expected 30)")
            
            if len(non_managers) != 30:
                print(f"✗ Expected 30 employees, found {len(non_managers)}")
                all_exist = False
        except:
            pass
        
        return all_exist
    except Exception as e:
        print(f"✗ Error checking data structure: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("WEEKEND TRUNK SHIFTS - LOCAL TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Dependencies", check_dependencies()))
    results.append(("Files", check_files()))
    results.append(("App Import", test_app_import()))
    results.append(("Data Structure", check_data_structure()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nYou're ready to deploy to Render!")
        print("\nNext steps:")
        print("1. Push code to GitHub")
        print("2. Create new Web Service on Render")
        print("3. Connect your GitHub repository")
        print("4. Deploy and test")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before deploying.")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
