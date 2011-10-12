#!/usr/bin/env python

from fabric.api import cd, env, prefix, local, run

env.hosts = ["zoidberg.adammck.com"]
code_dir = "/home/adammck/hunchworks/src"


def test():
  local("./manage.py test hunchworks")

def update_requirements():
  with cd(code_dir):
    with prefix("source ../bin/activate"):
      run("pip install -r requirements.txt")

def purge():
  with cd(code_dir):
    run("git clean -fx")

def update_code():
  with cd(code_dir):
    run("git pull")

def update_database():
  with cd(code_dir):
    with prefix("source ../bin/activate"):
      run("./manage.py syncdb --noinput")
      run("./manage.py loaddata sample_data")

def stop():
  run("sudo supervisorctl stop hunchworks")

def start():
  run("sudo supervisorctl start hunchworks")

def deploy():
  test()
  stop()
  purge()
  update_code()
  update_database()
  start()