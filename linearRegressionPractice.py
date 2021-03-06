# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M0Y4wsM4m2G3E4Lj7qM6qo2cVFd-dut0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEED = 1234
NUM_SAMPLES = 50

np.random.seed(SEED)
#set seed for reproducibility

def generate_data(num_samples):
  # Generate dummy data for linear regression
  X = np.array(range(num_samples))
  random_noise = np.random.uniform(-10, 20, size = num_samples)
  y = 3.5* X + random_noise #add some noise
  return X, y

#generate random (linear) data
X, y = generate_data(num_samples = NUM_SAMPLES)
data = np.vstack([X, y]).T
print(data[:5])

#load into a pandas dataframe
df = pd.DataFrame(data, columns = ["X", "y"])
X = df[["X"]].values
y = df[["y"]].values
df.head()

#scatter plot
plt.title("Generate Data")
plt.scatter(x = df["X"], y = df["y"])
plt.show()

TRAIN_SIZE = 0.7
VAL_SIZE = 0.15
TEST_SIZE = 0.15

#SHUFFLE DATA
indices = list(range(NUM_SAMPLES))
np.random.shuffle(indices)
X = X[indices]
y = y[indices]

#split indices
train_start = 0
train_end = int(0.7 * NUM_SAMPLES)
val_start = train_end
val_end = int((TRAIN_SIZE + VAL_SIZE) * NUM_SAMPLES)
test_start = val_end

#split data
X_train = X[train_start: train_end]
y_train = y[train_start: train_end]
X_val = X[val_start: val_end]
y_val = y[val_start: val_end]
X_test = X[test_start: ]
y_test = y[test_start: ]
print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"X_val: {X_val.shape}, y_test: {y_val.shape}")
print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")

def standardize_data(data, mean, std):
  return (data - mean)/std

#determine means and stds
X_mean = np.mean(X_train)
X_std = np.std(X_train)
y_mean = np.mean(y_train)
y_std = np.std(y_train)

#Standardize
X_train = standardize_data(X_train, X_mean, X_std)
y_train = standardize_data(y_train, y_mean, y_std)
X_val = standardize_data(X_val, X_mean, X_std)
y_val = standardize_data(y_val, y_mean, y_std)
X_test = standardize_data(X_test, X_mean, X_std)
y_test = standardize_data(y_test, y_mean, y_std)

#check (means should be ~0 and std should be ~1)
#check (means should be ~0 and std should be ~1)
print(f"mean: {np.mean(X_test, axis = 0)[0]:.1f}, std: {np.std(X_test, axis = 0)[0]:.1f}")
print(f"mean: {np.mean(y_test, axis = 0)[0]:.1f}, std: {np.std(y_test, axis = 0)[0]:.1f}")

INPUT_DIM = X_train.shape[1] #X is 1-Dimensional
OUTPUT_DIM = y_train.shape[1] #Y is 1-Dimensional

#Initialize random weights
W = 0.01 * np.random.randn(INPUT_DIM, OUTPUT_DIM)
b = np.zeros((1, 1))
print(f"W: {W.shape}")
print(f"b: {b.shape}")

#Forward pass [NX1] , [1X1] = [NX1]
y_pred = np.dot(X_train, W) + b
print(f"y_pred: {y_pred.shape}")

#loss
N = len(y_train)
loss = (1/N) * np.sum((y_train - y_pred) ** 2)
print(f"loss: {loss:.2f}")

#backpropagation
dW = -(2/N) * np.sum((y_train - y_pred) * X_train)
db = -(2/N) * np.sum((y_train - y_pred) * 1)

LEARNING_RATE = 1e-1

#updated weights
W += -LEARNING_RATE *dW
b += -LEARNING_RATE * db

NUM_EPOCHS = 100

#INITIALIZE RANDOM WEIGHTS
W = 0.01 * np.random.randn(INPUT_DIM, OUTPUT_DIM)
b = np.zeros((1, ))

#training loop
for epoch_num in range(NUM_EPOCHS):
  #forward pass [NX1] * [1X1] = [NX1]
  y_pred = np.dot(X_train, W) + b

  #loss
  loss = (1/len(y_train)) * np.sum((y_train - y_pred) ** 2)

  #show progress
  if epoch_num % 10 == 0:
    print(f"Epoch: {epoch_num}, loss: {loss:.3f}")

    #backpropagation
    dW = -(2/N) * np.sum((y_train - y_pred) * X_train)
    db = -(2/N) * np.sum((y_train - y_pred) * 1)

    #updated weights
    W += -LEARNING_RATE * dW
    b += -LEARNING_RATE * db

# Predictions
pred_train = W*X_train + b
pred_test = W*X_test + b

# Train and test MSE
train_mse = np.mean((y_train - pred_train) ** 2)
test_mse = np.mean((y_test - pred_test) ** 2)
print (f"train_MSE: {train_mse:.2f}, test_MSE: {test_mse:.2f}")

# Figure size
plt.figure(figsize=(15,5))

# Plot train data
plt.subplot(1, 2, 1)
plt.title("Train")
plt.scatter(X_train, y_train, label="y_train")
plt.plot(X_train, pred_train, color="red", linewidth=1, linestyle="-", label="model")
plt.legend(loc="lower right")

# Plot test data
plt.subplot(1, 2, 2)
plt.title("Test")
plt.scatter(X_test, y_test, label='y_test')
plt.plot(X_test, pred_test, color="red", linewidth=1, linestyle="-", label="model")
plt.legend(loc="lower right")

# Show plots
plt.show()

# Unscaled weights
W_unscaled = W * (y_std/X_std)
b_unscaled = b * y_std + y_mean - np.sum(W_unscaled*X_mean)
print ("[actual] y = 3.5X + noise")
print (f"[model] y_hat = {W_unscaled[0][0]:.1f}X + {b_unscaled[0]:.1f}")