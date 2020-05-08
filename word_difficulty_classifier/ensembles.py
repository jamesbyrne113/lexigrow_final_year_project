import sys
import os
sys.path.append(os.getcwd())

import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from data_preparation.word_difficulty_dataset_generator import WordDifficultyData
from common.model_accuracy import model_accuracy
from common.wdd_manager import WDDManager
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--datasets_path", 
    type=str,
    default="data/wdds",
    help="path to folder containing data sets"
)
 
args = parser.parse_args()

wdd_manager = WDDManager(args.datasets_path)
all_wdds = wdd_manager.get_wdds()

def print_results(results, info, parameter, display_graph=False):
    print("\n\n", info)
    print("\t{:20s} : {} : {}".format("parameter", "value", "score"))
    for param_value, result in results.items():
        val_str = "{:2f}".format(param_value) if param_value == float else param_value
        print("\t{:20s} : {} : {:.2f}".format(parameter, val_str, result))

    if display_graph:
        plt.plot(list(results.keys()), list(results.values()))

def get_best_wdd(wdds, results):
    best_wdd = None
    best_wdd_score = -1

    for wdd in wdds:
        score = results[wdd.info]
        if score > best_wdd_score:
            best_wdd_score = score
            best_wdd = wdd

    return best_wdd

def get_wdd(wdds, info):
    for wdd in wdds:
        if wdd.info == info:
            return wdd

    return None

def get_best_param(results):
    return max(results.items(), key=lambda x: x[1])[0]


def score_all_wdds(base_clf, wdds):
    scores = {}
    for wdd in wdds:
        clf = BaggingClassifier(base_clf)
        scores[wdd.info] = model_accuracy(clf, wdd)
    return scores


#########################################
#  KNN Ensembles
#########################################

def ensembles_num_features(base_clf, values, wdd):
    scores = {}

    for num_features in values:
        clf = BaggingClassifier(base_clf, max_features=num_features)

        scores[num_features] = model_accuracy(clf, wdd)
    return scores


def num_estimators_num_features(base_clf, values, wdd, best_num_features):
    scores = {}

    for num_estimators in values:
        clf = BaggingClassifier(base_clf, max_features=best_num_features, n_estimators=num_estimators)

        scores[num_estimators] = model_accuracy(clf, wdd)
    return scores


# This is the best performing combination of number of estimators and data set
num_neighbours = 5
best_wdd = get_wdd(all_wdds, "word_count, no change")

clf = KNeighborsClassifier(weights="distance", n_neighbors=num_neighbours)

################## num_features

values=list(range(5, 60, 5)) + [59]
results = ensembles_num_features(clf, values=values, wdd=best_wdd)
print_results(results, "KNN - value range [5, 60, 5] + [59] - {}".format(best_wdd.info), "num_features", display_graph=True)

best_num_features = get_best_param(results)
print("\nBest Num Features: {}".format(best_num_features))

values = range(max(1, best_num_features-5), min(59, best_num_features+5))
results = ensembles_num_features(clf, values=values, wdd=best_wdd)
print_results(results, "KNN - values [{}, {}] - {}".format(values[0], values[-1], best_wdd.info), "num_features", display_graph=True)

best_num_features = get_best_param(results)
print("\nBest Num Features: {}".format(best_num_features))


################## num_estimators

values=list(range(100, 1001, 100))
results = num_estimators_num_features(clf, values=values, wdd=best_wdd, best_num_features=best_num_features)
print_results(results, "KNN - value range [100, 1001] - {}".format(100, 1001, best_wdd.info), "num_estimators", display_graph=True)

best_num_estimators = get_best_param(results)
print("\nBest Num Estimators: {}".format(best_num_estimators))

values = range(best_num_estimators - 50, best_num_estimators + 50, 10)
results = num_estimators_num_features(clf, values=values, wdd=best_wdd, best_num_features=best_num_features)
print_results(results, "KNN - value range [{}, {}, 10] - {}".format(values[0], values[-1], best_wdd.info), "num_estimators", display_graph=True)

best_num_estimators = get_best_param(results)
print("\nBest Num Estimators: {}".format(best_num_estimators))



#########################################
#  DT Ensembles
#########################################

def ensembles_max_samples(base_clf, values, wdd):
    scores = {}

    for max_samples in values:
        clf = BaggingClassifier(base_clf, max_samples=max_samples)

        scores[max_samples] = model_accuracy(clf, wdd)
    return scores


def num_estimators_max_samples(base_clf, values, wdd, best_max_samples):
    scores = {}

    for num_estimators in values:
        clf = BaggingClassifier(base_clf, max_samples=best_max_samples, n_estimators=num_estimators)

        scores[num_estimators] = model_accuracy(clf, wdd)
    return scores


clf = DecisionTreeClassifier(criterion="gini")

results = score_all_wdds(clf, wdds=all_wdds)
print_results(results, "DT", "wdds", display_graph=False)

best_wdd = get_best_wdd(all_wdds, results)

################## num_features

values = np.arange(0.1, 1, 0.1)
results = ensembles_max_samples(clf, values=values, wdd=best_wdd)
print_results(results, "DT - value range [{}, {}, {}] - {}".format(values[0], values[-1], 0.1, best_wdd.info), "max_samples", display_graph=True)

best_max_samples = get_best_param(results)
print("\nBest Max Samples: {}".format(best_max_samples))


################## num_estimators

values=list(range(100, 1001, 100))
results = num_estimators_max_samples(clf, values=values, wdd=best_wdd, best_max_samples=best_max_samples)
print_results(results, "DT - range [100, 1001] - {}".format(best_wdd.info), "num_estimators", display_graph=True)

best_num_estimators = get_best_param(results)
print("\nBest Num Estimators: {}".format(best_num_estimators))

values = range(best_num_estimators - 50, best_num_estimators + 50, 10)
results = num_estimators_max_samples(clf, values=values, wdd=best_wdd, best_max_samples=best_max_samples)
print_results(results, "DT - value range [{}, {}, 10] - {}".format(values[0], values[-1], best_wdd.info), "num_estimators", display_graph=True)

best_num_estimators = get_best_param(results)
print("\nBest Num Estimators: {}".format(best_num_estimators))












