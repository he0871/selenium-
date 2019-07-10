"""
ENTS669G's Homework 2
Data mining
2018/7/15
Aurthor: Jingyuan He
"""
import numpy as np
import operator
import matplotlib.pyplot as plt

"""
!!!!!!!!Do not code python in C's way!!!!!!!
"""

def mode(x):
    #input is an one-dimensional array
    unique, counts = np.unique(x, return_counts=True)
    dt_mode = dict(zip(unique, counts))
    dt_mode = sorted(dt_mode.items(), key=operator.itemgetter(1))
    dt_mode = dt_mode[::-1]
    #print(max(dt_mode,key=operator.itemgetter(1) ))
    m = dt_mode[0][0] #present mode
    counts = dt_mode[0][1]
    list_m = [m]
    for walk in dt_mode:
        if walk[0] == m: #skip the first element
            continue
        if walk[1] < counts: #means there is only one mode in this array`
            break
        elif walk[1] == counts: #one more modes
            print(walk)
            list_m.append(walk[0])
        else: #error do occurs
            print("wft! sth wrong")
        
        
    return [list_m, counts]
   
def normalize(martix):
    """
    input martix supposed to be a array
    """
    avatar = []
    for row in martix:
        #print(max(row))
        row = np.true_divide(row , max(row) )
        avatar.append(row)
    arr_avatar = np.array(avatar)
    return(arr_avatar)

def located(index, dimension):
    #index start with 0
    index += 1
    rng = np.arange(1,dimension,1)
    rng = rng[::-1]
    address = []
    for walk in rng:
        #print(walk)
        #print(index)
        if index > walk:
            index -= walk
        else:
            address = [int(dimension - walk + index),(dimension - walk)]
            break
    return address
    
def linear_re(x,y_matrix):
    """
    input y_matrix supposed to be a numpy array or matrix
    y = mx +b
    """
    n = len(x)
    if 1 != np.shape(np.shape(y_matrix))[0]:
        sum_xy = np.sum(x * y_matrix, axis = 1)
        multi_sum = np.sum(y_matrix, axis = 1) * np.sum(x)
        sum_y = np.sum(y_matrix, axis = 1)
    else:
        sum_xy = np.sum(x * y_matrix)
        multi_sum = np.sum(y_matrix) * np.sum(x)
        sum_y = np.sum(y_matrix)
        
    sum_x2 = sum(x ** 2)
    sum_x_sq = sum(x) ** 2
    
    m_up = (n * sum_xy) - multi_sum
    m_down = (n * sum_x2) - sum_x_sq
    m = m_up / m_down
    
    b_up = (sum_y * sum_x2) - (np.sum(x)*sum_xy)
    b_down = n * sum_x2 - sum_x_sq
    b = b_up / b_down

    return[m,b]
 
def RegressionPlot(mb, matrix):
    """
    mb is a list containing 2 element
    first one is array of m
    second one is array of b
    """
    m = mb[0]
    b = mb[1]
    x = np.arange(0,len(matrix[0]),1)    
    
    file_path = "D:/code/HM3/picture/"
    
    n = 0
    while n < len(m):
        y = m[n] * x + b[n]
        fig = plt.figure()
        plt.plot(x,y,'r')
        plt.plot(x,matrix[n],'b')
        fig.savefig(file_path + str(n)+'.png')
        n += 1
    
def predict(m,b,day,current_price):
    percentage = 0.1
    y = m * day + b
    if y > current_price:
        rate = (y - current_price) / current_price
        if rate > percentage:
            info = 'BUY'
        else:
            info = 'HOLD'
    else: #y <= current_price
        rate = (current_price - y) / current_price
        if rate > percentage:
            info = 'SELL'
        else:
            info = 'HOLD'
    return info
    
def TendCmpPlot(arr1,arr2,name):
    file_path = "D:/code/HM3/picture/"
    fig = plt.figure()
    plt.plot(arr1, 'r')
    plt.plot(arr2, 'b')
    fig.savefig(file_path + name +'.png')

    
    

    
    