import sys
import os
import getopt
import subprocess
from downloader import Downloader

train_rate = 0

def do_cluster():
    FNULL = open(os.devnull, 'w') 
    for dir_name in os.listdir("./downloaded"):
        if os.path.isdir("./downloaded/" + dir_name):
            print "Clustering: " + dir_name
            args = "./cleaner/clean.exe \"" + os.path.abspath('./downloaded/' + dir_name) + "\" 0.45 \"" + os.path.abspath("./cleaned_data") + "\""
            subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

try:
    opts, args = getopt.getopt(sys.argv[1:],'hf:t:',['file=, trainRate='])
    print opts
except getopt.GetoptError:
        sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print "Help"
    elif opt in ('-f', '--file'):
        input_file = arg
        print 'Reading file: ', input_file
    elif opt in ('-t', '--trainRate'):
        train_rate = int(float(arg))

if train_rate is 0:
    train_rate = 80

print 'training set: ',  train_rate
print 'test set: ',  100 - train_rate

with open(input_file) as f:
    content = f.readlines()

downloader = Downloader([x.strip() for x in content])
downloader.recurring_retrieve()
do_cluster()

