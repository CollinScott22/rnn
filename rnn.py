from __future__ import absolute_import, division, print_function, unicode_literals


import numpy as np
import pandas as pd
import pathlib
import keras
import matplotlib.pyplot as plt
import os
import datetime
import tensorflow as tf 
import tensorflow_datasets as tfds


DIRECTORY_URL = 'https://storage.googleapis.com/download.tensorflow.org/data/illiad/'
FILE_NAMES = ['cowper.txt', 'derby.txt', 'butler.txt']

for name in FILE_NAMES:
	text_dir = tf.keras.utils.get_file(name, origin=DIRECTORY_URL+name)

parent_dir = os.path.dirname(text_dir)


def labeler(example, index):
	return example, tf.cast(index,tf.int64)

labeled_data_sets = []


for i, file_name in enumerate(FILE_NAMES):
	lines_dataset = tf.data.TextLineDataset(os.path.join(parent_dir, file_name))
	labeled_dataset = lines_dataset.map(lambda ex: labeler(ex, i))
	labeled_data_sets.append(labeled_dataset)

BUFFER_SIZE = 50000
BATCH_SIZE = 64
TAKE_SIZE = 5000

all_labeled_data = labeled_data_sets[0]
for labeled_dataset in labeled_data_sets[1:]:
	all_labeled_data = all_labeled_data.concatenate(labeled_dataset)

all_labeled_data = all_labeled_data.shuffle(
	BUFFER_SIZE, reshuffle_each_iteration=False)

for ex in all_labeled_data.take(5):
	print(ex)
