import os
import sys
import logging
import minium
import socket
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

async def main(project_path: str):
    server = Server("minium-mcp-server")
    # 根据操作系统设置开发者工具cli路径
    if sys.platform == 'darwin':  # macOS
        dev_tool_path = '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'
    elif sys.platform == 'win32':  # Windows
        dev_tool_path = 'C:/Program Files (x86)/Tencent/微信web开发者工具/cli.bat'
    else:
        raise Exception("Unsupported operating system")

    mini = minium.Minium({
        "project_path": project_path, # 替换成你的【小程序项目目录地址】
        "dev_tool_path": dev_tool_path,
        "debug_mode": "error"
    })
    mini.app.enable_log()

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
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
                        "value": {"type": "any", "description": "value of data"},
                    },
                    "required": [],
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
        logger.info(f"Received call tool request: {name} with args: {arguments}")
        try:
            match name.replace("minium_", ""):
                case "get_system_info":
                    return [types.TextContent(type="text", text=f"Error: {mini.get_system_info()}")]
                case "shutdown":
                    mini.shutdown()
                    return [types.TextContent(type="text", text=f"Success: Shutdown")]
                case "screen_shot":
                    output_path = os.path.join(project_path, "screenshots/{}_screen_shot.png".format(mini.app.get_current_page().page_id))
                    if not os.path.isdir(os.path.dirname(output_path)):
                        os.mkdir(os.path.dirname(output_path))
                    if os.path.isfile(output_path):
                        os.remove(output_path)
                    mini.app.screen_shot(output_path)
                    return [types.TextContent(type="text", text=f"Success: Screenshot, Path: {output_path}")]
                case "get_all_pages_path":
                    all_pages_path = mini.app.get_all_pages_path()
                    return [types.TextContent(type="text", text=f"Screenshot, Path: {all_pages_path}")]

                case "go_home":
                    mini.app.go_home()
                    return [types.TextContent(type="text", text=f"Success: Go home")]
                case "navigate_to":
                    mini.app.navigate_to(arguments["path"], arguments["query"])
                    return [types.TextContent(type="text", text=f"Success: Navigate to")]
                case "navigate_back":
                    mini.app.navigate_back()
                    return [types.TextContent(type="text", text=f"Success: Navigate back")]
                case "switch_tab":
                    mini.app.switch_tab(arguments["path"])
                    return [types.TextContent(type="text", text=f"Success: Switch tab")]
                case "redirect_to":
                    mini.app.redirect_to(arguments["path"], arguments["query"])
                    return [types.TextContent(type="text", text=f"Success: Redirect to")]

                case "evaluate":
                    msg_id = mini.app.evaluate(arguments["code"], arguments["params"], sync=False)
                    # 你可以做一些其他操作后, 再通过get_async_response方法获取前面注入代码的运行结果
                    result = mini.app.get_async_response(msg_id, 5)
                    return [types.TextContent(type="text", text=f"Success: Evaluate, Result: {result}")]
                case "call_method":
                    page = mini.app.get_current_page()
                    result = page.call_method(arguments["method"], arguments["params"])
                    return [types.TextContent(type="text", text=f"Success: Call method, Result: {result}")]
                case "page_scroll_to":
                    page = mini.app.get_current_page()
                    page.scroll_to(arguments["top"], arguments["duration"])
                    return [types.TextContent(type="text", text=f"Success: Page scroll to, Top: {arguments['top']}, Duration: {arguments['duration']}")]
                case "page_get_data":
                    page = mini.app.get_current_page()
                    return [types.TextContent(type="text", text=f"Data: {page.data}")]
                case "page_set_data":
                    page = mini.app.get_current_page()
                    data = page.data
                    data[arguments['key']] = arguments['value']
                    return [types.TextContent(type="text", text=f"Data: {page.data}")]

                case "tap":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.tap()
                    return [types.TextContent(type="text", text=f"Success: Tap")]
                case "long_press":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.long_press()
                    return [types.TextContent(type="text", text=f"Success: Long press")]
                case "move":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.move(arguments["left"], arguments["top"])
                    return [types.TextContent(type="text", text=f"Success: Move to, Top: {arguments['top']}, Left: {arguments['left']}")]
                case "input":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.input(arguments["text"])
                    return [types.TextContent(type="text", text=f"Success: Input, Text: {arguments['text']}")]
                case "switch":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.switch()
                    return [types.TextContent(type="text", text=f"Success: Switch")]
                case "slide_to":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.slide_to(arguments["value"])
                    return [types.TextContent(type="text", text=f"Success: Slide to, Value: {arguments['value']}")]
                case "pick":
                    page = mini.app.get_current_page()
                    el = page.get_element(arguments["element"])
                    el.pick(arguments["option"])
                    return [types.TextContent(type="text", text=f"Success: Pick, Option: {arguments['option']}")]
                case _:
                    raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

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
