Deploying HunchWorks
====================

This is the configuration of my Fedora 15 staging server.

* [VirtualEnv](http://www.virtualenv.org) to isolate the environment.
* [Gunicorn](http://gunicorn.org) to serve the Django WSGI app.
* [Supervisor](http://supervisord.org) to keep the Gunicorns running.
* [Nginx](http://wiki.nginx.org) to proxy requests to the Gunicorns.


### Server Configuration

```bash
# Create an isolated environment.
$ sudo yum install python-virtualenv
$ virtualenv --no-site-packages --python=python2.7 hunchworks
$ cd hunchworks
$ source bin/activate

# Grab the latest source from GitHub.
$ sudo yum install git
$ git clone git://github.com/global-pulse/HunchWorks.git src
$ cd src

# Install PIL build dependencies.
$ sudo yum install gcc libxml2-devel libxslt-devel libjpeg-devel

# Install dependencies with Pip.
$ pip install -r requirements.txt
$ pip install gunicorn

# Spawn the SQLite database.
$ ./manage.py syncdb

# Install Supervisor.
# (See below for config.)
$ sudo yum install supervisor
$ sudo /etc/init.d/supervisord start
$ sudo chkconfig --levels 235 supervisord on

# Install MongoDB.
$ sudo yum install mongodb-server
$ sudo /etc/init.d/mongod start
$ sudo chkconfig --levels 235 mongod on

# Install Nginx.
# (See below for config.)
$ sudo yum install nginx
$ sudo /etc/init.d/nginx start
$ sudo chkconfig --levels 235 nginx on

# Open port 80.
$ sudo yum install lokkit
$ sudo lokkit -p http:tcp
```


### Supervisor Configuration

```
[program:hunchworks]
directory=/home/adammck/hunchworks/src
command=/home/adammck/hunchworks/bin/gunicorn_django -b 0.0.0.0:8001
environment=HUNCHWORKS_DEBUG=False
user=adammck
umask=022
autostart=True
autorestart=True
redirect_stderr=True
```


### Nginx Configuration

```
upstream hunchworks_server {
  server 127.0.0.1:8001 fail_timeout=0;
}

server {
  server_name hw.adammck.com;
  listen 80;

  error_page 500 /static/error/500.html;
  error_page 502 /static/error/502.html;

  location /static/ {
    root /home/adammck/hunchworks/src;
  }

  location / {
    proxy_pass http://hunchworks_server;
    proxy_redirect off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

### Sudoers Configuration

```
adammck ALL=(ALL) NOPASSWD: /usr/bin/supervisorctl
```