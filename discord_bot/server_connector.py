import requests
    


class ServerConnector:
    def __init__(self, url, port, auth_token):
        self.url = url
        self.port = port
        self.auth_token = auth_token
        
    def get_server_status(self):
        response = requests.get(f"http://{self.url}:{self.port}/service/status", headers={"Authorization": "Bearer " + self.auth_token})
        if response.status_code == 200:
            return response.json()["isRunning"]
        else:
            raise Exception("Error getting server status: " + response.text)

    def get_server_logs(self):
        response = requests.get(f"http://{self.url}:{self.port}/service/logs", headers={"Authorization": "Bearer " + self.auth_token})
        if response.status_code == 200:
            return response.json()["logs"]
        else:
            raise Exception("Error getting server logs: " + response.text)
    
    def post_stop_server(self):
        response = requests.post(f"http://{self.url}:{self.port}/service/stop", headers={"Authorization": "Bearer " + self.auth_token})
        if response.status_code == 200:
            return True
        else:
            return False
        
    def post_start_server(self):
        response = requests.post(f"http://{self.url}:{self.port}/service/start", headers={"Authorization": "Bearer " + self.auth_token})
        if response.status_code == 200:
            return True
        else:
            return False
    
    def post_restart_server(self):
        response = requests.post(f"http://{self.url}:{self.port}/service/restart", headers={"Authorization": "Bearer " + self.auth_token})
        if response.status_code == 200:
            return True
        else:
            return False


    def send_message(self, message):
        requests.post(f"http://{self.url}:{self.port}", data=message)

    def send_file(self, file):
        requests.post(f"http://{self.url}:{self.port}", files=file)