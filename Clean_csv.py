import pandas as pd
import nltk
from nltk.corpus import stopwords


# Tek seferliğine stop worsds'leri indirdik
# nltk.download('stopwords')

# Csv okuyup dataframe şeklinde aldık
dfeval = pd.read_csv(r"C:\Users\alper\OneDrive\Belgeler\PYTHON PROJECTS\yazlab2\rows.csv",dtype={'Consumer complaint narrative': 'str', 'Consumer consent provided?': 'str','Consumer disputed?':'str'})

# Projede kullanacağımız gerekli Sütunları tanımladık
required_col=["Product","Issue","Company","State","ZIP code","Complaint ID"]


# Dataframe sütunlarını aldık
col_name=dfeval.columns

# Gerekli sütunları içinden çıkardık
for i  in required_col:

    col_name=col_name.drop(i)

# Kalan gereksiz sütunları sildik
for i in col_name:

    dfeval.pop(i)


# Boş olan satıları sildik
dfeval.dropna(inplace = True)


# Kullanacağımız stopword kütüphanesini seçtik
stop_word_list=stopwords.words('english')

# Stop wordleri ve noktalama işaretlerini sildik
for i in required_col[:3]:

    dfeval[str(i)]=dfeval[str(i)].str.replace("[^\w\s]","")
    dfeval[str(i)] = dfeval[str(i)].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_word_list)]))


# Out isimli yeni bir csv olarak kaydettik
dfeval.to_csv('out.csv',index=False)





