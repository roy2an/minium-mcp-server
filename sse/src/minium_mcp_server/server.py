import os
import sys
import logging
import json
import asyncio
import requests
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from mcp import types
from typing import Any
import mcp.server.stdio

HOST = 'http://127.0.0.1'
# HOST = 'http://192.168.3.42'
PORT = 9188

# reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logger = logging.getLogger('minium-mcp-server')
print("Starting Minium MCP Server")

async def main():
    server = Server("minium-mcp-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="minium_open",
                description="Open a project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Project path"},
                    },
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_get_system_info",
                description="Get system info",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_shutdown",
                description="Shutdown the developer tool",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_screen_shot",
                description="Take a screenshot of the current page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            types.Tool(
                name="minium_get_all_pages_path",
                description="Get paths of all pages",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_get_navigate_method_of_page",
                description="Get navigate method of a page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Page path"},
                    },
                    "required": ["path"],
                }
            ),
            types.Tool(
                name="minium_go_home",
                description="Go to the home page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_navigate_to",
                description="Navigate to a page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Page path"},
                        "query": {"type": "string", "description": "Query parameters"},
                    },
                    "required": ["path"],
                }
            ),
            types.Tool(
                name="minium_navigate_back",
                description="Navigate back to the previous page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_switch_tab",
                description="Switch to a tab",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Page path"},
                    },
                    "required": ["path"],
                }
            ),
            types.Tool(
                name="minium_redirect_to",
                description="Redirect to a page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Page path"},
                        "query": {"type": "string", "description": "Query parameters"},
                    },
                    "required": ["path"],
                }
            ),
            types.Tool(
                name="minium_relaunch",
                description="Close all pages and open a new one",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Page path"},
                        "query": {"type": "string", "description": "Query parameters"},
                    },
                    "required": ["path"],
                }
            ),
            # types.Tool(
            #     name="evaluate",
            #     description="Evaluate a JavaScript(es5) code",
            #     inputSchema={
            #         "type": "object",
            #         "properties": {
            #             "code": {"type": "string", "description": "Script code"},
            #             "params": {"type": "string", "description": "Script parameters"},
            #         },
            #         "required": ["code", "params"],
            #     }
            # ),
            types.Tool(
                name="minium_call_method",
                description="Call a method of page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "method": {"type": "string", "description": "Method name"},
                        "params": {"type": "object", "description": "Method parameters"},
                    },
                    "required": ["method", "params"],
                }
            ),
            types.Tool(
                name="minium_page_scroll_to",
                description="Scroll to the specified position of an page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "top": {"type": "number", "description": "Scroll to the top"},
                        "duration": {"type": "number", "description": "Scroll duration"},
                    },
                    "required": ["top", "duration"],
                }
            ),
            types.Tool(
                name="page_get_wxml",
                description="Get Dom structure of an page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_page_get_data",
                description="Get data of an page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="minium_page_set_data",
                description="Set data of an page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "key of data"},
                        "value": {"type": "string", "description": "value of data"},
                    },
                    "required": ["key", "value"],
                }
            ),
            types.Tool(
                name="minium_tap",
                description="Tap an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                    },
                    "required": ["element"],
                }
            ),
            types.Tool(
                name="minium_long_press",
                description="Long press an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                    },
                    "required": ["element"],
                }
            ),
            types.Tool(
                name="minium_move",
                description="Perform gestures on the element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                        "top": {"type": "number", "description": "Move to the top coordinate"},
                        "left": {"type": "number", "description": "Move to the left coordinate"},
                    },
                    "required": ["element", "top", "left"],
                }
            ),
            types.Tool(
                name="minium_input",
                description="Input text to an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                        "text": {"type": "string", "description": "Text to input"},
                    },
                    "required": ["element", "text"],
                }
            ),
            types.Tool(
                name="minium_switch",
                description="Change the switch status of an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                    },
                    "required": ["element"],
                }
            ),
            types.Tool(
                name="minium_slide_to",
                description="Slide to the specified position of an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                        "value": {"type": "number", "description": "Slide value"},
                    },
                    "required": ["element", "value"],
                }
            ),
            types.Tool(
                name="minium_pick",
                description="Pick an option of an element",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "element": {"type": "string", "description": "Element id"},
                        "option": {"type": "string", "description": "Option value"},
                    },
                    "required": ["element", "option"],
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ):
        """Handle tool execution requests"""
        print(f"Received call tool request: {name} with args: {arguments}")

        try:
            # Send HTTP request to web server
            response = requests.post(
                f"{HOST}:{PORT}/api/command",
                json={
                    "name": name.replace("minium_", ""),
                    "arguments": arguments or {}
                },
                timeout=600000
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP error: {response.status_code}")
                
            response_data = response.json()
            if response_data.get("status") == "error":
                raise Exception(response_data.get("message", "Unknown error"))

            if response_data.get("type") == "image":
                return [types.ImageContent(type="image", mimeType="image/png", data=response_data.get("data"))]
                
            return [types.TextContent(type="text", text=response_data.get("message"))]
            
        except Exception as e:
            logger.error(f"Error handling tool request: {str(e)}")
            raise

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="minium",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )