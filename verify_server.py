import subprocess
import json
import sys
import os

def run_verification():
    # Start the server process
    # Ensure PYTHONPATH includes the current directory so copado_mcp module can be found
    env = os.environ.copy()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env["PYTHONPATH"] = current_dir

    print("--- Environment Check ---")
    print(f"SALESFORCE_INSTANCE_URL: {'Set' if os.environ.get('SALESFORCE_INSTANCE_URL') else 'MISSING'}")
    print(f"SALESFORCE_ACCESS_TOKEN: {'Set' if os.environ.get('SALESFORCE_ACCESS_TOKEN') else 'MISSING'}")
    print("-------------------------")

    print(f"Starting server from {current_dir}...")
    process = subprocess.Popen(
        [sys.executable, "-m", "copado_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        text=True,
        env=env,
        cwd=current_dir
    )

    def send_request(req):
        json_req = json.dumps(req)
        process.stdin.write(json_req + "\n")
        process.stdin.flush()
        return process.stdout.readline()

    try:
        # Initialize
        print("Sending initialize...")
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "verifier", "version": "1.0"}
            }
        }
        resp = send_request(init_req)
        print(f"Initialize Response: {resp.strip()}")

        # List tools
        print("\nListing tools...")
        list_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        resp = send_request(list_req)
        print(f"List Tools Response: {resp.strip()}")

        # Call list_user_stories
        print("\nCalling list_user_stories...")
        call_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "list_user_stories",
                "arguments": {}
            }
        }
        resp = send_request(call_req)
        print(f"Call Response: {resp.strip()}")

    finally:
        process.terminate()

if __name__ == "__main__":
    run_verification()
