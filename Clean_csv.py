from functools import reduce
import pandas as pd
import nltk
from nltk.corpus import stopwords


# Tek seferliğine stop worsds'leri indirdik
# nltk.download('stopwords')

# Csv sadece gerekli sutünları okuyup dataframe şeklinde aldık
dfeval = pd.read_csv(r"rows.csv",usecols=[1,3,7,8,9,17], encoding="utf-8")


# Boş olan satıları sildik
dfeval.dropna(inplace = True)


# Kullanacağımız stopword kütüphanesini seçtik
stop_word_list=stopwords.words('english')

# Listedeki sutünlardan stop wordleri ve noktalama işaretlerini sildik ayrıca karakterleri küçülttük.
required_col=["Product","Issue","Company"]
for i in required_col:
    dfeval[str(i)]=dfeval[str(i)].str.replace("[^\w\s]","")
    dfeval[str(i)] = dfeval[str(i)].apply(lambda x: ' '.join(x.lower() for x in x.split()))
    dfeval[str(i)] = dfeval[str(i)].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_word_list)]))


# Out isimli yeni bir csv olarak kaydettik
dfeval.to_csv('out.csv',index=False)





