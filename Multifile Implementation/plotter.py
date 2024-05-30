import pandas as pd
import matplotlib.pyplot as plt
import csv

def data_extractor(fl,data):
    with open(fl, 'r') as file:
        reader = csv.reader(file)
        for row in reader: 
            data.append(float(row[1]))

if __name__ == "__main__":
    f1 = 'log_1.csv'
    f2 = 'log_2.csv'
    f3 = 'log_3.csv'
    f4 = 'log_4.csv'
    f5 = 'log_5.csv'
    d1=[]
    d2=[]
    d3=[]
    d4=[]
    d5=[]
    time = []
    data_extractor(f1,d1)
    data_extractor(f2,d2)
    data_extractor(f3,d3)
    data_extractor(f4,d4)
    data_extractor(f5,d5)
    n = len(d1)
    for i in range(1,n+1):
        time.append(i)
    plt.plot(time,d1, label='x1(t)')
    plt.plot(time,d2, label='x2(t)')
    plt.plot(time,d3, label='x3(t)')
    plt.plot(time,d4, label='x4(t)')
    plt.plot(time,d5, label='x5(t)')
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.title('State Evolution of Nodes')
    plt.legend()
    plt.grid(True)
    plt.show()
    