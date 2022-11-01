import pandas as pd
import numpy as np

df = pd.read_csv('dataset.txt', delimiter="\t",encoding='cp1252')
df.head()

#bestselling product
best = df.loc[df['qntysold'].idxmax()]
best

#worstselling product
worst = df.loc[df['qntysold'].idxmin()]
worst

#mean and standard deviation

Mean = df.price.mean()
Std = df.price.std()
price_dtl = pd.Series(data=[Mean,Std],index=['Mean','Standard deviation'])
price_dtl

#normalize with min/max
df['price'] = (df['price'] - 10) / (20 - 10)
df.head()

#normalize with z score

df['price'] = (df['price'] - Mean) / (Std)
df.head()

#normalize with decimal scaling
df['price'] = df['price'] / 1000
df.head()

#median and quartiles
med = df.qntysold.med()
quart = df.qntysold.quantile([0.25,0.5,0.75])