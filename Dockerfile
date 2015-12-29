# Using a compact OS
FROM ubuntu:14.04

MAINTAINER Liangchaob <liangchaob@163.com> 

# Add ITdmb stuff into daocloud server
COPY . /whenmgone

# Update sorcelist
RUN cp /etc/apt/sources.list /etc/apt/sources.list_backup

# apt-get
RUN apt-get update
RUN apt-get install -y libmysqld-dev
RUN apt-get install -y python-dev
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-pip


# pip
RUN pip install Flask
RUN pip install Flask-Bootstrap
RUN pip install Flask-Login
RUN pip install Flask-Mail
RUN pip install Flask-WTF
RUN pip install Jinja2
RUN pip install pymongo

# Adjust the python2.7 encoding
RUN cat /whenmgone/dockerpackage/sitecustomize.py_update >> /etc/python2.7/sitecustomize.py


# Open Ports
EXPOSE 80

WORKDIR /whenmgone/app/
CMD python main.py 