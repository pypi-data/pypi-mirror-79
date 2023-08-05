import numpy as np
import pandas as pd
import seaborn as sns

import keras
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers.advanced_activations import PReLU
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.utils import to_categorical
from keras.regularizers import l2
from keras.wrappers.scikit_learn import KerasClassifier

from sklearn import preprocessing
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, KFold, train_test_split
from sklearn.metrics import accuracy_score


class ANN():

    def __init__(self, X, Y):
        self.X = X
        self.Xs = preprocessing.MinMaxScaler().fit_transform(X)  # X_scale
        self.Y = Y
        self.Xs_train, X_val_and_test, self.Y_train, Y_val_and_test = train_test_split(
            self.Xs, self.Y, test_size=0.3)
        self.Xs_val, self.Xs_test, self.Y_val, self.Y_test = train_test_split(
            X_val_and_test, Y_val_and_test, test_size=0.5)
        self.n_cols = self.Xs.shape[1]
        self.n_class = self.Y[1]

    def get_optimizer(self, optimizer='adam', learning_rate=0.01):
        if optimizer == 'adam':
            return(keras.optimizers.Adam(lr=learning_rate))
        elif optimizer == 'sgd':
            return(keras.optimizers.SGD(lr=learning_rate))

    def create_model(self, optimizer='adam', activation='relu', learning_rate=0.01, loss='mse', nl=[1], nn=[1], dropout=0, last_activation='sigmoid'):
        model = Sequential()
        for index in enumerate(range(nl)):
            if not index:
                model.add(Dense(nn, input_shape=(self.n_cols,), activation=activation))
            else:
                model.add(Dense(nn, activation=activation))
        # if dropout_rate:
            #model.add(Dropout(p = dropout))
        model.add(Dense(self.n_class, activation=last_activation))
        model.compile(optimizer=self.get_optimizer(
            optimizer, learning_rate), loss=loss, metrics=['accuracy'])
        return model

    def get_best_model(self, params):
        model = KerasClassifier(build_fn=self.create_model)
        random_search = RandomizedSearchCV(model, params, cv=KFold(5))
        results = random_search.fit(self.Xs_train, self.Y_train)
        return(results.best_params_)

    def optimize(self, params):
        self.best_params = self.get_best_model(params)
        model = KerasClassifier(build_fn=self.create_model(optimizer=self.best_params['optimizer'], activation=self.best_params['activation'], learning_rate=self.best_params['learning_rate'], loss=self.best_params['loss'], nl=self.best_params['nl'], nn=self.best_params['nn']), epochs=self.best_params['epochs'],
                                batch_size=self.best_params['batch_size'], verbose=0)
        kfolds = cross_val_score(model, self.Xs_val, self.Y_val, cv=5)
        print('The mean accuracy was:', kfolds.mean())
        print('With a standard deviation of:', kfolds.std())

        # first we have to make sure to input data and params into the function
