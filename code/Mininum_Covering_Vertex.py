import networkx as nx
import numpy as np
import random

def construct_column_graph(Close):
    
    g=nx.DiGraph()
    for pair in Close:
        
        g.add_edge(pair[0],pair[1],weight=Close[pair])
        
    return g

def obtain_adjacent(g):
    
    n=g.number_of_nodes()
    A=np.ones((n,n))
    for i in range(n):
        
        for j in range(n):
            
            if i!=j:
                A[i][j]=g[i][j]['weight']
            #A[j][i]=A[i][j]
    return A


def Minimum_Covering_Set(g,lam,alp,bet):

    A=obtain_adjacent(g)
    #print(A)
    n=g.number_of_nodes()
    M=int(n/2)
    NS=np.zeros(n)
    NS=NS.reshape(-1,1)
    c=100
    O=np.ones((n,1))
    #Z=np.zeros(n)
    d=0
    node_set=list(range(n))
    for i in range(M):
        
        if i==0:
            p=random.random()
            if p<bet:
                loc=np.argmax(np.sum(A,axis=1))                
            else:
                loc=random.sample(range(n),1)[0]
            #print(loc)
            NS[loc][0]=1
            s=lam+1-np.sum(A[loc])
            if s<c:
                c=s
                node_set.remove(loc)
        elif i>0:
            flag=0
            #K=n-i
            
            D=-np.ones(n)
            for k in node_set:
                
                NS_temp=np.array(NS)
                NS_temp[k][0]=1
                #print(NS,NS_temp,k)
                delta=np.dot(np.dot(NS_temp.transpose(),A),(O-NS_temp))-np.dot(np.dot(NS.transpose(),A),(O-NS))
                D[k]=delta
                #print(D)
                if flag==0 and delta>lam:
                    c=c+lam-delta
                    loc=k
                    flag=1
                    d=delta
                elif flag==1 and delta>d:
                    c=c-delta+d
                    loc=k
                    d=delta
            #print(flag)        
            if flag==0:
                p=random.random()
                #print(p)
                if p<alp:
                    break
                else:
                    NS[np.argmax(D)][0]=1
                    #print(D,np.argmax(D),node_set)
                    node_set.remove(np.argmax(D))
            else:
                NS[loc][0]=1
                node_set.remove(loc)
                
    return NS
                    
            
            
#NS=Minimum_Covering_Set(g,0.5,0.9)
#print(NS)            
#g=construct_column_graph(CC)
#NS=Minimum_Covering_Set(g,0.8,0.7,0.85)
#A=obtain_adjacent(g)