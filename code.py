def MaduraiPredict():
    import warnings
    import os
    import csv
    import numpy as np
    import pandas as pd
    warnings.simplefilter(action="ignore",category=FutureWarning)
    with open('name.txt','r') as fp:
        location = fp.readlines()
    location = location[0]
    res = []
    file = open(location)
    df = pd.read_csv(location)
    reader = csv.reader(file, delimiter=',')
    features=[]
    for row in reader:
        j = []
        for col in row: 
            j.append(col)
        features.append(j)

    dates = features[0][0]
    products = features[0][1:]

    def relu (x):
        return  np.maximum(0,x)

    def derivatives_relu(x):
        return  np.maximum(0,x)

    for k in products:
        to_forecast = df[k]
        dates = df.Date.values # Date feature
        def organize_data(to_forecast, window, horizon):
            shape = to_forecast.shape[:-1] + (to_forecast.shape[-1] - window + 1, window)
            strides = to_forecast.strides + (to_forecast.strides[-1],)
            X = np.lib.stride_tricks.as_strided(to_forecast, shape=shape, strides=strides)
            y = np.array([X[i+horizon][-1] for i in range(len(X)-horizon)])
            return X[:-horizon], y
        k = 4   # number of previous observations to use
        h = 1   # forecast horizon
        X,y = organize_data(to_forecast, k, h)

    # Preprocessing of data
    # Replacing the nan median values of incomplete data

    #X[np.isnan(X)] = np.median(X[~np.isnan(X)])   
    #y[np.isnan(y)] = np.median(y[~np.isnan(y)])

        epoch=5000 #Setting training iterations
        lr=0.1 #Setting learning rate
        inputlayer_neurons = X.shape[1] #number of features in data set
        hiddenlayer_neurons = 3 #number of hidden layers neurons
        output_neurons = 1 #number of neurons at output layer
    
        wh=inputlayer_neurons/(hiddenlayer_neurons*lr*20)
        bh=lr*hiddenlayer_neurons
        wout=hiddenlayer_neurons*output_neurons
        bout=lr*output_neurons
    
        for i in range(epoch):
    
         #Forward Propogation
            hidden_layer_input1=wh
            hidden_layer_input=hidden_layer_input1 + bh
            hiddenlayer_activations = relu(hidden_layer_input)
            output_layer_input1=np.dot(hiddenlayer_activations,wout)
            output_layer_input= relu(output_layer_input1)
            output = relu(output_layer_input*(lr*bh))

        #Back Propogation
            E = y-output
            slope_output_layer = np.exp(-derivatives_relu(output))
            slope_hidden_layer = derivatives_relu(hiddenlayer_activations)
            d_output = 1/(1 + np.exp(-E))
            Error_at_hidden_layer = 1/(1 + np.exp(-E))*(wout/slope_hidden_layer) 
            d_hiddenlayer = d_output + ( Error_at_hidden_layer * slope_hidden_layer)
            wout += d_output *lr
            bout += d_output *lr
            wh += d_hiddenlayer *lr
            bh += d_hiddenlayer *lr
        
        #Outout Display        
        o = np.round(output[-3:])
        o = list(o)
        res.append(o)

    with open('result.csv','w',encoding='utf-8',newline='') as outfile:
        mywriter = csv.writer(outfile)
        #manually add header
        for d in res:
            mywriter.writerow(d)
    
MaduraiPredict()