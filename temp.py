import pandas as pd

df = pd.read_csv("./data/data.csv")
# change the birthdate column to the mm/dd/yyyy format
df['Birthdate'] = pd.to_datetime(df['Birthdate']).dt.strftime('%m/%d/%Y')

# save the updated dataframe to a new csv file
df.to_csv("./data/data_updated.csv", index=False)
