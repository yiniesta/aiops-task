# 作业
## 实现 Function Calling
* 定义 modify_config 函数，入参：service_name，key，value
* 定义 restart_service 函数，入参：service_name
* 定义 apply_manifest 函数，入参：resource_type，image

## 实践 Function Calling，观察以下输入是否能正确选择对应的函数
* 帮我修改 gateway 的配置，vendor 修改为 alipay
* 帮我重启 gateway 服务
* 帮我部署一个 deployment，镜像是 nginx

```shell
❯ python main.py
输入查询指令：帮我修改 gateway 的配置，vendor 修改为 alipay

ChatGPT want to call function:  [ChatCompletionMessageToolCall(id='call_ETVYs6fSzBXWnYYqNvmNb2OP', function=Function(arguments='{"service_name":"gateway","key":"vendor","value":"alipay"}', name='modify_config', parameters=None), type='function')]
调用 modify_config 函数
gateway vendor alipay
函数返回结果 None
LLM Res:  None

❯ python main.py
输入查询指令：帮我重启 gateway 服务

ChatGPT want to call function:  [ChatCompletionMessageToolCall(id='call_QMVYdMuqhXVhnh7xlrBFgTnp', function=Function(arguments='{"service_name":"gateway"}', name='restart_service', parameters=None), type='function')]
调用 restart_service 函数
gateway
函数返回结果 None
LLM Res:  None

❯ python main.py
输入查询指令：帮我部署一个 deployment，镜像是 nginx

ChatGPT want to call function:  [ChatCompletionMessageToolCall(id='call_uxlTvK2lfdK3jw2M6NKJjO5u', function=Function(arguments='{"image":"nginx","resource_type":"deployment"}', name='apply_manifest', parameters=None), type='function')]
调用 apply_manifest 函数
deployment nginx
函数返回结果 None
LLM Res:  None
```