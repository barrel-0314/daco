class Candidate:
    
    def __init__(self,name='',mention='',name_dis=-1,c_type=[],pos=[],literal=True,rin=[],rout=[]):
        
        self.name=name
        self.mention=mention
        self.name_dis=name_dis
        self.c_type=c_type
        self.pos=pos #list
        #self.value_dict=value_dict
        self.literal=literal
        self.rin=rin
        self.rout=rout
        #print(self.column_value)
    
    """        

    def initial_value_dict(self):
        for i in range(len(self.column)):
            self.value_dict[self.column[i]]=[]
    def add_value(self,V):
        
        v=Value(V.value,V.column_num,V.attribute,V.v_type,V.rel)
        self.value_dict[V.column_num].append(v)
        
    def obtain_name_distance(self):
        
        self.name_dis=Levenshtein.distance(self.name,self.mention)
    
    def obtain_type(self,type_list):
        
        self.c_type=type_list
        
    
    def obtain_value_dict(self,value_dict):
        
        self.value_dict=value_dict
    """    

