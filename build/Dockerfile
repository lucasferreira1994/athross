FROM redhat/ubi9:9.6-1749542372

RUN yum install -y python3 python3-pip

WORKDIR /opt/app

COPY . /opt/app

RUN cp build/entrypoint.sh /usr/local/bin

RUN chmod 0755 /usr/local/bin/entrypoint.sh

#user app
RUN useradd -m app -d /opt/app -s /bin/bash

RUN chown -R app:app /opt/app

RUN pip3 install --upgrade pip \
    && pip3 install -r /opt/app/build/requirements.txt

EXPOSE 8080


CMD ["/usr/local/bin/entrypoint.sh"]