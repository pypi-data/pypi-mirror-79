import logging
import os
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

from supervised.algorithms.algorithm import BaseAlgorithm
from supervised.algorithms.sklearn import (
    SklearnTreesEnsembleClassifierAlgorithm,
    SklearnTreesEnsembleRegressorAlgorithm,
)

from supervised.algorithms.registry import AlgorithmsRegistry
from supervised.algorithms.registry import BINARY_CLASSIFICATION
from supervised.algorithms.registry import MULTICLASS_CLASSIFICATION
from supervised.algorithms.registry import REGRESSION
from supervised.utils.config import LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class RandomForestAlgorithm(SklearnTreesEnsembleClassifierAlgorithm):

    algorithm_name = "Random Forest"
    algorithm_short_name = "Random Forest"

    def __init__(self, params):
        super(RandomForestAlgorithm, self).__init__(params)
        logger.debug("RandomForestAlgorithm.__init__")

        self.library_version = sklearn.__version__
        self.trees_in_step = additional.get("trees_in_step", 5)
        self.max_steps = additional.get("max_steps", 3)
        self.early_stopping_rounds = additional.get("early_stopping_rounds", 50)
        self.model = RandomForestClassifier(
            n_estimators=self.trees_in_step,
            criterion=params.get("criterion", "gini"),
            max_features=params.get("max_features", 0.8),
            max_depth=params.get("max_depth", 6),
            min_samples_split=params.get("min_samples_split", 4),
            warm_start=True,
            n_jobs=-1,
            random_state=params.get("seed", 1),
        )

    def file_extension(self):
        return "random_forest"


class RandomForestRegressorAlgorithm(SklearnTreesEnsembleRegressorAlgorithm):

    algorithm_name = "Random Forest"
    algorithm_short_name = "Random Forest"

    def __init__(self, params):
        super(RandomForestRegressorAlgorithm, self).__init__(params)
        logger.debug("RandomForestRegressorAlgorithm.__init__")

        self.library_version = sklearn.__version__
        self.trees_in_step = regression_additional.get("trees_in_step", 5)
        self.max_steps = regression_additional.get("max_steps", 3)
        self.early_stopping_rounds = regression_additional.get(
            "early_stopping_rounds", 50
        )
        self.model = RandomForestRegressor(
            n_estimators=self.trees_in_step,
            criterion=params.get("criterion", "mse"),
            max_features=params.get("max_features", 0.8),
            max_depth=params.get("max_depth", 6),
            min_samples_split=params.get("min_samples_split", 4),
            warm_start=True,
            n_jobs=-1,
            random_state=params.get("seed", 1),
        )

    def file_extension(self):
        return "random_forest"


# For binary classification target should be 0, 1. There should be no NaNs in target.
rf_params = {
    "criterion": ["gini", "entropy"],
    "max_features": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "min_samples_split": [10, 20, 30, 40, 50],
    "max_depth": [4, 6, 8, 10, 12],
}

classification_default_params = {
    "criterion": "gini",
    "max_features": 0.6,
    "min_samples_split": 30,
    "max_depth": 6,
}


additional = {
    "trees_in_step": 100,
    "train_cant_improve_limit": 1,
    "min_steps": 1,
    "max_steps": 50,
    "early_stopping_rounds": 50,
    "max_rows_limit": None,
    "max_cols_limit": None,
}
required_preprocessing = [
    "missing_values_inputation",
    "convert_categorical",
    "datetime_transform",
    "text_transform",
    "target_as_integer",
]

AlgorithmsRegistry.add(
    BINARY_CLASSIFICATION,
    RandomForestAlgorithm,
    rf_params,
    required_preprocessing,
    additional,
    classification_default_params,
)

AlgorithmsRegistry.add(
    MULTICLASS_CLASSIFICATION,
    RandomForestAlgorithm,
    rf_params,
    required_preprocessing,
    additional,
    classification_default_params,
)


#
# REGRESSION
#

regression_rf_params = {
    "criterion": [
        "mse"
    ],  # remove "mae" because it slows down a lot https://github.com/scikit-learn/scikit-learn/issues/9626
    "max_features": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "min_samples_split": [10, 20, 30, 40, 50],
    "max_depth": [4, 6, 8, 10, 12],
}

regression_default_params = {
    "criterion": "mse",
    "max_features": 0.6,
    "min_samples_split": 30,
    "max_depth": 6,
}

regression_additional = {
    "trees_in_step": 100,
    "train_cant_improve_limit": 1,
    "min_steps": 1,
    "max_steps": 50,
    "early_stopping_rounds": 50,
    "max_rows_limit": None,
    "max_cols_limit": None,
}
regression_required_preprocessing = [
    "missing_values_inputation",
    "convert_categorical",
    "datetime_transform",
    "text_transform",
    "target_scale",
]

AlgorithmsRegistry.add(
    REGRESSION,
    RandomForestRegressorAlgorithm,
    regression_rf_params,
    regression_required_preprocessing,
    regression_additional,
    regression_default_params,
)
