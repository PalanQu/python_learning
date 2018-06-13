kubectl apply -f redis.yaml
kubectl exec -it  redis-deployment-7bb59c555d-mh7j8 -- /tmp/redis-stable/src/redis-trib.rb create --replicas 1 172.17.0.6:6379 172.17.0.8:6379 172.17.0.5:6379 172.17.0.9:6379 172.17.0.7:6379 172.17.0.3:6379
kubectl expose deployment redis-deployment --type=NodePort --name=redis-service

