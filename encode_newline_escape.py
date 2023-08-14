import os
import csv
import pandas as pd

file_path = 'patient_therapist.csv'
clean_file_path = "clean_"+file_path
df = pd.read_csv(file_path)  
df.loc[:, "prompt"] = df["prompt"].apply(lambda x : x.replace('\n', '\\n'))
df.loc[:, "completion"] = df["completion"].apply(lambda x : x.replace('\n', '\\n'))
df.to_csv(clean_file_path, index=False)
