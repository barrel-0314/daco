import csv
from Class_Table import Web_Table
import numpy as np
import pickle
#from T2K.T2K_main import *
import random
import os

def read_sample_table(wt_name,outfile):

    f=open(outfile+wt_name+'_content.data','rb')
    content=pickle.load(f)
    f.close()
    f=open(outfile+wt_name+'_ns.data','rb')
    number_start=pickle.load(f)
    f.close()
    f=open(outfile+wt_name+'_core.data','rb')
    core=pickle.load(f)
    f.close()
    f=open(outfile+wt_name+'_header.data','rb')
    header=pickle.load(f)
    f.close()
    
    #print(number_start,content)
    if content!=[]:
        column_num=len(content[0])
    else:
        column_num=number_start
    row_num=len(content)
    column_class=['NULL']*column_num
    #header=['NULL']*column_num
    flag=np.zeros((row_num,number_start))
    entity='NULL'
    
    WT=Web_Table(content,row_num,column_num,header,entity,column_class,number_start,core,flag)
    return WT

def calculate_statistic_table(WT_list):
    
    n=len(WT_list)
    row_mean=np.zeros(n)
    column_mean=np.zeros(n)
    number_mean=np.zeros(n)
    
    for i in range(n):
        WT=WT_list[i]
        row_mean[i]=WT.row_num
        column_mean[i]=WT.column_num
        number_mean[i]=WT.column_num-WT.number_start
    
    rm=np.mean(row_mean)
    cm=np.mean(column_mean)
    nm=np.mean(number_mean)
    
    return rm,cm,nm

def read_data_sample(database):

                
    WT_list=[]
    if database=='iswc':
        
        infile='../../web_table/iswc_example/'
        tableset='../../iswcset'
        
    elif database=='t2d':
        
        infile='t2d_example/'
        tableset='t2dwhole'
        
    elif database=='git':
        
        infile='../../web_table/gittable_example/'
        tableset='../../gitset'
    
    elif database=='wiki':
        
        infile='../../web_table/wiki_example/'
        tableset='../../wikiset'
    elif database=='t2dc':
        
        infile='../../web_table/t2dc_example/'
        tableset='../../t2dcset'
        
    elif database=='santos':
        
        infile='../../web_table/santos_example/'
        tableset='../../santosset'
    elif database=='lsantos':
        
        infile='../../web_table/santos_example/'
        tableset='../../lsantosset'
        
    elif database=='multicc':
        
        infile='../../web_table/multicc_example/'
        tableset='../../multiccset'    
    f=open(tableset+'.data','rb')
    ts=pickle.load(f)
    f.close()
    #print(ts)
    for i in range(len(ts)):
        
        WT=read_sample_table(ts[i],infile)
        WT_list.append(WT)
        
    return ts,WT_list
    



