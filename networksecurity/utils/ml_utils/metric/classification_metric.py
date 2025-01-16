from networksecurity.entity.artifact_entity import ClassificationMetricArtifcat
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,recall_score,precision_score
import sys

def get_classification_metric(y_true,y_pred) ->ClassificationMetricArtifcat:
    try:
        f1_score_metric = f1_score(y_true,y_pred)
        recall_score_metric = recall_score(y_true,y_pred)
        precision_score_metric = precision_score(y_true,y_pred)

        classification_metric = ClassificationMetricArtifcat(
            f1_score = f1_score_metric,
            recall_score = recall_score_metric,
            precision_score = precision_score_metric
        )
    except Exception as e:
        raise NetworkSecurityException(e,sys)