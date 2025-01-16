## _cloud
This directory is dedicated to the deployment of other cloud infrastructure supporting our application.
Please take care not to commit any API keys or other sensitive information.

### TODO:
- See if you can allocate more resources to the poor pods.

### Useful commands

To apply ingress:\
`kubectl apply -f ingress.yaml`

To apply rabbitMQ:\
`helm repo add bitnami https://charts.bitnami.com/bitnami` \
`helm install my-release bitnami/rabbitmq-cluster-operator`

To see his status:\
`kubectl get deploy -w --namespace default -l app.kubernetes.io/name=rabbitmq-cluster-operator,app.kubernetes.io/instance=rabbit-release`
To config rabbit:\
```bash
username="$(kubectl get secret rabbit-default-user -o jsonpath='{.data.username}' | base64 --decode)"
echo "username: $username"
password="$(kubectl get secret rabbit-default-user -o jsonpath='{.data.password}' | base64 --decode)"
echo "password: $password"
kubectl port-forward "service/rabbit" 15672
```


