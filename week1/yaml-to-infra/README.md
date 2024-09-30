# 使用 YAML to Infra 模式创建云 Redis 数据库

## 执行命令

```bash
terraform init
terraform plan
terraform apply -auto-approve

export KUBECONFIG="$(pwd)/config.yaml"
kubectl apply -f tencent

# 获取vpc和subnet的id
kubectl -n crossplane-system get subnet  -ojsonpath='{$.items[0].status.atProvider.id}'
kubectl -n crossplane-system get vpc -ojsonpath='{$ .items[0].status.atProvider.id}' 

# 创建redis
kubectl apply -f tencent/redis.yaml

```


## 查看k8s命名空间内的资源

```bash
kubectl get all -n crossplane-system                                                   
NAME                                                      READY   STATUS    RESTARTS   AGE
pod/crossplane-79775db9c8-fnsrp                           1/1     Running   0          23m
pod/crossplane-rbac-manager-66998d5c5d-cx8zf              1/1     Running   0          23m
pod/provider-tencentcloud-8bf0507521fb-5fd5bc47dd-bqnn2   1/1     Running   0          13m

NAME                            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/crossplane-webhooks     ClusterIP   10.43.144.84    <none>        9443/TCP   23m
service/provider-tencentcloud   ClusterIP   10.43.146.210   <none>        9443/TCP   13m

NAME                                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/crossplane                           1/1     1            1           23m
deployment.apps/crossplane-rbac-manager              1/1     1            1           23m
deployment.apps/provider-tencentcloud-8bf0507521fb   1/1     1            1           13m

NAME                                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/crossplane-79775db9c8                           1         1         1       23m
replicaset.apps/crossplane-rbac-manager-66998d5c5d              1         1         1       23m
replicaset.apps/provider-tencentcloud-8bf0507521fb-5fd5bc47dd   1         1         1       13m

```

## 登录redis执行验证操作

```bash
[ crs-a96vw129 | DB0 ] # set a b
OK
[ crs-a96vw129 | DB0 ] # get a
b
[ crs-a96vw129 | DB0 ] # del a
1
[ crs-a96vw129 | DB0 ] # get a
null

```

## 删除资源
```bash
kubectl delete -f tencent/redis.yaml
kubectl delete all --all -n crossplane-system

terraform state rm 'helm_release.crossplane'
terraform state rm 'module.k3s'
terraform destroy -auto-approve

```