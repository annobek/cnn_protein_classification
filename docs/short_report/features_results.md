Key features of the model:

| Number of layers|         Activation function|             Loss function|                 Optimizer|Learning rate|Batch size|
|----------------:|---------------------------:|-------------------------:|-------------------------:|------------:|---------:|
| 4 + output layer|                     Sigmoid|      Binary Cross Entropy|Adaptive Moment Estimation|       0.0001|        64|

Convolutional layers parameters:

|Layer|Input feature maps|Output feature maps|Kernel size|Stride|
|----:|-----------------:|------------------:|----------:|-----:|
|  1st|                10|                 32|          7|     2|
|  2nd|                32|                 64|          5|     2|
|  3rd|                64|                128|          3|     2|
|  4th|               128|                256|          3|     2|

Max pooling layers after each convolutional layer (kernel size of 2, stride of 2) were applied to reduce overfitting. The model was trained during 40 epoches. Sequences of the length of 1500 aminoacids were used for this experiment.

Results:

|Precision|Recall|F1-score|   MCC|
|--------:|-----:|-------:|-----:|
|   0.9806|0.9623|  0.9712|0.9704|


Conclusion: Given the provided protein dataset and defined hyperparameters, the model performs accurate. 