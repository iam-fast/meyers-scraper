#!/usr/bin/env python3
"""
Simple test runner for the Meyers Scraper project.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n🧪 {description}")
    print("-" * 50)

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        print("✅ Passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Run all tests."""
    print("🚀 Meyers Scraper Test Suite")
    print("=" * 60)

    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Change to project root directory
    os.chdir(project_root)

    # Test core functionality
    core_success = run_command(
        "python tests/test_core.py", "Testing core functionality"
    )

    # Test imports
    import_success = run_command(
        "python -c \"from src.client import MeyersAPIClient; from src.processor import MenuDataProcessor; from src.display import MenuDisplay; print('✅ All imports working')\"",
        "Testing imports",
    )

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"Core tests: {'✅ Passed' if core_success else '❌ Failed'}")
    print(f"Import tests: {'✅ Passed' if import_success else '❌ Failed'}")

    if core_success and import_success:
        print("\n🎉 All tests passed! The new structure is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
