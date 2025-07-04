# AIOps Training Camp - Comprehensive API Documentation

## Project Overview

This repository contains homework assignments for the AIOps Training Camp, organized into three main weeks covering infrastructure automation, containerization, and AI-powered operations.

## Table of Contents

1. [Week 1: Infrastructure as Code (Terraform + Crossplane)](#week-1-infrastructure-as-code)
2. [Week 2: Containerization and Orchestration](#week-2-containerization-and-orchestration)
3. [Week 3: AI-Powered Operations (Function Calling)](#week-3-ai-powered-operations)

---

## Week 1: Infrastructure as Code

### Overview
Week 1 demonstrates the "YAML to Infrastructure" pattern using Terraform and Crossplane to provision cloud resources on Tencent Cloud.

### Components

#### Terraform Modules

##### Main Infrastructure Module (`week1/yaml-to-infra/`)

**Variables** (`variables.tf`)
```hcl
variable "secret_id" {
  description = "Tencent Cloud Secret ID"
  type        = string
  default     = ""
}

variable "secret_key" {
  description = "Tencent Cloud Secret Key"
  type        = string
  default     = ""
}

variable "regoin" {
  description = "Tencent Cloud Region"
  type        = string
  default     = "ap-hongkong"
}

variable "password" {
  description = "Default password for resources"
  type        = string
  default     = "AIOps@pwd2024"
}

variable "name" {
  description = "Resource name prefix"
  type        = string
  default     = "week01-yaml-to-infra"
}
```

**Usage Example:**
```bash
# Initialize Terraform
terraform init

# Plan infrastructure changes
terraform plan

# Apply infrastructure
terraform apply -auto-approve

# Set kubeconfig
export KUBECONFIG="$(pwd)/config.yaml"

# Apply Crossplane resources
kubectl apply -f tencent/
```

#### Crossplane Resources (`week1/yaml-to-infra/tencent/`)

##### VPC Configuration
**File:** `vpc.yaml`
```yaml
apiVersion: vpc.tencentcloud.crossplane.io/v1alpha1
kind: VPC
metadata:
  name: example-redis-vpc
spec:
  forProvider:
    cidrBlock: "10.2.0.0/16"
    name: "test-crossplane-redis-vpc"
```

##### Subnet Configuration
**File:** `subnet.yaml`
```yaml
apiVersion: vpc.tencentcloud.crossplane.io/v1alpha1
kind: Subnet
metadata:
  name: example-redis-subnet
spec:
  forProvider:
    availabilityZone: "ap-hongkong-1"
    cidrBlock: "10.2.1.0/24"
    name: "test-crossplane-redis-subnet"
    vpcIdSelector:
      matchLabels:
        name: example-redis-vpc
```

##### Redis Instance Configuration
**File:** `redis.yaml`
```yaml
apiVersion: redis.tencentcloud.crossplane.io/v1alpha1
kind: Instance
metadata:
  name: example-redis
spec:
  forProvider:
    availabilityZone: "ap-hongkong-1"
    memSize: 1024
    name: "test-crossplane-redis"
    password: "AIOps@pwd2024"
    port: 6379
    projectId: 0
    redisShardNum: 1
    redisReplicasNum: 1
    subnetIdSelector:
      matchLabels:
        name: example-redis-subnet
    typeId: 6
    vpcIdSelector:
      matchLabels:
        name: example-redis-vpc
```

#### Terraform Direct Module (`week1/terraform/`)

**CVM (Cloud Virtual Machine) Configuration** (`cvm.tf`)
```hcl
resource "tencentcloud_instance" "cvm" {
  instance_name              = var.name
  availability_zone          = data.tencentcloud_availability_zones.default.zones.0.name
  image_id                   = data.tencentcloud_images.default.images.0.image_id
  instance_type              = data.tencentcloud_instance_types.default.instance_types.0.instance_type
  system_disk_type           = "CLOUD_PREMIUM"
  system_disk_size           = 50
  hostname                   = var.name
  project_id                 = 0
  vpc_id                     = tencentcloud_vpc.vpc.id
  subnet_id                  = tencentcloud_subnet.subnet.id
  internet_max_bandwidth_out = 100

  data_disks {
    data_disk_type = "CLOUD_PREMIUM"
    data_disk_size = 50
    encrypt        = false
  }

  security_groups = [tencentcloud_security_group.default.id]
  password        = var.password

  tags = {
    Name = var.name
  }
}
```

### API Reference

#### Terraform Commands
```bash
# Initialize the working directory
terraform init

# Create an execution plan
terraform plan

# Apply the configuration
terraform apply [-auto-approve]

# Destroy the infrastructure
terraform destroy [-auto-approve]

# Show current state
terraform show

# List resources in state
terraform state list
```

#### Crossplane Commands
```bash
# Apply Crossplane configurations
kubectl apply -f tencent/

# Get VPC ID
kubectl -n crossplane-system get vpc -ojsonpath='{$.items[0].status.atProvider.id}'

# Get Subnet ID
kubectl -n crossplane-system get subnet -ojsonpath='{$.items[0].status.atProvider.id}'

# Check resource status
kubectl get all -n crossplane-system
```

---

## Week 2: Containerization and Orchestration

### Overview
Week 2 focuses on containerizing a Go TCP server application and deploying it using Docker and Helm on Kubernetes.

### Components

#### Go TCP Server (`week2/docker/tcp_server.go`)

**Public Functions:**

##### `main()`
**Description:** Entry point that starts the TCP server
**Parameters:** None
**Returns:** None
**Usage:**
```go
func main() {
    l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
    if err != nil {
        fmt.Println("Error listening:", err.Error())
        os.Exit(1)
    }
    defer l.Close()
    fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)

    for {
        conn, err := l.Accept()
        if err != nil {
            fmt.Println("Error accepting: ", err.Error())
            os.Exit(1)
        }
        go handleRequest(conn)
    }
}
```

##### `handleRequest(conn net.Conn)`
**Description:** Handles incoming TCP connections
**Parameters:**
- `conn`: Network connection object
**Returns:** None
**Usage:**
```go
func handleRequest(conn net.Conn) {
    buf, read_err := ioutil.ReadAll(conn)
    if read_err != nil {
        fmt.Println("failed:", read_err)
        return
    }
    fmt.Println("Got: ", string(buf))

    _, write_err := conn.Write([]byte("Message received.\n"))
    if write_err != nil {
        fmt.Println("failed:", write_err)
        return
    }
    conn.Close()
}
```

**Constants:**
```go
const (
    CONN_HOST = "localhost"  // Server host
    CONN_PORT = "3333"       // Server port
    CONN_TYPE = "tcp"        // Connection type
)
```

#### Docker Configuration

##### Multi-stage Dockerfile (`week2/docker/Dockerfile`)
```dockerfile
# Build stage
FROM golang:1.18 AS go-builder
ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOPROXY=https://goproxy.cn,direct

WORKDIR /app
COPY go.mod .
COPY . .
RUN go mod download
RUN go build -o /test-go-app

# Runtime stage
FROM alpine:3.14
COPY --from=go-builder /test-go-app /usr/local/bin/
ENV LISTEN_HOST=0.0.0.0
ENV LISTEN_PORT=3333
EXPOSE $LISTEN_PORT
CMD ["test-go-app"]
```

**Docker Commands:**
```bash
# Build the Docker image
docker build -t test-go-app .

# Run the container
docker run -d -p 3333:3333 test-go-app

# Check running containers
docker ps

# Test the TCP server
echo "Hello World" | nc localhost 3333
```

#### Helm Chart (`week2/helm/`)

##### Chart Configuration (`Chart.yaml`)
```yaml
apiVersion: v2
name: vote
description: A Helm chart for voting app
type: application
version: 0.1.0
appVersion: "1.16.0"
```

##### Values Configuration (`values.yaml`)
```yaml
worker:
  image: dockersamples/examplevotingapp_worker
  tag: latest

vote:
  image: dockersamples/examplevotingapp_vote
  tag: latest

result:
  image: dockersamples/examplevotingapp_result
  tag: latest

redis:
  deploy: true

postgres:
  deploy: true
```

##### Template Examples

**Vote Deployment** (`templates/vote-deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: vote
  name: vote
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vote
  template:
    metadata:
      labels:
        app: vote
    spec:
      containers:
      - image: "{{ .Values.vote.image }}:{{ .Values.vote.tag }}"
        name: vote
        ports:
        - containerPort: 80
          name: vote
```

**Pre-install Hook** (`templates/pre-install.yaml`)
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "vote.fullname" . }}-pre-install"
  labels:
    {{- include "vote.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: pre-install-job
        image: busybox
        command: ['sh', '-c', 'echo "Pre-install hook executed successfully!"']
```

### API Reference

#### Helm Commands
```bash
# Install the chart
helm install vote . -n example --create-namespace

# Upgrade the release
helm upgrade vote . -n example

# Check release status
helm status vote -n example

# List releases
helm list -n example

# Uninstall the release
helm uninstall vote -n example

# Dry run (template rendering)
helm install vote . --dry-run --debug
```

---

## Week 3: AI-Powered Operations

### Overview
Week 3 implements an AI-powered operations system using OpenAI's function calling capabilities to manage Kubernetes resources.

### Components

#### Main Application (`week3/main.py`)

**Public Functions:**

##### `modify_config(service_name, key, value)`
**Description:** Modifies service configuration parameters
**Parameters:**
- `service_name` (str): Name of the service to modify
- `key` (str): Configuration key to update
- `value` (str): New value for the configuration
**Returns:** None
**Usage:**
```python
modify_config("gateway", "vendor", "alipay")
# Output: gateway vendor alipay
```

##### `restart_service(service_name)`
**Description:** Restarts a specified service
**Parameters:**
- `service_name` (str): Name of the service to restart
**Returns:** None
**Usage:**
```python
restart_service("gateway")
# Output: gateway
```

##### `apply_manifest(resource_type, image)`
**Description:** Deploys a Kubernetes resource with specified image
**Parameters:**
- `resource_type` (str): Type of Kubernetes resource (e.g., "deployment")
- `image` (str): Container image to deploy
**Returns:** None
**Usage:**
```python
apply_manifest("deployment", "nginx:latest")
# Output: deployment nginx:latest
```

##### `analyze_loki_log(query_str)`
**Description:** Analyzes logs from Loki logging system
**Parameters:**
- `query_str` (str): Loki query string (e.g., '{app="grafana"} |= "Error"')
**Returns:** JSON string containing log analysis results
**Usage:**
```python
result = analyze_loki_log('{app="grafana"} |= "Error"')
# Returns: {"log": "this is error log"}
```

##### `run_conversation()`
**Description:** Main conversation loop that processes user queries and calls appropriate functions
**Parameters:** None
**Returns:** None
**Usage:**
```python
run_conversation()
# Prompts for user input and processes commands
```

#### OpenAI Function Definitions

The system defines four main functions for the AI model:

##### Function: `modify_config`
```json
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
          "description": "服务的名称，例如 \"nginx\""
        },
        "key": {
          "type": "string",
          "description": "配置的 key，例如 'replicas'"
        },
        "value": {
          "type": "string",
          "description": "配置的 value，例如 '3'"
        }
      },
      "required": ["service_name", "key", "value"]
    }
  }
}
```

##### Function: `restart_service`
```json
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
          "description": "服务的名称，例如 'nginx'"
        }
      },
      "required": ["service_name"]
    }
  }
}
```

##### Function: `apply_manifest`
```json
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
          "description": "资源的类型，例如 'deployment'"
        },
        "image": {
          "type": "string",
          "description": "镜像的名称，例如 'nginx:latest'"
        }
      },
      "required": ["resource_type", "image"]
    }
  }
}
```

##### Function: `analyze_loki_log`
```json
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
          "description": "Loki 查询字符串，例如：{app=\"grafana\"} |= \"Error\""
        }
      },
      "required": ["query_str"]
    }
  }
}
```

### API Reference

#### OpenAI Client Configuration
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxxxx",
    base_url="https://api.apiyi.com/v1",
)
```

#### Usage Examples

##### Example 1: Modify Service Configuration
**Input:** "帮我修改 gateway 的配置，vendor 修改为 alipay"
**Function Called:** `modify_config`
**Parameters:** `{"service_name":"gateway","key":"vendor","value":"alipay"}`
**Output:** `gateway vendor alipay`

##### Example 2: Restart Service
**Input:** "帮我重启 gateway 服务"
**Function Called:** `restart_service`
**Parameters:** `{"service_name":"gateway"}`
**Output:** `gateway`

##### Example 3: Deploy Application
**Input:** "帮我部署一个 deployment，镜像是 nginx"
**Function Called:** `apply_manifest`
**Parameters:** `{"image":"nginx","resource_type":"deployment"}`
**Output:** `deployment nginx`

##### Example 4: Analyze Logs
**Input:** "查看 app=grafana 且关键字包含 Error 的日志"
**Function Called:** `analyze_loki_log`
**Parameters:** `{"query_str":"{app=\"grafana\"} |= \"Error\""}`
**Output:** `{"log": "this is error log"}`

#### Running the Application
```bash
# Install dependencies
pip install openai

# Run the application
python main.py

# Follow the prompts to enter commands
```

---

## Common Patterns and Best Practices

### Infrastructure as Code
1. **Declarative Configuration**: Use YAML/HCL to define desired state
2. **Version Control**: Keep all infrastructure code in version control
3. **Modular Design**: Break infrastructure into reusable modules
4. **State Management**: Use remote state for Terraform

### Containerization
1. **Multi-stage Builds**: Optimize image size and security
2. **Environment Variables**: Configure applications via environment
3. **Health Checks**: Implement proper health check endpoints
4. **Resource Limits**: Set appropriate CPU and memory limits

### Kubernetes Deployment
1. **Helm Charts**: Use templates for reusable deployments
2. **ConfigMaps/Secrets**: Externalize configuration
3. **Rolling Updates**: Implement zero-downtime deployments
4. **Monitoring**: Add observability to all components

### AI-Powered Operations
1. **Function Definitions**: Clearly define function parameters and descriptions
2. **Error Handling**: Implement robust error handling for AI interactions
3. **Validation**: Validate AI responses before executing operations
4. **Logging**: Log all AI decisions and actions for audit trails

---

## Security Considerations

### Secrets Management
- Never commit sensitive data to version control
- Use environment variables or secret management systems
- Rotate credentials regularly
- Implement least privilege access

### Container Security
- Use minimal base images (e.g., Alpine Linux)
- Scan images for vulnerabilities
- Run containers as non-root users
- Keep dependencies updated

### Kubernetes Security
- Use RBAC for access control
- Implement network policies
- Scan manifests for security issues
- Use admission controllers

---

## Troubleshooting

### Common Issues

#### Terraform
```bash
# State lock issues
terraform force-unlock <LOCK_ID>

# Refresh state
terraform refresh

# Import existing resources
terraform import <resource_type>.<name> <resource_id>
```

#### Docker
```bash
# Check container logs
docker logs <container_id>

# Execute commands in container
docker exec -it <container_id> /bin/sh

# Clean up unused resources
docker system prune
```

#### Kubernetes
```bash
# Check pod status
kubectl describe pod <pod_name>

# View logs
kubectl logs <pod_name>

# Port forward for debugging
kubectl port-forward <pod_name> <local_port>:<pod_port>
```

#### AI Operations
```bash
# Check OpenAI API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models

# Validate function definitions
python -c "import json; print(json.loads(function_definition))"
```

---

## Contributing

When contributing to this project:

1. Follow the established patterns for each week
2. Update documentation for any new APIs or functions
3. Include usage examples for new components
4. Test all functionality before submitting
5. Use descriptive commit messages

## License

This project is part of the AIOps Training Camp educational materials.