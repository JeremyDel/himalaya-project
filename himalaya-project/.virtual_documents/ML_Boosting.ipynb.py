import pandas as pd
import numpy as np



from data import Data
df = Data().get_match_table()


df.head()


df.info()


corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')


col_num = []
col_bool =[]
col_object =[]

for col in df:
    if df[col].dtype == "float64":
        col_num.append(col)
        
    if df[col].dtype == "int64":
        col_num.append(col)
        
    if df[col].dtype == 'bool':
        col_bool.append(col)
        
    if df[col].dtype == 'object':
        col_object.append(col)
        
col_bool.remove('summit_success')


for col in df:        
    if df[col].dtype == 'bool':
        df[col].fillna(method='bfill')


from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer, KNNImputer
from scipy.stats import uniform
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=2)),
    ('scaler', MinMaxScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

# boolean_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, col_num),
        ('cat', categorical_transformer, col_object)])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor)])

X = df.drop('summit_success', axis=1)
y = df.summit_success

X_trans = clf.fit_transform(X)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=0.3, random_state=42)


from xgboost import XGBClassifier

boost = XGBClassifier()
boost.fit(X_train, y_train)


from sklearn.metrics import classification_report

y_pred = boost.predict(X_test)
print(classification_report(y_test, y_pred))


param = {}
param['booster'] = 'gbtree'
param['objective'] = 'binary:logistic'
param["eval_metric"] = "error"
param['eta'] = 0.003
param['learning_rate'] = 0.1
param['max_depth'] = 12
param['min_child_weight']=1
param['max_delta_step'] = 0
param['subsample']= 1
param['reg_alpha']= 0.0001
param['seed'] = 0
param['base_score'] = 0.6


xgboost = XGBClassifier(**param)
xgboost.fit(X_train, y_train)


from sklearn.metrics import classification_report

y_pred = xgboost.predict(X_test)
print(classification_report(y_test, y_pred))


import xgboost as xgb

xgb.plot_importance(xgboost)


from xgboost import plot_tree


# plot_tree(boost)


from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier()
tree.fit(X_train, y_train)


y_pred = tree.predict(X_test)
print(classification_report(y_test, y_pred))





import matplotlib.pyplot as plt
plt.figure(figsize = (40, 40))
plot_tree(tree)
plt.show()


from sklearn.svm import SVC
svc_model = SVC()
svc_model.fit(X_train, y_train)
y_pred = svc_model.predict(X_test)
print('Support Vector Classifier report')
print(classification_report(y_test, y_pred))


from sklearn.linear_model import LogisticRegression

log_model = LogisticRegression(max_iter = 500, class_weight = 'balanced', )
log_model.fit(X_train, y_train)
y_pred = log_model.predict(X_test)
print('Logistic Regression report')
print(classification_report(y_test, y_pred))


from sklearn.ensemble import AdaBoostClassifier
tree = DecisionTreeClassifier()
boosted = AdaBoostClassifier(tree)
boosted.fit(X_train, y_train)


y_pred = boosted.predict(X_test)
print(classification_report(y_test, y_pred))


from sklearn.feature_selection import SelectFromModel
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
 

def select_features(X_train, y_train, X_test):
    # configure to select a subset of features
    fs = SelectFromModel(XGBClassifier(), max_features=18)
    # learn relationship from training data
    fs.fit(X_train, y_train)
    # transform train input data
    X_train_fs = fs.transform(X_train)
    # transform test input data
    X_test_fs = fs.transform(X_test)
    return X_train_fs, X_test_fs, fs


#applying function to X
X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test)


xgboost_fs = XGBClassifier()


xgboost_fs.fit(X_train_fs, y_train)


y_pred = xgboost_fs.predict(X_test_fs)
print(classification_report(y_test, y_pred))


importance = xgboost_fs.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
    print('Feature: get_ipython().run_line_magic("0d,", " Score: %.5f' % (i,v))")
# plot feature importance
plt.bar([x for x in range(len(importance))], importance)
plt.show()





feature_selection =fs.get_support()


feature_selection


# from sklearn.feature_selection import RFE
# from sklearn.pipeline import FeatureUnion, Pipeline


# numeric_transformer = Pipeline(steps=[
#     ('imputer', KNNImputer(n_neighbors=2)),
#     ('scaler', MinMaxScaler())])

# categorical_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent')),
#     ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

# # boolean_transformer = Pipeline(steps=[
# #     ('imputer', SimpleImputer(strategy='most_frequent'))])

# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', numeric_transformer, col_num),
#         ('cat', categorical_transformer, col_object)])

# # Append classifier to preprocessing pipeline.
# # Now we have a full prediction pipeline.

# feautre_selector = RFE(estimator=XGBClassifier(), n_features_to_select=20, step=1)

# clf = Pipeline(steps=[('features', FeatureUnion([('preprocessor', preprocessor)])), ('feature_selection', feautre_selector)])


# from sklearn.model_selection import train_test_split

# X_train_rfe, X_test_rfe, y_train_rfe, y_test_rfe = train_test_split(X, y, test_size=0.3, random_state=42)


# X = df.drop('summit_success', axis=1)
# y = df.summit_success

# clf.fit(X_train_rfe, y_train_rfe)






# features_rfe = clf.named_steps['feature_selection'].support_









numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=2)),
    ('scaler', MinMaxScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

# boolean_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, col_num),
        ('cat', categorical_transformer, col_object)])


preprocessor.fit_transform(X)


from sklearn.feature_extraction.text import _VectorizerMixin
from sklearn.feature_selection._base import SelectorMixin


def get_feature_out(estimator, feature_in):
    if hasattr(estimator,'get_feature_names'):
        if isinstance(estimator, _VectorizerMixin):
            # handling all vectorizers
            return [f'vec_{f}' \
                for f in estimator.get_feature_names()]
        else:
            return estimator.get_feature_names(feature_in)
    elif isinstance(estimator, SelectorMixin):
        return np.array(feature_in)[estimator.get_support()]
    else:
        return feature_in


def get_ct_feature_names(ct):
    # handles all estimators, pipelines inside ColumnTransfomer
    # doesn't work when remainder =='passthrough'
    # which requires the input column names.
    output_features = []

    for name, estimator, features in ct.transformers_:
        if nameget_ipython().getoutput("='remainder':")
            if isinstance(estimator, Pipeline):
                current_features = features
                for step in estimator:
                    current_features = get_feature_out(step, current_features)
                features_out = current_features
            else:
                features_out = get_feature_out(estimator, features)
            output_features.extend(features_out)
        elif estimator=='passthrough':
            output_features.extend(ct._feature_names_in[features])
                
    return output_features


feature_names =  get_ct_feature_names(preprocessor)


def get_names(feature_selection, feature_names):
    list_features = []
    for i, name in enumerate(feature_names):
        if feature_selection[i]:
            list_features.append(name)
    return list_features


names =get_names(feature_selection, feature_names)


names


import seaborn as sns

importance = xgboost_fs.feature_importances_
# summarize feature importance

# plot feature importance
plt.figure(figsize=(10,12))
plt.barh(y=names, width=importance)
plt.show()


for i, col in enumerate(col_num):
    if col == 'route1' or col == 'ascent1':
        col_num.pop(i)





numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=2)),
    ('scaler', MinMaxScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

# boolean_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, col_num),
        ('cat', categorical_transformer, col_object)])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor)])


X_without = X.drop(['route1','ascent1'], axis=1)





X_trans_ok = clf.fit_transform(X_without)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_trans_ok, y, test_size=0.3, random_state=42)


from xgboost import XGBClassifier

boost_ok = XGBClassifier()
boost_ok.fit(X_train, y_train)


from sklearn.metrics import classification_report

y_pred = boost_ok.predict(X_test)
print(classification_report(y_test, y_pred))


X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test)


fs.get_support().shape


feature_names =  get_ct_feature_names(preprocessor)


names =get_names(feature_selection, feature_names)











import seaborn as sns

importance = xgboost_fs.feature_importances_
# summarize feature importance

# plot feature importance
plt.figure(figsize=(10,12))
plt.barh(y=names, width=importance)
plt.show()


names


columns_to_keep = ['peak_id', 
'status', 
'season', 
'peak_heigth',
'age', 
'mintempC',
 'moon_illumination',
 'HeatIndexC',
 'WindChillC',
 'summit_days',
 'camps',
 'tot_hired']


df[['status']].value_counts()


X_without.columns


from hyperopt import Trials, STATUS_OK, tpe, hp, fmin

def objective(space):

    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    classifier = xgb.XGBClassifier(n_estimators = space['n_estimators'],
                            max_depth = int(space['max_depth']),
                            learning_rate = space['learning_rate'],
                            gamma = space['gamma'],
                            min_child_weight = space['min_child_weight'],
                            subsample = space['subsample'],
                            colsample_bytree = space['colsample_bytree']
                            )
    
    classifier.fit(X_train, y_train)

    # Applying k-Fold Cross Validation
    from sklearn.model_selection import cross_val_score
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
    CrossValMean = accuracies.mean()

    print("CrossValMean:", CrossValMean)

    return{'loss':1-CrossValMean, 'status': STATUS_OK }

space = {
    'max_depth' : hp.choice('max_depth', range(5, 30, 1)),
    'learning_rate' : hp.quniform('learning_rate', 0.01, 0.5, 0.01),
    'n_estimators' : hp.choice('n_estimators', range(20, 205, 5)),
    'gamma' : hp.quniform('gamma', 0, 0.50, 0.01),
    'min_child_weight' : hp.quniform('min_child_weight', 1, 10, 1),
    'subsample' : hp.quniform('subsample', 0.1, 1, 0.01),
    'colsample_bytree' : hp.quniform('colsample_bytree', 0.1, 1.0, 0.01)}

trials = Trials()
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=50,
            trials=trials)

print("Best: ", best)


# Fitting XGBoost to the Training set
from xgboost import XGBClassifier
classifier = XGBClassifier(n_estimators = best['n_estimators'],
                            max_depth = best['max_depth'],
                            learning_rate = best['learning_rate'],
                            gamma = best['gamma'],
                            min_child_weight = best['min_child_weight'],
                            subsample = best['subsample'],
                            colsample_bytree = best['colsample_bytree']
                            )

classifier.fit(X_train, y_train)

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
CrossValMean = accuracies.mean()
print("Final CrossValMean: ", CrossValMean)

CrossValSTD = accuracies.std()

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = pd.DataFrame(y_pred) 
y_pred.columns = ['Survived'] 
submission = submission.join(y_pred) 

# Exporting dataset to csv
submission.to_csv("Titanic_Submission.csv", index=False, sep=',')
