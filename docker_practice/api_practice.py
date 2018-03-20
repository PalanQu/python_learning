import os
import requests

DAEMON_URL = "http://127.0.0.1:2376"
def check_connection(daemon_url=DAEMON_URL):
    """
    Test the docker connection

    :param daemon_url: docker daemon url
    :return: the first parameter is equals to 200 or not, the second parameter is the response body
    """
    check_connection_url = os.path.join(daemon_url, "containers/json")
    params = {"all": 1}
    r = requests.get(url=check_connection_url, params=params)
    return r.status_code == 200, r.text


def create_container(
        container_name, *,
        daemon_url=DAEMON_URL,
        image="ubuntu"):
    """
    Create a new container

    :param container_name:  container name
    :param daemon_url: docker daemon url
    :param image: name of the image which you create the container based on
    :return: the first parameter is equals to 200 or not, the second parameter is the response body
    """

    r = requests.post(
        url=os.path.join(daemon_url, "containers/create"),
        params={"name": container_name},
        json={"Image": image},
        headers={"Content-Type": "application/json"})
    return r.status_code == 201, r.text


def commit_container(
        container_name, *,
        daemon_url=DAEMON_URL,
        comment="my comments"):
    """
    Commit the changes to container

    :param container_name: container name
    :param daemon_url: docker daemon url
    :param comment: the comment of the commit
    :return: the first parameter is equals to 200 or not, the second parameter is the response body
    """

    r = requests.post(
        url=os.path.join(daemon_url, "commit"),
        params={
            "container": container_name,
            "comment": comment
        },
        headers={"Content-Type": "application/json"})
    return r.status_code == 201, r.text


def push_modified_commit(
        repo_name="palanqu/docker_learning", *,
        daemon_url=DAEMON_URL,
        registry_auth):
    """
    Push the commit to repo
    :param repo_name: repo name
    :param daemon_url: docker daemon url
    :param registry_auth: the registry_auth of the user, you need commit the json like {"username":"","password":"", "auth":"","email":""} to base64
    :return: the first parameter is equals to 200 or not, the second parameter is the response body
    """
    r = requests.post(
        url=os.path.join(daemon_url, "images", repo_name, "push"),
        headers={"X-Registry-Auth": registry_auth})
    return r.status_code == 200, r.text


if __name__ == "__main__":
    image = "ubuntu"
    container_name = "ubuntu-container"
    registry_auth = "eyJ1c2VybmFtZSI6InBhbGFucXUiLCJwYXNzd29yZCI6Ik1ESjAyMTQ4MDQxOTMtKyIsICJhdXRoIjoiIiwiZW1haWwiOiJwYWxhbl93b3JrQDE2My5jb20ifQ"
    repo_name = "palanqu/docker_learning"
    comment = "commit test"

    if_connection_success, check_connection_response_text = \
        check_connection(DAEMON_URL)

    if if_connection_success:
        print("checked the connection")
        if_create_container_success, create_container_response_text = \
            create_container(
                container_name,
                daemon_url=DAEMON_URL,
                image=image)
        if if_create_container_success:
            print("create container success, container name: ",
                  container_name)
            if_commit_container_success, commit_container_response_text = \
                commit_container(
                    container_name,
                    daemon_url=DAEMON_URL,
                    comment=comment)
            if if_commit_container_success:
                print("commit container success")
                if_push_modified_commit_success, push_modified_commit_response_text = \
                    push_modified_commit(repo_name,
                                         daemon_url=DAEMON_URL,
                                         registry_auth=registry_auth)
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




