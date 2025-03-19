import os
import sys
import logging
import json
import asyncio
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp import types
from typing import Any
import mcp.server.stdio

# reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logger = logging.getLogger('minium-mcp-server')
logger.info("Starting Minium MCP Server")

# Global connection variables
reader = None
writer = None

async def main():
    global reader, writer
    server = Server("minium-mcp-server")

    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="open",
                description="Open Project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Project path"},
                    },
                    "required": [],
                }
            ),
            types.Tool(
                name="get_system_info",
                description="Get system info",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="shutdown",
                description="Shutdown the developer tool",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="screen_shot",
                description="Take a screenshot of the current page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            types.Tool(
                name="go_home",
                description="Go Home Page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="navigate_to",
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
                name="navigate_back",
                description="Navigate back to the previous page",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
            ),
            types.Tool(
                name="switch_tab",
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
                name="redirect_to",
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
                name="relaunch",
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
            types.Tool(
                name="evaluate",
                description="Evaluate a JavaScript(es5) code",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Script code"},
                        "params": {"type": "string", "description": "Script parameters"},
                    },
                    "required": ["code", "params"],
                }
            ),
            types.Tool(
                name="call_method",
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
                name="page_scroll_to",
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
                name="tap",
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
                name="long_press",
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
                name="move",
                description="TouchMove on an element",
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
                name="input",
                description="Input text to an form element",
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
                name="switch",
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
                name="slide_to",
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
                name="pick",
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

    async def ensure_connection():
        """Ensure we have an active connection"""
        global reader, writer
        if writer is None or writer.is_closing():
            logger.info("Reconnecting to server...")
            reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
            logger.info("Reconnected successfully")

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ):
        """Handle tool execution requests"""
        logger.info(f"Received call tool request: {name} with args: {arguments}")
        command = {
            "name": name,
            "arguments": arguments or {}
        }
        
        try:
            await ensure_connection()
            
            writer.write(json.dumps(command).encode('utf-8'))
            await writer.drain()

            # Receive the response using the improved receive_full_response method
            response_data = await receive_full_response(reader)
            response = json.loads(response_data.decode('utf-8'))
            if response.get("status") == "error":
                logger.error(f"error: {response.get('message')}")
                raise Exception(response.get("message", "Unknown error from Blender"))
            
            return [types.TextContent(type="text", text=response.get("message"))]
        except (ConnectionError, asyncio.TimeoutError) as e:
            logger.error(f"Connection error: {str(e)}")
            # Attempt to reconnect and retry once
            try:
                await ensure_connection()
                
                writer.write(json.dumps(command).encode('utf-8'))
                await writer.drain()
                
                response_data = await receive_full_response(reader)
                response = json.loads(response_data.decode('utf-8'))
                if response.get("status") == "error":
                    logger.error(f"error: {response.get('message')}")
                    raise Exception(response.get("message", "Unknown error from Blender"))
                
                return [types.TextContent(type="text", text=response.get("message"))]
            except Exception as e:
                logger.error(f"Failed after retry: {str(e)}")
                raise

    async def receive_full_response(reader, buffer_size=8192):
        """Receive the complete response, potentially in multiple chunks"""
        chunks = []
        try:
            while True:
                chunk = await reader.read(buffer_size)
                if not chunk:
                    # If we get an empty chunk, the connection might be closed
                    if not chunks:  # If we haven't received anything yet, this is an error
                        raise Exception("Connection closed before receiving any data")
                    break
                
                chunks.append(chunk)
                
                # Check if we've received a complete JSON object
                try:
                    data = b''.join(chunks)
                    json.loads(data.decode('utf-8'))
                    # If we get here, it parsed successfully
                    logger.info(f"Received complete response ({len(data)} bytes)")
                    return data
                except json.JSONDecodeError:
                    # Incomplete JSON, continue receiving
                    continue
        except asyncio.TimeoutError:
            logger.warning("Socket timeout during chunked receive")
        except Exception as e:
            logger.error(f"Error during receive: {str(e)}")
            raise
            
        # If we get here, we either timed out or broke out of the loop
        # Try to use what we have
        if chunks:
            data = b''.join(chunks)
            logger.info(f"Returning data after receive completion ({len(data)} bytes)")
            try:
                # Try to parse what we have
                json.loads(data.decode('utf-8'))
                return data
            except json.JSONDecodeError:
                # If we can't parse it, it's incomplete
                raise Exception("Incomplete JSON response received")
        else:
            raise Exception("No data received")
        

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
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
