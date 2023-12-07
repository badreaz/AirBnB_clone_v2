#!/usr/bin/python3
""" do_pack function module """
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """ generates a .tgz archive from the contents
    of the web_static folder """
    today = datetime.utcnow()
    archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        today.year, today.month, today.day,
        today.hour, today.minute, today.second)
    if not os.path.isdir("veersions"):
        os.mkdir("versions")
    if local("tar -cvzf {} web_static".format(archive)).failed:
        return None
    return archive
