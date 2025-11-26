from typing import Dict, List, Any
from datetime import datetime

class MockData:
    USER_STORIES: List[Dict[str, Any]] = [
        {
            "id": "US-001",
            "title": "Implement Login Page",
            "status": "In Progress",
            "priority": "High",
            "description": "Create a responsive login page with OAuth support.",
            "project": "Copado-Demo"
        },
        {
            "id": "US-002",
            "title": "Setup CI/CD Pipeline",
            "status": "Open",
            "priority": "Critical",
            "description": "Configure Jenkins pipeline for automated testing.",
            "project": "Copado-Demo"
        },
        {
            "id": "US-003",
            "title": "Fix Navigation Bug",
            "status": "Completed",
            "priority": "Medium",
            "description": "Fix the issue where the menu doesn't collapse on mobile.",
            "project": "Copado-Demo"
        }
    ]

    PROMOTIONS: List[Dict[str, Any]] = [
        {
            "id": "P-1001",
            "source_env": "Dev",
            "target_env": "UAT",
            "status": "Completed",
            "user_stories": ["US-003"],
            "created_at": "2023-10-26T10:00:00Z"
        }
    ]

    ENVIRONMENTS: List[str] = ["Dev", "UAT", "Staging", "Prod"]
