import os
import subprocess

def clean(directory):
    print(f"Deleting non-.py files in: {os.path.abspath(directory)}")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if not item_path.endswith('.py'):
            print(f"Deleting: {item_path}")
            subprocess.run(['rm', '-rf', item_path], check=True)


# Example usage
directory = "./repo/"
clean(directory)
