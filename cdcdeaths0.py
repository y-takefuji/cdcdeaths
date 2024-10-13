import subprocess as sp
import pandas as pd
import sys,os
if os.path.exists('rows.csv'):
 d=pd.read_csv('rows.csv')
else:
 sp.call("wget https://data.cdc.gov/api/views/9bhg-hcku/rows.csv",shell=True)
 d=pd.read_csv('rows.csv')
age=d['Age Group'].head(18)[1:-1]
age=age.drop(labels=[12],axis=0)
deaths=d['COVID-19 Deaths'].head(18)[1:-1]
deaths=deaths.drop(labels=[12],axis=0)
import matplotlib.pyplot as plt
plt.xticks(rotation=90)
plt.plot(age,deaths)
plt.tight_layout()
plt.savefig('result.png')
plt.show()
