# coding: utf-8

import requests

#测试与docker的连接是否已经建立成功
def check_connection(url):
    check_connection_url = url + "/containers/json"
    params = {'all':1}
    response = requests.get(url=check_connection_url,params=params)



    if response.status_code == 200:
        return True
    else:
        return False

#建立一个新的container
def create_container(url, image, container_name):

    create_container_url = url + "/containers/create"
    request_data = {"Image": image}
    request_header = {"Content-Type": "application/json"}
    request_paras = {"name":container_name}

    response = requests.post(url=create_container_url,params=request_paras,json=request_data,headers=request_header)
    if response.status_code == 201:
        print("create container successful, container name:", container_name)
    else:
        print("create container fail, ", response.text)

#提交对container的修改
def commit_container(url, container_name, comment):
    commit_container_url = url + "/commit"
    request_header = {"Content-Type": "application/json"}
    request_paras = {"container": container_name, "comment": comment}

    response = requests.post(url=commit_container_url, params=request_paras, headers=request_header)
    print(response.status_code)
    if response.status_code == 201:
        print("commit successful")
    else:
        print("commit fail: ", response.text)

#将commit提交到repo上
def push_commit(url, registry_auth, repo_name):
    push_commit_url = url + "/images/" + repo_name + "/push"
    request_header = {"X-Registry-Auth": registry_auth}

    response = requests.post(push_commit_url, headers=request_header)
    print(push_commit_url)
    if response.status_code == 200:
        print("push successful")
    else:
        print("push fail: ", response.text)



if __name__ == '__main__':
    url = "http://127.0.0.1:2376"
    image = "ubuntu"
    container_name = "ubuntu-container"
    registry_auth = "eyJ1c2VybmFtZSI6InBhbGFucXUiLCJwYXNzd29yZCI6Ik1ESjAyMTQ4MDQxOTMtKyIsICJhdXRoIjoiIiwiZW1haWwiOiJwYWxhbl93b3JrQDE2My5jb20ifQ=="
    repo_name = "palanqu/docker_learning"

    if check_connection(url):
        print("checked the connection")
        create_container(url=url,image=image,container_name=container_name)
        commit_container(url=url,container_name=container_name, comment="commit test")
        push_commit(url=url,registry_auth=registry_auth,repo_name=repo_name)


    else:
        print("There is something wrong with the connection")




