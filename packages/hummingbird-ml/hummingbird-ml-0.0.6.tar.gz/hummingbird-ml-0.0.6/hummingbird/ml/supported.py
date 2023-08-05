# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
All operators, backends, and configurations settings supported in Hummingbird are registered here.

**Supported Backends**
PyTorch,
TorchScript,
ONNX

**Supported Operators**
BernoulliNB,
Binarizer,
DecisionTreeClassifier,
DecisionTreeRegressor,
ExtraTreesClassifier,
ExtraTreesRegressor,
FastICA,
GaussianNB,
GradientBoostingClassifier,
GradientBoostingRegressor,
HistGradientBoostingClassifier,
HistGradientBoostingRegressor,
IsolationForest,
KernelPCA,
KBinsDiscretizer,
LinearRegression,
LinearSVC,
LogisticRegression,
LogisticRegressionCV,
MaxAbsScaler,
MinMaxScaler,
MissingIndicator,
MLPClassifier,
MLPRegressor,
MultinomialNB,
Normalizer,
OneHotEncoder,
PCA,
PolynomialFeatures,
RandomForestClassifier,
RandomForestRegressor,
RobustScaler,
SelectKBest,
SelectPercentile,
SimpleImputer,
SGDClassifier,
StandardScaler,
TreeEnsembleClassifier,
TreeEnsembleRegressor,
TruncatedSVD,
VarianceThreshold,

LGBMClassifier,
LGBMRanker,
LGBMRegressor,


XGBClassifier,
XGBRanker,
XGBRegressor
"""
from collections import defaultdict

from .exceptions import MissingConverter
from ._utils import torch_installed, sklearn_installed, lightgbm_installed, xgboost_installed, onnx_runtime_installed


def _build_sklearn_operator_list():
    """
    Put all suported Sklearn operators on a list.
    """
    if sklearn_installed():
        # Enable experimental to import HistGradientBoosting*
        from sklearn.experimental import enable_hist_gradient_boosting

        # Tree-based models
        from sklearn.ensemble import (
            ExtraTreesClassifier,
            ExtraTreesRegressor,
            GradientBoostingClassifier,
            GradientBoostingRegressor,
            HistGradientBoostingClassifier,
            HistGradientBoostingRegressor,
            IsolationForest,
            RandomForestClassifier,
            RandomForestRegressor,
        )

        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

        # Linear-based models
        from sklearn.linear_model import (
            LinearRegression,
            LogisticRegression,
            LogisticRegressionCV,
            SGDClassifier,
        )

        # SVM-based models
        from sklearn.svm import LinearSVC, SVC, NuSVC

        # Imputers
        from sklearn.impute import MissingIndicator, SimpleImputer

        # MLP Models
        from sklearn.neural_network import MLPClassifier, MLPRegressor

        # Naive Bayes Models
        from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB

        # Matrix decomposition transformers
        from sklearn.decomposition import PCA, KernelPCA, FastICA, TruncatedSVD

        # Preprocessing
        from sklearn.preprocessing import (
            Binarizer,
            KBinsDiscretizer,
            MaxAbsScaler,
            MinMaxScaler,
            Normalizer,
            OneHotEncoder,
            PolynomialFeatures,
            RobustScaler,
            StandardScaler,
        )

        try:
            from sklearn.preprocessing import Imputer
        except ImportError:
            # Imputer was deprecate in sklearn >= 0.22
            Imputer = None

        # Features
        from sklearn.feature_selection import SelectKBest, SelectPercentile, VarianceThreshold

        supported_ops = [
            # Trees
            DecisionTreeClassifier,
            DecisionTreeRegressor,
            ExtraTreesClassifier,
            ExtraTreesRegressor,
            GradientBoostingClassifier,
            GradientBoostingRegressor,
            HistGradientBoostingClassifier,
            HistGradientBoostingRegressor,
            IsolationForest,
            OneHotEncoder,
            RandomForestClassifier,
            RandomForestRegressor,
            # Linear-methods
            LinearRegression,
            LinearSVC,
            LogisticRegression,
            LogisticRegressionCV,
            SGDClassifier,
            # Other models
            BernoulliNB,
            GaussianNB,
            MLPClassifier,
            MLPRegressor,
            MultinomialNB,
            # SVM
            NuSVC,
            SVC,
            # Imputers
            Imputer,
            MissingIndicator,
            SimpleImputer,
            # Preprocessing
            Binarizer,
            KBinsDiscretizer,
            MaxAbsScaler,
            MinMaxScaler,
            Normalizer,
            PolynomialFeatures,
            RobustScaler,
            StandardScaler,
            # Matrix Decomposition
            FastICA,
            KernelPCA,
            PCA,
            TruncatedSVD,
            # Feature selection
            SelectKBest,
            SelectPercentile,
            VarianceThreshold,
        ]

        # Remove all deprecated operators given the sklearn version. E.g., Imputer for sklearn > 0.21.3.
        return [x for x in supported_ops if x is not None]

    return []


def _build_xgboost_operator_list():
    """
    List all suported XGBoost (Sklearn API) operators.
    """
    if xgboost_installed():
        from xgboost import XGBClassifier, XGBRanker, XGBRegressor

        return [XGBClassifier, XGBRanker, XGBRegressor]

    return []


def _build_lightgbm_operator_list():
    """
    List all suported LightGBM (Sklearn API) operators.
    """
    if lightgbm_installed():
        from lightgbm import LGBMClassifier, LGBMRanker, LGBMRegressor

        return [LGBMClassifier, LGBMRanker, LGBMRegressor]

    return []


# Associate onnxml types with our operator names.
def _build_onnxml_operator_list():
    """
    List all suported ONNXML operators.
    """
    if onnx_runtime_installed():
        return [
            # Linear-based models
            "LinearClassifier",
            "LinearRegressor",
            # ONNX operators.
            "Cast",
            "Concat",
            "Reshape",
            # Preprocessing
            "ArrayFeatureExtractor",
            "OneHotEncoder",
            "Normalizer",
            "Scaler",
            # Tree-based models
            "TreeEnsembleClassifier",
            "TreeEnsembleRegressor",
        ]
    return []


def _build_backend_map():
    """
    The set of supported backends is defined here.
    """
    backends = defaultdict(lambda: None)

    if torch_installed():
        import torch

        backends[torch.__name__] = torch.__name__
        backends["py" + torch.__name__] = torch.__name__  # For compatibility with earlier versions.

        backends[torch.jit.__name__] = torch.jit.__name__
        backends["torchscript"] = torch.jit.__name__  # For reference outside Hummingbird.

    if onnx_runtime_installed():
        import onnx

        backends[onnx.__name__] = onnx.__name__

    return backends


def _build_sklearn_api_operator_name_map():
    """
    Associate Sklearn with the operator class names.
    If two scikit-learn (API) models share a single name, it means they are equivalent in terms of conversion.
    """
    # Pipeline ops. These are ops injected by the parser not "real" sklearn operators.
    pipeline_operator_list = [
        "ArrayFeatureExtractor",
        "Concat",
        "Multiply",
    ]

    return {
        k: "Sklearn" + k.__name__ if hasattr(k, "__name__") else k
        for k in sklearn_operator_list + pipeline_operator_list + xgb_operator_list + lgbm_operator_list
    }


def _build_onnxml_api_operator_name_map():
    """
    Associate ONNXML with the operator class names.
    If two ONNXML models share a single name, it means they are equivalent in terms of conversion.
    """
    return {k: "ONNXML" + k for k in onnxml_operator_list if k is not None}


def get_sklearn_api_operator_name(model_type):
    """
    Get the operator name for the input model type in *scikit-learn API* format.

    Args:
        model_type: A scikit-learn model object (e.g., RandomForestClassifier)
                    or an object with scikit-learn API (e.g., LightGBM)

    Returns:
        A string which stands for the type of the input model in the Hummingbird conversion framework
    """
    if model_type not in sklearn_api_operator_name_map:
        raise MissingConverter("Unable to find converter for model type {}.".format(model_type))
    return sklearn_api_operator_name_map[model_type]


def get_onnxml_api_operator_name(model_type):
    """
    Get the operator name for the input model type in *ONNX-ML API* format.

    Args:
        model_type: A ONNX-ML model object (e.g., TreeEnsembleClassifier)

    Returns:
        A string which stands for the type of the input model in the Hummingbird conversion framework.
        None if the model_type is not supported
    """
    if model_type not in onnxml_api_operator_name_map:
        return None
    return onnxml_api_operator_name_map[model_type]


# Supported operators.
sklearn_operator_list = _build_sklearn_operator_list()
xgb_operator_list = _build_xgboost_operator_list()
lgbm_operator_list = _build_lightgbm_operator_list()
onnxml_operator_list = _build_onnxml_operator_list()

sklearn_api_operator_name_map = _build_sklearn_api_operator_name_map()
onnxml_api_operator_name_map = _build_onnxml_api_operator_name_map()


# Supported backends.
backends = _build_backend_map()

# Supported configurations settings accepted by Hummingbird are defined below.
N_FEATURES = "n_features"
"""Number of features expected in the input data."""

TREE_IMPLEMENTATION = "tree_implementation"
"""Which tree implementation to use. Values can be: gemm, tree-trav, perf_tree_trav."""

ONNX_OUTPUT_MODEL_NAME = "onnx_model_name"
"""For ONNX models we can set the name of the output model."""

ONNX_INITIAL_TYPES = "onnx_initial_types"
"""For ONNX models we can explicitly set the input types and shapes."""

ONNX_TARGET_OPSET = "onnx_target_opset"
"""For ONNX models we can set the target opset to use. 9 by default."""

INPUT_NAMES = "input_names"
"""Set the names of the inputs. Assume that the numbers onf inputs_names is equal to the number of inputs."""

OUTPUT_NAMES = "output_names"
"""Set the names of the outputs."""

CONTAINER = "container"
"""Whether to return the container for Sklearn API or just the model"""
