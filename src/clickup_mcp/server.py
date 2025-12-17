import os
import httpx
from typing import Any
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

load_dotenv()

# ClickUp API Configuration
CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
CLICKUP_API_BASE = "https://api.clickup.com/api/v2"
CLICKUP_TEAM_ID = os.getenv("CLICKUP_TEAM_ID")
CLICKUP_DEFAULT_LIST_ID = os.getenv("CLICKUP_DEFAULT_LIST_ID")

app = Server("clickup-stories-mcp")

async def clickup_request(method: str, endpoint: str, **kwargs) -> dict:
    """Make authenticated request to ClickUp API"""
    headers = {
        "Authorization": CLICKUP_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=f"{CLICKUP_API_BASE}{endpoint}",
            headers=headers,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available ClickUp tools"""
    return [
        Tool(
            name="clickup_create_task",
            description="Create a new task/story in ClickUp",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (supports markdown)"
                    },
                    "list_id": {
                        "type": "string",
                        "description": "ClickUp List ID (optional, uses default if not provided)"
                    },
                    "status": {
                        "type": "string",
                        "description": "Task status (e.g., 'to do', 'in progress')"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority: 'urgent', 'high', 'normal', 'low'",
                        "enum": ["urgent", "high", "normal", "low"]
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags for the task"
                    },
                    "assignees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of usernames or user IDs to assign the task to"
                    },
                    "custom_fields": {
                        "type": "object",
                        "description": "Custom field values as key-value pairs"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="clickup_get_lists",
            description="Get all lists in a space or folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "Space ID to get lists from"
                    },
                    "folder_id": {
                        "type": "string",
                        "description": "Folder ID to get lists from (optional)"
                    }
                }
            }
        ),
        Tool(
            name="clickup_get_custom_fields",
            description="Get custom fields for a list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_id": {
                        "type": "string",
                        "description": "List ID to get custom fields for"
                    }
                },
                "required": ["list_id"]
            }
        ),
        Tool(
            name="clickup_get_spaces",
            description="Get all spaces in the team",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    if name == "clickup_create_task":
        list_id = arguments.get("list_id", CLICKUP_DEFAULT_LIST_ID)

        task_data = {
            "name": arguments["name"],
            "description": arguments.get("description", ""),
            "status": arguments.get("status"),
            "tags": arguments.get("tags", [])
        }

        # Handle priority conversion from string to integer
        if "priority" in arguments and arguments["priority"]:
            priority_map = {
                "urgent": 1,
                "high": 2,
                "normal": 3,
                "low": 4
            }
            priority_value = arguments["priority"].lower()
            if priority_value in priority_map:
                task_data["priority"] = priority_map[priority_value]

        # Handle assignees - support both usernames and user IDs
        if "assignees" in arguments and arguments["assignees"]:
            assignee_list = []
            for assignee in arguments["assignees"]:
                # If it's a number, treat as user ID
                if isinstance(assignee, (int, str)) and str(assignee).isdigit():
                    assignee_list.append(int(assignee))
                # If it's "Vitor Scarpinetti", convert to known user ID
                elif assignee == "Vitor Scarpinetti":
                    assignee_list.append(96271408)  # Known Vitor user ID
                # Otherwise, try to use as-is (could be username or user ID)
                else:
                    try:
                        # Try to convert to int if it's a string of digits
                        assignee_list.append(int(assignee))
                    except ValueError:
                        # If not a number, we'd need to look up the username
                        # For now, skip invalid assignees
                        pass

            if assignee_list:
                task_data["assignees"] = assignee_list

        # Handle custom fields if provided
        if "custom_fields" in arguments:
            task_data["custom_fields"] = [
                {"id": field_id, "value": value}
                for field_id, value in arguments["custom_fields"].items()
            ]

        # Remove None values
        task_data = {k: v for k, v in task_data.items() if v is not None}

        result = await clickup_request(
            "POST",
            f"/list/{list_id}/task",
            json=task_data
        )

        return [TextContent(
            type="text",
            text=f"Task created successfully!\nID: {result['id']}\nURL: {result['url']}"
        )]
    
    elif name == "clickup_get_lists":
        if "folder_id" in arguments:
            endpoint = f"/folder/{arguments['folder_id']}/list"
        else:
            endpoint = f"/space/{arguments['space_id']}/list"
        
        result = await clickup_request("GET", endpoint)
        
        lists_info = "\n".join([
            f"- {lst['name']} (ID: {lst['id']})"
            for lst in result.get("lists", [])
        ])
        
        return [TextContent(
            type="text",
            text=f"Available Lists:\n{lists_info}"
        )]
    
    elif name == "clickup_get_custom_fields":
        result = await clickup_request(
            "GET",
            f"/list/{arguments['list_id']}"
        )
        
        fields = result.get("custom_fields", [])
        fields_info = "\n".join([
            f"- {field['name']} (ID: {field['id']}, Type: {field['type']})"
            for field in fields
        ])
        
        return [TextContent(
            type="text",
            text=f"Custom Fields:\n{fields_info}" if fields_info else "No custom fields found"
        )]
    
    elif name == "clickup_get_spaces":
        result = await clickup_request(
            "GET",
            f"/team/{CLICKUP_TEAM_ID}/space"
        )
        
        spaces_info = "\n".join([
            f"- {space['name']} (ID: {space['id']})"
            for space in result.get("spaces", [])
        ])
        
        return [TextContent(
            type="text",
            text=f"Available Spaces:\n{spaces_info}"
        )]
    
    raise ValueError(f"Unknown tool: {name}")

def main():
    """Run the MCP server"""
    import asyncio
    import mcp.server.stdio
    
    async def run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run())

if __name__ == "__main__":
    main()