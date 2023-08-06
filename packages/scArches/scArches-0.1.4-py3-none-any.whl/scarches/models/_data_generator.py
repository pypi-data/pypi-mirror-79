import keras
import numpy as np
from scipy import sparse
from scipy.sparse import issparse


class UnsupervisedDataGenerator(keras.utils.Sequence):
    def __init__(self, adata, encoded_conditions, n_conditions=1, size_factor_key=None,
                 batch_size=32, use_mmd=True,
                 shuffle=True):
        self.encoded_conditions = encoded_conditions
        self.batch_size = batch_size
        self.n_conditions = n_conditions
        self.size_factor_key = size_factor_key
        self.shuffle = shuffle
        self.use_mmd = use_mmd

        self.expr = adata.X.A if sparse.issparse(adata.X) else adata.X
        if self.size_factor_key:
            self.raw_expr = adata.raw.X.A if sparse.issparse(adata.raw.X) else adata.raw.X
            self.size_factors = adata.obs[self.size_factor_key].values

        self.on_epoch_end()

    def __len__(self):
        return len(self.expr)

    def __getitem__(self, index):
        start = index
        end = index + self.batch_size
        indexes = self.indexes[start:end]

        expression = self.expr[indexes]
        encoded_condition = self.encoded_conditions[indexes]
        one_hot_condition = keras.utils.to_categorical(encoded_condition, num_classes=self.n_conditions)

        if self.size_factor_key:
            X = [expression, one_hot_condition, one_hot_condition, self.size_factors[indexes]]
            target_expression = self.raw_expr[indexes]
        else:
            X = [expression, one_hot_condition, one_hot_condition]
            target_expression = expression

        if self.use_mmd:
            y = [target_expression, encoded_condition]
        else:
            y = [target_expression]

        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.expr))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)


class SupervisedDataGenerator(keras.utils.Sequence):
    def __init__(self, adata, encoded_conditions, encoded_labels, use_mmd=False,
                 size_factor_key=None, n_conditions=1, n_cell_types=1,
                 batch_size=32,
                 shuffle=True):
        self.adata = adata
        self.encoded_conditions = encoded_conditions
        self.encoded_cell_types = encoded_labels
        self.batch_size = batch_size
        self.n_conditions = n_conditions
        self.n_cell_types = n_cell_types
        self.size_factor_key = size_factor_key
        self.use_mmd = use_mmd
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return len(self.adata)

    def __getitem__(self, index):
        start = index
        end = index + self.batch_size
        indexes = self.indexes[start:end]

        expression = self.adata.X[indexes]
        encoded_condition = self.encoded_conditions[indexes]
        encoded_cell_type = self.encoded_cell_types[indexes]
        one_hot_condition = keras.utils.to_categorical(encoded_condition, num_classes=self.n_conditions)
        one_hot_cell_type = keras.utils.to_categorical(encoded_cell_type, num_classes=self.n_cell_types)

        if self.size_factor_key:
            X = [expression, one_hot_condition, one_hot_condition, self.adata.obs[self.size_factor_key].values[indexes]]
            target_expression = self.adata.raw.X[indexes]
        else:
            X = [expression, one_hot_condition, one_hot_condition]
            target_expression = expression

        if self.use_mmd:
            y = [target_expression, encoded_condition, one_hot_cell_type]
        else:
            y = [target_expression, one_hot_cell_type]

        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.adata))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)


def unsupervised_data_generator(x, y, batch_size=128, size_factor=False, use_mmd=True):
    if size_factor:
        expression, one_hot_condition, size_factors = x
        raw_expression, = y
    elif use_mmd:
        expression, one_hot_condition = x
        encoded_condition, = y
    else:
        expression, one_hot_condition = x

    n_samples = expression.shape[0]
    batch_expression_source, batch_expression_target = [], []
    batch_encoded_condition, batch_one_hot_condition = [], []
    batch_size_factors = []

    while True:
        for _ in range(batch_size):
            index = np.random.choice(n_samples, 1)[0]
            batch_expression_source.append(expression[index])
            batch_one_hot_condition.append(one_hot_condition[index])
            if size_factor:
                batch_size_factors.append(size_factors[index])
                batch_expression_target.append(raw_expression[index])
            elif use_mmd:
                batch_encoded_condition.append(encoded_condition[index])
                batch_expression_target.append(expression[index])
            else:
                batch_expression_target.append(expression[index])

        if size_factor:
            x_batch = [np.array(batch_expression_source), np.array(batch_one_hot_condition),
                       np.array(batch_one_hot_condition), np.array(batch_size_factors)]
            y_batch = [np.array(batch_expression_target)]
        elif use_mmd:
            x_batch = [np.array(batch_expression_source), np.array(batch_one_hot_condition),
                       np.array(batch_one_hot_condition)]
            y_batch = [np.array(batch_expression_target), np.array(batch_encoded_condition)]
        else:
            x_batch = [np.array(batch_expression_source), np.array(batch_one_hot_condition),
                       np.array(batch_one_hot_condition)]
            y_batch = [np.array(batch_expression_target)]

        yield x_batch, y_batch
