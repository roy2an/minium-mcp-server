from flask import Flask, request, jsonify
import json
import os
import sys
import minium
import base64

app = Flask(__name__)
print("Starting Minium MCP Web Server")

mini = None
project_path = ''
HOST = '0.0.0.0'
PORT = 9188

@app.route('/api/command', methods=['POST'])
def handle_command():
    global mini, project_path
    try:
        command = request.json
        arguments = command['arguments']

        print(f"COMMAND: {json.dumps(command)}")
        
        match command['name']:
            case "open":
                if sys.platform == 'darwin':  # macOS
                    dev_tool_path = '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'
                elif sys.platform == 'win32':  # Windows
                    dev_tool_path = 'C:/Program Files (x86)/Tencent/微信web开发者工具/cli.bat'
                else:
                    raise Exception("Unsupported operating system")

                project_path = arguments['path']
                try:
                    mini = minium.Minium({
                        "project_path": project_path,
                        "dev_tool_path": dev_tool_path,
                        "debug_mode": "error"
                    })
                    mini.app.enable_log()
                except Exception as e:
                    # 重试
                    return jsonify({
                        "status": "error",
                        "message": str(e)
                    })

                return jsonify({
                    "status": "success",
                    "message": "Started"
                })

            case "get_system_info":
                return jsonify({
                    "status": "success",
                    "message": mini.get_system_info()
                })

            case "shutdown":
                mini.shutdown()
                return jsonify({
                    "status": "success", 
                    "message": "Shutdown"
                })

            case "screen_shot":
                output_path = os.path.join(project_path, "screenshots/{}_screen_shot.png".format(mini.app.get_current_page().page_id))
                if not os.path.isdir(os.path.dirname(output_path)):
                    os.makedirs(os.path.dirname(output_path))
                if os.path.isfile(output_path):
                    os.remove(output_path)
                mini.app.screen_shot(output_path)
                # 获取截图
                with open(output_path, "rb") as f:
                    image = f.read()
                    # 返回base64编码的图片
                    image_base64 = base64.b64encode(image).decode('utf-8')
                # 删除截图
                os.remove(output_path)
                return jsonify({
                    "status": "success",
                    "type": "image",
                    "data": image_base64
                })
            
            case "get_all_pages_path":
                all_pages_path = mini.app.get_all_pages_path()
                with open(os.path.join(project_path, "app.json"), "r", encoding="utf-8") as file:  # 建议指定 encoding
                    app = json.load(file)  # 解析 JSON 文件 → Python 字典/列表
                    tabbar = app.get('tabBar').get('list')
                
                result = []
                for path in all_pages_path:
                    if path in [item.get('pagePath') for item in tabbar]:
                        result.append({
                            "path": f"/{path}",
                            "method": "switch_tab"
                        })
                    else:
                        result.append({
                            "path": f"/{path}",
                            "method": "navigate_to"
                        })
                return jsonify({
                    "status": "success",
                    "message": f"Get all pages path, Path: {result}"
                })
            
            case "get_navigate_method_of_page":
                with open(os.path.join(project_path, "app.json"), "r", encoding="utf-8") as file:  # 建议指定 encoding
                    app = json.load(file)  # 解析 JSON 文件 → Python 字典/列表
                    tabbar = app.get('tabBar').get('list')
                    if arguments["path"] in [item.get('pagePath') for item in tabbar]:
                        return jsonify({
                            "status": "success",
                            "message": "switch_tab"
                        })
                    else:
                        return jsonify({    
                            "status": "success",
                            "message": "navigate_to"
                        })

            case "go_home":
                mini.app.go_home()
                return jsonify({
                    "status": "success",
                    "message": "Go home"
                })

            case "navigate_to":
                mini.app.navigate_to(arguments["path"], arguments["query"])
                return jsonify({
                    "status": "success",
                    "message": "Navigate to"
                })

            case "navigate_back":
                mini.app.navigate_back()
                return jsonify({
                    "status": "success",
                    "message": "Navigate back"
                })

            case "switch_tab":
                mini.app.switch_tab(arguments["path"])
                return jsonify({
                    "status": "success",
                    "message": "Switch tab"
                })

            case "redirect_to":
                mini.app.redirect_to(arguments["path"], arguments["query"])
                return jsonify({
                    "status": "success",
                    "message": "Redirect to"
                })

            # case "evaluate":
            #     msg_id = mini.app.evaluate(arguments["code"], arguments["params"], sync=False)
            #     result = mini.app.get_async_response(msg_id, 5)
            #     return jsonify({
            #         "status": "success",
            #         "message": f"Evaluate, Result: {result}"
            #     })

            case "call_method":
                page = mini.app.get_current_page()
                result = page.call_method(arguments["method"], arguments["params"])
                return jsonify({
                    "status": "success",
                    "message": f"Call method, Result: {result}"
                })

            case "page_scroll_to":
                page = mini.app.get_current_page()
                page.scroll_to(arguments["top"], arguments["duration"])
                return jsonify({
                    "status": "success",
                    "message": f"Page scroll to, Top: {arguments['top']}, Duration: {arguments['duration']}"
                })

            case "page_get_wxml":
                page = mini.app.get_current_page()
                return jsonify({
                    "status": "success",
                    "message": f"WXML: {page.wxml}"
                })
            
            case "page_get_data":
                page = mini.app.get_current_page()
                return jsonify({
                    "status": "success",
                    "message": f"Data: {page.data}"
                })
            
            case "page_set_data":
                page = mini.app.get_current_page()
                data = page.data
                data[arguments['key']] = json.load(arguments['value'])
                return jsonify({
                    "status": "success",
                    "message": f"Data: {page.data}"
                })

            case "tap":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.tap()
                return jsonify({
                    "status": "success",
                    "message": "Tap"
                })

            case "long_press":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.long_press()
                return jsonify({
                    "status": "success",
                    "message": "Long press"
                })

            case "move":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.move(arguments["left"], arguments["top"])
                return jsonify({
                    "status": "success",
                    "message": f"Move to, Top: {arguments['top']}, Left: {arguments['left']}"
                })

            case "input":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.input(arguments["text"])
                return jsonify({
                    "status": "success",
                    "message": f"Input, Text: {arguments['text']}"
                })

            case "switch":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.switch()
                return jsonify({
                    "status": "success",
                    "message": "Switch"
                })

            case "slide_to":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.slide_to(arguments["value"])
                return jsonify({
                    "status": "success",
                    "message": f"Slide to, Value: {arguments['value']}"
                })

            case "pick":
                page = mini.app.get_current_page()
                el = page.get_element(arguments["element"])
                el.pick(arguments["option"])
                return jsonify({
                    "status": "success",
                    "message": f"Pick, Option: {arguments['option']}"
                })

            case _:
                return jsonify({
                    "status": "error",
                    "message": f"Unknown command: {command['name']}"
                })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
