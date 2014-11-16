## Solution for ISTA 421/521 Fall 2014, HW 2, Problem 1
## Author: Clayton T. Morrison, 14 September 2014

import numpy as np
import matplotlib.pyplot as plt

### -------------------------------------------------------------------------

def read_data(filepath, d = ','):
    """ returns an np.matrix of the data """
    return np.asmatrix(np.genfromtxt(filepath, delimiter = d, dtype = None))

def plot_data(x, t):
    plt.figure()
    plt.scatter(np.asarray(x), np.asarray(t),
                edgecolor = 'b', color = 'w', marker = 'o')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.title('Data')
    plt.pause(.1) # required on some systems so that rendering can happen
    
def plot_model(x, w):
    flatx = np.asarray(x)
    flatx = np.asarray(sorted(flatx))
    plotx = np.asmatrix(np.linspace(flatx[0]-1, flatx[-1]+1,
                                    (flatx[-1]-flatx[0]+4)/0.01 + 1)).conj().transpose()
    plotX = np.asmatrix(np.zeros((plotx.shape[0], w.size)))
    for k in range(w.size):
        plotX[:,k] = np.power(plotx, k)
    #tgen = plotX*w
    plt.plot(plotx, plotX*w, color = 'r', linewidth = 2)
    plt.pause(.1) # required on some systems so that rendering can happen
    return plotx, plotX*w

def plot_model2(x,w,t):
    # plot the synthetic data
    print w
    tgen = np.asarray( w[3]*x**3 + w[2]*x**2 + w[1]*x + w[0])
    plt.close()
    plt.figure(0)
    plt.scatter(np.asarray(x), np.asarray(t), edgecolor = 'b', color = 'w', marker = 'o')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.title('Plot of synthetic data; green curve is original generating function');
    plt.plot(x , tgen, color='g', linewidth=2)
    plt.pause(.1) # required on some systems so that rendering can happen

### -------------------------------------------------------------------------

def fitpoly(x, t, model_order):
    
    #### YOUR CODE HERE ####
    w = np.zeros((model_order + 1 , 1))  ### Calculate w column vector (as an np.matrix)
    X = np.ones((len(x) , model_order+1))
    for i in range(model_order+1):
        for j in range(len(x)):
           X[j,i] = x[j]**i
    print X.shape
    w = np.linalg.inv((X.T.dot(X)))
    print w.shape
    print t.shape
    w = w.dot(X.T).dot(t)
    return w

def xnew(w,newx,truey,model_order):
    e = 0
    for i in range(model_order+1):
        e += w[i]*newx**i
    return e

### -------------------------------------------------------------------------
### Script to run on particular data set

filepath1 = '../data/womens100.csv'       ## Problem 2
#filepath1 = '../data/synthdata2014.csv'   ## Problem 4

## The following data is provided just for fun, not used in HW 2.
## This is the data for the men's 100, which has been the recurring 
## example in the class
#filepath1 = '../data/mens100.csv'

model_order = 1 # for problem 2
#model_order = 3 # for problem 4

Data = read_data(filepath1, ',')

x = Data[:, 0] # extract x (slice first column)
t = Data[:, 1] # extract t (slice second column)

plt.ion()

plot_data(x, t)
w = fitpoly(x, t, model_order)
#e = xnew(w,2012,10.75,model_order)
#f = xnew(w,2016,10.75,model_order)

print 'Identified model parameters:'
print w
#print 'Predicting values:'
#print e
#print f

#print "Error:"
#print (e-10.75)**2
#[plotX, plotXW] = plot_model(x,w)
#print plotX

#print 'Predicting values:'
#print plotXW

plot_model(x,w)

#plot_model2(x,plotXW,t)

 #This last line may or may not be necessary to keep your matplotlib window open
raw_input('Press <ENTER> to quit...')
