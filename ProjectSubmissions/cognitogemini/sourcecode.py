import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_algorithms.optimizers import COBYLA, ADAM, SPSA
from qiskit_algorithms.utils import algorithm_globals
from qiskit.primitives import Sampler
from qiskit.circuit.library import ZZFeatureMap, EfficientSU2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
import time

# Set random seed for reproducibility
algorithm_globals.random_seed = 12345  

# Define XOR dataset
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([0, 1, 1, 0])

# Normalize data to range [0, π] for better quantum encoding
scaler = MinMaxScaler(feature_range=(0, np.pi))
X_train_scaled = scaler.fit_transform(X_train)

# Define test datasets with more XOR-aligned points
X_test = np.array([
    [0.0, 0.0], [0.1, 0.9], [0.9, 0.1], [1.0, 1.0], 
    [0.2, 0.8], [0.8, 0.2], [0.4, 0.6], [0.6, 0.4]
])
y_test = np.array([0, 1, 1, 0, 1, 1, 1, 1])  # Expected labels
X_test_scaled = scaler.transform(X_test)

# Define feature map (improved with ZZFeatureMap)
num_qubits = 2
feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)

# Define a variational ansatz (EfficientSU2 for expressivity)
ansatz = EfficientSU2(num_qubits, entanglement="full", reps=3)

# Use Sampler primitive with shots for better statistics
sampler = Sampler(options={"shots": 5000})

# Define multiple optimizers
optimizers = [
    ("COBYLA", COBYLA(maxiter=500)),
    ("ADAM", ADAM(maxiter=300)),  # Fixed ADAM optimizer
    ("SPSA", SPSA(maxiter=200))
]

# Track best optimizer
best_accuracy = 0
best_classifier = None
best_optimizer_name = None

# Train quantum model with different optimizers
for optimizer_name, optimizer in optimizers:
    print(f"\nTraining with {optimizer_name} optimizer...")
    
    # Initialize quantum classifier
    quantum_classifier = VQC(
        optimizer=optimizer, 
        feature_map=feature_map,
        ansatz=ansatz,
        sampler=sampler,
        initial_point=algorithm_globals.random.random(ansatz.num_parameters),
        loss="cross_entropy",
        warm_start=True
    )
    
    # Train the quantum model
    try:
        start_time = time.time()
        quantum_classifier.fit(X_train_scaled, y_train)
        training_time = time.time() - start_time
        print(f"Training completed in {training_time:.2f} seconds")
        
        # Evaluate model
        y_pred_train = quantum_classifier.predict(X_train_scaled)
        train_accuracy = accuracy_score(y_train, y_pred_train)
        print(f"{optimizer_name} - Training accuracy: {train_accuracy:.4f}")

        y_pred_test = quantum_classifier.predict(X_test_scaled)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        print(f"{optimizer_name} - Test accuracy: {test_accuracy:.4f}, Predictions: {y_pred_test}")

        # Track best model
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            best_classifier = quantum_classifier
            best_optimizer_name = optimizer_name
            print(f"New best model found with {optimizer_name}!")

    except Exception as e:
        print(f"{optimizer_name} training failed: {e}")

# Use the best model
if best_classifier is not None:
    print(f"\nBest model trained with {best_optimizer_name} (accuracy: {best_accuracy:.4f})")
    quantum_classifier = best_classifier
else:
    print("All training attempts failed. Using last trained model.")

# Train classical model for comparison
classical_model = LogisticRegression()
classical_model.fit(X_train, y_train)
y_pred_classical = classical_model.predict(X_train)
classical_accuracy = accuracy_score(y_train, y_pred_classical)
print(f"Classical Model Accuracy on XOR training data: {classical_accuracy:.4f}")

# Visualization function
def plot_decision_boundary(classifier, scaler, title):
    x_min, x_max = -0.1, 1.1
    y_min, y_max = -0.1, 1.1
    step = 0.02
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step), np.arange(y_min, y_max, step))
    mesh_points = np.c_[xx.ravel(), yy.ravel()]
    mesh_points_scaled = scaler.transform(mesh_points)

    Z = classifier.predict(mesh_points_scaled)
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, cmap=plt.cm.RdBu, alpha=0.8)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=plt.cm.RdBu, edgecolors='k', s=80, label='Training')
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.RdBu, edgecolors='k', marker='s', s=60, alpha=0.7, label='Test')

    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title(title)
    plt.legend()
    plt.colorbar(label='Class prediction')
    plt.show()

# Plot decision boundary for the quantum model
try:
    plot_decision_boundary(quantum_classifier, scaler, f"Quantum Model Decision Boundary ({best_optimizer_name})")
except Exception as e:
    print(f"Could not plot decision boundary: {e}")

# Analyze predictions in detail
print("\nDetailed Prediction Analysis:")
for i, (x, y, pred) in enumerate(zip(X_test, y_test, quantum_classifier.predict(X_test_scaled))):
    correct = "✓" if y == pred else "✗"
    print(f"Test Point {x}: True={y}, Predicted={pred} {correct}")