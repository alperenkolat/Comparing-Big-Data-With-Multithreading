import pandas as pd
import nltk



required_col=["Product","Issue","Company","State","ZIP code","Complaint ID"]

def similarity_calculator (first, second):
    first = nltk.word_tokenize(first)
    second = nltk.word_tokenize(second)
    count = 0
    if(len(first)>len(second)):
        max=len(first)
    else:
        max=len(second)
        
    for f in first:
        if f in second:
            count += 1
    
    return(int((count/max )*100))


def dataframe_roam_Forsimple(dataframe,compare_col,similarity_ratio_condition,visiable_col):   

    df=dataframe
    first_list=[]
    second_list=[]
    score_list=[]
    dict_visiable_list=[[],[],[],[],[],[]]
    df_len=df.shape
    for i in range(1,40):#df_len[0]):
        for j in range(1,140):#,df_len[0]):
            first=df.iloc[i,compare_col]
            second=df.iloc[j,compare_col]
            score=similarity_calculator(first,second)

            if(score>=similarity_ratio_condition):
                first_list.append(first)
                second_list.append(second)
                score_list.append(score)
                for k in range(0,6):
                    if(visiable_col[k]!=None):
                        dict_visiable_list[k].append(df.iloc[j,k])

            

    dict = {'first': first_list, 'second': second_list, 'score':score_list }
    
    for i in range(0, 6):

        if (dict_visiable_list[i]!=[]):
            dict[required_col[i]]=dict_visiable_list[i]
    result =pd.DataFrame(dict)
    return result 


def dataframe_roam_where(dataframe ,compare_col,similarity_ratio_condition,col_Id,Id,visiable_col):   
    df=dataframe
    first_list=[]
    second_list=[]
    score_list=[]
    same_list_Id1=[]
    same_list_Id2=[]
    dict_visiable_list=[[],[],[],[],[],[]]
    df_len=df.shape
    a=df.where(df[required_col[col_Id]] == Id)
    a.dropna(inplace=True)
    first=a.iloc[0,compare_col]
    for i in range(1,30): #df_len[0]):
        
        second=df.iloc[i,compare_col]
        score=similarity_calculator(first,second)
        if(score>=similarity_ratio_condition):
            first_list.append(first)
            second_list.append(second)
            score_list.append(score)
            same_list_Id1.append(Id)
            same_list_Id2.append(df.iloc[i,5])
            
            for k in range(0,6):
                    if(visiable_col[k]!=None):
                        dict_visiable_list[k].append(df.iloc[i,k])

    dict = {'first': first_list, 'second': second_list, 'score':score_list,'Complaint ID_1':same_list_Id1,"Complaint ID_2" :same_list_Id2 }
    for i in range(0, 6):
        if (dict_visiable_list[i]!=[]):
            dict[required_col[i]]=dict_visiable_list[i]
    result =pd.DataFrame(dict)
    return result 


def dataframe_roam_sameColumn(dataframe,compare_col,similarity_ratio_condition,same_col,visiable_col):   
    df=dataframe
    same_list=[]
    same_list_Id1=[]
    same_list_Id2=[]
    first_list=[]
    second_list=[]
    score_list=[]
    dict_visiable_list=[[],[],[],[],[],[]]
    df_len=df.shape
    for i in range(1,100): #df_len[0]):
        for j in range(1,100): #df_len[0]):
            if(i!=j):
                first=df.iloc[i,compare_col]
                second=df.iloc[j,compare_col]
                if(None!=same_col):
                    if(df.iloc[i,same_col]==df.iloc[j,same_col]):

                        score=similarity_calculator(first,second)
                        if(score>=similarity_ratio_condition):
                            first_list.append(first)
                            second_list.append(second)
                            score_list.append(score)
                            same_list.append(df.iloc[j,same_col])
                            same_list_Id1.append(df.iloc[j,5])
                            same_list_Id2.append(df.iloc[i,5])
                           
                            for k in range(0,6):
                                if(visiable_col[k]!=None):
                                    dict_visiable_list[k].append(df.iloc[j,k])

    dict = {'same' :same_list,'first': first_list, 'second': second_list, 'score':score_list, 'Complaint ID_1':same_list_Id1,"Complaint ID_2" :same_list_Id2}
    
    for i in range(0, 6):

        if (dict_visiable_list[i]!=[]):
            dict[required_col[i]]=dict_visiable_list[i]
    result =pd.DataFrame(dict)
    result =result[:int(result.shape[0]/2)]
    return result 




# df=pd.read_csv(r"C:\Users\alper\OneDrive\Belgeler\PYTHON PROJECTS\yazlab2\out.csv")
# visiable_col_=[True,True,True,True,True,True]
# visiable_col_=[None,None,None,None,None,None]
# out=dataframe_roam_Forsimple(df,2,0,visiable_col_)
# out=dataframe_roam_where(df,0,80,5,3198084,visiable_col_)
# out=dataframe_roam_sameColumn(df,3,0,3,visiable_col_)
# out.to_csv('result222.csv',index=False)