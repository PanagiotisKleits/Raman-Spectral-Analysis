import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data1=pd.read_csv("data/raman_spectrum.csv")
columns={data1.columns[0]:'wavelengths',data1.columns[1]:'intensity'}
data1.rename(columns,axis='columns',inplace=True)

data1.info()

data1

for column in data1.columns:
    data1[column] = pd.to_numeric(data1[column],errors='coerce')

plt.figure(figsize=(12,6))
data1.plot('wavelengths', color = 'r')
plt.ylabel('intensity')
plt.show()

data1 = data1.apply(lambda col: (col.fillna(method="ffill") + col.fillna(method="bfill"))/2)
plt.figure(figsize=(12,6))
data1.plot('wavelengths',c='black')
plt.xlabel("Wavelegths",fontsize=12)
plt.ylabel("Intensity",fontsize=12)
plt.show()

