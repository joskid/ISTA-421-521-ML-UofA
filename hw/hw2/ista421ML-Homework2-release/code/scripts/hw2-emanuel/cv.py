import numpy as np
import matplotlib.pyplot as plt

def read_data(filepath, d = ','):
    """ returns an np.matrix of the data """
    return np.asmatrix(np.genfromtxt(filepath, delimiter = d, dtype = None))


def plot_model(x, w):
    flatx = np.asarray(x).flatten()
    flatx = np.asarray(sorted(flatx))
    plotx = np.asmatrix(np.linspace(flatx[0]-1, flatx[-1]+1,
                                    (flatx[-1]-flatx[0]+4)/0.01 + 1)).conj().transpose()
    plotX = np.asmatrix(np.zeros((plotx.shape[0], w.size)))
    for k in range(w.size):
        plotX[:,k] = np.power(plotx, k)
    plt.plot(plotx, plotX*w, color = 'r', linewidth = 2)
    plt.pause(.1) # required on some systems so that rendering can happen
    return plotx, plotX*w

def plot_data(x, t):
    plt.figure()
    plt.scatter(np.asarray(x), np.asarray(t),
                edgecolor = 'b', color = 'w', marker = 'o')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.title('Data')
    plt.pause(.1) # required on some systems so that rendering can happen

def fitpoly(x, t, model_order):
    
    #### YOUR CODE HERE ####
    w = None  ### Calculate w column vector (as an np.matrix)

    myarray = np.ones((x.shape[0], 1))

    if(model_order > 1):
        x = np.column_stack((myarray, x))

         #clear our array
        myarray = np.zeros((x.shape[0], 1))

        mypow = 2;
        for col in range(model_order -1):
          myarray = np.power(x.T[1], mypow)
          mypow += 1
          x = np.column_stack((x,myarray.T))

    elif(model_order == 1):
         x = np.column_stack((myarray, x))

    elif(model_order == 0):
        x = myarray           


    #m1 = ((X^t)X)
    m1 = x.T.dot(x)



    #m2 = m1^-1 = ((X^t)X)^1

    m2 = np.linalg.inv(m1)

    #print m2

    #m3 = m2.X^t = (((X^t)X)^1) X^t

    m3 = m2.dot(x.T)

    w = m3.dot(t)

    #w = cloumn vector
    return np.asmatrix(w).T


def setPolyMatrix(x, model_order):
    myarray = np.ones((x.shape[0], 1))


    if(model_order > 1):
        x = np.column_stack((myarray, x))

         #clear our array
        myarray = np.zeros((x.shape[0], 1))

        mypow = 2;
        for col in range(model_order -1):
          myarray = np.power(x.T[1], mypow)
          #print(myarray)
          #rint(x.T[1])
          mypow += 1
          x = np.column_stack((x,myarray.T))

    elif(model_order == 1):
         x = np.column_stack((myarray, x))

    elif(model_order == 0):
        x = myarray   


     #w = cloumn vector
    return x       

#END OF OUR FUNCTIONS    
###############################################################    
#filepath1 = '../data/test1.csv'   ## Problem 4
filepath1 = '../data/synthdata2014.csv'   ## Problem 4



## Run a cross-validation over model orders
maxorder = 7
Data = read_data(filepath1, ',')

X = Data[:, 0] # extract x (slice first column)
t = Data[:, 1] # extract t (slice second column)
#X = np.asmatrix(np.zeros(shape = (x.shape[0], maxorder + 1)))
#testX = np.asmatrix(np.zeros(shape = (testx.shape[0], maxorder + 1)))

K = 10 # K-fold CV
N = Data.shape[0]

#prints 3rd row and column zero
#print Data[3, 0]


indexArray = list(range(N))
np.random.seed(1)
np.random.shuffle(indexArray)

#print indexArray

elements_each_folder = N/K

cv_loss = np.zeros((K, maxorder + 1))
train_loss = np.zeros((K, maxorder + 1))

#tests
my_best_order =100
for cur_order in range(maxorder +1):
#for cur_order in range(3,4):

    my_ws = np.zeros(shape=(cur_order +1, K))

    for k in range(K):
        #reset our test matrices
        testx = np.zeros(elements_each_folder)
        testt = np.zeros(elements_each_folder)
        trainx = np.zeros(N - elements_each_folder)
        traint = np.zeros(N - elements_each_folder)

        #train sets
        #only one fold ... up to now :((    
        indextrain = 0
        indextestx = 0
        for i in range(N):
            idxmin = k*elements_each_folder
            idxmax = idxmin + elements_each_folder
            #print "min max ", idxmin, idxmax
            indexArrayTmp = indexArray[idxmin:idxmax]
            if i not in indexArrayTmp:
                #print i, " nao esta em indexArray  "
                #print indexArrayTmp
                trainx[indextrain] = Data[i, 0]
                traint[indextrain] = Data[i, 1]

                indextrain += 1
                #print "i vale ", i
            #make our test data    
            else:
                testx[indextestx] = Data[i, 0]
                testt[indextestx] = Data[i, 1]
                indextestx += 1


        #print "index train: ", indextrain, "\n"
        #print trainx.shape
        #print testx.shape
        #print "k = ", k
        w = fitpoly(trainx, traint, model_order=cur_order)

        if(cur_order == my_best_order):
            w_array = np.array(w.T)
            my_ws[:, k] = w_array


        testx = setPolyMatrix(testx, model_order=cur_order)
        #testt = setPolyMatrix(testt, model_order=cur_order)

        testt = np.asmatrix(testt).T

        fold_pred = testx * w

       

        trainx = setPolyMatrix(trainx, model_order=cur_order)
        #print traint
        traint = np.asmatrix(traint).T
        train_pred = trainx * w
        
        #print fold_pred
        if testt.shape[0] == 1:
            cv_loss[k, cur_order] = np.power(fold_pred - testt, 2)
        else:
            cv_loss[k, cur_order] = np.mean(np.power(fold_pred - testt, 2))
        train_loss[k, cur_order] = np.mean(np.power(train_pred - traint, 2))  

        #prints the best model if my_best_order is set  
    if(cur_order == my_best_order):
        #print my_ws
        best_parameters_w = np.mean(my_ws, axis=1)
        print "Best parameters considering model_oder = ",\
         my_best_order, "are: "
        print best_parameters_w
        plt.ion()
        plot_data(X, t)
        plot_model(X, np.matrix(best_parameters_w).T)
        plt.pause(100)
 


log_cv_loss = np.log(cv_loss)
log_train_loss = np.log(train_loss)

## Plot log scale loss results
plt.figure(1);
plt.title('Log-scale Loss')

plt.subplot(131)
plt.plot(np.arange(0, maxorder + 1), np.mean(log_cv_loss, 0), linewidth = 2)
plt.xlabel('Model Order')
plt.ylabel('Log Loss')
plt.title('CV Loss')
plt.pause(.1) # required on some systems so that rendering can happen

plt.subplot(132)
plt.plot(np.arange(0, maxorder + 1), np.mean(log_train_loss, 0), linewidth = 2)
plt.xlabel('Model Order')
plt.ylabel('Log Loss')
plt.title('Train Loss')
plt.pause(100) # required on some systems so that rendering can happen





   

#print indexArray


