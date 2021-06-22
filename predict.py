from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics as metrics
from sklearn.tree import export_graphviz


def predict(df, used_features, catagory):
    XTrain, XTest, YTrain, YTest = train_test_split(df[used_features].values, df[catagory].values, random_state=1,
                                                    test_size=0.3)

    print("\nRandom forest for catagory: " + catagory)

    forest = RandomForestClassifier(bootstrap=True, n_estimators=300, random_state=0)

    trained_forest = forest.fit(XTrain, YTrain)

    y_pred_train = trained_forest.predict(XTrain)
    print('Accuracy on training data= ', metrics.accuracy_score(y_true=YTrain, y_pred=y_pred_train))

    y_pred = trained_forest.predict(XTest)
    print('Accuracy on test data= ', metrics.accuracy_score(y_true=YTest, y_pred=y_pred))

    estimator = forest.estimators_[5]
    export_graphviz(estimator, out_file='tree.dot',
                    feature_names=used_features,
                    class_names=catagory,
                    rounded=True, proportion=False,
                    precision=2, filled=True)


def predictList(df, used_features,category_list):
    for category in category_list:
        predict(df, used_features, category)

