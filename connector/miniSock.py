import os
import sys
import logging
import json
import minium
import socket

logger = logging.getLogger('minium-mcp-server')
logger.info("Starting Minium MCP Server")

# 创建一个Socket服务器
def start_socket_server(host='127.0.0.1', port=8888):

    """启动一个TCP Socket服务器"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Socket服务器已启动，监听 {host}:{port}")
        mini = None
        project_path = ''
        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"接收到来自 {addr} 的连接")
                data = client_socket.recv(1024)
                print(f"收到数据: {data.decode('utf-8')}")
                if data:
                    command = json.loads(data.decode('utf-8'))
                    arguments = command['arguments']
                    try:
                        match command['name']:
                            case "open":
                                # 根据操作系统设置开发者工具cli路径
                                if sys.platform == 'darwin':  # macOS
                                    dev_tool_path = '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'
                                elif sys.platform == 'win32':  # Windows
                                    dev_tool_path = 'C:/Program Files (x86)/Tencent/微信web开发者工具/cli.bat'
                                else:
                                    raise Exception("Unsupported operating system")

                                project_path = arguments['path']
                                mini = minium.Minium({
                                    "project_path": project_path, # 替换成你的【小程序项目目录地址】
                                    "dev_tool_path": dev_tool_path,
                                    "debug_mode": "error"
                                })

                                response = {
                                    "status": "success",
                                    "message": f"Success: Started"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "get_system_info":

                                response = {
                                    "status": "success",
                                    "message": f"Success: {mini.get_system_info()}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "shutdown":
                                mini.shutdown()

                                response = {
                                    "status": "success",
                                    "message": f"Success: Shutdown"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "screen_shot":
                                output_path = os.path.join(project_path, "screenshots/{}_screen_shot.png".format(mini.app.get_current_page().page_id))
                                if not os.path.isdir(os.path.dirname(output_path)):
                                    os.mkdir(os.path.dirname(output_path))
                                if os.path.isfile(output_path):
                                    os.remove(output_path)
                                mini.app.screen_shot(output_path)

                                response = {
                                    "status": "success",
                                    "message": f"Success: Screenshot, Path: {output_path}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "go_home":
                                mini.app.go_home()

                                response = {
                                    "status": "success",
                                    "message": f"Success: Go home"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "navigate_to":
                                mini.app.navigate_to(arguments["path"], arguments["query"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Navigate to"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "navigate_back":
                                mini.app.navigate_back()

                                response = {
                                    "status": "success",
                                    "message": f"Success: Navigate back"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "switch_tab":
                                mini.app.switch_tab(arguments["path"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Switch tab"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "redirect_to":
                                mini.app.redirect_to(arguments["path"], arguments["query"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Redirect to"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "evaluate":
                                msg_id = mini.app.evaluate(arguments["code"], arguments["params"], sync=False)
                                # 你可以做一些其他操作后, 再通过get_async_response方法获取前面注入代码的运行结果
                                result = mini.app.get_async_response(msg_id, 5)

                                response = {
                                    "status": "success",
                                    "message": f"Success: Evaluate, Result: {result}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "call_method":
                                page = mini.app.get_current_page()
                                result = page.call_method(arguments["method"], arguments["params"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Call method, Result: {result}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "page_scroll_to":
                                page = mini.app.get_current_page()
                                page.scroll_to(arguments["top"], arguments["duration"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Page scroll to, Top: {arguments['top']}, Duration: {arguments['duration']}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "tap":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.tap()

                                response = {
                                    "status": "success",
                                    "message": f"Success: Tap"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "long_press":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.long_press()

                                response = {
                                    "status": "success",
                                    "message": f"Success: Long press"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "move":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.move(arguments["left"], arguments["top"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Move to, Top: {arguments['top']}, Left: {arguments['left']}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "input":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.input(arguments["text"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Input, Text: {arguments['text']}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "switch":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.switch()

                                response = {
                                    "status": "success",
                                    "message": f"Success: Switch"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "slide_to":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.slide_to(arguments["value"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Slide to, Value: {arguments['value']}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case "pick":
                                page = mini.app.get_current_page()
                                el = page.get_element(arguments["element"])
                                el.pick(arguments["option"])

                                response = {
                                    "status": "success",
                                    "message": f"Success: Pick, Option: {arguments['option']}"
                                }

                                client_socket.send(json.dumps(response).encode('utf-8'))
                                # break
                            case _:
                                raise ValueError(f"Unknown tool: {command['name']}")
                    except Exception as e:
                        logger.error(f"Error executing tool: {e}")
                        error_response = {
                            "status": "error",
                            "message": str(e)
                        }
                        client_socket.sendall(json.dumps(error_response).encode('utf-8'))

if __name__ == "__main__":
    start_socket_server()
