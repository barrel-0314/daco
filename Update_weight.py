import numpy as np

def update_num(S,O,UN):
    
    for s in S:
        for o in O:
            UN[s][o]+=1
            UN[o][s]+=1
    return UN
              
#def update_weight()              
def update_array(ite,d,Cs,Rel,UN,n,S,O,Cw,Tw,cot,CR):
    
    #if ite==0:
        
        #for pos in Cs:
            
            #Uw[pos]=[1]*len(Cs[pos])
        #UN=np.zeros((n,n))
    #CR={}    
    UN=update_num(S,O,UN)
    Uw={}
    Utw={}
    for pos in Cs:
            
        Uw[pos]=[0]*len(Cs[pos])
    
    for col in cot:
        Utw[col]={}
        for t in cot[col]:
            #print(t)
            Utw[col][t[0]]=0
        
    for cp in Rel:
        if cp[1] in S:
            canl=Cs[cp]
            for can in canl:
                if can.name in Rel[cp]:
                    for r in Rel[cp][can.name]:
                        #r=Rel[cp][can.name]['node'][i]
                        
                        #print(r)
                        if r[0] in O:
                            
                            if (cp[1],r[0]) not in CR:
                                
                                CR[(cp[1],r[0])]=[cp[0]]
                                
                            else:
                                
                                if cp[0] not in CR[(cp[1],r[0])]:
                                    
                                    CR[cp[1],r[0]].append(cp[0])
                                
                            Uw[cp][canl.index(can)]=1
                            Uw[(cp[0],r[0])][r[1]]=1
                            #if r[-1] in list(cot[r[0]].keys()):
                            #    Utw[r[0]][r[-1]]=1
                            int_rel=list(set(can.rout).intersection(Cs[(cp[0],r[0])][r[1]].rin))
                            out_rel=list(set(can.rin).intersection(Cs[(cp[0],r[0])][r[1]].rout))
                            for ct in can.c_type:
                                #print(ct)
                                cct=str(ct).split('/')[-1]
                                Utw[cp[1]][cct]=1
                            for ct in Cs[(cp[0],r[0])][r[1]].c_type:
                                cct=str(ct).split('/')[-1]
                                Utw[r[0]][cct]=1
                            for re in int_rel:
                                ccr=str(re).split('/')[-1]
                                #Utw[cp[1]][re]=1
                                Utw[r[0]][ccr]=1
                            for re in out_rel:
                                ccr=str(re).split('/')[-1]
                                #Utw[cp[1]][re]=1
                                Utw[cp[1]][ccr]=1
                            #if r[-1] in can.rin:
                            #    Utw[cp[1]][r[-1]]=1
                            #if r[-1] in Cs[(cp[0],r[0])][r[1]].c_rin:
                            #    Utw[r[0]][ct]=1
                               
    
    for pos in Cw:
        #print(Uw[pos],len(Cw[pos]))
        for i in range(len(Cw[pos])):
            if Uw[pos][i]==0:
                p=(np.sum(UN[pos[1]]))/((n-1)*(ite+1))
                Cw[pos][i]*=(p*(d**(1/(ite+1))))
    for col in cot:
        for t in cot[col]:
            if Utw[col][t[0]]==0:
                p=(np.sum(UN[col]))/((n-1)*(ite+1))
                Tw[col][t[0]]*=(p*(d**(1/(ite+1))))
                    
    return Uw,Cw,Utw,Tw,CR
            
                               
                               
        
#Uw,Cw,Utw,Tw=update_array(0,0.85,Cs,Rel,np.zeros((4,4)),4,S,O,Cw,Tw,cot) 
        
            
        