FROM ubuntu:jammy
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq install python3-pip

WORKDIR /client
COPY requirements.txt model/
RUN pip3 install -r model/requirements.txt
COPY model/train.py model/
COPY model/trained_model_rf.sav model/

COPY data/history.csv /data/
COPY database_load.py /client/
COPY parse.py /client/
COPY patients.db /client/
COPY preprocessing.py /client/
COPY client.py /client/

EXPOSE 8440
EXPOSE 8441
ENV MLLP_ADDRESS="host.docker.internal:8440"
ENV PAGER_ADDRESS="host.docker.internal:8441"
ENV PYTHONUNBUFFERED=1
RUN chmod +x /client/client.py
CMD ["python3", "/client/client.py --history=/hospital-history/history.csv"]