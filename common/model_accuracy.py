import statistics

import numpy as np
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

stratified_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
# balanced_scorer = make_scorer(balanced_accuracy_score)

def balanced_scorer(estimator, X, y):
	y_hat = list(estimator.predict(X))

	return balanced_accuracy_score(np.array(y), np.array(y_hat, dtype=np.int))


def model_accuracy(clf, wdd):
	X = wdd.features()
	y = wdd.output()
	
	cv_score = cross_val_score(clf, X, y, cv=stratified_cv, scoring=balanced_scorer)
	avg_cv_score = float(statistics.mean(cv_score))
	
	return 100 * avg_cv_score

def regression_scorer(estimator, X, y):
	predictions = estimator.predict(X)
	y_hat = []

	for prediction in predictions:
		if prediction > 5:
			y_hat.append(5)
		elif prediction < 0:
			y_hat.append(0)
		else:
			y_hat.append(int(prediction))
	return 100 * balanced_accuracy_score(y, np.array(y_hat))


def linear_regression_accuracy(clf, wdd, default_scorer=False):
	"""default_scorer: Boolean, returns tuple (balanced accuracy average, default scorer)"""

	X = wdd.features()
	y = wdd.output()
	
	cv_score_balanced = cross_val_score(clf, X, y, cv=stratified_cv, scoring=regression_scorer)
	cv_score_default = cross_val_score(clf, X, y, cv=stratified_cv)

	avg_cv_score_balanced = float(statistics.mean(cv_score_balanced))
	avg_cv_score_default = float(statistics.mean(cv_score_default))
	
	return (avg_cv_score_balanced, avg_cv_score_default)