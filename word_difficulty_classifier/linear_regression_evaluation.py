import sys
import os
sys.path.append(os.getcwd())

import warnings
import argparse

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from data_preparation.word_difficulty_dataset_generator import WordDifficultyData
from common.model_accuracy import linear_regression_accuracy
from common.wdd_manager import WDDManager

warnings.filterwarnings('ignore')

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



wdd_manager = WDDManager()
all_wdds = wdd_manager.get_wdds()

# Linear Regression : All WDDs
def linear_regression_all_wdds(normalize=False, return_results=False):
    print("linear regression with normalized {}".format(str(normalize)))
    print("\t{:29s} {} : {}".format("WDD Type", "balanced", "default"))

    results = {}
    for wdd in all_wdds:

        balanced, default = linear_regression_accuracy(LinearRegression(normalize=normalize), wdd)
        if return_results:
            results[wdd.info] = (balanced, default)
        print("\t{:31s}: {:.2f} : {:.2f}".format(wdd.info, balanced, default))
    return results

def polynomial_regression_all_wdds(interaction_only=False, return_results=False):
    print("Polynomial features with linear regression: interaction_only={}".format(str(interaction_only)))

    results = {}
    for degree in range (2, 4):
        print("\t degree:", degree)

        wdd_results = {}
        for wdd in all_wdds:
            clf = make_pipeline(
                PolynomialFeatures(
                    degree=degree, 
                    interaction_only=interaction_only
                ), 
                LinearRegression()
            )
            balanced, default = linear_regression_accuracy(clf, wdd)
            if return_results:
                wdd_results[wdd.info] = (balanced, default)
            print("\t\t{:28s}: {:.2f} : {:.2f}".format(wdd.info, balanced, default))
        if return_results:
            results[degree] = wdd_results

linear_regression_all_wdds()
# linear_regression_all_wdds(normalize=True)
polynomial_regression_all_wdds(interaction_only=True)
