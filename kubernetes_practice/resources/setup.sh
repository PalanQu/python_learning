# pull ubuntu image
docker pull ubuntu

# use Dockerfile to build an docker image
docker build Dockerfile

# download minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# change the mod of minikube
chmod +x minikube

# move minikube to /use/local/bin so that we can use command 'minikube' directly
sudo mv minikube /usr/local/bin/

# start minikube
minikube start

# create deployment named logi
kubectl run -it --image=palanqu/docker_learning --port=8088 logi-test

# check the deployment
kubectl get deploy

# set the environment variable
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')

# start the script
kubectl exec $POD_NAME -- nohup ./start.sh > /dev/null 2>&1 &
