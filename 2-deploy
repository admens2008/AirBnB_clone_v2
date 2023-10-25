#!/usr/bin/python3
# Write a Fabric script (based on the file 1-pack_web_static.py)
# that distributes an archive to your web servers,
# using the function do_deploy
import os.path
from fabric.api import *

env.hosts = ["52.91.148.97", "54.82.199.153"]


def do_deploy(archive_path):
    """ Prototype: def do_deploy(archive_path):"""

    if os.path.isfile(archive_path) is False:
        return False
    filename = os.path.basename(archive_path)
    # remove '.tgz'
    name_only = os.path.splitext(filename)[0]

    if put(archive_path, "/tmp/{}".format(filename)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name_only)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name_only)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(filename, name_only)).failed is True:
        return False
    if run("rm /tmp/{}".format(filename)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(name_only, name_only)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name_only)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name_only)).failed is True:
        return False
    return True
