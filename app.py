import os
import subprocess
import requests
from backend import create_app
from flask import Response

app = create_app()


@app.route("/deploy", methods=["GET", "HEAD", "POST", "OPTIONS"])
def deploy():
    server_hash = (
        subprocess.check_output("git -C ~/app log -1 --pretty=format:%H", shell=True)
    ).decode("utf-8")
    gh_token = os.environ["PYBLOG_API_TOKEN"]
    headers = {"Authorization": f"Bearer {gh_token}"}
    headers["X-GitHub-Api-Version"] = "2022-11-28"
    headers["Accept"] = "application/vnd.github+json"
    src_hash = requests.get(
        "https://api.github.com/repos/chipndell/databox/commits", headers=headers
    ).json()[0]["sha"]
    if not src_hash == server_hash:
        subprocess.check_output("git -C ~/app pull -f origin master", shell=True)
        subprocess.check_output(
            "touch /var/www/mb9_pythonanywhere_com_wsgi.py", shell=True
        )
        return Response("Deploy done", status=200)
    return Response("No deploy needed.", status=403)


if __name__ == "__main__":
    app.run(debug=True)
