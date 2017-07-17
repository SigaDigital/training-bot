from os import listdir
from os.path import isfile, join, abspath, exists, basename
from shutil import copyfile, rmtree

import os
import random

class Recognizer:
    train_rate = 0
    prepare_output_path = "./prepared/"

    def __init__(self, train_rate):
        self.train_rate = train_rate
        
    def prepare(self):
        for dir_name in os.listdir("./cleaned_data/data_set"):
            self._randomize(abspath("./cleaned_data/data_set/" + dir_name))

    def _randomize(self, dir):
        name = basename(dir)

        if exists(abspath(self.prepare_output_path + name)):
            rmtree(abspath(self.prepare_output_path + name))

        if not exists(abspath(self.prepare_output_path + name)):
            os.makedirs(abspath(self.prepare_output_path + name))
            os.makedirs(abspath(self.prepare_output_path + name + "/train"))
            os.makedirs(abspath(self.prepare_output_path + name + "/test"))

        files = [abspath(dir + "/" + f) for f in listdir(dir) if isfile(join(dir, f))]

        train_set_number = int((self.train_rate * 0.01) * len(files))
        randomed_train = random.sample(files, train_set_number)
        randomed_test = []

        for f in files:
            if f not in randomed_train:
                randomed_test.append(f)

        for f in randomed_train:
            copyfile(f, abspath(self.prepare_output_path + name) + "/train/" + basename(f))

        for f in randomed_test:
            copyfile(f, abspath(self.prepare_output_path + name) + "/test/" + basename(f))