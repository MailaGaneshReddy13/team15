import subprocess
import sys
import os

# Set environment variable just in case
env = os.environ.copy()
# env['PYTHONPATH'] = os.getcwd()

with open("migration_debug.txt", "w", encoding="utf-8") as f:
    try:
        f.write(f"Running makemigrations from {os.getcwd()}\n")
        result = subprocess.run(
            [sys.executable, "manage.py", "makemigrations"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=os.getcwd(),
            env=env
        )
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
        f.write(f"\nReturn Code: {result.returncode}\n")
    except Exception as e:
        f.write(f"Exception: {e}")
