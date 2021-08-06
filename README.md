# Introduction
(c) Isazi 2021

There are many domains in real life that require an optimal decision tree to be
inferred over a dataset. This problem will explore an easier (and well understood)
subset of this domain.

# Problem

## Part 1

Given two example files (cars.csv, and sports.csv), you are required to write a
program, in your programming language of choice, that will produce an output file
(in JSON format) that will describe an optimal decision tree.

In other words, program an algorithm that calculates an optimal branching order of
categories to reach a decision.

By convention the last column of the input file will always be the desired decision
or outcome.

For example, given the following toy input:
```
Category 1,Category 2,Decision
1A,2A,Y
1A,2B,Y
1B,2A,Y
1B,2B,N
```

The program could produce a JSON file as follows:
```
{
    "Category 1": {
        "1A": "Y",
        "1B": {
            "Category 2": {
                "2A": "Y",
                "2B": "N"
            }
        }
    }
}
```

Note, another valid JSON file could also be:
```
{
    "Category 2": {
        "2A": "Y",
        "2B": {
            "Category 1": {
                "1A": "Y",
                "1B": "N"
            }
        }
    }
}
```

An optimal tree means the tree with the fewest number of nodes that correctly
classifies all the data. In the above example, either tree is optimal.

## Part 2

Write a program that accepts your output file in the previous section and draws
it either on the screen or to an image file (such as png).

# Evaluation

1. Please ensure that you have placed your code in a Github repo and granted us access to view it.
2. If your program makes use of libraries or other dependencies please ensure that detailed instructions
   are provided along with your code on how to get the programs running. Ideally, you should use
   your programming language's package manager to facilitate this process (e.g. for Python this is pipenv, for C# this is nuget, etc.)
3. It is your choice what to implement vs. what to use a library for and either of these choices are considered equally valid
4. Remember we are primarily evaluating your ability to solve a problem.
