# 实践 Terraform，开通腾讯云虚拟机，并安装 Docker

## 执行命令

```bash
terraform init
terraform plan
terraform apply -auto-approve
terraform destroy -auto-approve
```


## 登录服务器查看是否安装成功

```bash
[root@VM-0-14-rockylinux ~]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@VM-0-14-rockylinux ~]# systemctl status docker
● docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; preset: disabled)
     Active: active (running) since Mon 2024-09-30 16:27:31 CST; 48s ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 45634 (dockerd)
      Tasks: 9
     Memory: 23.9M
        CPU: 246ms
     CGroup: /system.slice/docker.service
             └─45634 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

Sep 30 16:27:30 VM-0-14-rockylinux systemd[1]: Starting Docker Application Container Engine...
Sep 30 16:27:30 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:30.881838164+08:00" level=info msg="Starting up"
Sep 30 16:27:30 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:30.940799368+08:00" level=info msg="Loading containers: start."
Sep 30 16:27:31 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:31.225813504+08:00" level=info msg="Loading containers: done."
Sep 30 16:27:31 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:31.243163760+08:00" level=warning msg="WARNING: bridge-nf-call-iptables is disabled"
Sep 30 16:27:31 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:31.243188221+08:00" level=warning msg="WARNING: bridge-nf-call-ip6tables is disabled"
Sep 30 16:27:31 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:31.243218869+08:00" level=info msg="Docker daemon" commit=41ca978 containerd-snapshotter=fals>
Sep 30 16:27:31 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:31.243331348+08:00" level=info msg="Daemon has completed initialization"
Sep 30 16:27:31 VM-0-14-rockylinux dockerd[45634]: time="2024-09-30T16:27:31.283266471+08:00" level=info msg="API listen on /run/docker.sock"
Sep 30 16:27:31 VM-0-14-rockylinux systemd[1]: Started Docker Application Container Engine.

```