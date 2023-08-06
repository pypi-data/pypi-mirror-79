



Code example for XOR problem:
```
##first import tensorflow
import tensorflow as tf
##second import BrainMl
import BrainMl as dl
from BrainMl.layers import Dense,Dropout
from BrainMl.optimizer import Optimizer,Adam
##from BrainMl.activation import Activator,relu,softmax

##define an empty model
model=dl.Model()
##define Sequential model and add layers
save=model.Sequential([
    ##Here we add 4 dense layers and a Dropout
    Dense(4,activation="relu",shape=[2,2]),
    Dense(8, activation="relu"),
    Dense(2, activation="relu"),
    Dropout(0.9),
    Dense(1, activation="relu")

    ],name="model1")

## X is our data
X = [[0,0],[0,1],[1,0],[1,1]]
## y is our label
Y = [[0],[1],[1],[0]]

##we define an optimizer
optim=Adam(learning_rate=0.01)
##and compile the model along with optimizer
model.compile(optimizer=optim)
##than we start trainning the model
model.fit(X,Y,epochs=100,display=["all"])
##all-displays current epoch and error
##in list you can add "epoch"-to show just epoch or "error"-just for the error
```