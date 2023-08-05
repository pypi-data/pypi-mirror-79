from client import client

client = client()
df = client.getuserportfolio(11)
client.export_df(df,'json',r"D:\filename")