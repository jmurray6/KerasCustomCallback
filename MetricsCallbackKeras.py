from tensorflow import keras
import tensorflow.keras.backend as K
from datetime import datetime
import os 
from db_util import write_training_metrics

class MetricsCallback(keras.callbacks.Callback):

    def __init__(self, cursor):
        self.cursor = cursor
        self.epochs = 0
        self.start = None
        self.end = None
        self.accuracy_list = []
        self.loss_list = []
        self.duration = 0

    def on_train_begin(self, logs=None):
        self.start = datetime.now()

    def on_train_end(self, logs=None):
        self.end = datetime.now()
        self.duration = (self.end - self.start).total_seconds()
        self.write_metrics(logs)

    def on_epoch_end(self, epoch, logs=None):
        self.epochs += 1
        self.accuracy_list.append(logs['accuracy'])
        self.loss_list.append(logs['loss'])
    
    def write_metrics(self, logs):
        model_name = os.environ.get("MODEL_NAME")
        model_type = os.environ.get("MODEL_TYPE")
        learning_rate = K.eval(self.model.optimizer.lr)

        write_training_metrics(
            self.cursor, 
            model_name, 
            model_type, 
            'keras', 
            self.duration,
            self.params.get("epochs"),
            learning_rate, 
            logs['accuracy'], 
            logs['loss'], 
            self.accuracy_list,
            self.loss_list
        )
        

