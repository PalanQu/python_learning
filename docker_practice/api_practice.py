import os
import requests

def check_connection(daemon_url="http://127.0.0.1:2376"):
    '''测试与docker的连接是否已经建立成功'''
    check_connection_url = os.path.join(daemon_url, "containers/json")
    params = {"all": 1}
    r = requests.get(url=check_connection_url, params=params)
    return [r.status_code == 200, r.text]


def create_container(
        container_name= "test-container", *,
        daemon_url="http://127.0.0.1:2376",
        image="ubuntu"):
    '''建立一个新的container'''
    params = {
        "create_container_url": os.path.join(daemon_url, "containers/create"),
        "request_data": {"Image": image},
        "request_header": {"Content-Type": "application/json"},
        "request_params": {"name": container_name}
    }
    r = requests.post(
        url=params["create_container_url"],
        params=params["request_params"],
        json=params["request_data"],
        headers=params["request_header"])
    return [r.status_code == 201, r.text]


def commit_container(
        container_name="ubuntu-test", *,
        daemon_url="http://127.0.0.1:2376",
        comment="my comments"):
    '''提交对container的修改'''
    params = {
        "commit_container_url": os.path.join(daemon_url, "commit"),
        "request_header": {"Content-Type": "application/json"},
        "request_paras": {"container": container_name, "comment": comment}
    }
    r = requests.post(
        url=params["commit_container_url"],
        params=params["request_paras"],
        headers=params["request_header"])
    return [r.status_code == 201, r.text]


def push_modified_commit(
        repo_name="palanqu/docker_learning", *,
        daemon_url="http://127.0.0.1:2376",
        registry_auth):
    '''将commit提交到repo上'''
    params = {
        "push_modified_commit_url":
            os.path.join(daemon_url, "images", repo_name, "push"),
        "request_header": {"X-Registry-Auth": registry_auth}
    }
    r = requests.post(
        url=params["push_modified_commit_url"],
        headers=params["request_header"])
    return [r.status_code == 200, r.text]


if __name__ == "__main__":
    params = {
        "daemon_url": "http://127.0.0.1:2376",
        "image": "ubuntu",
        "container_name": "ubuntu-container",
        "registry_auth": "eyJ1c2VybmFtZSI6InBhbGFucXUiLCJwYXNzd29yZCI6Ik1ESjAyMTQ4MDQxOTMtKyIsICJhdXRoIjoiIiwiZW1haWwiOiJwYWxhbl93b3JrQDE2My5jb20ifQ",
        "repo_name": "palanqu/docker_learning",
        "comment": "commit test"
    }
    if_connection_success, check_connection_response_text = \
        check_connection(params["daemon_url"])

    if if_connection_success:
        print("checked the connection")
        if_create_container_success, create_container_response_text = \
            create_container(
                params["container_name"],
                daemon_url=params["daemon_url"],
                image=params["image"])
        if if_create_container_success:
            print("create container success, container name: ",
                  params["container_name"])
            if_commit_container_success, commit_container_response_text = \
                commit_container(
                    params["container_name"],
                    daemon_url=params["daemon_url"],
                    comment=params["comment"])
            if if_commit_container_success:
                print("commit container success")
                if_push_modified_commit_success, push_modified_commit_response_text = \
                    push_modified_commit(params["repo_name"],
                                         daemon_url=params["daemon_url"],
                                         registry_auth=params["registry_auth"])
                if if_push_modified_commit_success:
                    print("push modified commit success")
                else:
                    print("push modified commit fail: ",
                          push_modified_commit_response_text)
            else:
                print("commit container fail: ",
                      commit_container_response_text)
        else:
            print("create container fail: ",
                  create_container_response_text)


    else:
        print("There is something wrong with the connection: ",
              check_connection_response_text)




