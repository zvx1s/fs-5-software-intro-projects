# Import PyTorch and matplotlib
import torch
from torch import nn # nn contains all of PyTorch's building blocks for neural networks
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

car = make_car(desired_v=20.0, dt=0.1)

# Create weight and bias
weight = 0.7
bias = 0.3

# Create range values
start = 0
end = 20.0
step = 550

K_P = 0.4
K_I = 0.035
K_D = 0.1
    
STEPS = 550
    
X = torch.arange(start, end, step).unsqueeze(dim=1) # without unsqueeze, errors will happen later on (shapes within linear layers)
y = weight * X + bias
print([car["v"], car["desired_v"]], [calculate_desired_acceleration(car, K_P, K_I, K_D)])



# Split data
train_split = int(0.8 * len(X))
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]

len(X_train), len(y_train), len(X_test), len(y_test)

class LinearRegressionModelV2(nn.Module):
    def __init__(self):
        super().__init__()
        # Use nn.Linear() for creating the model parameters
        self.linear_layer = nn.Linear(in_features=2, 
                                    out_features=1)
    
    # Define the forward computation (input data x flows through nn.Linear())
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)

model_1 = LinearRegressionModelV2()
model_1, model_1.state_dict()



# Create the loss function
loss_fn = nn.L1Loss() # MAE loss is same as L1Loss

# Create the optimizer
optimizer = torch.optim.SGD(params=model_1.parameters(), # parameters of target model to optimize
                            lr=0.01) # learning rate (how much the optimizer should change parameters at each step, higher=more (less stable), lower=less (might take a long time))

# Make predictions with model
with torch.inference_mode(): 
    y_preds = model_1(X_test)

# Note: If you've reset your runtime, this function won't work, 
# you'll have to rerun the cell above where it's instantiated.
def plot_predictions(train_data=X_train, 
    train_labels=y_train, 
    test_data=X_test, 
    test_labels=y_test, 
    predictions=None):
    """
    Plots training data, test data and compares predictions.
    """
    plt.figure(figsize=(10, 7))

    # Plot training data in blue
    plt.scatter(train_data, train_labels, c="b", s=4, label="Training data")
    
    # Plot test data in green
    plt.scatter(test_data, test_labels, c="g", s=4, label="Testing data")

    if predictions is not None:
        # Plot the predictions in red (predictions were made on the test data)
        plt.scatter(test_data, predictions, c="r", s=4, label="Predictions")

    
    # Show the legend
    plt.legend(prop={"size": 14});

# Set the manual seed when creating the model (this isn't always needed but is used for demonstrative purposes, try commenting it out and seeing what happens)
torch.manual_seed(42)
model_1 = LinearRegressionModelV2()
model_1, model_1.state_dict()

#WRITE CODE HERE
velocities = torch.tensor([[]])
a_des = torch.tensor([])

'''learn passing in python function arguments in python docs, learn slicing, indexing'''

# Set the number of epochs 
epochs = 1000 

# Put data on the available device
# Without this, error will happen (not all model/data on device)
X_train = X_train.to(device)
X_test = X_test.to(device)
y_train = y_train.to(device)
y_test = y_test.to(device)

for epoch in range(epochs):
    ### Training
    model_1.train() # train mode is on by default after construction

    # 1. Forward pass
    y_pred = model_1(X_train)

    # 2. Calculate loss
    loss = loss_fn(y_pred, y_train)

    # 3. Zero grad optimizer
    optimizer.zero_grad()

    # 4. Loss backward
    loss.backward()

    # 5. Step the optimizer
    optimizer.step()

    ### Testing
    model_1.eval() # put the model in evaluation mode for testing (inference)
    # 1. Forward pass
    with torch.inference_mode():
        test_pred = model_1(X_test)
    
        # 2. Calculate the loss
        test_loss = loss_fn(test_pred, y_test)

    if epoch % 100 == 0:
        print(f"Epoch: {epoch} | Train loss: {loss} | Test loss: {test_loss}")

def a_des_over_time(calc_thrott):
    for i in range(STEPS):
        calc_des, error = calculate_desired_acceleration(car, K_P, K_I, K_D)
        calc_thrott = acceleration_to_throttle_percentage(calc_des, 1000, 5000)
        update(car, calc_thrott, 1000, 5000, 2.0)
        velocities.append([car["v"]], [car["desired_v"]])
        a_des.append([calc_des])
        

plt.figure()
plt.xlabel("time(s)")
plt.ylabel("velocity(m/s)")
plt.plot(velocities)
plt.figure()
plt.xlabel("time(s)")
plt.ylabel("errors(e)")
plot_predictions(predictions=y_preds)

plt.show()


