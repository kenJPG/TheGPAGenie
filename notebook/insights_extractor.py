import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


os.chdir(
	(os.path.abspath(os.path.dirname(__file__)))
)
df = pd.read_csv('data/cleaned.csv')
df = df.drop('Unnamed: 0', axis=1)
df['Total_alc'] = list(map(lambda x: int(x), ((df['Total_alc'] ** 0.5).values)))

import numpy as np
import matplotlib as mpl
from utils import InsightExtractor

extractor = InsightExtractor(df)

sampled = df.sample(1)
good_insights, good_fig, improve_insights, improve_fig = extractor.extract(sampled)
good_fig

import joblib
joblib.dump(extractor, 'weights/extractor.pkl')