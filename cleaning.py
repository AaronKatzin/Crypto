def cleanDF(df):
    """
    cleanDF(df)
    cleans the dataframe of NULLS by filling S&P values and deleting other rows with NULLs

    arguments:
    df: a pandas dataframe to be cleaned

    :returns a cleaned dataframe
    """
    # fill S&P weekend null values
    df["SPAvg"] = df["SPAvg"].fillna(method='ffill', inplace=False)

    # clean nulls
    # print datafram before cleaning
    print("Dataframe shape before cleaning: " + str(df.shape))
    null_columns = df.columns[df.isnull().any()]
    print("null columns before cleaning: ", df[null_columns].isnull().sum())

    # drop NULLs
    df.dropna(axis=0, how='any', inplace=True)

    # print datafram after dropping NULLs
    null_columns = df.columns[df.isnull().any()]
    print("Cleaned Dataframe shape: " + str(df.shape))
    print("After cleaning null columns: ", df[null_columns].isnull().sum())

    return df
