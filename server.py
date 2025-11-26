import sys
import json
import logging
from typing import Any, Dict, List, Optional
from .client import CopadoClient

# Configure logging to stderr so it doesn't interfere with stdout JSON-RPC
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os

class MCPServer:
    def __init__(self):
        # Check for Salesforce credentials in environment variables
        instance_url = os.environ.get("SALESFORCE_INSTANCE_URL")
        access_token = os.environ.get("SALESFORCE_ACCESS_TOKEN")
        
        # If credentials are present, disable mock mode
        mock_mode = not (instance_url and access_token)
        if not mock_mode:
            logger.info(f"Found Salesforce credentials. Running in real mode with Instance URL: {instance_url}")
        else:
            logger.info("No Salesforce credentials found. Running in MOCK mode.")

        self.client = CopadoClient(instance_url=instance_url, access_token=access_token, mock=mock_mode)
        self.tools = {
            "list_user_stories": self.list_user_stories,
            "list_promotions": self.list_promotions,
            "create_promotion": self.create_promotion,
            "deploy_promotion": self.deploy_promotion
        }

    def list_user_stories(self, status: Optional[str] = None) -> str:
        return json.dumps(self.client.get_user_stories(status), indent=2)

    def list_promotions(self) -> str:
        return json.dumps(self.client.get_promotions(), indent=2)

    def create_promotion(self, source_env: str, target_env: str, user_story_ids: List[str]) -> str:
        try:
            return json.dumps(self.client.create_promotion(source_env, target_env, user_story_ids), indent=2)
        except ValueError as e:
            return f"Error: {str(e)}"

    def deploy_promotion(self, promotion_id: str) -> str:
        try:
            return json.dumps(self.client.deploy_promotion(promotion_id), indent=2)
        except ValueError as e:
            return f"Error: {str(e)}"

    def run(self):
        logger.info("Starting Copado MCP Server (Stdio)...")
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                self.handle_request(request)
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
            except Exception as e:
                logger.error(f"Error processing request: {e}")

    def handle_request(self, request: Dict[str, Any]):
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        response = None

        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "copado-mcp-server",
                        "version": "0.1.0"
                    }
                }
            }
        elif method == "notifications/initialized":
            # No response needed for notifications
            return
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "list_user_stories",
                            "description": "List user stories from Copado",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string", "description": "Optional status filter"}
                                }
                            }
                        },
                        {
                            "name": "list_promotions",
                            "description": "List all promotions",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "create_promotion",
                            "description": "Create a new promotion",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "source_env": {"type": "string"},
                                    "target_env": {"type": "string"},
                                    "user_story_ids": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["source_env", "target_env", "user_story_ids"]
                            }
                        },
                        {
                            "name": "deploy_promotion",
                            "description": "Deploy an existing promotion",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "promotion_id": {"type": "string"}
                                },
                                "required": ["promotion_id"]
                            }
                        }
                    ]
                }
            }
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            
            if name in self.tools:
                try:
                    result_text = ""
                    if name == "list_user_stories":
                        result_text = self.list_user_stories(status=args.get("status"))
                    elif name == "list_promotions":
                        result_text = self.list_promotions()
                    elif name == "create_promotion":
                        result_text = self.create_promotion(
                            source_env=args.get("source_env"),
                            target_env=args.get("target_env"),
                            user_story_ids=args.get("user_story_ids")
                        )
                    elif name == "deploy_promotion":
                        result_text = self.deploy_promotion(promotion_id=args.get("promotion_id"))
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": result_text}]
                        }
                    }
                except Exception as e:
                     response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32603, "message": str(e)}
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": "Method not found"}
                }
        
        if response:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    server = MCPServer()
    server.run()
