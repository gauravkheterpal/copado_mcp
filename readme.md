# Copado MCP Server Walkthrough

I have built a Copado MCP Server that exposes DevOps capabilities to LLMs.

## Features
- **List User Stories**: Retrieve user stories with optional status filtering.
- **List Promotions**: View existing promotions.
- **Create Promotion**: Create a new promotion between environments.
- **Deploy Promotion**: Deploy a promotion.

## Implementation Details
- **Server**: Implements MCP protocol over stdio using a custom `MCPServer` class (due to Python version constraints).
- **Client**: `CopadoClient` with mock data support.
- **Mock Data**: Pre-populated user stories and promotions for testing.

## Verification
I ran a verification script `verify_server.py` that connects to the server process and executes the tools.

### Results
- `initialize`: Successful handshake.
- `tools/list`: Correctly lists all 4 tools.
- `tools/call`: Successfully called `list_user_stories`.

## How to Run
To run the server and verify functionality:

1. **Set Environment Variables** (Optional - for Real API):
   ```bash
   export SALESFORCE_INSTANCE_URL="https://your-instance.salesforce.com"
   export SALESFORCE_ACCESS_TOKEN="your_access_token"
   ```
   *Note: If these are not set or if the API call fails, the server will automatically fallback to Mock Mode.*

2. **Run the Verification Script**:
   ```bash
   python3 verify_server.py
   ```
   This script starts the server and acts as a client to call the tools.

3. **Run Standalone Server**:
   To run the server for use with an MCP client (like Claude Desktop):
   ```bash
   python3 -m copado_mcp.server
   ```
   This will start the server on stdio. Configure your MCP client to run this command.
