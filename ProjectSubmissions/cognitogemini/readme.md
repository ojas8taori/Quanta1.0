# Quantum XOR Classification using Variational Quantum Classifier (VQC)

This project demonstrates how to use a Variational Quantum Classifier (VQC) to classify the XOR problem using Qiskit. The quantum classifier is compared against a classical logistic regression model.

## Project Overview
- Implements a quantum machine learning model using Qiskit.
- Trains the model on the XOR dataset.
- Uses different optimizers (COBYLA, ADAM, SPSA) to compare performance.
- Compares quantum classification with a classical logistic regression model.
- Visualizes the decision boundary of the trained quantum model.


## Dataset
The XOR dataset is used:
```
X_train = [[0,0], [0,1], [1,0], [1,1]]
y_train = [0, 1, 1, 0]
```
Additional test points are included to assess model performance.

## Feature Engineering
- Data is scaled to the range \([0, \pi]\) for better quantum encoding.
- Uses `ZZFeatureMap` for feature encoding.
- Uses `EfficientSU2` as the variational ansatz.

## Optimizers Used
- COBYLA
- ADAM
- SPSA

The best performing optimizer is selected based on test accuracy.

## Training and Evaluation
- The quantum classifier is trained using the `VQC` algorithm.
- Accuracy scores are calculated for both training and test datasets.
- A classical logistic regression model is trained for comparison.

## Visualization
- The decision boundary of the trained quantum model is plotted.
- Predictions on test data are analyzed.

## Results
- The best optimizer is selected based on test accuracy.
- Performance is compared to a classical model.

## Running the Code
Execute the script with:
```bash
python quantum_xor.py
```

## Author
Shubhaditya
Manasi
Likhita 

