#!/usr/bin/python3
"""web server distribution"""
from fabric.api import *
import os.path
import tarfile
from datetime import datetime


env.hosts = ["54.87.250.97", "54.85.91.142"]


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
    arc_file_without_ext = arc[1].strip('.tgz')

    # upload the archive to /tmp/
    put(archive_path, '/tmp/{}'.format(arc[1]), use_sudo=True)

    # uncompress the archive
    sudo('mkdir -p /data/web_static/releases/{}'.format(arc_file_without_ext))
    main = "/data/web_static/releases/{}".format(arc_file_without_ext)
    sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))

    # delete the archive file
    sudo('rm /tmp/{}'.format(arc[1]))

    # move uncompressed file's content
    sudo('mv {}/web_static/* {}/'.format(main, main))

    # remove uncompressed folder
    sudo('rm -rf {}/web_static/'.format(main))

    # remove old symlink
    sudo('rm -rf /data/web_static/current')

    # create new symlink
    sudo('ln -s {}/ "/data/web_static/current"'.format(main))

    return True


def deploy():
    """  creates and distributes an archive to your web servers """
    path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
