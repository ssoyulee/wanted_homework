FROM python:3

###########################
## package update
###########################
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y vim
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

## pip update
###########################
RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /data01/source
#RUN cp -r /data01/source/ssg-item-sync/* /workspace/ssg-item-sync
#CMD sh deploy.sh

CMD tail -f /dev/null
