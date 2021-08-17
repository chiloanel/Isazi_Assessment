# Isazi Assessment

This repository aims to be the main store of source code for the Isazi's Optimal Decision Tree Assessment. The solution is built using Python and its libraries.

"An optimal tree means the tree with the fewest number of nodes that correctly classifies all the data"

The implemented solution uses gini impurity and information gain to ask the best question at each dataset/node, then split the dataset with the question, and recursively repeat this method until reaching a leaf (point where there are no further questions to ask). The resulting optimal tree is printed in a json and png - file.

The assessment is divided into two main parts:

- Part 1: Accepts a dataset and generates a decision tree (in json format).
- Part 2: Uses the json file to draw its content to a png file.

# Running the program

This section outlines how to run the program.

## Libraries

The pillow (PIL) library is used to draw the json content to an image file. This library can be installed via using "pip install pillow".

The csv library used for reading from a csv file, and the json library used for writing/reading from a json file are built in in Python.

## Run the script

The solution is written in the "DecisionTree.py" script which can be found under the "solution/" directory. This script can be ran using the command-line/terminal "python DecisionTree.py"

The algorithm uses the data stored in the "datafiles/"" directory. Each data filename must be inputted manually in the main function to generate the tree.

The json and png files containing the tree are stored in the "results/"" directory.

# Problems with the solution and possible improvements

The implemented algorithm makes use recursive functions. There are possible giant stack traces for large datasets, "cars.cv" in the examples reaches python's maximum recursion depth, and its tree cannot be generated. This issue has not been fixed; below are the possible solutions I have thought of implementing.

## Solution 1
Increase the recursion limit using "sys.setrecursionlimit(limit)". This could cause stack overflow - not a good solution.
## Solution 2
Write an equivalent iterative method.