from flask import Flask, request
import subprocess
import time
import re
import threading

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("ref") == 'refs/heads/main':  # only main
        repository_name = data['repository']['name']
        commits = data['commits']
        for commit in commits:
            message = commit['message']
            if re.search(r'Merge pull request', message) or re.search(r'publish', message):  # only MR request
                print(f"update {repository_name} at {time.time()}\n")
                if repository_name == 'JobGPT-Frontend':
                    thread = threading.Thread(target=handle_frontend)
                    thread.start()
                if repository_name == 'JobGPT-Backend':
                    thread = threading.Thread(target=handle_backend)
                    thread.start()
    return 'OK', 200


def handle_backend():
    path = "/root/JobGPT-Backend"
    subprocess.call(["sh", "/root/JobGPT-Backend/scripts/bootstrap.sh"], cwd=path)


def handle_frontend():
    path = "/root/JobGPT-Frontend"
    subprocess.call(["sh", "/root/JobGPT-Frontend/bootstrap.sh"], cwd=path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666)
