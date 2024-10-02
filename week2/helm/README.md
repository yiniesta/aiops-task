# 为 Helm Demo 增加 Pre-install Hooks（Job 类型），并打印一段内容

## 执行

```bash
helm install vote . -n example --create-namespace 
@MacBook-Pro-2 helm % helm install vote . -n example --create-namespace 
NAME: vote
LAST DEPLOYED: Wed Oct  2 16:15:56 2024
NAMESPACE: example
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## 查看

```bash
@MacBook-Pro-2 helm % helm status vote -n example
NAME: vote
LAST DEPLOYED: Wed Oct  2 16:33:11 2024
NAMESPACE: example
STATUS: deployed
REVISION: 1
TEST SUITE: None
@MacBook-Pro-2 helm % helm uninstall vote -n example
release "vote" uninstalled
```

