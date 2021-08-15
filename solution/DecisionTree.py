# Written by Learn Chiloane [date: 10/08/2021]
import csv
import sys

def readData(file_name):
	categories = []
	options = [[]]
	dataset = []
	with open(file_name, newline='') as csv_data_file:
		data_reader = csv.reader(csv_data_file, delimiter='\n')
		
		for row in data_reader:
			row_array = row[0].split(',')

			# Extract the column headers and
			# Create an empty 2D array with the column size
			if not categories:
				categories = row_array
				options = [[] for i in range(len(categories))]
				continue

			# Append the options for each header/category - exclude duplicates
			for data_idx in range(len(categories)):
				if (row_array[data_idx] not in options[data_idx]):
					options[data_idx].append(row_array[data_idx])

			# Take all data elements after the headers
			dataset.append(row_array)

	return categories, options, dataset


class SplitDatasetQuestion():
	""" Splits the dataset based on the asked question """
	def __init__(self, column_num_, column_val_):
		self.column_num = column_num_
		self.column_val = column_val_

	def isQuestionTrue(self, data_row): #""" Returns true when the question is correct - column value found in the row """
		return data_row[self.column_num] == self.column_val

	def __repr__(self):
		return str(categories[self.column_num]) #+": "+str(self.column_val)



def sliceDataset(dataset, category_col):

	category_count = classCount(dataset,category_col)

	slice_data = [[] for i in range(len(category_count))]
	for (category, value) in (category_count).items():
		category_idx = list(category_count.keys()).index(category)
		for data_row in dataset:
			if category in data_row:
				slice_data[category_idx].append(data_row)

	return slice_data


class UncertaintyCalculation():
	"""Calcultes the uncertainty in order to select the best question to splice the dataset"""
	def __init__(self):
		self.power = 2
		self.impurity_init = 1

	def giniImpurity(self, dataset):
		# https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity

		# determine the duplicated decisions and calculate the gini impurity
		outcome_count = classCount(dataset, -1)

		gini_impurity = self.impurity_init
		for (outcome_name, total_appearance) in outcome_count.items():
			outcome_prob = float(total_appearance/float(len(dataset)))
			gini_impurity -= outcome_prob**self.power

		return gini_impurity

	def informationGain(self, split_dataset, current_uncertainty):
		# information gain:

		prob_data = []
		total_dataset = 0;
		for split_data in split_dataset:
			total_dataset += len(split_data)

		# calculate the probability of each split dataset then 
		# calculate the information gain
		information_gain = current_uncertainty
		for split_data in split_dataset:
			p = float(len(split_data))/float(total_dataset)
			information_gain -= p*self.giniImpurity(split_data)

		return information_gain


class Leaf:
    def __init__(self, leaf_data, question_asked):
        decision_outcome =  leaf_data[0][-1] # take the first/any decision of the leaf (the leaf data should have one type of outcome)
        common_option = leaf_data[0][question_asked.column_num] # the leaf category option is not influenced by other options
        self.option_decision = common_option, decision_outcome
        # print("Leaf:", leaf_data,"\n")


class DecisionNode:
    def __init__(self, split_question_, split_dataset_, split_option_):
        self.split_question = split_question_
        self.split_dataset = split_dataset_
        self.split_option = split_option_
        # print("Option:", split_option_)
        # print("Datatype:", split_dataset_)

def optimalSlice(dataset):

	best_infor_gain = 0
	best_question = None
	uncertainty = UncertaintyCalculation()
	current_uncertainty = uncertainty.giniImpurity(dataset)

	for category_col in range (len(categories)-1):

		for option_val in options[category_col]:
			
			split_question = SplitDatasetQuestion(category_col, option_val)
			split_dataset = sliceDataset(dataset, category_col)


			# Continue to the next question (column and value) after an unsuccessful split
			if not split_dataset[0]:
				continue

			infor_gain = uncertainty.informationGain(split_dataset, current_uncertainty)


			if infor_gain > best_infor_gain:
				best_infor_gain, best_question = infor_gain, split_question

	return best_infor_gain, best_question


def getOptimalTree(dataset, question_node = None):

	infor_gain, split_question = optimalSlice(dataset)

	if infor_gain == 0:
		return Leaf(dataset, question_node)

	print("Question -", split_question)
	split_dataset = sliceDataset(dataset, split_question.column_num)

	split_data_branch = []
	split_option = ""
	for split_data in split_dataset:
		split_data_branch = getOptimalTree(split_data, split_question)
		
		if not isinstance(split_data_branch, Leaf):
			split_option = split_data[0][split_question.column_num]# the common option in the selected split data
			print("Node:", split_data_branch)
		else:
			print("Leaf:", split_data_branch.option_decision[0]+": "+split_data_branch.option_decision[1])

	# print("Decision Node:", split_data_branch)
	return DecisionNode(split_question, split_data_branch, split_option)


## 10/10
def classCount(dataset, class_col):
		class_count = {}
		for data_row in dataset:
			option = data_row[class_col] # class option
			if option not in class_count:
				class_count[option] = 0 # first time store zero
			class_count[option] +=1

		return class_count


def printTree(node, spacing = ""):
    """Tree printing function."""

    # Reached the leaf: display the option and the decision then return
    if isinstance(node, Leaf):
    	print(spacing + node.option_decision[0] + ":" , node.option_decision[1])
    	return

    # Display the label of this category
    
    # print(node.split_dataset)

    # for split_data in node.split_dataset:

    # if not isinstance(node, Leaf):
    print(node.split_question)
    printTree(node.split_dataset, spacing + "  ")
    # if isinstance(node, list):
    # 	for nd in node:
    # 		print(nd)
    		



if __name__ == '__main__':
	file_name = 'sports.csv'

	categories, options, dataset = readData(file_name)

	my_tree = getOptimalTree(dataset)

	print("--------------------------------------")

	print(my_tree.split_question)

	# print("tree = ", my_tree)
	print("--------------------------------------")
	printTree(my_tree)
