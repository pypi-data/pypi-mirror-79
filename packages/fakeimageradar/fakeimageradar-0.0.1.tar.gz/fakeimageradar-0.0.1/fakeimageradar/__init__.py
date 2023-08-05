import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import itertools
import os
import re

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import Adam
from PIL import Image, ImageChops, ImageEnhance
from pylab import *


class Fakeimageradar():

    def __init__(self):
        np.random.seed(2)

    def convert_to_ela_image(self, path, quality):
        filename = path
        resaved_filename = 'tempresaved.jpg'
        ELA_filename = 'tempela.png'

        im = Image.fromarray(np.uint8(filename))
        im.save(resaved_filename, 'JPEG', quality = quality)
        resaved_im = Image.open(resaved_filename)

        ela_im = ImageChops.difference(im, resaved_im)
        
        extrema = ela_im.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        
        ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
        
        return ela_im

    def predict(self, image):
        test = array(convert_to_ela_image(image, 90).resize((128, 128))).flatten() / 255.0
        test = test.reshape(-1,128,128,3)

        model = load_model('data/model.h5')
        result = model.predict(test)

        real = result[0][0]
        fake = result[0][1]

        return real, fake
