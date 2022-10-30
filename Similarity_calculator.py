import pandas as pd
import nltk
# nltk.download('punkt')

df=pd.read_csv(r"C:\Users\alper\OneDrive\Belgeler\PYTHON PROJECTS\yazlab2\out.csv")


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


def dataframe_roam(dataframe  ,first_col,second_col,similarity_ratio_condition):   
    df=dataframe
    first_list=[]
    second_list=[]
    score_list=[]
    df_len=df.shape
    for i in range(1,100): #df_len[0]):
        for j in range(1,100): #df_len[0]):
            first=df.iloc[i,first_col]
            second=df.iloc[j,second_col]
            score=similarity_calculator(first,second)

            if(score>similarity_ratio_condition):
                first_list.append(first)
                second_list.append(second)
                score_list.append(score)

    dict = {'first': first_list, 'second': second_list, 'score':score_list }
    result =pd.DataFrame(dict)
    return result 


out=dataframe_roam(df,0,1,0)
out.to_csv('result.csv',index=False)



    