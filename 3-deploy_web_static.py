#!/usr/bin/python3
""" deploy function module """
import os
from datetime import datetime
from fabric.api import env, local, put, run

def do_pack():
    """ generates a .tgz archive from the contents
    of the web_static folder """
    today = datetime.utcnow()
    archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        today.year, today.month, today.day,
        today.hour, today.minute, today.second)
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    if local("tar -cvzf {} web_static".format(archive)).failed:
        return None
    return archive

env.hosts = ['100.25.33.231', '54.237.87.188']


def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        file_name = file.split(".")[0]
        put(archive_path, "/tmp/")
        run("sudo mkdir -p /data/web_static/releases/{}/".format(file_name))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file, file_name))
        run("sudo rm /tmp/{}".format(file))
        run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(file_name, file_name))
        run("sudo rm -rf /data/web_static/releases/{}/web_static".format(file_name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name))
        return True
    except Exception:
        return False
    
def deploy():
    """  create and distribute an archive to a web server """
    return do_deploy(do_pack())
