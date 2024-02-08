FROM ubuntu:jammy
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq install python3-pip
COPY requirements.txt /model/
RUN pip3 install -r /model/requirements.txt

COPY model/model.py /model/
COPY model/preprocess_data.py /model/
COPY model/train.py /model/
COPY model/trained_model.sav /model/

COPY parse.py /simulator/
COPY patients.db /simulator/
COPY tests/aki.csv /simulator/
COPY preprocessing.py /simulator/
COPY client.py /simulator/
COPY simulator.py /simulator/
COPY simulator_test.py /simulator/

WORKDIR /simulator
# RUN ./simulator_test.py
COPY messages.mllp /data/
EXPOSE 8440
EXPOSE 8441
# CMD /simulator/simulator.py --messages=/data/messages.mllp
ENV MLLP_ADDRESS="host.docker.internal:8440"
ENV PAGER_ADDRESS="host.docker.internal:8441"
# RUN chmod +x /simulator/client.py
CMD ["python3", "/simulator/client.py"]
# access port that they sent over
# CMD /model/model.py --input=/data/test.csv --output=/data/aki.csv