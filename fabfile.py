#!/usr/bin/env python

from fabric.api import cd, env, prefix, local, run

env.hosts = ["zoidberg.adammck.com"]
code_dir = "/home/adammck/hunchworks/src"


def test():
  local("./manage.py test hunchworks")

def stop():
  run("sudo supervisorctl stop hunchworks")

def start():
  run("sudo supervisorctl start hunchworks")

def deploy():
  test()
  stop()

  with cd(code_dir):
    with prefix("source ../bin/activate"):

      # trash any local changes and pull the latest code.
      run("git reset --hard")
      run("git clean -dfx")
      run("git pull")

      # install any new requirements.
      run("pip install -r requirements.txt")

      # spawn a pristine instance with sample data.
      run("./manage.py syncdb --noinput")
      run("./manage.py collectstatic --noinput")
      run("./manage.py loaddata sample_data")

  start()