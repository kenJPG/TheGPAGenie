import pandas as pd

import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor, make_column_transformer, ColumnTransformer, make_column_selector
from sklearn.base import clone
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error as mae, mean_absolute_percentage_error as mape, r2_score as r2, make_scorer

from scipy.stats import percentileofscore
import pandas as pd

from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

import numpy as np
from utils import TwoTransformers

random_state = 21

def rmspe(y_true, y_pred):
    error = np.sqrt(np.mean(np.square(((y_true - y_pred) / y_true))))
    return error

rmspe_scorer = make_scorer(
    rmspe,
    greater_is_better=False
)

math_df = pd.read_csv('data/student-mat.csv')
lang_df = pd.read_csv('data/student-por.csv')

lang_df['is_math'] = 0
math_df['is_math'] = 1

data_df = pd.concat([lang_df, math_df])

def calc_grade(df_pass):
	df = df_pass.copy()
	# df = df.apply(lambda x: x.max(axis=0), axis=1)
	count = df.apply(lambda x: int(x['G1'] > 0) + int(x['G2'] > 0) + int(x['G3'] > 0), axis=1)
	df = df.sum(axis=1) / count
	return df

X = data_df.drop(['G1', 'G2', 'G3'], axis=1)
y = calc_grade(data_df[['G1', 'G2', 'G3']])


def to_percentile(series):
	return series.apply(lambda x: percentileofscore(sorted(series), x))

# NUS Bell Curve formula taken from https://blog.nus.edu.sg/provost/2012/01/20/the-bell-curve/
percentile_reg = RandomForestRegressor(n_estimators = 1000)
percentile = np.array([0.0016, 0.0016, 0.0016, 0.0381, 0.1397, 0.1794, 0.2048, 0.1921, 0.1429, 0.0698, 0.0286])
percentile = np.cumsum(percentile)
gpa = np.array([0, 1.0, 1.3, 2.0, 2.4, 2.7, 3.0, 3.3, 3.7, 4, 4])
percentile_reg.fit(percentile.reshape((-1, 1)), gpa)

def percentile_to_gpa(percentile):
	if len(percentile.shape) == 1:
		percentile = percentile.values.reshape((-1, 1))
	return percentile_reg.predict(percentile / 100)
yt = percentile_to_gpa(to_percentile(y))

data_df['Total_alc'] = (data_df['Dalc'] * data_df['Walc']) ** 0.5


final_columns = ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']
small_columns = ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime']

model = TransformedTargetRegressor(
	HistGradientBoostingRegressor(
		min_samples_leaf = 20,
		max_leaf_nodes = 15,
		max_iter = 150,
		max_depth = 9,
		max_bins = 200,
		l2_regularization = 1,
		early_stopping = False,
		random_state = 21
	),
	transformer=TwoTransformers()
)

small_model = TransformedTargetRegressor(
	HistGradientBoostingRegressor(
		min_samples_leaf = 20,
		max_leaf_nodes = 15,
		max_iter = 150,
		max_depth = 9,
		max_bins = 200,
		l2_regularization = 1,
		early_stopping = False,
		random_state = 21
	),
	transformer=TwoTransformers()
)

CategoricalOHE = make_column_transformer(
	(OneHotEncoder(sparse = False), make_column_selector(dtype_include='object')),
	remainder='passthrough'
)

preprocess = Pipeline(steps=[
	('preprocessing', CategoricalOHE),
	('scaler', StandardScaler()),
])

final = Pipeline([
	('preprocess', preprocess),
	('model', model)
])

small_final = clone(final)

final.fit(data_df[final_columns], percentile_to_gpa(to_percentile(calc_grade(data_df[['G1', 'G2', 'G3']]))))
small_final.fit(data_df[final_columns], percentile_to_gpa(to_percentile(calc_grade(data_df[['G1', 'G2', 'G3']]))))

with open('weights/full_model_xgb.pkl', 'wb') as pickle_file:
	joblib.dump(final, pickle_file)

with open('weights/small_model_xgb.pkl', 'wb') as pickle_file:
	joblib.dump(small_final, pickle_file)

with open('weights/full_cols.pkl', 'wb') as pickle_file:
	joblib.dump(final_columns, pickle_file)

with open('weights/small_cols.pkl', 'wb') as pickle_file:
	joblib.dump(small_columns, pickle_file)