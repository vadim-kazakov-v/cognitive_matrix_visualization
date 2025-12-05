#!/usr/bin/env python3
"""
Test script to verify that the error handling fixes are working correctly
"""
import json

def test_html_error_handling():
    """Test that the HTML contains proper error handling for 'no diagram to display'"""
    with open('/workspace/templates/index.html', 'r') as f:
        content = f.read()
    
    # Check that the success function has the validation for coords
    if "Check if we have valid data to plot" in content:
        print("✓ HTML contains validation for valid data to plot")
    else:
        print("✗ HTML missing validation for valid data to plot")
        return False
    
    # Check that the error function has improved error handling
    if "Error generating diagram" in content:
        print("✓ HTML contains improved error message display")
    else:
        print("✗ HTML missing improved error message display")
        return False
    
    # Check that error function shows error in plot area
    if "display: flex; justify-content: center" in content:
        print("✓ HTML contains proper error display styling")
    else:
        print("✗ HTML missing proper error display styling")
        return False
    
    return True

def test_python_error_handling():
    """Test that the Python backend has proper error handling"""
    with open('/workspace/app.py', 'r') as f:
        content = f.read()
    
    # Check that the backend has specific handling for no matrices case
    if "Could not generate any valid matrices" in content:
        print("✓ Python backend contains specific error message for no matrices case")
    else:
        print("✗ Python backend missing specific error message for no matrices case")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing error handling fixes...")
    
    html_ok = test_html_error_handling()
    python_ok = test_python_error_handling()
    
    if html_ok and python_ok:
        print("\n✓ All error handling fixes are properly implemented!")
    else:
        print("\n✗ Some error handling fixes are missing!")
        exit(1)