import subprocess
import sys
import os


def check_and_install_dependencies():
    """Check if required packages are installed"""
    required = ['pandas', 'numpy', 'matplotlib',
                'seaborn', 'sqlalchemy', 'pymysql']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing packages: {missing}")
        for package in missing:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package])
        print("All dependencies installed!\n")
    else:
        print("All dependencies are already installed.\n")


def run_module(module_name, description):
    """Run a Python module (dotted path) and handle errors"""
    print("=" * 60)
    print(f"▶ Running: {description}")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "-m", module_name],
            capture_output=True,
            text=True,
            encoding="latin1"
        )

        if result.returncode == 0:
            print(result.stdout)
            print(f"✓ {description} completed successfully!\n")
        else:
            print(f"✗ Error in {description}:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"✗ Exception in {description}: {e}")
        return False

    return True


def main():
    """Main execution pipeline"""
    print("\n" + "=" * 60)
    print(" JAPAN EARTHQUAKE ANALYSIS PIPELINE ")
    print("=" * 60 + "\n")

    check_and_install_dependencies()

    if not run_module("src.processing.all_csv", "Data Cleaning & Combining"):
        print("Stopping pipeline due to error in data cleaning.")
        return

    if not run_module("src.visualization.visualization", "Visualization & Plotting"):
        print("Warning: Visualization had issues, but continuing...")

    print("\n" + "=" * 60)
    print("▶ Database Operations")
    print("=" * 60)
    print("Note: Make sure MySQL is running and credentials are correct in src/database/database.py")

    response = input("Do you want to run database operations? (y/n): ")
    if response.lower() == 'y':
        if not run_module("src.database.database", "Database Setup"):
            print("Database connection failed. Check your MySQL configuration.")
        else:
            run_module("src.database.sql_queries", "SQL Queries & Analysis")

    print("\n" + "=" * 60)
    print("✓ PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
