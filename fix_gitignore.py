import os
import subprocess

def run_git_command(command):
    """Git komutunu çalıştır ve çıktıyı döndür"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return None

def fix_gitignore():
    """Git cache'ini temizle ve .gitignore'ı uygula"""
    print("Starting gitignore fix process...")
    
    # 1. Git cache'ini temizle
    print("Cleaning Git cache...")
    run_git_command("git rm -r --cached .")
    
    # 2. Staged dosyaları yeniden ekle (.gitignore'ı dikkate alarak)
    print("Re-adding all files (respecting .gitignore)...")
    run_git_command("git add .")
    
    print("Git cache cleaned and files re-added.")
    print("Now you can commit changes with:")
    print("git commit -m \"Fixed .gitignore to properly exclude trash-bin directory\"")
    print("git push")

if __name__ == "__main__":
    fix_gitignore()
