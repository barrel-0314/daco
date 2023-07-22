import pickle
import difflib
import time
import Levenshtein
import os
#from candidate_generate import other_dir
#s='A'


#label='america'

#start=time.time()

def other_dir(label):
    
    if len(label)==0 or ord(label[0])>1000:        
        dire='other_1000'
    elif '1'<=label[0]<='9':
        if label[0]!='1'and label:
            dire='other_'+label[0]
        else:
            if len(label)==1:
                dire='other_non'
            elif '0'<=label[1]<='8':
                dire='other_08'
            elif label[1]=='9':
                dire='other_91'
            else:
                dire='other_non'
    elif label[0]=='0':
        
        dire='other_non'
    elif ord(label[0])<=100:
        dire='other_100'
    else:
        dire='other_500'
    
    return dire


def candidate_search_index(char):
    f=open('index_KG/list_data_char/'+char+'_llist.data','rb')
    el=pickle.load(f)
    f.close()

    #can=[]
    L={}

    for l in el:
        firstsplit=l.split('/')
        entity1=firstsplit[-1]
        if len(entity1) not in L:
            L[len(entity1)]=[entity1]
        
        else:
            L[len(entity1)].append(entity1)

    lenL={}
    for ll in L:
    
        if ll not in lenL:
            lenL[ll]=len(L[ll])
        
    lenL=sorted(lenL.items(),key=lambda kv:kv[0])
    N=5000
    n=0
    index_d={}
    temp=''
    temp_l=[]
    for i in range(len(lenL)):
    
        if temp=='':
        
            temp_l.append(lenL[i][0])
            
            n+=lenL[i][1]
            if n>N:
            
                if len(temp_l)>1:
                    index_d[(temp_l[0],temp_l[-1])]=n
                else:
                    index_d[(temp_l[0],temp_l[0])]=n
                temp_l=[]
                n=0
            else:
                temp='con'
            
        
        elif temp=='con':
        
            if lenL[i][1]>N:
                if len(temp_l)>1:
                    index_d[(temp_l[0],temp_l[-1])]=n
                else:
                    index_d[(temp_l[0],temp_l[0])]=n

                index_d[(lenL[i][0],lenL[i][0])]=lenL[i][1]
                temp_l=[]
                temp=''
                n=0
            else:
            
                temp_l.append(lenL[i][0])
                n+=lenL[i][1]
                if n>N:
            
                    if len(temp_l)>1:
                        index_d[(temp_l[0],temp_l[-1])]=n
                    else:
                        index_d[(temp_l[0],temp_l[0])]=n

                    temp_l=[]
                    n=0
                    temp=''
                else:
                    temp='con'
    if temp=='con':
        if len(temp_l)>1:
            index_d[(temp_l[0],temp_l[-1])]=n
        else:
            index_d[(temp_l[0],temp_l[0])]=n

        
    isExists = os.path.exists('index KG/list_data_char_index/'+char+'_ll')

    if not isExists:
        
        os.makedirs('index KG/list_data_char_index/'+char+'_ll')    
    f=open('index KG/list_data_char_index/'+char+'_ll/index_dict.data','wb')
    pickle.dump(index_d,f)
    f.close()        
                
    list_d={}
    
    for i in index_d:
        list_d[i]=[]
        for ll in L:
            if i[0]<=ll<=i[1]:
                list_d[i]+=L[ll]
        #lo=os.listdir('../KG/list_data_char_index/'+char+'_el/')
        f=open('index KG/list_data_char_index/'+char+'_ll/'+str(i[0])+'_to_'+str(i[1])+'.data','wb')
        pickle.dump(list_d[i],f)
        f.close()        
        
    return list_d    

def candidate_index(label,isliteral):
    
    if len(label)!=0 and isliteral==False:
        
        s=label[0].upper()
        if s>='A' and s<='Z':
            S=s
        else:
            S='other'
            
        #print(S)
        f=open('index KG/list_data_char_index/'+S+'_el/index_dict.data','rb')
        index_dict=pickle.load(f)
        f.close()
        
        tosearch=[]
        for rg in index_dict:
            if 0<=(len(label)-rg[1])<=3 or 0<=(rg[0]-len(label))<=3:
                #print(len(label)-rg[1],rg[0]-len(label))
                tosearch.append(rg)
                
            elif rg[0]<=len(label)<=rg[1]:
                
                tosearch.append(rg)
    if len(label)!=0 and isliteral==True:
        s=label[0].upper()
        
        if s>='A' and s<='Z':
            S=s
        else:
            S=other_dir(label)
        f=open('index KG/list_data_char_index/'+S+'_ll/index_dict.data','rb')
        index_dict=pickle.load(f)
        f.close()
        
        tosearch=[]
        for rg in index_dict:
            #print(len(label)-rg[1])
                
            if 0<=(len(label)-rg[1])<=3 or 0<=(rg[0]-len(label))<=3:
                #print(rg)
                tosearch.append(rg)
                
            elif rg[0]<=len(label)<=rg[1]:
                
                tosearch.append(rg)
                
            
                
    return tosearch


