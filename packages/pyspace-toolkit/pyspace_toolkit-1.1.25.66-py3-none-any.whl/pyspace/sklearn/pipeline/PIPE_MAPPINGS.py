# %%
import pyspace
import pyspace.sklearn.core as pyspace_sklearn_core

# %%
import sklearn

# %%
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# %%
from sklearn.decomposition import PCA, TruncatedSVD

# %%
from sklearn.svm import LinearSVC

# %%
from sklearn.cluster import AgglomerativeClustering

# %%
PIPE_MAPPINGS = {
    'pdseries': pyspace_sklearn_core.transformer.common_transformers.pdSeriesTransformer,
    'pdvalues': pyspace_sklearn_core.transformer.common_transformers.pdValuesTransformer,
    'npfloat64': pyspace_sklearn_core.transformer.common_transformers.npFloat64Transformer,
    'toarray': pyspace_sklearn_core.transformer.common_transformers.DenseTransformer,
    'identity': pyspace_sklearn_core.transformer.common_transformers.IdentityTransformer,
    
    'tokenize': pyspace_sklearn_core.transformer.text_transformers.TokenizerTransformer,
    'ontoken': pyspace_sklearn_core.transformer.text_transformers.TokenTransformer,
    'onsent': pyspace_sklearn_core.transformer.text_transformers.SentenceTransformer,
    
    'wordvector': pyspace_sklearn_core.transformer.text_transformers.WordvectorTransformer,
    'discrete': pyspace_sklearn_core.transformer.text_transformers.WordvectorDiscreteTransformer,

    'onehot': OneHotEncoder,
    'tfidf': TfidfVectorizer,
    'tf': CountVectorizer,
    'mtfidf': pyspace_sklearn_core.transformer.text_transformers.SupervisedMergedTfidfTransformer,
    'cdfidf': pyspace_sklearn_core.transformer.text_transformers.SupervisedCdfidfTransformer,
    
    'pca': PCA,
    'tsvd': TruncatedSVD,
    
    'lsvm': LinearSVC,
    'lsvm+': pyspace_sklearn_core.model.custom_classifier.LinearSVCExtended,
    
    'agg+': pyspace_sklearn_core.model.custom_cluster.AgglomerativeClusteringThreshold,
    'agg': AgglomerativeClustering,
    
    'hierarchic': pyspace_sklearn_core.model.custom_classifier.HierarchicalClassifierExtended,
}

# %%
try:
    import lightgbm
    PIPE_MAPPINGS['lgbm'] = lightgbm.LGBMClassifier
except:
    pass

# %%
try:
    import xgboost
    PIPE_MAPPINGS['xgb'] = xgboost.XGBClassifier
except:
    pass
