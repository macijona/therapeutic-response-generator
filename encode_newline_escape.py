import pandas as pd

class filePreparer:
    @staticmethod
    def clean_file(filepath, newfilepath):
        df = pd.read_csv(filepath)
        df.loc[:, "prompt"] = df["prompt"].apply(lambda x : x.replace('\n', '\\n'))
        df.loc[:, "completion"] = df["completion"].apply(lambda x : x.replace('\n', '\\n'))
        df.to_csv(newfilepath, index=False)

