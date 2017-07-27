import sys
import os
import argparse
import preparator
from downloader import Downloader
from recognizer import Recognizer

parser = argparse.ArgumentParser(description='Proceed auto train video tagging')
parser.add_argument('--file', '-f', help='name list input file path')
parser.add_argument('--trainrate', '-t', help='specify training set rate', default = 100)
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

preparator.empty_directory('./core/Descriptor')
preparator.empty_directory('./core/Descriptor/Faces')
preparator.empty_directory('./core/Descriptor/Svms')

if descriptor_clean_required is True:
   preparator.empty_directory(descriptor_path)
   preparator.empty_directory(descriptor_path + "/Faces")
   preparator.empty_directory(descriptor_path + "/Svms")

downloader = Downloader([x.strip() for x in content])
downloader.recurring_retrieve()
downloader.do_cluster()

recognizer = Recognizer(train_rate)
recognizer.prepare()
recognizer.train(descriptor_path)

