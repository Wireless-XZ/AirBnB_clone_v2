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
    if not os.path.exists(archive_path):
        return False

    filename = os.path.basename(archive_path)
    filename_without_extension = os.path.splitext(filename)[0]

    # upload archive to /tmp/ directory on web server
    put(archive_path, '/tmp/')

    # uncompress archive to /data/web_static/releases/<filename without extension>
    run('mkdir -p /data/web_static/releases/{}/'.format(filename_without_extension))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, filename_without_extension))

    # delete archive from web server
    run('rm /tmp/{}'.format(filename))

    # delete symbolic link /data/web_static/current
    run('rm -rf /data/web_static/current')

    # create new symbolic link /data/web_static/current
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(filename_without_extension))
    return True
