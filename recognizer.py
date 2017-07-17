from os import listdir
from os.path import isfile, join, abspath, exists, basename
from shutil import copyfile, rmtree

import os
import random
import subprocess

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
        
    def train(self, descriptor_path):
        for dir_name in os.listdir("./prepared"):
            if os.path.isdir("./prepared/" + dir_name):
                 self._classification(dir_name, descriptor_path)
        for dir_name in os.listdir("./prepared"):
            if os.path.isdir("./prepared/" + dir_name):
                test_rate = 0.0
                while test_rate < 0.8:
                    test_rate = self._testing(dir_name, descriptor_path)
                    print str(test_rate)

                    if test_rate < 0.8:
                        self._classification(dir_name, descriptor_path)

    def _classification(self, dir_name, descriptor_path):
        FNULL = open(os.devnull, 'w') 
        print "Training: " + dir_name
        args = "./core/video-tagging.exe train \"" + dir_name + "\" \"" + os.path.abspath('./prepared/' + dir_name + '/train') + "\" \"" + descriptor_path + "\""
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

    def _testing(self, dir_name, descriptor_path):
        true = 0.0
        total = 0.0
        FNULL = open(os.devnull, 'w') 
        if os.path.isdir("./prepared/" + dir_name):
            for file_name in os.listdir("./prepared/" + dir_name + "/test"):
                total += 1
                absolute_path = os.path.abspath("./prepared/" + dir_name + "/test/" + file_name)
                output = subprocess.check_output(["./core/video-tagging.exe", "test", absolute_path, descriptor_path])
                if dir_name == output:
                    true += 1
        return true / total


                