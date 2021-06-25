from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics as metrics
from sklearn.tree import export_text


def predict(df, used_features, category):
    """
    predict(df, used_features, category)
    trains and tests the random forest algorithm/model based on the given features and requested categories

    arguments:
    df: a pandas dataframe containing our data
    used_features: a list of features to use in the predictions
    category: the category to predict

    :returns nothing. prints results to console
    """

    # split data into test and train
    XTrain, XTest, YTrain, YTest = train_test_split(df[used_features].values, df[category].values, random_state=1,
                                                    test_size=0.5)

    print("\nRandom forest for category: " + category)

    # creating the classifier
    forest = RandomForestClassifier(bootstrap=True, n_estimators=300, random_state=0)

    # train the model
    trained_forest = forest.fit(XTrain, YTrain)

    # predict on training data
    y_pred_train = trained_forest.predict(XTrain)
    print('Accuracy on training data= ', metrics.accuracy_score(y_true=YTrain, y_pred=y_pred_train))

    # predict on test data
    y_pred = trained_forest.predict(XTest)
    print('Accuracy on test data= ', metrics.accuracy_score(y_true=YTest, y_pred=y_pred))

    # print the tree
    estimator = forest.estimators_[5]
    print(export_text(estimator,
                    feature_names=used_features))


def predictList(df, used_features,category_list):
    """
    predictList(df, used_features, category)
    calls the predict function for each category in the given list

    arguments:
    df: a pandas dataframe containing our data
    used_features: a list of features to use in the predictions
    category: a list of categories to predict

    :returns nothing. prints results to console
    """
    # iterate over categories
    for category in category_list:
        # call helper function
        predict(df, used_features, category)

