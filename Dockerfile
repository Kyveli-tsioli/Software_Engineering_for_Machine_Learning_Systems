FROM python:3.10-slim

WORKDIR /model

COPY requirements.txt /model/requirements.txt
COPY Models/inference_model_version.pickle /model/Models/inference_model_version.pickle
COPY model.py /model/model.py
COPY training.py /model/training.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Grant execute permissions to the script
RUN chmod +x /model/model.py

CMD [ "python", "/model/model.py", "--input=/data/test.csv", "--output=/data/aki.csv" ]

