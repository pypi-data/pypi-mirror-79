import matplotlib.pyplot as plt # plotting
import os # for file/folder creations
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

def train_test_model_with(args, save_name=None):
    """
    args must follow convention
    
    global:
    + x_train, y_train
    + x_val, y_val
    + x_test, y_test
    """
    # initialize and build
    # --------------------
    baseline_model = TestModel(args)
    # compile
    baseline_model.compile_model(args)
    
    # Train eval, save and plot
    # -------------------------
    baseline_model.fit((x_train, y_train),(x_val, y_val), 0, args)
    # save
    if save_name is not None:
        os.makedirs(f'SavedModels', exist_ok=True)
        baseline_model.save_to(f"./SavedModels/{save_name}.h5")
    # Evaluate the performance (unseen data)
    baseline_model.evaluate(x_test, y_test, v=1)
    # plot
    baseline_model.plot()