

class Web_Table:
    
    def __init__(self,content,row_num,column_num,header,entity,column_class,number_start,core_column,flag):
        
        self.content=content
        self.row_num=row_num
        self.column_num=column_num
        self.header=header
        self.entity=entity
        self.column_class=column_class
        self.number_start=number_start
        self.core_column=core_column
        self.flag=flag
        
    def change_header(self,header_ch,num):
        
        self.header[num]=header_ch
        
    def change_entity(self,entity_ch,num):
        
        self.entity[num]=entity_ch
        
    def change_column_class(self,column_class_ch,num):
        
        self.column_class[num]=column_class_ch
        
    def set_core_column(self,core_num):
        
        self.core_column=core_num
        
    def change_content(self,entity,if_linked,row,column):
        
        self.content[row][column]=entity

        if if_linked==1:
            
            self.flag[row][column]=1
    def add_row(self,row_list):
        
        self.content.append(row_list)
        self.flag.append([0]*self.column_num)
        
    
 
        