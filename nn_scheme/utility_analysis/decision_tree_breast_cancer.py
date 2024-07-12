from sklearn.model_selection import RandomizedSearchCV
from utils import *
from nn_scheme.NBNN_scheme import CategoricalNeighbourhood
import numpy as np
from time import time
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

gamma = 1
n_exp = 20

start = time()

# brast cancer data
breast_cancer, pk = import_dataset('breast_cancer_full')
print(breast_cancer)
# preprocess
breast_cancer = breast_cancer.drop('Id', axis=1)
# separate target from the data
c = len(breast_cancer.columns)
target = breast_cancer.values[:, (c-1)]
breast_cancer = breast_cancer.drop("recurrence", axis=1)
# one-hot encode
breast_cancer = pd.get_dummies(breast_cancer)
# a bit more preprocessing
breast_cancer = breast_cancer.drop(['breast_left', 'irradiat_yes'], axis=1)
data = breast_cancer.values

# define the model and possible hyperparameters
random_state = 25 # increase every run
criterion_range = ["gini", "entropy"]
max_depth_range = range(1, 30)

# hyperparameter random search
# take the best accuracy from 10-fold cross validation as a benchmark performance
model = DecisionTreeClassifier(random_state=random_state)
param_dist = dict(criterion=criterion_range, max_depth=max_depth_range)
rand_search = RandomizedSearchCV(model, param_dist, cv=10, n_iter=15, scoring="accuracy", random_state=random_state)
rand_search.fit(data, target)
best_params = rand_search.best_params_
print(best_params)
print(rand_search.best_score_)
print(rand_search.best_estimator_)

results = []
for n in range(n_exp):
    # fingerprint the data
    scheme = CategoricalNeighbourhood(gamma=gamma, xi=2, fingerprint_bit_length=8)
    secret_key = 3255  # increase every run
    fp_dataset = scheme.insertion(dataset_name="breast_cancer", buyer_id=1, secret_key=secret_key)
    # same prepocessing as above
    fp_dataset = fp_dataset.drop("Id", axis=1)
    fp_dataset = pd.get_dummies(fp_dataset)
    fp_dataset = fp_dataset.drop(['breast_left', 'irradiat_yes'], axis=1)
    fp_dataset = fp_dataset.values
    # hyperparameter seach

    model2 = DecisionTreeClassifier(random_state=random_state, criterion=best_params['criterion'],
                                    max_depth=best_params['max_depth'])
    scores = cross_val_score(model2, fp_dataset, target, cv=10)
    print(np.mean(scores))
    # note the  best accuracy from the 10-fold
    # repeat
    results.append(np.mean(scores))
    secret_key = secret_key - 3

print(np.mean(results))
print("Time: " + str(int(time()-start)) + " sec.")

# --------- # 0.7167832167832168 # 0.6678321678321678  # 0.6783216783216783 # 0.7517482517482518
# --------------------------------------------------------------------------------------------
# --------- # decision tree      # logistic regression # gradient boosting  # knn
# gamma = 1 | 0.6853146853146851 #                     #                    #
# ----------------------------------------------------------------------------------------------#
# gamma = 2 | 0.6993006993006995
# ----------------------------------------------------------------------------------------------#
# gamma = 3 | 0.6643356643356643 # 0.6608391608391608  #
# ----------------------------------------------------------------------------------------------#
# gamma = 5 | 0.6993006993006995
# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------
# gamma = 1 |        ?                     ?                     ?          # 0.7382266009852217
# gamma = 2          ?                     ?                      ?         # 0.7308374384236453
# gamma = 3          ?                     ?                      ?         # 0.7381034482758622
# gamma = 5          ?                     ?                      ?         # 0.7488177339901477
#