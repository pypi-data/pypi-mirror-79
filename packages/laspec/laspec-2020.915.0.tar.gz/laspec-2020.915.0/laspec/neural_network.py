from tensorflow import keras
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, BatchNormalization, Input
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, MaxPooling1D, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.datasets import imdb
from tensorflow.keras.optimizers import RMSprop, SGD, Adam
from tensorflow.keras import backend as K
from tensorflow.keras import losses
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split


def create_c3nn2_classifier(ninput=100, nfilters=32, kernel_size=4, ndense=(128, 16), pool_size=2, dropout_rate=0.5,
                            noutput=1, activation_hidden="relu", activation_out="sigmoid"):
    """ An easy way of creating a CNN with 3 convolutional layers and 2 dense layers

    Parameters
    ----------
    ninput:
        input shape
    nfilters:
        number of filters
    kernel_size:
        kernel size
    ndense: tuple
        number of neurons in dense layers
    pool_size:
        pool size in MaxPooling
    dropout_rate:
        dropout rate
    noutput:
        output shape
    activation_hidden:
        the activation function used in hidden layers
    activation_out:
        the activation function used in output layers


    Returns
    -------

    """
    model = Sequential()
    model.add(
        Conv1D(filters=nfilters, kernel_size=kernel_size, strides=1, padding="valid", activation=activation_hidden,
               input_shape=(ninput, 1)))
    # ,data_format="channels_last"
    model.add(MaxPooling1D(pool_size, padding="valid"))
    model.add(BatchNormalization())

    model.add(Conv1D(nfilters, kernel_size, padding="valid", activation=activation_hidden))
    model.add(MaxPooling1D(pool_size, padding="valid"))
    model.add(BatchNormalization())

    model.add(Conv1D(nfilters, kernel_size, padding="valid", activation=activation_hidden))
    model.add(MaxPooling1D(pool_size, padding="valid"))
    model.add(BatchNormalization())
    model.add(Dropout(dropout_rate))

    model.add(Flatten())
    model.add(Dense(ndense[0], activation=activation_hidden, ))  # input_shape=(4000,)
    model.add(BatchNormalization())
    model.add(Dropout(dropout_rate))

    model.add(Dense(ndense[1], activation=activation_hidden))
    model.add(Dropout(dropout_rate))
    model.add(BatchNormalization())

    model.add(Dense(noutput, activation=activation_out))
    return model


class CNN:
    model = None
    filepath = ""
    callbacks_list = []
    history = None

    def __init__(self, kind="c3nn2", ninput=100, *args):
        if kind == "c3nn2":
            # a fast way of creating c3nn2 classifier
            self.model = create_c3nn2_classifier(ninput=ninput, *args)
        else:
            raise ValueError("Bad value for *kind*!")

        # default device
        self.get_gpu()

        # default callbacks
        self.set_callbacks()
        return

    def set_callbacks(self, monitor_earlystopping="val_loss", patience_earlystopping=5,
                      monitor_modelcheckpoint="val_loss", filepath='./data/v12/v12_class_B_cw1e2_sw.hdf5',
                      monitor_reducelronplateau="val_loss", patience_reducelronplateau=2, factor_reducelronplateau=0.33,
                      ):
        """ set callbacks """
        self.callbacks_list = [
            # This callback will interrupt training when we have stopped improving
            keras.callbacks.EarlyStopping(
                # This callback will monitor the validation accuracy of the model
                monitor=monitor_earlystopping,
                # Training will be interrupted when the accuracy
                # has stopped improving for *more* than 1 epochs (i.e. 2 epochs)
                patience=patience_earlystopping,
            ),
            # This callback will save the current weights after every epoch
            keras.callbacks.ModelCheckpoint(
                filepath=filepath,  # Path to the destination model file
                # The two arguments below mean that we will not overwrite the
                # model file unless `val_loss` has improved, which
                # allows us to keep the best model every seen during training.
                monitor=monitor_modelcheckpoint,
                save_best_only=True,
            ),
            keras.callbacks.ReduceLROnPlateau(
                # This callback will monitor the validation loss of the model
                monitor=monitor_reducelronplateau,
                # It will divide the learning by 10 when it gets triggered
                factor=factor_reducelronplateau,
                # It will get triggered after the validation loss has stopped improving
                # for at least 10 epochs
                patience=patience_reducelronplateau,
            )
        ]
        return

    def train(self, x, y, sw, test_size=0.2, random_state=0, epochs=200, batch_size=256,
              optimizer=Adam, lr=1e-5, loss="binary_crossentropy", metrics=['accuracy']):
        # split sample
        xtrain, xtest, ytrain, ytest, swtrain, swtest = train_test_split(
            x, y, sw, test_size=test_size,random_state=random_state)

        # compile optimizer
        self.model.compile(optimizer=optimizer(lr), loss=loss, metrics=metrics, )

        # train model
        self.history = self.model.fit(
            xtrain, ytrain, sample_weight=swtrain,
            batch_size=batch_size, epochs=epochs, callbacks=self.callbacks_list,
            validation_data=(xtest, ytest, swtest))

        # reload the best model
        self.model = keras.models.load_model(self.filepath)

        return self.history

    @staticmethod
    def set_gpu(device="0"):
        """ set gpu device """
        old_device = os.environ["CUDA_VISIBLE_DEVICES"]
        os.environ["CUDA_VISIBLE_DEVICES"] = device
        new_device = os.environ["CUDA_VISIBLE_DEVICES"]
        print("Changing device {} to {}".format(old_device, new_device))
        return

    @staticmethod
    def get_gpu():
        """ get gpu device """
        old_device = os.environ["CUDA_VISIBLE_DEVICES"]
        print("Current device is {} ".format(old_device))
        return old_device

    def dump(self, filepath):
        """ dump CNN object """
        self.model.save(filepath)
        self.model = None
        joblib.dump(self, filepath + ".cnn")
        return

    @staticmethod
    def load(filepath):
        """ load CNN object """
        assert os.path.exists(filepath)
        assert os.path.exists(filepath + ".cnn")
        cnn = joblib.load(filepath + ".cnn")
        cnn.model = load_model(filepath)
        return cnn

    def predict(self, *args, **kwargs):
        """ an alias for model.predict """
        return self.model.predict(*args, **kwargs)

    def evaluate(self, *args, **kwargs):
        """ an alias for model.evaluate """
        return self.model.evaluate(*args, **kwargs)
