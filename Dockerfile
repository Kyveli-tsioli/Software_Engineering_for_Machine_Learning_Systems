FROM ubuntu:jammy
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq install python3-pip

COPY requirements.txt /model/
RUN pip3 install -r /model/requirements.txt
COPY model/train.py /model/
COPY model/trained_model.sav /model/

COPY parse.py /client/
COPY database/patients.db /client/
COPY preprocessing.py /client/
COPY client.py /client/

WORKDIR /client
EXPOSE 8440
EXPOSE 8441
ENV MLLP_ADDRESS="host.docker.internal:8440"
ENV PAGER_ADDRESS="host.docker.internal:8441"
# RUN chmod +x /simulator/client.py
CMD ["python3", "/client/client.py"]