FROM ubuntu:latest

LABEL maintainer="harshjais369@gmail.com" version="1.0" description="Docker image for restarting GCP spot VMs."

RUN apt -y update && apt -y upgrade
RUN apt -y install git && apt -y install curl && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt -y install python3 && python3 get-pip.py && pip3 install --upgrade pip
COPY . /root/harshjais369
WORKDIR /root/harshjais369
RUN pip3 install -U -r requirements.txt

# TODO: Replace these with your own ones or use a .env file
# ENV GOOGLE_APPLICATION_CREDENTIALS=/root/harshjais369/gcpproj-harshjais369_service_key.json
# ENV PROJECT_ID=gcpproj-harshjais369
# ENV ZONE=us-central1-c
# ENV INSTANCE_NAME=instance-6

CMD ["python3", "run.py"]
