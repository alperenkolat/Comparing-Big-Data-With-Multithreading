import pandas as pd
import nltk
import json
import multiprocessing,threading
from datetime import datetime
import time

f = open("time.txt", "w")
f.close()

f = open("demofile2.csv", "w")
f.close()

total_df = pd.DataFrame(None)
total_df = total_df.fillna(0) 
visiable_col_=[None,None,None,None,None,None]
df=pd.read_csv(r"out.csv")

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


def dataframe_roam_Forsimple(dataframe,compare_col,similarity_ratio_condition,visiable_col,start_finish):   

    df=dataframe

    f = open("time.txt", "a")
    f.write(str(time.time())+" " + str(start_finish[0])+ "\n")
    f.close()


    first_list=[]
    second_list=[]
    score_list=[]
    dict_visiable_list=[[],[],[],[],[],[]]
    df_len=df.shape
    for i in range(start_finish[0],start_finish[1]):#df_len[0]):
        # print(i)
        for j in range(1,1000):#,df_len[0]):
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
    f = open("demofile2.csv", "a")
    f.write(pd.DataFrame(dict).to_csv(index_label=False,index=False,header=False))
    f.close()

    f = open("time.txt", "a")
    f.write(str(time.time())+" " + str(start_finish[0])+"\n")
    f.close()
    #total_df = pd.concat([total_df,pd.DataFrame(dict)])    # result =pd.DataFrame(dict)
    # return result 


def dataframe_roam_where(dataframe ,compare_col,similarity_ratio_condition,col_Id,Id,visiable_col,start_finish):   
    df=dataframe
    global total_df
    f = open("time.txt", "a")
    f.write(str(time.time())+" " + str(start_finish[0])+ "\n")
    f.close()

    first_list=[]
    second_list=[]
    score_list=[]
    same_list_Id1=[]
    same_list_Id2=[]
    dict_visiable_list=[[],[],[],[],[],[]]
    df_len=df.shape
    a=df.where(df[required_col[col_Id]] == Id)
    a.dropna(inplace=True)
    print("--")
    if a.empty :
        print("-2-")
        a=df.where(df[required_col[col_Id]] == str(Id))
        print("--")
        a.dropna(inplace=True)
        print(a)
    first=a.iloc[0,compare_col]
    for i in range(start_finish[0],start_finish[1]): #df_len[0]):
        
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

    dict = {'first': first_list, 'second': second_list, 'score':score_list,'Search':same_list_Id1,"Complaint ID_2" :same_list_Id2 }
    for i in range(0, 6):
        if (dict_visiable_list[i]!=[]):
            dict[required_col[i]]=dict_visiable_list[i]
    f = open("demofile2.csv", "a")
    f.write(pd.DataFrame(dict).to_csv(index_label=False,index=False,header=False))
    f.close()

    f = open("time.txt", "a")
    f.write(str(time.time())+" " + str(start_finish[0])+"\n")
    f.close()


def dataframe_roam_sameColumn(dataframe,compare_col,similarity_ratio_condition,same_col,visiable_col,start_finish):   
    df=dataframe
    global total_df

    f = open("time.txt", "a")
    f.write(str(time.time())+" " + str(start_finish[0])+ "\n")
    f.close()

    same_list=[]
    same_list_Id1=[]
    same_list_Id2=[]
    first_list=[]
    second_list=[]
    score_list=[]
    dict_visiable_list=[[],[],[],[],[],[]]
    df_len=df.shape
    for i in range(start_finish[0],start_finish[1]): #df_len[0]):
        for j in range(1,200): #df_len[0]):
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

    f = open("demofile2.csv", "a")
    f.write(pd.DataFrame(dict).to_csv(index_label=False,index=False,header=False))
    f.close()

    f = open("time.txt", "a")
    f.write(str(time.time())+" " + str(start_finish[0])+ "\n")
    f.close()

def man(thread_amount,similarity_ratio,column_to_compare,visiable_col_):

    f = open("demofile2.csv", "a")
    f.write("first,"+"second,"+"score")
    for i in range(0,len(visiable_col_)):
        if visiable_col_[i]!=None:
            f.write(","+required_col[i])

    f.write("\n")
    f.close()

    data_size=df.shape[0]
    data_size=500
    increase_amount=int(data_size/thread_amount)


    #Multiprocessing
    cores = []
    if(thread_amount<10):
        for i in range(1):#multiprocessing.cpu_count()):
            cores.append([])
    else:
        for i in range((int) (thread_amount/10)):#multiprocessing.cpu_count()):
            cores.append([])
    
    first=0
    second=increase_amount
    start_finish=[1,second]
    for i in range(thread_amount): 
        print(start_finish)
        t = threading.Thread(target=dataframe_roam_Forsimple,args= (df,column_to_compare,similarity_ratio,visiable_col_,start_finish,))
        if(i==thread_amount-2):
            first=first+increase_amount
            start_finish=[first,data_size]
        else:
            first=first+increase_amount
            second=second+increase_amount
            start_finish=[first,second]
        if(thread_amount<10):
            cores[0].append(t)
        else:
            cores[i%(int) (thread_amount/10)].append(t)

    process_list = []
    for t in cores:
        if(len(t) != 0):
            process = multiprocessing.Process(target=thread_starter, args=(t,))
            process_list.append(process)
            process.start()

    for p in process_list:
        p.join()

def thread_starter(thread_array):
    for t in thread_array:
        t.start()
    for t in thread_array:
        #t.join()
        pass





def man2(thread_amount,similarity_ratio,column_to_compare,visiable_col_,col_Id,Id):
    data_size=df.shape[0]
    data_size=500
    increase_amount=int(data_size/thread_amount)
    f = open("demofile2.csv", "a")
    f.write("first,"+"second,"+"score,"+"Search,"+"Complaint ID_2")
    for i in range(0,len(visiable_col_)):
        if visiable_col_[i]!=None:
            f.write(","+required_col[i])

    f.write("\n")
    f.close()

    #Multiprocessing
    cores = []
    if(thread_amount<10):
        for i in range(1):#multiprocessing.cpu_count()):
            cores.append([])
    else:
        for i in range((int) (thread_amount/10)):#multiprocessing.cpu_count()):
            cores.append([])
    
    first=0
    second=increase_amount
    start_finish=[1,second]
    for i in range(thread_amount): 
        print(start_finish)
        t = threading.Thread(target=dataframe_roam_where,args= (df,column_to_compare,similarity_ratio,col_Id,Id,visiable_col_,start_finish,))
        if(i==thread_amount-2):
            first=first+increase_amount
            start_finish=[first,data_size]
        else:
            first=first+increase_amount
            second=second+increase_amount
            start_finish=[first,second]
        if(thread_amount<10):
            cores[0].append(t)
        else:
            cores[i%(int) (thread_amount/10)].append(t)

    process_list = []
    for t in cores:
        if(len(t) != 0):
            process = multiprocessing.Process(target=thread_starter, args=(t,))
            process_list.append(process)
            process.start()

    for p in process_list:
        p.join()



def man3(thread_amount,similarity_ratio,column_to_compare,visiable_col_,same_column):
    data_size=df.shape[0]
    data_size=1000
    increase_amount=int(data_size/thread_amount)
    f = open("demofile2.csv", "a")
    f.write("same,"+"first,"+"second,"+"score,"+"Complaint ID_1,"+"Complaint ID_2")
    for i in range(0,len(visiable_col_)):
        if visiable_col_[i]!=None:
            f.write(","+required_col[i])

    f.write("\n")
    f.close()

    #Multiprocessing
    cores = []
    if(thread_amount<10):
        for i in range(1):#multiprocessing.cpu_count()):
            cores.append([])
    else:
        for i in range((int) (thread_amount/10)):#multiprocessing.cpu_count()):
            cores.append([])
    
    first=0
    second=increase_amount
    start_finish=[1,second]
    for i in range(thread_amount): 
        print(start_finish)
        t = threading.Thread(target=dataframe_roam_sameColumn,args= (df,column_to_compare,similarity_ratio,same_column,visiable_col_,start_finish,))
        if(i==thread_amount-2):
            first=first+increase_amount
            start_finish=[first,data_size]
        else:
            first=first+increase_amount
            second=second+increase_amount
            start_finish=[first,second]
        if(thread_amount<10):
            cores[0].append(t)
        else:
            cores[i%(int) (thread_amount/10)].append(t)

    process_list = []
    for t in cores:
        if(len(t) != 0):
            process = multiprocessing.Process(target=thread_starter, args=(t,))
            process_list.append(process)
            process.start()

    for p in process_list:
        p.join()




def man00(thread_amount):
    increase_amount=int (2000/thread_amount)

    #Multiprocessing
    core = []
    first=1
    second=increase_amount
    start_finish=[first,second]
    for i in range(thread_amount): 

        t = multiprocessing.Process(target=dataframe_roam_where,args= (df,0,80,5,3198084,visiable_col_))
        if(i==thread_amount-1):
            first=first+increase_amount
            start_finish=[first,df.shape[0]-1]
        else:
            first=first+increase_amount
            second=second+increase_amount
            start_finish=[first,second]
        core.append(t)
        t.start()


    for p in core:
        p.join()


def timer():
    times = list()
    f = open("time.txt","r")
    data = f.readlines()

    for i in range(int(len(data)/2)):
        for j in range(int(len(data)/2),len(data)):
            if(data[i].split(" ")[1] == data[j].split(" ")[1]):
                time1 = float(data[i].split(" ")[0])
                time2 = float(data[j].split(" ")[0])
                start_ts = datetime.fromtimestamp(time1)
                end_ts = datetime.fromtimestamp(time2)
                delta = end_ts - start_ts
                times.append(delta)
                break
    dict={"Time":times}
    return pd.DataFrame(dict)
