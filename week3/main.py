from openai import OpenAI
import json
import time

client = OpenAI(
    api_key="sk-xxxxxxxxxx",
    base_url="https://api.apiyi.com/v1",
)

# 定义 modify_config 函数，入参：service_name，key，value
def modify_config(service_name, key, value):
    print(service_name, key, value)

# 定义 restart_service 函数，入参：service_name
def restart_service(service_name):
    print(service_name)


# 定义 apply_manifest 函数，入参：resource_type，image
def apply_manifest(resource_type, image):
    print(resource_type, image)


def analyze_loki_log(query_str):
    print("\n函数调用的参数: ", query_str)
    return json.dumps({"log": "this is error log"})


def run_conversation():
    """Query: 查看 app=grafana 且关键字包含 Error 的日志"""

    # 步骤一：把所有预定义的 function 传给 chatgpt
    query = input("输入查询指令：")
    messages = [
        {
            "role": "system",
            "content": "你是一个 k8s 专家，你可以调用多个函数来帮助用户完成任务",
        },
        {
            "role": "user",
            "content": query,
        },
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "modify_config",
                "description": "从用户的输入获取信息，如果是修改服务的配置，则调用该方法，把给定的 key 和 value 更新到给定的配置中",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": '服务的名称，例如 "nginx"',
                        },
                        "key": {
                            "type": "string",
                            "description": "配置的 key，例如 'replicas'",
                        },
                        "value": {
                            "type": "string",
                            "description": "配置的 value，例如 '3'",
                        },
                    },
                    "required": ["service_name", "key", "value"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "restart_service",
                "description": "重启一个服务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": "服务的名称，例如 'nginx'",
                        },
                    },
                    "required": ["service_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "apply_manifest",
                "description": "部署一个服务，会给定一个镜像名称",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "资源的类型，例如 'deployment'",
                        },
                        "image": {
                            "type": "string",
                            "description": "镜像的名称，例如 'nginx:latest'",
                        },
                    },
                    "required": ["resource_type", "image"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "analyze_loki_log",
                "description": "从 Loki 获取日志",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query_str": {
                            "type": "string",
                            "description": 'Loki 查询字符串，例如：{app="grafana"} |= "Error"',
                        },
                    },
                },
                "required": ["query_str"],
            },
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print("\nChatGPT want to call function: ", tool_calls)
    # 步骤二：检查 LLM 是否调用了 function
    if tool_calls is None:
        print("not tool_calls")
    if tool_calls:
        available_functions = {
            "modify_config": modify_config,
            "restart_service": restart_service,
            "apply_manifest": apply_manifest,
            "analyze_loki_log": analyze_loki_log
        }
        messages.append(response_message)
        # 步骤三：把每次 function 调用和返回的信息传给 model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            print("调用", function_name, "函数")
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            print("函数返回结果", function_response)

print("LLM Res: ", run_conversation())
