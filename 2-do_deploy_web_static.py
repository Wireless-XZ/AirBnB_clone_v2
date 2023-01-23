#!/usr/bin/python3
"""web server distribution"""
from fabric.api import *
import os.path
import tarfile
from datetime import datetime


env.hosts = ["3.94.181.17", "54.157.165.12"]
env.user = 'ubuntu'
env.key_filename = '~/key'


def do_pack():
    """The function that generates the .tgz file"""
    local("mkdir -p versions")
    date = str(datetime.now()).replace("-", "")\
                              .replace(":", "")\
                              .replace(" ", "")\
                              .replace(".", "")
    output_name = "web_static_" + date + ".tgz"

    tar = local('tar -cvzf versions/{} web_static'.format(output_name))

    if os.path.exists("./versions/{}".format(output_name)):
        return os.path.normpath("/versions/{}.tgz".format(output_name))
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers
    """
    if os.path.exists(archive_path) is False:
        return False

    arc = archive_path.split("/")
    base = arc[1].strip('.tgz')
    put(archive_path, '/tmp/')
    sudo('mkdir -p /data/web_static/releases/{}'.format(base))
    main = "/data/web_static/releases/{}".format(base)
    sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))
    sudo('rm /tmp/{}'.format(arc[1]))
    sudo('mv {}/web_static/* {}/'.format(main, main))
    sudo('rm -rf /data/web_static/current')
    sudo('ln -s {}/ "/data/web_static/current"'.format(main))
    return True
