class create_train_NNclassifier:

    def __init__(self, X, Y, input_dim, layer_dims, learning_rate=0.001, iter=3000, print_cost=False, plot_cost=False):


        import numpy as np
        import pandas as pd 
        import matplotlib.pyplot as plt
        

        

        X = X.T
        Y = Y.T

        self.layer_dims = [input_dim] + list(layer_dims)

        np.random.seed(1)
        self.grads = {}
        self.costs = []              
        self.m = X.shape[1] 
        self.learning_rate = learning_rate
        self.iter = iter
        
        self.parameters = self.initialize_parameters()

        

        for i in range(0,self.iter+1):
            
            AL, caches = self.linear_forward_deep(X, self.parameters)


            cost = self.compute_cost(AL, Y)


            self.grads = self.linear_backward_deep(AL, Y, caches)

            


            self.parameters = self.update_parameters(self.parameters, self.grads)


            


            if print_cost and i % 100 == 0:
                print("Cost after iteration {}: {}".format(i, np.squeeze(cost)))
            if print_cost and i % 100 == 0:
                self.costs.append(cost)


        if(plot_cost):
            self.plot_cost()
            

    def initialize_parameters(self):

        import numpy as np

        np.random.seed(3)
        parameters = {}
        L = len(self.layer_dims)            

        for l in range(1, L):
            
            parameters['W' + str(l)] = np.random.randn(self.layer_dims[l], self.layer_dims[l-1])*0.01
            parameters['b' + str(l)] = np.zeros((self.layer_dims[l], 1))
            
            
            

            
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


    def linear_forward_deep(self, X, parameters):

        caches = []
        A = X
        L = len(parameters) // 2                  
        
        
        for l in range(1, L):
            A_prev = A 
            
            A, cache = self.linear_activation_forward(A_prev, parameters['W'+str(l)], parameters['b'+str(l)], "relu")
            caches.append(cache)
            
        
        
        AL, cache = self.linear_activation_forward(A, parameters['W'+str(L)], parameters['b'+str(L)], "sigmoid")
        caches.append(cache)
        
        
        
                
        return AL, caches



    def linear_activation_forward(self, A_prev, W, b, activation):

        if activation == "sigmoid":
            Z, linear_cache = self.linear_forward(A_prev, W, b)
            A, activation_cache = self.sigmoid(Z)


        elif activation == "relu":
            Z, linear_cache = self.linear_forward(A_prev, W, b)
            A, activation_cache = self.relu(Z)

        
        cache = (linear_cache, activation_cache)
        return A, cache


    def linear_forward(self, A, W, b):

        import numpy as np

        Z = np.dot(W,A)+b

        cache = (A, W, b)
        return Z, cache



    def compute_cost(self, AL, Y):

        import numpy as np

        m = self.m

        cost = (-1/m) * np.sum(np.multiply(np.log(AL), Y) + np.multiply(np.log(1-AL), 1-Y))
        cost = np.squeeze(cost)  

        return cost


    def linear_backward_deep(self, AL, Y, caches):

        import numpy as np

        grads = {}
        L = len(caches) 
        m = AL.shape[1]
        Y = Y.reshape(AL.shape) 
        
        
        dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
        
        
        
        current_cache = caches[-1]
        grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = self.linear_activation_backward(dAL, current_cache, 'sigmoid')
        
        
        
        for l in reversed(range(L-1)):
            
            current_cache = caches[l]
            dA_prev_temp, dW_temp, db_temp = self.linear_activation_backward(grads["dA" + str(l + 1)], current_cache, 'relu')
            grads["dA" + str(l)] = dA_prev_temp
            grads["dW" + str(l + 1)] = dW_temp
            grads["db" + str(l + 1)] = db_temp
            

        return grads



    def linear_activation_backward(self, dA, cache, activation):

        linear_cache, activation_cache = cache

        if activation == "relu":
            dZ = self.relu_backward(dA, activation_cache)
            dA_prev, dW, db = self.linear_backward(dZ, linear_cache)

        elif activation == "sigmoid":
            dZ = self.sigmoid_backward(dA, activation_cache)
            dA_prev, dW, db = self.linear_backward(dZ, linear_cache)

        
        return dA_prev, dW, db

    
    def linear_backward(self, dZ, cache):

        import numpy as np

        A_prev, W, b = cache
        m = A_prev.shape[1]

        dW = np.dot(dZ,A_prev.T)/m
        db = np.sum(dZ, axis=1, keepdims=True)/m
        dA_prev = np.dot(W.T, dZ)


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

        

        AL, caches = self.linear_forward_deep(X, self.parameters)

        
        
        return np.where(AL >= threshold, 1, 0)
