import csv
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from connect import * 

# Initialize empty lists
states = []
wdl = []

# CSV file path
file_name = 'connect4_depth2_openingsd6nostart.csv'

# Read data from CSV file
with open(file_name, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)

    # Skip header if it exists
    next(reader)  # Skip the header row

    # Read each row and append to states and wdl lists
    for row in reader:
        states.append(row[0])  # Assuming states are in the first column
        wdl.append(float(row[1]))  # Assuming wdl are in the second column and converting to float

# Function to parse board and flatten into a 1D list of 42 elements
def parse_and_flatten(state):
    board = parse_board(stdBoard(), state)
    return flatten(board)

# Create x_train by parsing and flattening each state
x_train = np.array([parse_and_flatten(state) for state in states])

# Convert y_train to numpy array and reshape for compatibility with Keras
y_train = np.array(wdl)
y_train = y_train.reshape(-1, 1)  # Reshape to (num_samples, 1)

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

# Define the neural network model
model = Sequential([
    Dense(256, activation='sigmoid', input_shape=(42,)),  # 16 hidden nodes
    Dense(1, activation='sigmoid')  # 1 output node
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print model summary
model.summary()

# Define early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True)

# Train the model with early stopping
history = model.fit(x_train, y_train, epochs=1000, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model on test data
loss, accuracy = model.evaluate(x_test, y_test)
print(f'Final test loss: {loss:.4f}, test accuracy: {accuracy:.4f}')

# Save the model (optional)
model.save('connect4_512x1_model.h5')

# Best acc x64x1: 0.6711
# Best acc x128x1: 0.6948 (0.6884)
# Best acc x256x1: 0.7274 (0.7176)
# Best acc x512x1: 0.7171 (0.7094)

# D6 Opening Data
# Best acc x256x1: 