import subprocess
import time
import os
import sys
import threading
import re

def run_flask_app():
    print("Starting Flask application...")
    app_path = os.path.join(os.getcwd(), 'app.py')
    if not os.path.exists(app_path):
        print(f"Error: {app_path} not found.")
        sys.exit(1)
    flask_process = subprocess.Popen([sys.executable, app_path])
    time.sleep(5)  # Give Flask some time to start
    return flask_process

def establish_ssh_tunnel():
    print("Establishing SSH tunnel...")
    ssh_command = "ssh -p 443 -R0:localhost:8000 qr@a.pinggy.io"
    
    ssh_process = subprocess.Popen(
        ssh_command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Wait for the SSH prompt and send 'yes' if needed
    while True:
        output = ssh_process.stderr.readline()
        print(output.strip())  # Print SSH output for debugging
        if "Are you sure you want to continue connecting" in output:
            ssh_process.stdin.write("yes\n")
            ssh_process.stdin.flush()
        elif "http://" in output or "https://" in output:
            # Extract and print the URLs
            urls = re.findall(r'(https?://\S+)', output)
            for url in urls:
                print(f"Your application is accessible at: {url}")
            break
        elif not output:
            break

    return ssh_process

def restart_ssh_tunnel(ssh_process):
    if ssh_process:
        ssh_process.terminate()
    return establish_ssh_tunnel()

def ssh_tunnel_manager():
    ssh_process = establish_ssh_tunnel()
    while True:
        time.sleep(55 * 60)  # Wait for 55 minutes
        print("Restarting SSH tunnel...")
        ssh_process = restart_ssh_tunnel(ssh_process)

def main():
    flask_process = run_flask_app()
    
    # Start the SSH tunnel manager in a separate thread
    ssh_thread = threading.Thread(target=ssh_tunnel_manager)
    ssh_thread.daemon = True
    ssh_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        flask_process.terminate()

if __name__ == "__main__":
    main()