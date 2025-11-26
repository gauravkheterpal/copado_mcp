# Copado MCP Server Implementation Plan

## Goal
Build a Model Context Protocol (MCP) server that exposes Copado DevOps capabilities to LLMs. This will allow an AI assistant to interact with Copado to manage user stories, promotions, and deployments.

## User Review Required
- **Authentication**: We will switch to using **Salesforce REST API** to access Copado objects (`copado__User_Story__c`, `copado__Promotion__c`).
- **Credentials**: Requires `SALESFORCE_INSTANCE_URL` and `SALESFORCE_ACCESS_TOKEN` (or Username/Password/Security Token flow).
- **Mocking**: Mock mode will remain available.

## Proposed Changes

### [MODIFY] `copado_mcp/client.py`
- Refactor `CopadoClient` to use `simple-salesforce` or direct `requests` to Salesforce REST API.
- Update methods to query SOQL for User Stories and Promotions.
- Update `create_promotion` to create Salesforce records.

### [MODIFY] `copado_mcp/server.py`
- Update environment variable reading to look for Salesforce credentials.

### [MODIFY] `walkthrough.md`
- Update run instructions with Salesforce credential setup.

## Verification Plan
### Automated Tests
- We will write a simple script `test_server.py` that uses `mcp` client to call tools on our local server and assert responses.
