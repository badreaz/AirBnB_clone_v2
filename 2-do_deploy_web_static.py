#!/usr/bin/python3
""" do_depoy function module """
import os
from fabric.api import env, put, run

env.hosts = ['100.25.33.231', '54.237.87.188']


def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1].split(".")[0]
        put(archive_path, "/tmp/")
        run("rm -rf /data/web_static/releases/{}/".format(file))
        run("mkdir -p /data/web_static/releases/{}/".format(file))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file + ".tgz", file))
        run("rm /tmp/{}".format(file + ".tgz"))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(file, file))
        run("rm -rf /data/web_static/releases/{}/web_static".format(file))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ \
            /data/web_static/releases/{}/".format(file))
        return True
    except Exception:
        return False
