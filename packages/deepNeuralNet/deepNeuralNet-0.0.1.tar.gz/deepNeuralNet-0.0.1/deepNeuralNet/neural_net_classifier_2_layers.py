class create_train_NNclassifier_2:

    def __init__(self, X, Y, layers_dim, learning_rate=0.001, iter=3000, print_cost=False, plot_cost=False):


        import numpy as np
        import pandas as pd 
        import matplotlib.pyplot as plt
        

        (n_x, n_h, n_y) = layers_dim
        self.n_x = n_x
        self.n_h = n_h
        self.n_y = n_y

        np.random.seed(1)
        self.grads = {}
        self.costs = []              
        self.m = X.shape[1] 
        self.learning_rate = learning_rate
        self.iter = iter
        
        self.parameters = self.initialize_parameters()

        W1 = self.parameters["W1"]
        b1 = self.parameters["b1"]
        W2 = self.parameters["W2"]
        b2 = self.parameters["b2"]

        for i in range(0,self.iter):
            
            A1, cache1 = self.linear_activation_forward(X, W1, b1, "relu")
            A2, cache2 = self.linear_activation_forward(A1, W2, b2, "sigmoid")


            cost = self.compute_cost(A2, Y)

            dA2 = - (np.divide(Y, A2) - np.divide(1 - Y, 1 - A2))

            dA1, dW2, db2 = self.linear_activation_backward(dA2, cache2, "sigmoid")
            dA0, dW1, db1 = self.linear_activation_backward(dA1, cache1, "relu")


            self.grads['dW1'] = dW1
            self.grads['db1'] = db1
            self.grads['dW2'] = dW2
            self.grads['db2'] = db2


            self.parameters = self.update_parameters(self.parameters, self.grads)


            W1 = self.parameters["W1"]
            b1 = self.parameters["b1"]
            W2 = self.parameters["W2"]
            b2 = self.parameters["b2"]


            if print_cost and i % 100 == 0:
                print("Cost after iteration {}: {}".format(i, np.squeeze(cost)))
            if print_cost and i % 100 == 0:
                self.costs.append(cost)


        if(plot_cost):
            self.plot_cost()
            
    def initialize_parameters(self):

        import numpy as np

        W1 = np.random.randn(self.n_h, self.n_x)*0.01
        b1 = np.zeros((self.n_h,1))
        W2 = np.random.randn(self.n_y, self.n_h)*0.01
        b2 = np.zeros((self.n_y,1))

        parameters = {"W1": W1, "b1": b1, "W2": W2, "b2": b2}

        return parameters



    def sigmoid(self, z):

        import numpy as np
        
        A = 1/(1+np.exp(-z))
        cache = z
        
        return A, cache


    def relu(self, z):

        import numpy as np

        A = np.maximum(0,z)
    
    
        cache = z
        return A, cache



    def sigmoid_backward(self, dA, cache):

        import numpy as np

        Z = cache
    
        s = 1/(1+np.exp(-Z))
        dZ = dA * s * (1-s)
        
        return dZ

    
    def relu_backward(self, dA, cache):

        import numpy as np

        Z = cache
        dZ = np.array(dA, copy=True) # just converting dz to a correct object.
        
        # When z <= 0, you should set dz to 0 as well. 
        dZ[Z <= 0] = 0
        
        return dZ

    
    def linear_forward(self, A, W, b):

        import numpy as np

        Z = np.dot(W,A)+b

        cache = (A, W, b)
        return Z, cache


    def linear_activation_forward(self, A_prev, W, b, activation):

        if activation == "sigmoid":
            Z, linear_cache = self.linear_forward(A_prev, W, b)
            A, activation_cache = self.sigmoid(Z)


        elif activation == "relu":
            Z, linear_cache = self.linear_forward(A_prev, W, b)
            A, activation_cache = self.relu(Z)

        
        cache = (linear_cache, activation_cache)
        return A, cache


    def compute_cost(self, AL, Y):

        import numpy as np

        m = self.m

        cost = (-1/m) * np.sum(np.multiply(np.log(AL), Y) + np.multiply(np.log(1-AL), 1-Y))
        cost = np.squeeze(cost)  

        return cost


    def linear_backward(self, dZ, cache):

        import numpy as np

        A_prev, W, b = cache
        m = A_prev.shape[1]

        dW = np.dot(dZ,A_prev.T)/m
        db = np.sum(dZ, axis=1, keepdims=True)/m
        dA_prev = np.dot(W.T, dZ)


        return dA_prev, dW, db



    def linear_activation_backward(self, dA, cache, activation):

        linear_cache, activation_cache = cache

        if activation == "relu":
            dZ = self.relu_backward(dA, activation_cache)
            dA_prev, dW, db = self.linear_backward(dZ, linear_cache)

        elif activation == "sigmoid":
            dZ = self.sigmoid_backward(dA, activation_cache)
            dA_prev, dW, db = self.linear_backward(dZ, linear_cache)

        
        return dA_prev, dW, db

    
    def update_parameters(self, parameters, grads):

        L = len(parameters) // 2

        for l in range(L):
            parameters["W" + str(l+1)] -= self.learning_rate*grads["dW"+str(l+1)]
            parameters["b" + str(l+1)] -= self.learning_rate*grads["db"+str(l+1)]

        return parameters


    def plot_cost(self):
        
        import numpy as np
        from matplotlib import pyplot as plt

        l = len(self.costs)
        plt.plot(np.arange(1,l+1), self.costs)
        

    
    def predict(self, X, threshold = 0.5):

        import numpy as np

        W1 = self.parameters["W1"]
        b1 = self.parameters["b1"]
        W2 = self.parameters["W2"]
        b2 = self.parameters["b2"]

        A1, cache1 = self.linear_activation_forward(X, W1, b1, "relu")
        A2, cache2 = self.linear_activation_forward(A1, W2, b2, "sigmoid")

        

        return np.where(A2 >= threshold, 1, 0)
