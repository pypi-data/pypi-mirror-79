
import numpy as np

from tensorflow import keras

from NiLBS.weighting.weighting_function import WeightingFunction


class WeightingFunctionMLPNaive(WeightingFunction):
    """


    Weighting function backed by a Keras regression network.
    Queries are performed using the naive pose encoding.


    """
    def __init__(self, model=None, model_path=None):

        if model_path is not None:

            self.model = keras.models.load_model(model_path)
        else:

            self.model = model

    def generate_query(self, x, pose):

        return np.concatenate((x, pose.get_naive_encoding()), axis=0)

    def generate_query_set(self, X, pose):

        pose_encoding = pose.get_naive_encoding()
        pose_encoding_list = np.tile(pose_encoding, (X.shape[0], 1))
        result = np.concatenate((X, pose_encoding_list), axis=1)

        return result

    def evaluate(self, x, pose):

        query = self.generate_query(x, pose)

        return self.model.predict(np.array([query]))[0]

    def evaluate_set(self, X, pose):

        query_set = self.generate_query_set(X, pose)

        return self.model.predict(query_set)
