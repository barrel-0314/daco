from candidate_generate_norm import candidate_main,initial_candidate2
from candidate_iter import initial_candidate_weight, candidate_score, column_type, initial_type_weight,weight_column_type_score,column_type_filter, calculate_closeness,close_mix
from Mininum_Covering_Vertex import construct_column_graph, Minimum_Covering_Set
from Relation_Discover_norm import relation_discovery
#from Relation_Discover_letter import relation_discovery
from Update_weight import update_array
from Validation import valid_main
import numpy as np
import pickle
import time
import read_data
import random
import heapq
import os

def identify_covergency(theta,Cw,w0,cn):
    
    flag=False
    w1=0
    for pos in Cw:
        for w in Cw[pos]:
            w1+=w
    w1/=cn
    if np.abs(w1-w0)<theta:
        flag=True
    
    return w1,flag
    
def core_column_iterative(Cs,Cw,WT,lam,alp,bet,d,N,mix,theta,q,td,wd):
    
    ite=0
    n=WT.number_start
    cn=0
    w0=100
    CR={}
    for pos in Cw:
        cn+=len(Cw[pos])
        
    for ite in range(N):
        if ite==0:
            Rel={}
            RR={}
            UN=np.zeros((n,n))
            
            
        cs=candidate_score(Cs,Cw,n)
        Cot=column_type(Cs,cs) 
        if ite==0:
            Tw=initial_type_weight(Cot)
        cot=weight_column_type_score(Cot,Tw)
        ctf=column_type_filter(cot)
        #print(ctf)
        Close=calculate_closeness(ctf,q)
        CloseR,CloseM,CR=close_mix(Close,CR,WT.row_num,mix)
        #print(Close)
        g=construct_column_graph(CloseM)
        NS=Minimum_Covering_Set(g,lam,alp,bet)
    
        Rel,RR,S,O,R=relation_discovery(Cs,NS,Rel,RR,td,wd)
        #Rel,RR,S,O,R=relation_discovery(Cs,NS,Rel,RR)
        Uw,Cw,Utw,Tw,CR=update_array(ite,d,Cs,Rel,UN,n,S,O,Cw,Tw,cot,CR)
        w1,flag=identify_covergency(theta,Cw,w0,cn)
        #print(w0,w1,ite,NS)
        
        if flag==True:
            #print(w0,w1,ite,Close)
            break
        else:
            w0=w1
        #ite+=1candidate
    return NS,Uw,Cw,ctf,CloseM,CR

def dict_adjcent(C,n):
    
    A=np.ones((n,n))
    for p in C:
        
        A[p[0]][p[1]]=C[p]
        
    
        
    return A
    
def statistic_number_column(con,m,n):

    N=np.zeros(n)
    num_N=np.zeros(n)
    NL=m*np.ones(n)
    num_L=np.zeros(n)
    for r in con:
        
        for o in range(n):
            
            c=r[o]
            #print(o,len(c))
            
            N[o]+=len(c)
            num_L[o]+=len(c)
            if ' (' in c:
                
                fs=c.split(' (')[0]
                num_L[o]+=len(fs)
                
            for i in c:
                
                if '0'<=i<='9':
                    num_N[o]+=1
                elif i=='-' or i=='+':
                    num_N[o]+=1
                elif i=='.':
                    num_N[o]+=1
                elif i=='/' or i==' ':
                    num_N[o]+=1
                
                
    per1=num_N/N
    #print(num_L)
    per2=num_L/NL
    return per1,per2
    
                
def core_final_result(A,n):
    
    
    C=dict_adjcent(A,n)
    #print(C)
    #C=A
    cl=list(range(n))
    cc=[]
    cc0=[]
    NS=np.zeros(n)
    S=np.sum(C,axis=1)
    #print(S)
    loc=np.argmax(S)
    #print(loc)
    NS[loc]=1
    cl.remove(loc)
    cc.append(loc)
    S[loc]=0
    loc=np.argmax(S)
    #print(loc)
    while len(cc0)!=len(cc) and np.sum(S)!=0:
        
        flag=0
        for col in cl:
        
            if col!=loc:
                
                c=C[:,col]
                #print(c)
                s1=np.sum(c[cc])
                s2=C[loc][col]
                #print(s1,s2,col)
                if s2>s1:
                
                    flag=1
                    break
        if flag==1:
        
            NS[loc]=1
            cl.remove(loc)
            cc0=cc
            cc.append(loc)
            S[loc]=0
            loc=np.argmax(S)
            
        else:
            S[loc]=0
            loc=np.argmax(S)
        #print(loc)
        
    return cc

def termination_check(fpath,WT,cc,td,wd,db,wt_name,ctf,Cs,Cw,num):
    
    #print(WT.row_num)
    if num<WT.row_num<=num+2:
        
        vld_num=WT.row_num-num
        
    elif num<=2:
        vld_num=num
    
    else:
        
        vld_num=3
    
    #print(vld_num)
    vld_flag,vld_row,Vs=valid_main(fpath,wt_name,WT,Cs,ctf,vld_num,td,wd,db,cc[0])
    #print(vld_flag)
    if vld_flag==0:
        cws={}
        for p in Cw:
            if p[0] not in cws:
                cws[p[0]]=0
            if len(Cw[p])!=0:
                cws[p[0]]+=np.mean(np.array(Cw[p]))
        min_sam=heapq.nsmallest(vld_num, list(cws.values()))
        sub_r=[]
        for r in cws:
            
            if cws[r] in min_sam:
                
                sub_r.append(r)
                
            if len(sub_r)==vld_num:
                
                break
        
        for i in range(vld_num):
            #print(i) 
            for j in range(WT.number_start):
                #print(j)
                #print(Cs.keys())
                del Cs[(sub_r[i],j)]
                del Cw[(sub_r[i],j)]
                #print('ff')
                Cs[(vld_row[i],j)]=Vs[(vld_row[i],j)]
                #print('vv')
                Cw[(vld_row[i],j)]=[1]*len(Vs[(vld_row[i],j)])
                
    #print(vld_flag,'vf')
    return vld_flag, Cs, Cw       

def save_core_result(wt_name,WT,fpath,order,ifsample,db,eps=0.6,lam=0.2,q=1.0,eta=0.01,mix=0.5):
    
    
    if WT.number_start==1:
        
        #CC[kk]=0
        cc=[0]
        f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
        pickle.dump(cc,f)
        f.close()
        
    else:
        
        if WT.row_num<10:
            N=WT.row_num
        else:
            N=10
            
        #N=WT.row_num
        try:
            #generate and save candidate
            C=candidate_main(WT)
            f=open(fpath+'_candidate/'+wt_name+'_can_set.data','wb')
            pickle.dump(C,f)
            f.close()
            
            if WT.row_num>0:
                Cs,Cw,td,wd=initial_candidate2(fpath,WT,wt_name,N,ifsample,db)  #generate candidate type
            
                cn=0
                for pos in Cw:
                    cn+=len(Cw[pos])
            else:
                cn=0
                    
            if cn!=0:
                #print(cn)
                NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,lam,eps,eps,0.85,50,mix,eta,q,td,wd)  #inner iteration 
                
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)  
                for p in C:
                
                    if per1[p[0]]>0.5:
                    
                        C[p]=0
                    
                    elif per2[p[0]]<5:
                    
                        C[p]=0
                    
                    elif per2[p[1]]<5:
                    
                        C[p]=0
                
                #print(C)    
                cc=core_final_result(C,WT.number_start)
                #print(cc)
                if WT.row_num<=10:
                    vf=1
                else:
                    num=min(3,WT.row_num-10)
                    vf,Cs,Cw=termination_check(fpath,WT, cc, td, wd, db, wt_name, ctf, Cs, Cw,num) #termination check
                
                if vf==0:
                    print('valid')
                    i=0
                    while i<20 and vf==0:  #outer iteration
                        
                        #st=time.time()
                        cn=0
                        for pos in Cw:
                            cn+=len(Cw[pos])
                        if cn!=0:
                            NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,lam,eps,eps,0.85,50,mix,eta,q,td,wd)   
                            per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                            cc=core_final_result(C,WT.number_start)
                            vf,Cs,Cw=termination_check(fpath,WT, cc, td, wd, db, wt_name, ctf, Cs, Cw,num) 
                #save result
                f=open(fpath+'_result/'+wt_name+'_re.data','wb')
                pickle.dump(Uw,f)
                f.close()
                f=open(fpath+'_result/'+wt_name+'_cw.data','wb')
                pickle.dump(Cw,f)
                f.close()
                f=open(fpath+'_result/'+wt_name+'_ctf.data','wb')
                pickle.dump(ctf,f)
                f.close()
                f=open(fpath+'_result/'+wt_name+'_A.data','wb')
                pickle.dump(C,f)
                f.close()
                f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
                pickle.dump(cc,f)
                f.close()
 
                            
            else:
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                cc=[0]
            
                f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
                pickle.dump(cc,f)
                f.close()
            
            
            print('success!'+str(order),cc)
            return ('success')
            
        except:
            print('n',order)        
            return 'fail' 


if __name__ == '__main__':        

    db='t2d'
    M,WL=read_data.read_data_sample(db)
    fpath='test'
    
    
    for i in range(1):

        print(M[i])
        state=save_core_result(M[i],WL[i],fpath,i,True,db)
        