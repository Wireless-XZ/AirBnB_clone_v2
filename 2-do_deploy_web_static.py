#!/usr/bin/python3
"""A Fabric script that distributes
an archive to your web servers"""
from fabric.api import *
import os


env.hosts = ["3.94.181.17", "54.157.165.12"]
env.user = "ubuntu"

def do_deploy(archive_path):
    """distributes an archive to your web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        arc = archive_path.split("/")[1]
        unarc = arc.strip(".tgz")
        main = "data/web_static/releases/{}".format(unarc)
        put(archive_path, '/tmp/')
        sudo('tar -xzf /tmp/{} -C {}/'.format(arc, main))
        sudo("rm -rf /tmp/{}".format(arc))
        sudo("rm /data/web_static/current")
        sudo('ln -s {}/ "/data/web_static/current"'.format(main))

        return True
    except:
        return False

