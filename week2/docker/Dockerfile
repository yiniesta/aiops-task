# 第一阶段：构建阶段
FROM golang:1.18 AS go-builder

ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOPROXY=https://goproxy.cn,direct

# 切换工作目录
WORKDIR /app
COPY go.mod .
COPY . .
# 获取依赖
RUN go mod download
# 构建应用程序
RUN go build -o /test-go-app

# 第二阶段：运行阶段
FROM alpine:3.14
# 从构建阶段复制二进制文件
COPY --from=go-builder /test-go-app /usr/local/bin/
# 设置环境变量
ENV LISTEN_HOST=0.0.0.0
ENV LISTEN_PORT=3333
# 暴露端口
EXPOSE $LISTEN_PORT
# 启动应用程序
CMD ["test-go-app"]