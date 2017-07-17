import sys
import os
import argparse
import subprocess
import preparator
from downloader import Downloader
from recognizer import Recognizer

def do_cluster():
    FNULL = open(os.devnull, 'w') 
    for dir_name in os.listdir("./downloaded"):
        if os.path.isdir("./downloaded/" + dir_name):
            print "Clustering: " + dir_name
            args = "./cleaner/clean.exe \"" + os.path.abspath('./downloaded/' + dir_name) + "\" 0.45 \"" + os.path.abspath("./cleaned_data") + "\""
            subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--file', '-f', help='name list input file path')
parser.add_argument('--trainrate', '-t', help='specify training set rate', default = 80)
parser.add_argument('--descriptor', '-d', help='specify descriptor path', default = os.path.abspath('./core/Descriptor'))
parser.add_argument('--clean', help='clean descriptor before proceed', default = False, action='store_true')

args = parser.parse_args()
input_file = os.path.abspath(args.file)
train_rate = int(float(args.trainrate))
descriptor_path = os.path.abspath(args.descriptor)
descriptor_clean_required = args.clean

print 'Name List File Path: ' + input_file
print 'Working Descriptor Path: ' + descriptor_path
print 'Descriptor Clean Required: ' + str(descriptor_clean_required)
print 'Training Set Rate: ',  train_rate
print 'Test Set Rate: ',  100 - train_rate

with open(input_file) as f:
    content = f.readlines()

preparator.empty_directory('./prepared')
preparator.empty_directory('./cleaned_data')
preparator.empty_directory('./downloaded')

if descriptor_clean_required is True:
    preparator.empty_directory(descriptor_path)
    preparator.empty_directory(descriptor_path + "/Faces")
    preparator.empty_directory(descriptor_path + "/Svms")

downloader = Downloader([x.strip() for x in content])
downloader.recurring_retrieve()
do_cluster()

recognizer = Recognizer(train_rate)
recognizer.prepare()

