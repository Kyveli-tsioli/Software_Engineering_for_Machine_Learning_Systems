# SWEMLS: Coursework 3: Implementing inference

### Modelling

A logistic regression model was trained on the training dataset. The input features used are the: a) age,
b) gender, c) minimum creatinine measurement, d) mean creatinine measurement, e) most recent
creatinine measurement for each patient. The code for training is located at ```train.py```.
The trained model is stored  in ```model/trained_model.sav```.

By splitting the training dataset in 80%-20% for training and test examples, the model showed an F3 score
of approximately 99%.

### Inference

The trained model is then used in our inference system to detect acute kidney injury (AKI) from blood test results sent by a simulator program. If our model predicts AKI, the system will send a pager request with the patient's MRN.

### External Libraries Used
For the implementation, the ```scikit-learn``` package was used for the training of 
the logistic regression model. The built-in model is optimised in terms of computational speed
and memory requirements. Moreover, the ```numpy``` package was used to speed up certain preprocessing
computations, like finding the mean and median of measurements.


### Running the Inference System

To run the code, follow these steps:

1. ```docker build -t coursework3 .```

2. ```docker run coursework3```
   
This will connect a client to the default ports for MLLP (8440) and pager (8441) systems. In order
to customize the port numbers, please pass in new values for environment variables ```MLLP_ADDRESS```
and ```PAGER_ADDRESS``` when running the docker, i.e. 
``` 
docker run \
--env MLLP_ADDRESS=host.docker.internal:8440 \
--env PAGER_ADDRESS=host.docker.internal:8441 \
coursework3
```
# Software_Engineering_for_Machine_Learning_Systems
