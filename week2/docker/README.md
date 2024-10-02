# 为这段 Golang 代码写一个多阶段构建的 Dockerfile： https://gist.github.com/abhishekkr/3beebbc1db54b3b54914#file-tcp_server-go

# 使用以下命令构建 Docker 镜像：
docker build -t test-go-app .

# 使用以下命令运行 Docker 容器：
docker run -d -p 3333:3333 test-go-app

## 查看

```bash
MacBook-Pro-2 docker % docker ps
CONTAINER ID   IMAGE                            COMMAND                  CREATED         STATUS         PORTS                                                                 NAMES
032d263d35fa   test-go-app                      "test-go-app"            5 seconds ago   Up 4 seconds   0.0.0.0:3333->3333/tcp                                                peaceful_tharp

```