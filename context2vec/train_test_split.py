import sys
import numpy as np
import argparse

from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_file_path", 
    type=str,
    help="path to file containing sentences"
)
parser.add_argument(
	"--output_folder_path", 
    type=str,
    help="path to output folder"
)
 
args = parser.parse_args()

with open(args.input_file_path, "r") as f:
	phrases = f.read().split("\n")

train, test = train_test_split(phrases, test_size=0.2, shuffle=True)

with open(args.output_folder_path + "/train.txt", "w") as f:
	f.write("\n".join(train))

with open(args.output_folder_path + "/test.txt", "w") as f:
	f.write("\n".join(test))

print("Done")