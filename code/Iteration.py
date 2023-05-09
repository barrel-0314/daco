from candidate_generate import candidate_main,initial_candidate2
from candidate_iter import initial_candidate_weight, candidate_score, column_type, initial_type_weight,weight_column_type_score,column_type_filter, calculate_closeness,close_mix
from Mininum_Covering_Vertex import construct_column_graph, Minimum_Covering_Set
from Relation_Discover import relation_discovery
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
    
def core_column_iterative(Cs,Cw,WT,lam,alp,bet,d,N,theta,q,td,wd):
    
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
        CloseR,CloseM,CR=close_mix(Close,CR,WT.row_num,theta)
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

def validation(WT,cc,td,wd,db,wt_name,ctf,Cs,Cw,num):
    
    #print(WT.row_num)
    if num<WT.row_num<=num+2:
        
        vld_num=WT.row_num-num
        
    elif num<=2:
        vld_num=num
    
    else:
        
        vld_num=3
    
    #print(vld_num)
    vld_flag,vld_row,Vs=valid_main(wt_name,WT,Cs,ctf,vld_num,td,wd,db,cc[0])
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
                
    
def noise_random(Cs,Cw,nper):

    pair=list(Cs.keys())
    
    n=len(pair)
    no=int(n*nper)
    npair=random.sample(pair,no)
    
    for p in npair:
        
        Cs[p]=[]
        Cw[p]=[]
        
    return Cs,Cw,npair
    
def save_core_result(wt_name,WT,fpath,order,ifsample,db,lam,q,eta):
    
    
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
            '''
            C=candidate_main(WT)
            f=open('../../web_table/git_candidate/'+wt_name+'_can_set.data','wb')
            pickle.dump(C,f)
            f.close()
            '''
            if WT.row_num>0:
                print('yy')
                Cs,Cw,td,wd=initial_candidate2(WT,wt_name,N,ifsample,db)
            
                #st=time.time()
                cn=0
                for pos in Cw:
                    cn+=len(Cw[pos])
                #print(cn)    
            else:
                cn=0
                    
            if cn!=0:
                print(cn)
                NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,lam,0.85,0.7,0.85,50,eta,q,td,wd)   
                
                
                '''
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
                '''
            
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                '''
                f=open(fpath+'_result/'+wt_name+'_per.data','wb')
                pickle.dump((per1,per2),f)
                f.close()
                '''
                for p in C:
                
                    if per1[p[0]]>0.5:
                    
                        C[p]=0
                    
                    elif per2[p[0]]<5:
                    
                        C[p]=0
                    
                    elif per2[p[1]]<5:
                    
                        C[p]=0
                
                #print(C)    
                cc=core_final_result(C,WT.number_start)
                print(cc)
                if WT.row_num<=10:
                    vf=1
                else:
                    num=min(3,WT.row_num-10)
                    vf,Cs,Cw=validation(WT, cc, td, wd, db, wt_name, ctf, Cs, Cw,num) 
                
                if vf==0:
                    print('valid')
                    i=0
                    while i<20 and vf==0:
                        
                        #st=time.time()
                        cn=0
                        for pos in Cw:
                            cn+=len(Cw[pos])
                        if cn!=0:
                            NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,lam,0.85,0.7,0.85,50,eta,q,td,wd)   
                            per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                            cc=core_final_result(C,WT.number_start)
                            vf,Cs,Cw=validation(WT, cc, td, wd, db, wt_name, ctf, Cs, Cw,num) 
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
                print(per1,per2)
                cc=[0]
            
                f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
                pickle.dump(cc,f)
                f.close()
            
            
            print('success!'+str(order),cc)
            return ('success')
            
        except:
            print('n',order)        
            return 'fail' 
        


def save_core_result_noise(wt_name,WT,prepath,aftpath,order,ifsample,nper,db):
    
    
    if WT.number_start==1:
        
        #CC[kk]=0
        cc=[0]
        f=open(prepath+'_result/'+wt_name+'_cc.data','wb')
        pickle.dump(cc,f)
        f.close()
        
    else:
        
        if WT.row_num<10:
            N=WT.row_num
        else:
            N=10
        
        #N=WT.row_num
        try:
            '''
            C=candidate_main(WT)
            f=open('../../web_table/git_candidate/'+wt_name+'_can_set.data','wb')
            pickle.dump(C,f)
            f.close()
            '''
            
            Cs,Cw,td,wd=initial_candidate2(WT,wt_name,N,ifsample,db)
            Cs,Cw,npa=noise_random(Cs, Cw,nper)
            print(nper)
            #st=time.time()
            cn=0
            for pos in Cw:
                cn+=len(Cw[pos])
                    
                    
            if cn!=0 and WT.row_num>10:
                
                NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
            
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                
                
                for p in C:
                
                    if per1[p[0]]>0.5:
                    
                        C[p]=0
                    
                    elif per2[p[0]]<5:
                    
                        C[p]=0
                    
                    elif per2[p[1]]<5:
                    
                        C[p]=0
                
                    
                cc=core_final_result(C,WT.number_start)
                vf,Cs,Cw=validation(WT, cc, td, wd, db, wt_name, ctf, Cs, Cw) 
                print(vf)
                if vf==0:
                    print('valid')
                    i=0
                    while i<20 and vf==0:
                        
                        #st=time.time()
                        cn=0
                        for pos in Cw:
                            cn+=len(Cw[pos])
                        if cn!=0:
                            NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
                            per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                            cc=core_final_result(C,WT.number_start)
                            vf,Cs,Cw=validation(WT, cc, td, wd, db, wt_name, ctf, Cs, Cw) 
                    f=open(aftpath+'_result/'+wt_name+'_re.data','wb')
                    pickle.dump(Uw,f)
                    f.close()
                    f=open(aftpath+'_result/'+wt_name+'_cw.data','wb')
                    pickle.dump(Cw,f)
                    f.close()
                    f=open(aftpath+'_result/'+wt_name+'_ctf.data','wb')
                    pickle.dump(ctf,f)
                    f.close()
                    f=open(aftpath+'_result/'+wt_name+'_A.data','wb')
                    pickle.dump(C,f)
                    f.close()
                    f=open(aftpath+'_result/'+wt_name+'_cc.data','wb')
                    pickle.dump(cc,f)
                    f.close()
                else:
                    print(order,'vf=1')
                    f=open(prepath+'_result/'+wt_name+'_re.data','wb')
                    pickle.dump(Uw,f)
                    f.close()
                    f=open(prepath+'_result/'+wt_name+'_cw.data','wb')
                    pickle.dump(Cw,f)
                    f.close()
                    f=open(prepath+'_result/'+wt_name+'_ctf.data','wb')
                    pickle.dump(ctf,f)
                    f.close()
                    f=open(prepath+'_result/'+wt_name+'_A.data','wb')
                    pickle.dump(C,f)
                    f.close()
                    f=open(prepath+'_result/'+wt_name+'_cc.data','wb')
                    pickle.dump(cc,f)
                    f.close()
                    
            elif cn!=0:
                print(order,'row<=10')
                #Cs,Cw,npa=noise_random(Cs, Cw,nper)
                NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
            
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                
                
                for p in C:
                
                    if per1[p[0]]>0.5:
                    
                        C[p]=0
                    
                    elif per2[p[0]]<5:
                    
                        C[p]=0
                    
                    elif per2[p[1]]<5:
                    
                        C[p]=0
                
                    
                cc=core_final_result(C,WT.number_start)
                f=open(prepath+'_result/'+wt_name+'_re.data','wb')
                pickle.dump(Uw,f)
                f.close()
                f=open(prepath+'_result/'+wt_name+'_cw.data','wb')
                pickle.dump(Cw,f)
                f.close()
                f=open(prepath+'_result/'+wt_name+'_ctf.data','wb')
                pickle.dump(ctf,f)
                f.close()
                f=open(prepath+'_result/'+wt_name+'_A.data','wb')
                pickle.dump(C,f)
                f.close()
                f=open(prepath+'_result/'+wt_name+'_cc.data','wb')
                pickle.dump(cc,f)
                f.close()
                
            '''
            f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
            pickle.dump(cc,f)
            f.close()
            '''
            
            print('success!'+str(order))
            return ('success')
            
        except:
            print('n',order)        
            return 'fail'               

            

def save_core_result_sample(wt_name,WT,fpath,order,ifsample,num,db):
    
    
    if WT.number_start==1:
        
        #CC[kk]=0
        cc=0
        f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
        pickle.dump(cc,f)
        f.close()
        
    else:
        
        '''
        if WT.row_num<10:
            N=WT.row_num
        else:
            N=10
        
        if int(WT.row_num*nper)==0:
            N=1
        else:
            N=int(WT.row_num*nper)
        '''
        #N=WT.row_num
        try:
            '''
            C=candidate_main(WT)
            f=open('../../web_table/git_candidate/'+wt_name+'_can_set.data','wb')
            pickle.dump(C,f)
            f.close()
            '''
            Cs,Cw,td,wd=initial_candidate2(WT,wt_name,num,ifsample,db)
            
            st=time.time()
            cn=0
            for pos in Cw:
                cn+=len(Cw[pos])
            if cn!=0:
                #Cs,Cw,npa=noise_random(Cs, Cw,nper)
                NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
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
            
            
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                f=open(fpath+'_result/'+wt_name+'_per.data','wb')
                pickle.dump((per1,per2),f)
                f.close()
                '''
                f=open(fpath+'_result/'+wt_name+'_np.data','wb')
                pickle.dump(np,f)
                f.close()
                '''
                for p in C:
                
                    if per1[p[0]]>0.5:
                    
                        C[p]=0
                    
                    elif per2[p[0]]<5:
                    
                        C[p]=0
                    
                    elif per2[p[1]]<5:
                    
                        C[p]=0
                
                    
                cc=core_final_result(C,WT.number_start)
                
            else:
                cc=[0]
        
            f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
            pickle.dump(cc,f)
            f.close()
            
            
            print('success!'+str(order))
            return (st,'success')
            
        except:
            print('n',order)        
            return 'fail'  
        
def save_core_result_sample_aft(wt_name,WT,fpath,order,ifsample,num,db,label):
    
    #print(wt_name)
    if WT.number_start==1:
        
        #CC[kk]=0
        cc=[0]
        f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
        pickle.dump(cc,f)
        f.close()
        
    else:
        
        
        if WT.row_num<=num:
            #N=WT.row_num
            f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
            pickle.dump(label,f)
            f.close()
        else:
            
            try:
                Cs,Cw,td,wd=initial_candidate2(WT,wt_name,num,ifsample,db)
                #print(nper)
                #st=time.time()
                cn=0
                for pos in Cw:
                    cn+=len(Cw[pos])
                #print(cn)
                if cn!=0:
                    #Cs,Cw,npa=noise_random(Cs, Cw,nper)
                    NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
                    #print(ctf)
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
                    vf,Cs,Cw=validation(WT, cc, td, wd, db, wt_name, ctf, Cs, Cw,num) 
                    #print(vf)
                    if vf==0:
                        print('valid')
                        i=0
                        while i<20 and vf==0:
                        
                            cn=0
                            for pos in Cw:
                                cn+=len(Cw[pos])
                            if cn!=0:
                                NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
                                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                                cc=core_final_result(C,WT.number_start)
                                vf,Cs,Cw=validation(WT, cc, td, wd, db, wt_name, ctf, Cs, Cw,num) 
                    
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
                    print('save')
            
                else:
                    cc=[0]
        
                    f=open(fpath+'_result/'+wt_name+'_cc.data','wb')
                    pickle.dump(cc,f)
                    f.close()
                    
                print('success!'+str(order))
                return ('success')    
            except:
                print('n',order)        
                return 'fail'
            
def non_label_t2d(wt_name,UU,i):
    
    
    f=open('../../web_table/t2d_example/'+wt_name+'_ccl.data','rb')
    ccl=pickle.load(f)
    f.close()
    
    f=open('t2d_result/'+wt_name+'_cc.data','rb')
    cc=pickle.load(f)
    f.close()
    
    for col in ccl:
        
        if col.split('/')[-1]=='rdf-schema#label':
            core=ccl.index(col)
    
    print(core,UU[i][0])
    if core==cc:
        
        r1=True
    elif core==cc[0]:
        r1=True
    
        
        
    else:
        
        r1=False
    if core==0:
        r2=True
    else:
        r2=False
    
    if UU[i][0]!=core:
        
        r3=False
        
    else:
        
        r3=True
    F=(r1,r2,r3)
    return F,core

def obtain_git_pre(CC):
    
    
    M,WL=read_data.read_data_sample('git')
    f=open('no_need_git.data','rb')
    nor=pickle.load(f)
    f.close()

    f=open('git_label_int.data','rb')
    gl=pickle.load(f)
    f.close()
    
    f=open('story2.data','rb')
    sw=pickle.load(f)
    f.close()

    f=open('id_name.data','rb')
    inm=pickle.load(f)
    f.close()
    
    
    N=len(CC)
    n=0
    W=[]
    F=[]
    for i in CC:
        
        if i not in nor and gl[i][0]!=-1:
            W.append(i)
            #print(gl)
            #print(gl[i],CC[i])
            if CC[i][0]!=gl[i][0]:
            
                if i in sw:
                
                    if CC[i][0]!=3:
                    
                        n+=1
                        F.append(i)
                elif i in inm:
                
                    if CC[i][0]!=0:
                    
                        n+=1
                        F.append(i)
                else:
                
                    n+=1
                    F.append(i)
    return n,N,W,F
    
def process_cc(wt_name,fpath,n):
    
    f=open(fpath+'_result/'+wt_name+'_cc.data','rb')
    cc=pickle.load(f)
    f.close()
    
    f=open(fpath+'_result/'+wt_name+'_per.data','rb')
    per=pickle.load(f)
    f.close()
    
    f=open(fpath+'_result/'+wt_name+'_A.data','rb')
    A=pickle.load(f)
    f.close()
    
    
    C=dict_adjcent(A, n)
    per1=per[0]
    per2=per[1]
    for p in A:
    
        if per1[p[0]]>0.5:
        
            A[p]=0
        
        elif per2[p[0]]<5:
        
            A[p]=0
        
        elif per2[p[1]]<5:
        
            A[p]=0
    c2=core_final_result(A,n)
    C2=dict_adjcent(A, n)
    flag=0
    for i in range(n):
        
        for j in range(n):
            
            if i!=j:
                
                if C[i][j]!=0:
                    
                    flag=1
                    break
    if flag==0:
        
        for i in range(n):
            
            if per[0][i]<0.5 and per[1][i]>5:
                
                c=[i]
                break
            
    else:
        
        c=cc
    
    for i in range(n):
        
        for j in range(n):
            
            if i!=j:
                
                if C2[i][j]!=0:
                    
                    flag=1
                    break
    if flag==0:
        
        for i in range(n):
            
            if per[0][i]<0.5 and per[1][i]>5:
                
                c2=[i]
                break
            
    else:
        
        c2=cc        
    
    return c,c2
        
def valid_num(prepath,aftpath,db,M,snum,WL):
    
    L=os.listdir(aftpath)
    L2=os.listdir(prepath)
    CC={}
    F=[]   
    f=open('../result/'+db+'_pro_res.data','rb')
    pr=pickle.load(f)
    f.close()
    for i in range(len(M)):
        nn=0
        WT=WL[i]
        if M[i]+'_cc.data' in L:
            #print(i)
            try:
                f=open(aftpath+M[i]+'_cc.data','rb')
                cc=pickle.load(f)
                f.close()
                if cc==0:
                    cc=[0]
                CC[i]=cc
            except:
                WT=WL[i]
            
        elif M[i]+'_cc.data' in L2:
            #print(i)
            try:
                #print(i)
                '''
                per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
                f=open(prepath+M[i]+'_A.data','rb')
                C=pickle.load(f)
                f.close()
                #print('cc')
                for p in C:
                
                    if per1[p[0]]>0.5:
                    
                        C[p]=0
                    
                    elif per2[p[0]]<5:
                    
                        C[p]=0
                    
                    elif per2[p[1]]<5:
                    
                        C[p]=0
                
                #print('C')    
                cc=core_final_result(C,WT.number_start)
                f=open(prepath+M[i]+'_cc.data','wb')
                pickle.dump(cc,f)
                f.close()
                #print('cc')
                '''
                
                f=open(prepath+M[i]+'_cc.data','rb')
                cc=pickle.load(f)
                f.close()
                
                if cc==0:
                    cc=[0]
                CC[i]=cc
                if snum>=WT.row_num and M[i] in pr:
                    CC[i]=pr[i]
            except:
                nn+=1
            
        
    #print(CC)
    if db!='git':
        f=open('../result/'+db+'_res.data','rb')
        ir=pickle.load(f)
        f.close()
        
        for i in ir:
            
            if i in CC and CC[i][0]!=ir[i][0]:
                #print(i)
                F.append(i)
                
    else:
        #print(len(CC))
        CC2={}
        for i in range(len(M)):
            
            if i in CC and M[i] in pr:
                CC2[M[i]]=CC[i]
                #del CC[i]
                
        n,N,W,F=obtain_git_pre(CC2)
        #print(len(W))
    return F
    
    
def multi_result(wt_name,n):
    
    f=open('multicc_result/'+wt_name+'_cc.data','rb')
    cc=pickle.load(f)
    f.close()
    
    if len(cc)<2:
        
        f=open('multicc_result/'+wt_name+'_A.data','rb')
        A=pickle.load(f)
        f.close()
    
        C=dict_adjcent(A, n)
        
        print(C)
        m=np.sum(C,axis=1)
        m[cc[0]]=0
        loc=np.argmax(m)
        print(loc)
        cc.append(loc)
    
    return cc
        
db='multicc'
M,WL=read_data.read_data_sample(db)
#WT=WL[2]
#per1,per2=statistic_number_column(WT.content,WT.row_num, WT.number_start)
F=[]
fpath='multicc'
#Cs,Cw,td,wd=initial_candidate2(WT,M[0],WT.row_num,True,db)
#NS,Uw,Cw,ctf,C,CR=core_column_iterative(Cs,Cw,WT,0.2,0.85,0.7,0.85,50,0.01,1,td,wd)   
fl=os.listdir(fpath+'_result/')
f=open('need_multi.data','rb')
nd=pickle.load(f)
f.close()
CC={}
for i in range(94):
    #f=open(fpath+'_result/'+M[i]+'_cc.data','rb')
    #cc=pickle.load(f)
    #f.close()
    '''
    if M[i] in nd:
        #F.append(i)
        #print(cc,'st')
        WL[i].number_start=WL[i].column_num
        state=save_core_result(M[i],WL[i],fpath,i,True,db,0.0001,1,0.01)    
        cc=multi_result(M[i], WL[i].column_num)
    
        #print(cc,'ed')
        CC[M[i]]=cc
    '''
'''
f=open('../result/multicc_res.data','rb')
mr=pickle.load(f)
f.close()

N=0
nd=[]
for i in range(94):
    
    if set(CC[M[i]])!=set(mr[M[i]]):
        
        nd.append(M[i])

'''
'''
db='t2d'
M,WL=read_data.read_data_sample(db)
fpath='Noise/Sample_aft/'+db+'/'

f=open('../result/'+db+'_pro'+'_res.data','rb')
ir=pickle.load(f)
f.close()


i=8
s=8


state=save_core_result_sample_aft(M[i],WL[i],fpath+str(s),i,True,s,db,ir[i])
'''
'''
db='iswc'

M,WL=read_data.read_data_sample(db)
Q=[1.75]

#E=[0.001,0.002,0.005,0.02,0.05,0.1]
fpath='para_q_result/'
for q in Q:
    
    ise=os.path.exists(fpath+db+'_valid_'+str(q)+'_result')
    if not ise:
        os.makedirs(fpath+db+'_valid_'+str(q)+'_result')
    
    for i in range(len(M)):
        state=save_core_result(M[i],WL[i],fpath+db+'_valid_'+str(q),i,True,db,q,0.01)    
    

db='t2d'
M,WL=read_data.read_data_sample(db)

Q=[1.75]
#E=[0.001,0.002,0.005,0.02,0.05,0.1]
fpath='para_q_result/'
for q in Q:
    
    ise=os.path.exists(fpath+db+'_valid_'+str(q)+'_result')
    if not ise:
        os.makedirs(fpath+db+'_valid_'+str(q)+'_result')
    
    for i in range(len(M)):
        state=save_core_result(M[i],WL[i],fpath+db+'_valid_'+str(q),i,True,db,q,0.01)    
    

'''





'''
for i in range(len(M)):
    state=save_core_result(M[i],WL[i],db+'_valid',i,True,db,1,0.01)    

#Q=[0.5,0.75,1.25,1.5,2.0]
E=[0.001,0.002,0.005,0.02,0.05,0.1]
for e in E:
    L=os.listdir('para_eta_result/'+db+'_valid_'+str(e)+'_result')
    nr=[]
    nnr=[]
    CC={}
    f=open('para_eta_result/'+db+'_'+str(e)+'_res.data','rb')
    pr=pickle.load(f)
    f.close()
    for i in range(len(M)):

        if M[i]+'_cc.data' in L and i in pr:
        
            f=open('para_eta_result/'+db+'_valid_'+str(e)+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            if cc==0:
                cc=[0]
            if WL[i].number_start==1:
                pr[i]=[0]
            
            CC[i]=cc
        elif i in pr:
            if WL[i].number_start==1:
                pr[i]=[0]
            
            CC[i]=pr[i]
    n=0        
    for i in pr:
        
        if ir[i][0]!=CC[i][0]:
            
            n+=1
            
    print(n)
            
f=open('para_eta_result/iswc_eta_n.data','rb')            
en=pickle.load(f)
f.close()
print(en)
'''

"""
db='iswc'

M,WL=read_data.read_data_sample(db)

#L=os.listdir(db+'_valid_result/')
f=open('../result/'+db+'_pro_res.data','rb')
pr=pickle.load(f)
f.close()
'''
f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()

fpath=db+'_valid'
n=0
for i in range(len(M)):
    
    #if i in pr and pr[i][0]!=ir[i][0]:
    #   n+=1
    state=save_core_result(M[i],WL[i],fpath,i,True,db,0.75,0.01)
    

f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
'''
#Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
Noi=list(range)
fpath='Noise/Noise_random_valid/'
#Q=[0.5,0.75,1.25,1.5,2.0]
#Q=[0.001,0.002,0.005,0.02,0.05,0.1]
for j in range(10):
    L=os.listdir(fpath+db+'/'+str(Noi[j])+'_result/')

    for i in range(len(M)):
    
        if M[i]+'_A.data' in L:
        
            f=open(fpath+db+'/'+str(Noi[j])+'_result/'+M[i]+'_A.data','rb')            
            C=pickle.load(f)
            f.close()
            per1,per2=statistic_number_column(WL[i].content,WL[i].row_num, WL[i].number_start)
            for p in C:
                
                if per1[p[0]]>0.5:
                    
                    C[p]=0
                    
                elif per2[p[0]]<5:
                    
                    C[p]=0
                    
                elif per2[p[1]]<5:
                    
                    C[p]=0
                
                    
            cc=core_final_result(C,WL[i].number_start)
            f=open(fpath+db+'/'+str(Noi[j])+'_result/'+M[i]+'_cc.data','wb')
            pickle.dump(cc,f)
            f.close()
"""
'''
db='iswc'

M,WL=read_data.read_data_sample(db)
I=np.zeros((4,10))
#Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
Noi=list(range(2,22,2))
fpath='Noise/Noise_random_valid/'+db+'/'
Res={}

for j in range(10):
    
    prepath='Noise/Sample_pre/'+db+'/'+str(Noi[j])+'_result/'
    aftpath='Noise/Sample_aft/'+db+'/'+str(Noi[j])+'_result/'
    
    F=valid_num(prepath,aftpath,db,M,Noi[j],WL)
    print(len(F))
    Res[j]=F
    I[0][j]=1-len(F)/180
    
print(I[0])


db='t2d'

M,WL=read_data.read_data_sample(db)
fpath='Noise/Noise_random_valid/'+db+'/'
Res={}

for j in range(10):
    
    prepath='Noise/Sample_pre/'+db+'/'+str(Noi[j])+'_result/'
    aftpath='Noise/Sample_aft/'+db+'/'+str(Noi[j])+'_result/'
    
    F=valid_num(prepath,aftpath,db,M,Noi[j],WL)
    print(len(F))
    Res[j]=F
    I[1][j]=1-len(F)/233
    


Noi=list(range(2,22,2))    
db='git'
I=np.zeros(10)
M,WL=read_data.read_data_sample(db)
fpath='Noise/Noise_random_valid/'+db+'/'
Res={}

for j in range(10):
    
    prepath='Noise/Sample_pre/'+db+'/'+str(Noi[j])+'_result/'
    aftpath='Noise/Sample_aft/'+db+'/'+str(Noi[j])+'_result/'
    
    F=valid_num(prepath,aftpath,db,M,Noi[j],WL)
    print(len(F))
    Res[j]=F
    I[j]=1-len(F)/460    

    
db='wiki'

M,WL=read_data.read_data_sample(db)
fpath='Noise/Noise_random_valid/'+db+'/'
Res={}

for j in range(10):
    
    prepath='Noise/Sample_pre/'+db+'/'+str(Noi[j])+'_result/'
    aftpath='Noise/Sample_aft/'+db+'/'+str(Noi[j])+'_result/'
    
    F=valid_num(prepath,aftpath,db,M,Noi[j],WL)
    print(len(F))
    Res[j]=F
    I[3][j]=1-len(F)/428 

'''
'''    
for j in [0,3,5,6]:
    
    prepath='Noise/Noise_random/'+db+'/'+str(Noi[j])
    aftpath=fpath+str(Noi[j])    
    for i in Res[j]:
        if db=='git':
            k=M.index(i)
            state=save_core_result_noise(M[k],WL[k],prepath,aftpath,k,True,Noi[j],db)
        else:
            state=save_core_result_noise(M[i],WL[i],prepath,aftpath,i,True,Noi[j],db)
            
'''

        
'''
    N[j]=[]
    F[j]=[]
    num[j]=0
    L=os.listdir(fpath+str(Noi[j])+'_result/')
    f=open('Noise/Noise_random/'+db+'/'+str(Noi[j])+'_res.data','rb')
    pr=pickle.load(f)
    f.close()
    
    for i in range(len(M)):
    
        if M[i]+'_cc.data' in L:
            f=open(fpath+str(Noi[j])+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            if cc==0:
                cc=[0]
            if i not in pr:
                pr[i]=[0]
            if pr[i][0]==ir[i][0] and ir[i][0]!=cc[0]:
                N[j].append(i)
            if pr[i][0]!=ir[i][0] and ir[i][0]==cc[0]:
                F[j].append(i)
        elif i in pr and pr[i][0]!=ir[i][0]:
            num[j]+=1
    
        if i in pr and cc[0]!=ir[i][0]:
            F.append(i)
            #print(pr[i],ir[i],cc)
    if i in pr and pr[i][0]!=ir[i][0]:
        A.append(i)
'''
       



"""
f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
fpath='Noise/Noise_random_valid/'
for j in range(9):
    '''
    ise=os.path.exists(fpath+db+'/'+str(Noi[j])+'_result')
    if not ise:
        os.makedirs(fpath+db+'/'+str(Noi[j])+'_result')
    '''
    n=0
    L=os.listdir(fpath+db+'/'+str(Noi[j])+'_result')
    L2=os.listdir('Noise/Noise_random/'+db+'/'+str(Noi[j])+'_result')
    for i in range(len(M)):
        
        if M[i]+'_cc.data' in L:
            
            f=open(fpath+db+'/'+str(Noi[j])+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            
            if cc==0:
                cc=[0]
            if cc[0]!=ir[i][0]:
                
                n+=1
        elif M[i]+'_cc.data' in L2:
            
            f=open(fpath+db+'/'+str(Noi[j])+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            if cc==0:
                cc=[0]
            if cc[0]!=ir[i][0]:
                
                n+=1
    print(n)
        #state=save_core_result_noise(M[i],WL[i],fpath+db+'/'+str(Noi[j]),i,False,Noi[j],db) 
        #wt_name,WT,fpath,order,ifsample,nper,db



db='t2d'

M,WL=read_data.read_data_sample(db)

f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
fpath='Noise/Noise_random_valid/'
for j in range(9):
    ise=os.path.exists(fpath+db+'/'+str(Noi[j])+'_result')
    if not ise:
        os.makedirs(fpath+db+'/'+str(Noi[j])+'_result')
   
    for i in range(len(M)):
        state=save_core_result_noise(M[i],WL[i],fpath+db+'/'+str(Noi[j]),i,False,Noi[j],db) 

db='wiki'

M,WL=read_data.read_data_sample(db)

f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
fpath='Noise/Noise_random_valid/'
for j in range(9):
    ise=os.path.exists(fpath+db+'/'+str(Noi[j])+'_result')
    if not ise:
        os.makedirs(fpath+db+'/'+str(Noi[j])+'_result')
   
    for i in range(len(M)):
        state=save_core_result_noise(M[i],WL[i],fpath+db+'/'+str(Noi[j]),i,False,Noi[j],db) 


db='git'

M,WL=read_data.read_data_sample(db)
'''
f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
'''
Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
fpath='Noise/Noise_random_valid/'
for j in range(9):
    ise=os.path.exists(fpath+db+'/'+str(Noi[j])+'_result')
    if not ise:
        os.makedirs(fpath+db+'/'+str(Noi[j])+'_result')
   
    for i in range(len(M)):
        state=save_core_result_noise(M[i],WL[i],fpath+db+'/'+str(Noi[j]),i,False,Noi[j],db) 

"""

'''    
M,WL=read_data.read_data_sample('wiki')

    
db='wiki'
fai=[]
f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()

fpath='wiki'
#Noi=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
CC={}
for i in range(len(M)):

    try:
        f=open(fpath+'_result/'+M[i]+'_cc.data','rb')
        cc=pickle.load(f)
        f.close()
        if cc==0:
            CC[i]=[cc]
        else:
            CC[i]=cc
    except:
        fai.append(i)

C2={}
C1={}
for i in CC:

    try:
    
        f=open(fpath+'_result/'+M[i]+'_A.data','rb')
        A=pickle.load(f)
        f.close()
        c1,c2=process_cc(M[i],fpath,WL[i].number_start)
        C2[i]=c2
        C1[i]=c1
    except:
        fai.append(i)
    
    
N=0
N2=0
N1=0
for i in CC:
    if i in ir and CC[i][0]!=ir[i][0]:
        N+=1
    
for i in C2:
    if i in ir and C2[i][0]!=ir[i][0]:
        N2+=1
for i in C1:
    if i in ir and C1[i][0]!=ir[i][0]:
        N1+=1   

            
f=open(fpath+'_res.data','wb')
pickle.dump(C2,f)
f.close()

print(N,N2,N1)
'''

"""

f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()


for j in range(9):
    
    CC={}
    for i in range(len(M)):
    
        try:
            f=open(fpath+str(Noi[j])+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            if cc==0:
                CC[i]=[cc]
            else:
                CC[i]=cc
        except:
            fai.append(i)

    C2={}
    C1={}
    for i in CC:
    
        try:
        
            f=open(fpath+str(Noi[j])+'_result/'+M[i]+'_A.data','rb')
            A=pickle.load(f)
            f.close()
            c1,c2=process_cc(M[i],fpath+str(Noi[j]),WL[i].number_start)
            C2[i]=c2
            C1[i]=c1
        except:
            fai.append(i)
        
        
    N=0
    N2=0
    N1=0
    for i in CC:
        if i in ir and CC[i][0]!=ir[i][0]:
            N+=1
        
    for i in C2:
        if i in ir and C2[i][0]!=ir[i][0]:
            N2+=1
    for i in C1:
        if i in ir and C1[i][0]!=ir[i][0]:
            N1+=1                
    f=open(fpath+str(Noi[j])+'_res.data','wb')
    pickle.dump(C2,f)
    f.close()
    print(N,N2,N1)
    
 

#git_label
for j in range(9):
    
    CC={}
    for i in range(len(M)):
    
        try:
            f=open(fpath+str(Noi[j])+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            if cc==0:
                CC[M[i]]=[cc]
            else:
                CC[M[i]]=cc
        except:
            fai.append(i)
    
    N,_,W=obtain_git_pre(CC)
    C2={}
    C1={}
    for i in W:
    
        try:
            k=M.index(i)
            f=open(fpath+str(Noi[j])+'_result/'+i+'_A.data','rb')
            A=pickle.load(f)
            f.close()
            c1,c2=process_cc(i,fpath+str(Noi[j]),WL[k].number_start)
            C2[i]=c2
            C1[i]=c1
        except:
            fai.append(i)
        
        
    
    N2,_,W2=obtain_git_pre(C2)
    N1,_,W1=obtain_git_pre(C1)
    
        for i in CC:
            if CC[i][0]!=ir[i][0]:
                N+=1
        
        for i in C2:
            if C2[i][0]!=ir[i][0]:
                N2+=1
        for i in C1:
            if C1[i][0]!=ir[i][0]:
                N1+=1 
    
    
    f=open(fpath+str(Noi[j])+'_res.data','wb')
    pickle.dump(C2,f)
    f.close()
    print(N,N2,N1)  
"""   
"""


for j in range(5,9):
    
    ise=os.path.exists(fpath+str(Noi[j])+'_result')
    if not ise:
        os.makedirs(fpath+str(Noi[j])+'_result')
    
    
    fpa=fpath+str(Noi[j])
    
    f=open(fpath+str(Noi[j])+'_res.data','rb')
    irr=pickle.load(f)
    f.close()
    
    for i in range(len(M)):
        
        try:
            if irr[i][0]!=ir[i][0]:
                state=save_core_result_sample(M[i],WL[i],fpa,i,True,Noi[j],db)
            
        except:
            fai.append(i)

"""
      


"""
f=open('../result/t2d_pro_res.data','rb')
pv=pickle.load(f)
f.close()


CC={}
AA={}
P={}
Cp={}
Cr={}
q=0.1
for i in range(len(M)):
    
    try:
        f=open(fpath+'_result/t2d_'+str(q)+'_result/'+M[i]+'_cc.data','rb')
        cc=pickle.load(f)
        f.close()
        
        f=open(fpath+'_result/t2d_'+str(q)+'_result/'+M[i]+'_A.data','rb')
        A=pickle.load(f)
        f.close()
        
        f=open(fpath+'_result/t2d_'+str(q)+'_result/'+M[i]+'_per.data','rb')
        per=pickle.load(f)
        f.close()
        
        C=dict_adjcent(A,WL[i].number_start)
        CC[i]=cc
        AA[i]=C
        P[i]=per
        
        Cp[i],Cr[i]=process_cc(M[i], fpath, WL[i].number_start)
    except:
        print(i)

"""

'''
f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()

fa=[]

f=open('../result/'+db+'_'+'pro'+'_res.data','rb')
irr=pickle.load(f)
f.close()

for i in range(len(M)):
    try:
        if irr[i][0]!=ir[i][0]:
            
            #p=random.random()
            #if p>0.3:
            state=save_core_result(M[i],WL[i],fpath,i,True,db,1,0.01)
    except:
        fa.append(i)


CC={}
#fpa=fpath+'_'+str(Q[j])
#q=Q[j]
for i in range(len(M)):

    try:
        f=open(fpath+'_result/'+M[i]+'_cc.data','rb')
        cc=pickle.load(f)
        f.close()
        if cc==0:
            CC[i]=[cc]
        else:
            CC[i]=cc
    except:
        fai.append(i)

C2={}
C1={}
for i in CC:

    try:
    
        f=open(fpath+'_result/'+M[i]+'_A.data','rb')
        A=pickle.load(f)
        f.close()
        c1,c2=process_cc(M[i],fpath,WL[i].number_start)
        C2[i]=c2
        C1[i]=c1
    except:
        fai.append(i)
    
    
N=0
N2=0
N1=0
for i in CC:
    if i in ir and CC[i][0]!=ir[i][0]:
        N+=1
    
for i in C2:
    if i in ir and C2[i][0]!=ir[i][0]:
        N2+=1
for i in C1:
    if i in ir and C1[i][0]!=ir[i][0]:
        N1+=1 
               
f=open('para_q_result/'+db+'_'+str(q)+'_res.data','wb')
pickle.dump(C2,f)
f.close()

print(N,N2,N1)

'''
"""
fa=[]
for q in [0.002,0.02]:
    fpath='para_eta_result/'+db+'_'+str(q)
    '''
    f=open('para_eta_result/'+db+'_'+str(q)+'_res.data','rb')
    irr=pickle.load(f)
    f.close()
    '''
    for i in range(len(M)):
        try:
            #if irr[i][0]!=ir[i][0]:
                
            #p=random.random()
            #if p>0.3:
            state=save_core_result(M[i],WL[i],fpath,i,False,db,1,q)
        except:
            fa.append((q,i))
"""
"""
M,WL=read_data.read_data_sample('ISWC')    
db='iswc'
fpath='para_eta_result/'+db

f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
fa=[]

for q in [0.02]:
    fpath='para_eta_result/'+db+'_'+str(q)
    
    f=open('para_eta_result/'+db+'_'+str(q)+'_res.data','rb')
    irr=pickle.load(f)
    f.close()
    
    for i in range(len(M)):
        try:
            if irr[i][0]!=ir[i][0]:
                
            #p=random.random()
            #if p>0.3:
                state=save_core_result(M[i],WL[i],fpath,i,False,db,1,q)
        except:
            fa.append((q,i))


Q=[0.001,0.002,0.005,0.02,0.05,0.1]
QQ={}
CC={}
f=open('../result/'+db+'_res.data','rb')
ir=pickle.load(f)
f.close()
fai=[]
for j in range(6):
    
    CC={}
    fpa=fpath+'_'+str(Q[j])
    q=Q[j]
    for i in range(len(M)):
    
        try:
            f=open(fpa+'_result/'+M[i]+'_cc.data','rb')
            cc=pickle.load(f)
            f.close()
            if cc==0:
                CC[i]=[cc]
            else:
                CC[i]=cc
        except:
            fai.append(i)

    C2={}
    C1={}
    for i in CC:
    
        try:
        
            f=open(fpa+'_result/'+M[i]+'_A.data','rb')
            A=pickle.load(f)
            f.close()
            c1,c2=process_cc(M[i],fpa,WL[i].number_start)
            C2[i]=c2
            C1[i]=c1
        except:
            fai.append(i)
        
        
    N=0
    N2=0
    N1=0
    for i in CC:
        if i in ir and CC[i][0]!=ir[i][0]:
            N+=1
        
    for i in C2:
        if i in ir and C2[i][0]!=ir[i][0]:
            N2+=1
    for i in C1:
        if i in ir and C1[i][0]!=ir[i][0]:
            N1+=1 
    '''               
    f=open('para_q_result/'+db+'_'+str(q)+'_res.data','wb')
    pickle.dump(C2,f)
    f.close()
    '''
    QQ[q]=N2
    print(N,N2,N1)

    
f=open('para_eta_result/iswc_q_n.data','wb')
pickle.dump(QQ,f)
f.close()
"""
""" 
M,WL=read_data.read_data_sample('t2d')
f=open('../result/t2d_gor_res.data','rb')
GG=pickle.load(f)
f.close()

FF=[]

for i in range(233):
    
    FF.append(non_label_t2d(M[i],GG,i))

#CC={}

#kk=14
#per=statistic_number_column(WL[0].content, WL[0].number_start)
#Cs,Cw,td,wd=initial_candidate2(WL[kk],M[kk],5)
fpath='wiki'

fa=[39,43,103,159,158]
faa=[]   
#print(con)    
           
f=open('need_restart_iswc.data','rb')
R=pickle.load(f)
f.close() 
#R=[]
   
L=[] 
PP={}
for i in range(180):
    
    try:
        
        f=open(fpath+'_result/'+M[i]+'_cc.data','rb')
        cc=pickle.load(f)
        f.close()
        PP[i]=cc
        
        if i not in R:
            CC[i]=cc
            
        else:
            print(cc)
            print(WL[i].header,M[i])
            print(i)
            
    
    except:
        
        print(i)
    

  
for i in range(12):
    
    
    wt_name=R[i]
    f=open('../../web_table/t2d_example/'+R[i]+'_ccl.data','rb')
    ccl=pickle.load(f)
    f.close()
    
    f=open(fpath+'_result/'+wt_name+'_ctf.data','rb')
    ctf=pickle.load(f)
    f.close()
    f=open(fpath+'_result/'+wt_name+'_A.data','rb')
    C=pickle.load(f)
    f.close()
    per1,per2=statistic_number_column(WL[M.index(R[i])].content, WL[M.index(R[i])].row_num,WL[M.index(R[i])].number_start)
    for p in C:
        
        if per1[p[0]]>0.5:
            
            C[p]=0
            
        elif per2[p[0]]<5:
            
            C[p]=0
            
        elif per2[p[1]]<5:
            
            C[p]=0
            
            
    cc=core_final_result(C,WL[M.index(R[i])].number_start)
    
    
    print(ccl,ctf,cc,i)
    
    try:
        
        flag=non_label_t2d(R[i])
        #CC[i]=flag[0]
        #print(flag,WL[R[i]].row_num)
        #if WL[R[i]].row_num>10:
        #    L.appemd(R[i])
        print(flag)
        
        #if flag[0]==True:
        #    L.append(i)
        
    except:
        fa.append(i)

"""    

#F=[]
"""
f=open('../../../数据集/wikitable/xml_results/f3.data','rb')
F1=pickle.load(f)
f.close()


for k in range(len(fa)):
    
    
    if i in R:
        
        ifs=True
    else:
        ifs=False
    
    i=fa[k]
    flag=0
    WT=WL[i]
    wt_name=M[i]
    
    for ii in WT.content:
        
        for j in ii:
            
            if j!='':
                flag=1
        
    print(M[i])
    if flag==0:
        faa.append(i)
    else:
        state=save_core_result(wt_name,WT,fpath,i,True)
    if state=='fail':
        
        faa.append(i)        

"""

            
            







#f=open('t2d_result_now.data','rb')
#CC=pickle.load(f)
#f.close()


