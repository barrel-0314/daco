import numpy as np
import Levenshtein
from sklearn.cluster import KMeans #导入K均值聚类算法
import pickle
import networkx as nx
import math

def Lexical_Similarity(entity,mention):
    
    ED=1-Levenshtein.distance(entity.upper(), mention.upper())/max(len(entity),len(mention))
    LD=len(list(set(entity.upper()).intersection(mention.upper())))/max(len(entity),len(mention))
    
    if (entity.upper() in mention.upper()) or (mention.upper() in entity.upper()):
        SI=1
    else:
        SI=0
    
    score=np.sum(np.array([ED,LD,SI]))/3
    return score

def Type_array(can_set):
    
    n=len(can_set)
    eer=np.zeros((n,n))
    ee=np.zeros((n,n))
    el=np.zeros((n,n))
    ll=np.zeros((n,n))
    
    for i in range(n):
        
        for j in range(n):
            if i>j:
                can0=can_set[i]
                can1=can_set[j]
                if can0.literal==False and can1.literal==False:
                    if not(len(can0.c_type)==0 or len(can1.c_type)==0):
                        """
                            et=len(list(set(can0.c_type).intersection(can1.c_type)))/max(len(can1.c_type),len(can0.c_type))
                            else:
                                et=0
                                if not(len(can0.rin)==0 or len(can1.rin)==0):
                                    er=len(list(set(can0.rin).intersection(can1.rin)))/max(len(can1.rin),len(can0.rin))
                                    else:
                                        er=0
                                        n1=len(can0.c_type)
                                        n2=len(can1.c_type)
                                        ee[i][j]=(et+er)/2
                        """
                        e1=len(list(set(can0.c_type).intersection(can1.c_type)))/max(len(can1.c_type),len(can0.c_type))
                        if not(len(can0.rin)==0 or len(can1.rin)==0):
                            e2=len(list(set(can0.rin).intersection(can1.rin)))/max(len(can1.rin),len(can0.rin))
                            eer[i][j]=(e1+e2)/2
                            eer[j][i]=eer[i][j]
                        else:
                            ee[i][j]=e1
                            ee[j][i]=ee[i][j]
                    else:
                        if not(len(can0.rin)==0 or len(can1.rin)==0):
                            e2=len(list(set(can0.rin).intersection(can1.rin)))/max(len(can1.rin),len(can0.rin))
                            ll[i][j]=e2
                            ll[j][i]=ll[i][j]
                elif can0.literal==True and can1.literal==True:
                    if not(len(can0.rin)==0 or len(can1.rin)==0):
                    
                        ll[i][j]=len(list(set(can0.rin).intersection(can1.rin)))/max(len(can1.rin),len(can0.rin))
                        ll[j][i]=ll[i][j]
                else:
                    if not(len(can0.rin)==0 or len(can1.rin)==0):
                    
                        el[i][j]=len(list(set(can0.rin).intersection(can1.rin)))/max(len(can1.rin),len(can0.rin))
                        el[j][i]=el[i][j]
            
    return ee,el,ll,eer
    
def Type_Similarity(ee,el,ll,eer,loc):
    
    m,n=np.shape(ee)
    
    #N1=n-np.size(np.argwhere(ee[loc]))
    #N2=n-np.size(np.argwhere(el[loc]))
    #N3=n-np.size(np.argwhere(ll[loc]))
    if np.max(ee)!=0:
        een=ee/np.max(ee)
    else:
        een=np.zeros((m,n))
    if np.max(el)!=0:
        
        eln=el/np.max(el)
    else:
        eln=np.zeros((m,n))
        
    if np.max(ll)!=0:
        
        lln=ll/np.max(ll)
    else:
        lln=np.zeros((m,n))
    if np.max(eer)!=0:
        
        eern=eer/np.max(eer)
    else:
        eern=np.zeros((m,n))
        
    #print(np.sum(een[loc]),np.sum(eln[loc]),np.sum(lln[loc]))
    ts=(np.sum(een[loc])+np.sum(eln[loc])+np.sum(lln[loc])+np.sum(eern[loc]))/n
    
    return ts
    
def initial_candidate_weight(can_set):
    can_w={}
    for pos in can_set:
        
        can_w[pos]=[1]*len(can_set[pos])
    return can_w
        
def candidate_score(can_set,can_w,col_num):
    
    can_s={}
    can_tarray={}
    for col in range(col_num):
        can_col=[]
        for p in can_set:
            if p[1]==col:
                can_col+=can_set[p]
        ee,el,ll,eern=Type_array(can_col)
        can_tarray[col]={}
        can_tarray[col]['ts']=[ee,el,ll,eern]
        can_tarray[col]['set']=can_col
    
    
    for pos in can_set:
        can_s[pos]=[]
        for c in can_set[pos]:
            ls=Lexical_Similarity(c.name,c.mention)
            loc=can_tarray[pos[1]]['set'].index(c)
            #print(loc,can_tarray[pos[1]]['ts'][0])
            ts=Type_Similarity(can_tarray[pos[1]]['ts'][0],can_tarray[pos[1]]['ts'][1],can_tarray[pos[1]]['ts'][2],can_tarray[pos[1]]['ts'][3],loc)
            #print(can_set[pos].index(c))
            can_s[pos].append([ls,ts,can_w[pos][can_set[pos].index(c)]])
            
    return can_s

def column_type(can_set,can_s):
    
    Column_type={}
    can_num={}
    
    for pos in can_set:
        
        if pos[1] not in Column_type:
            Column_type[pos[1]]={}
        if pos[1] not in can_num:
            can_num[pos[1]]=0
        for i in range(len(can_set[pos])):
            c=can_set[pos][i]
            if c.literal==False:
                ct=list(set(c.c_type+c.rin))
                
                for t in ct:
                    t_normal=str(t).split('/')[-1]
                    if t_normal not in Column_type[pos[1]]:
                        Column_type[pos[1]][t_normal]=can_s[pos][i][0]*can_s[pos][i][1]*can_s[pos][i][2]
                    else:
                        Column_type[pos[1]][t_normal]+=can_s[pos][i][0]*can_s[pos][i][1]*can_s[pos][i][2]
            else:
                
                cr=c.rin
                for t in cr:
                    if can_s[pos][i][0]==0 or can_s[pos][i][1]==0:
                        continue
                    t_normal=str(t).split('/')[-1]
                    if t_normal not in Column_type[pos[1]]:
                        Column_type[pos[1]][t_normal]=can_s[pos][i][0]*can_s[pos][i][1]*can_s[pos][i][2]
                    else:
                        Column_type[pos[1]][t_normal]+=can_s[pos][i][0]*can_s[pos][i][1]*can_s[pos][i][2]
            
            can_num[pos[1]]+=len(can_s[pos])
    ct={} 
    #print(Column_type)       
    for col in Column_type:
        ct[col]={}
        if Column_type[col]=={}:
            
            continue
        
        #print(Column_type)
        M=max(list(Column_type[col].values()))
        #print(M)
        for t in Column_type[col]:
            if Column_type[col][t]!=0:
                ct[col][t]=(Column_type[col][t])/M
                
        ct[col]=sorted(ct[col].items(),key=lambda kv:(kv[1],kv[0]),reverse=True)
    
    return ct         
                
def weight_column_type_score(Cot,Tw):
    
    ct={}
    for col in Cot:
        T=[i[0] for i in Cot[col]]
        ct[col]={}
        for t in T:
            #print(Tw[col][t])
            #print(Cot)
            loc=T.index(t)
            ct[col][t]=Tw[col][t]*Cot[col][loc][1]
    
    cot={}    
    for col in ct:
        cot[col]={}
        if ct[col]=={}:
            continue
        T=list(ct[col].keys())
        M=max(list(ct[col].values()))
        fl=1
        if 'owl#thing' in T and ct[col]['owl#thing']==M:
            fl=0
            #loc=T.index('owl#thing')
            ct[col]['owl#thing']=0
            M=max(list(ct[col].values()))
            if 'name' in T and ct[col]['name']==M:
                #loc2=T.index('name')
                ct[col]['name']=0
                M=max(list(ct[col].values()))
                fl=2
        elif 'name' in T and ct[col]['name']==M:
            ct[col]['name']=0
            M=max(list(ct[col].values()))
            fl=3
            #print(M,col)
        M=max(list(ct[col].values()))
        #print(M,fl,ct[col].values(),ct)
        for t in ct[col]:
            if fl==0 and t=='owl#thing':
                cot[col][t]=1
            elif fl==2 and t=='owl#thing':
                cot[col][t]=1
            elif fl==3 and t=='name':
                cot[col][t]=1
            else:
                #print(fl,col,M)
                cot[col][t]=ct[col][t]/M
                #print(fl,cot[col][t],M)
                
        
        cot[col]=sorted(cot[col].items(),key=lambda kv:(kv[1],kv[0]),reverse=True)
    
    return cot
                            
def column_type_filter(ct):
    
    Column_type={}
    for c in ct:
        Column_type[c]={}
        if len(ct[c])<4:
            for f in range(len(ct[c])):
                Column_type[c][ct[c][f][0]]=ct[c][f][1]
            continue
        else:
            C1={}
            C2={}
            for f in range(len(ct[c])):
                #print(ct[c])
                if ct[c][f][1]>0.75:
                    C1[ct[c][f][0]]=ct[c][f][1]
        
            type_score=(np.array([i[1] for i in ct[c]])).reshape(-1,1)
            k=2
            kmodel = KMeans(n_clusters = k)
            kmodel.fit(type_score)
            #L.append(kmodel.labels_)
            flag=kmodel.labels_[0]
            for f in range(len(ct[c])):
            
                if kmodel.labels_[f]==flag:
                    C2[ct[c][f][0]]=ct[c][f][1]
            if len(C1.keys())>len(C2.keys()):
                Column_type[c]=C2
            else:
                Column_type[c]=C1
    
                
    for c in Column_type:
        
       
        
            
        if 'rdf-schema#seeAlso' in Column_type[c]:
                
            del Column_type[c]['rdf-schema#seeAlso']
            
        if 'name' in Column_type[c] and len(list(Column_type[c].keys()))>1:
            
            del Column_type[c]['name']
            
        if 'owl#thing' in Column_type[c] and len(list(Column_type[c].keys()))>1:
            
            del Column_type[c]['owl#thing']
            
        if len(list(Column_type[c].keys()))>1:
            
            L=list(Column_type[c])
            for l in L:
                
                if 'a'<=l[0]<='z':
                    
                    ll=l[0].upper()+l[1:]
                    if ll in Column_type[c]:
                        
                        del Column_type[c][l]        
        
                
    return Column_type 

def og_distance(t1,t2):
    
    f=open('../column correction/ontology_graph_undirect.data','rb')
    ogud=pickle.load(f)
    f.close()
    
    if t1 not in ogud.nodes() or t2 not in ogud.nodes():
        d=100
    else:    
        if nx.has_path(ogud,t1,t2)==True:
        
            d=nx.shortest_path_length(ogud,t1,t2)
        
        else:
        
            d=100
        
    return d

def closs(ct1,ct2,td,tic,ric,q,pt):
    Cn=0
    tl1=list(ct1.keys())
    tl2=list(ct2.keys())
    
    n1=len(ct1.keys())
    #w1={}
    #w2={}
    n2=len(ct2.keys())
    ttd=np.zeros((n1,n2))
    
    tt=np.zeros((n1,n2))
    tr=np.zeros((n1,n2))
    rr=np.zeros((n1,n2))
    #T=np.zeros((n1,n2))
    for t1 in ct1:
        #w1[t1]=1
        for t2 in ct2:
            #print(t1,t2)
            #w2[t2]=1
            loc1=tl1.index(t1)
            loc2=tl2.index(t2)
            if t1==t2:
                if ct1[t1]=='type':
                    tt[loc1][loc2]=1
                    #tt[loc2][loc1]=1
            elif ct1[t1]=='type' and ct2[t2]=='type':
                if t1 not in tic or t2 not in tic:
                    #print(t1,t2,'y')
                    
                    continue
                elif t1 not in td or t2 not in td:
                    tt[loc1][loc2]=tic[t1]+tic[t2]
                    #print(t1,t2,'n',tt[loc1][loc2])
                    
                else:
                    d=og_distance(t1,t2)
                    ttd[loc1][loc2]=(tic[t1]+tic[t2]+td[t1]+td[t2])/d
                    #ttd[loc1][loc2]=(1/(1+d*k1**(tic[t1]+tic[t2])+k2**(td[t1]+td[t2])))
                    #print(t1,t2,ttd[loc1][loc2])
                    #T[loc1][loc2]=tic[t1]+tic[t2]+td[t1]+t2[t2]
                #tt[loc2][loc1]=tt[loc1][loc2]
            elif ct1[t1]=='type' and ct2[t2]=='rel':
                if t1 not in tic or t1 not in td:
                    continue
                
                else:
                    
                    tr[loc1][loc2]=tic[t1]+ric[t2]
                    #tr[loc1][loc2]=((1/(1+k1**(tic[t1]+ric[t2]))))
                    #T[loc1][loc2]=tic[t1]+ric[t2]
                    
                    #tr[loc2][loc1]=tr[loc1][loc2]
            elif ct1[t1]=='rel' and ct2[t2]=='type':
                if t2 not in tic:
                    continue
                else:
                    tr[loc1][loc2]=ric[t1]+tic[t2]
                    #tr[loc1][loc2]=((1/(1+k1**(ric[t1]+tic[t2]))))
                    #T[loc1][loc2]=ric[t1]+tic[t2]
                    
                    #tr[loc2][loc1]=tr[loc1][loc2]
            else:
                rr[loc1][loc2]=ric[t1]+ric[t2]
                #rr[loc1][loc2]=((1/1+k1**(ric[t1]+ric[t2])))
                #T[loc1][loc2]=ric[t1]+ric[t2]
                
                #rr[loc2][loc1]=rr[loc1][loc2]
    if np.max(ttd)!=0:
        ttd=ttd/(np.max(ttd))
                
    if np.max(tt)!=0:
        tt=tt/(np.max(tt))
    if np.max(tr)!=0:
        tr=tr/(np.max(tr))
    if np.max(rr)!=0:
        rr=rr/(np.max(rr))
    #S=0
    #O=0
    #print(tt+tr+rr)
    Set=list(set(ct1).intersection(ct2))
    Nt2=0
    #Nr2=0
    tic2=0
    #ric2=0
    N2=len(ct2)
    O=0
    
    Loc=['Place','PopulatedPlace','Location','Settlement']
    sset=list(set(Set).intersection(Loc))
    if len(sset)!=0:
        for l in Loc:
            
            if l not in Set:
                
                Set.append(l)
    Spe=['Species','Eukaryote']
    sset=list(set(Set).intersection(Spe))      
    if len(sset)==len(Spe):
        Set=[]
        
    f2=0
    for t2 in ct2:
        
        if t2 in pt and t2 not in Set:
            O+=pt[t2][1]
            f2=1
            #print('o',pt[t2][1],O,n2)
        
        elif t2 not in pt and t2 not in Set:
            f2=1
            O+=1
        if t2 in Set:
            
            continue
            
        if ct2[t2]=='type' and t2 in tic:
            Nt2+=1
            tic2+=tic[t2]
            #N2+=1
        """
        elif ct2[t2]=='rel':
            Nr2+=1
            ric2=ric[t2]
            N2+=1
        """
        
    
    if Nt2==0:
        
        ic2=0
        
    else:
        
        ic2=tic2/Nt2
    
    """
    elif Nt2==0 and Nr2!=0:
        
        ic2=ric2/Nr2
        
    elif Nt2!=0 and Nr2==0:
        
        ic2=tic2/Nt2
        
    
    """
    
    
    
    S=0
    Nt1=0
    #Nr1=0
    tic1=0
    #ric1=0
    N1=len(ct1)   
    f1=0     
    for t1 in ct1:
        
        if t1 in pt and t1 not in Set:
            S+=pt[t1][0]
            #print('s',pt[t1][0],S,n1)
            f1=1
            #print('N',t1)
        if t1 in Set:
            continue
            
        if ct1[t1]=='type' and t1 in tic:
            Nt1+=1
            tic1+=tic[t1]
            #N1+=1
        """
        elif ct1[t1]=='rel':
            Nr1+=1
            ric1=ric[t1]
            N1+=1            
        """    
        #print(t1)
        
    if Nt1==0:
        
        ic1=0
       
    else:
        
        ic1=tic1/Nt1
    """    
    elif Nt1==0 and Nr1!=0:
        
        ic1=ric1/Nr1
        
    elif Nt1!=0 and Nr1==0:
        
        ic1=tic1/Nt1
    """ 
            
    for t1 in ct1:
        
        for t2 in ct2:
            #O=0
            loc1=tl1.index(t1)
            loc2=tl2.index(t2)
            #print(t1,t2,tt[loc1][loc2]+tr[loc1][loc2]+rr[loc1][loc2])
            
            
            Cn+=(tt[loc1][loc2]+tr[loc1][loc2]+rr[loc1][loc2]+ttd[loc1][loc2])
    #print('R',Cn,ct1,ct2)
    
    if ic2==0:
        
        ic=1
        
    else:
        
        ic=1/(1+np.exp(-(ic1/ic2)))
        
    S/=n1
    O/=n2
    if f1!=0 and f2==0:
        
        O=1
        
    elif f1==0 and f2!=0:
        
        S=0
        
    elif f1==0 and f2==0:
        
        if n1>n2:
            
            S=1
            O=1
            
        elif n2>n1:
            
            S=0
            
        else:
            
            S=0.5
            O=0.5
            
            
    #print('para',S,O,ic1,ic2,ic)
    Cn*=((S*O*ic)**q)
    Cn/=((n1*n2))
    return Cn
       
def initial_type_weight(Cot):

    type_w={}
    for col in Cot:
        type_w[col]={}
        #print('owl#thing' in Cot[col])
        for t in Cot[col]:
            type_w[col][t[0]]=1
                  
    return type_w
                
    
                
                
def calculate_closeness(ctf,q):
    f=open('../column correction/type_depth.data','rb')
    td=pickle.load(f)
    f.close()
    #f=open('../column_correction/type_freq.data','rb')
    #tf=pickle.load(f)
    #f.close()
    f=open('../column correction/type_ic.data','rb')
    tic=pickle.load(f)
    f.close()
    f=open('../column correction/rel_ic.data','rb')
    ric=pickle.load(f)
    f.close()
    
    f=open('../../KG/frequency_data/pt.data','rb')
    pt=pickle.load(f)
    f.close()
    
    Close={}
    Ctf={}
    #print(ctf)
    for col in ctf:
        Ctf[col]={}
        for t in ctf[col]:
            if not ('A'<=t[0]<='Z' or t=='owl#thing'):
                Ctf[col][t]='rel'
            else:
                Ctf[col][t]='type'
    for col in ctf:
        
        for rol in ctf:
            
            if col!=rol:    
                if ctf[col]=={} or ctf[rol]=={}:
                    Close[(col,rol)]=0
                else:
                    #print('col',col,rol)
                    cn=closs(Ctf[col],Ctf[rol],td,tic,ric,q,pt)
                    Close[(col,rol)]=cn
                    #print('rol',col,rol,cn)
            else:
                Close[(col,rol)]=1
    
    #print(Close)                  
    return Close

def close_mix(Close,CR,m,theta):
    
    CloseR={}
    CloseM={}
    MC=0
    MR=0
    for cp in Close:
        
        if cp in CR and cp[0]!=cp[1]:
            
            CloseR[cp]=len(CR[cp])/m
            if CloseR[cp]>MR:
                MR=Close[cp]
                
            if Close[cp]>MC:
                MC=Close[cp]
            #CloseM[cp]=Close[cp]*CloseR[cp]
            
        #elif :
            
            #CloseM[cp]=(1-theta)*Close[cp]
    for cp in Close:
            
        if cp in CR and cp[0]!=cp[1]:
            
            if MR==0:
                
                CloseM[cp]=Close[cp]
            elif MC==0:
                
                CloseM[cp]=CloseR[cp]
            else:
                CloseM[cp]=0.5*(Close[cp]+CloseR[cp]*(MC/MR))
            
        elif cp not in CR and cp[0]!=cp[1]:
            
            CloseM[cp]=0.5*Close[cp]
    
    return CloseR,CloseM,CR