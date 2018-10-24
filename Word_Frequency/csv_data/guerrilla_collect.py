import pandas as pd

df = pd.read_excel('/Volumes/usb/20180115ai/2013.08.01-13twitter.xlsx', sheet_name=5, usecols=[2,21], header=None)
df = df.rename(columns={0:"created_at", 1:"text"})
df["created_at"]=df["created_at"].astype(str)

with open('output.csv', 'w') as f:
   #df[~df["created_at"].str.contains("2013-07-23 15") & ~df["created_at"].str.contains("2013-07-23 16") & ~df["created_at"].str.contains("2013-07-23 17") & ~df["created_at"].str.contains("2013-07-23 18")][['created_at','text']].to_csv(f, index=None, header=None)
   #df[df["created_at"].str.contains("2013-08-06 10") | df["created_at"].str.contains("2013-08-06 14") | df["created_at"].str.contains("2013-08-06 15") | df["created_at"].str.contains("2013-08-06 16") | df["created_at"].str.contains("2013-08-06 19")][['created_at','text']].to_csv(f, index=None, header=None)
   df[df["created_at"].str.contains("2013-08-12")][['created_at','text']].to_csv(f, index=None, header=None)
