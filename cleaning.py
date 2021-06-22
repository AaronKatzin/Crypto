import pandas as pd

def cleanDF(df):

    #clean nulls
    print("Dataframe shape before cleaning: " + str(df.shape))
    null_columns=df.columns[df.isnull().any()]
    print("null columns before cleaning: ", df[null_columns].isnull().sum())
    df.dropna(axis=0, how='any',inplace=True)
    null_columns=df.columns[df.isnull().any()]
    print("Cleaned Dataframe shape: " + str(df.shape))
    print("After cleaning null columns: ", df[null_columns].isnull().sum())

    return df