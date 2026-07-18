"""One-click Windows launcher for the desktop experience."""
import os
import socket
import subprocess
import sys
import time
import webbrowser
from urllib.request import urlopen


def free_port():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def wait_for_api(url, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.25)
    return False


def main():
    api_port, ui_port = free_port(), free_port()
    env = os.environ.copy()
    env["SUBTITLE_API_HOST"] = "127.0.0.1"
    env["SUBTITLE_API_PORT"] = str(api_port)
    env["SUBTITLE_API_BASE_URL"] = f"http://127.0.0.1:{api_port}"
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    api = subprocess.Popen([sys.executable, "-m", "uvicorn", "src.api.main:app", "--host", "127.0.0.1", "--port", str(api_port)], env=env, creationflags=creationflags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ui = None
    try:
        if not wait_for_api(f"http://127.0.0.1:{api_port}/health"):
            raise RuntimeError("The translation service could not start.")
        ui = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py", "--server.address=127.0.0.1", "--server.port", str(ui_port), "--server.headless=true"], env=env, creationflags=creationflags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        webbrowser.open(f"http://127.0.0.1:{ui_port}")
        ui.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for process in (ui, api):
            if process and process.poll() is None:
                process.terminate()
        for process in (ui, api):
            if process:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


if __name__ == "__main__":
    main()
