import subprocess
import platform

def open_bluetooth_settings():
    system_platform = platform.system()

    if system_platform == 'Windows':
        try:
            subprocess.run(['control', 'bthprops.cpl'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    else:
        print(f"Unsupported platform: {system_platform}")

if __name__ == "__main__":
    open_bluetooth_settings()
