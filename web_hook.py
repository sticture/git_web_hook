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
            if re.search(r'Merge pull request', message):  # only MR request
                print(f"update {repository_name} at {time.time()}\n")
                if repository_name == 'JA-FE':
                    thread = threading.Thread(target=handle_jafe)
                    thread.start()
                if repository_name == 'JobAssistant':
                    thread = threading.Thread(target=handle_jobassistant)
                    thread.start()
    return 'OK', 200


def handle_jobassistant():
    path = "/root/GoProject/JobAssistant"
    subprocess.call(["sh", "/root/GoProject/JobAssistant/bootstrap.sh"], cwd=path)


def handle_jafe():
    path = "/root/JA-FE"
    subprocess.call(["sh", "/root/JA-FE/bootstrap.sh"], cwd=path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666)
