# Written by Learn Chiloane [date: 10/08/2021]
import csv
import json

def readData(file_name):
	""" Function that reads the dataset from a csv file
		Format: each row is a complete dataset,
		the first row is the header, and
		the last column is the decision.

		Returns dataset header, list of options in each header, and the rest of data after the header
	"""
	categories = []
	options = [[]]
	dataset = []
	with open(file_name, newline='') as csv_data_file:
		data_reader = csv.reader(csv_data_file, delimiter='\n')
		
		for row in data_reader:
			row_array = row[0].split(',')

			# Extract the headers and create an empty 2D array with the column size
			if not categories:
				categories = row_array
				options = [[] for i in range(len(categories))]
				continue

			# Append the options for each category(header) - exclude duplicates
			for data_idx in range(len(categories)):
				if (row_array[data_idx] not in options[data_idx]):
					options[data_idx].append(row_array[data_idx])

			# Append all data elements after the headers
			dataset.append(row_array)

	return categories, options, dataset


class SplitDatasetQuestion():
	""" A SplitDatasetQuestion splits the dataset based on the asked question
		Records the header column used to split (e.g Category 1)
		Prints the header in a readable format
	 """
	def __init__(self, column_num_):
		self.column_num = column_num_

	def isQuestionTrue(self, data_row):
	 # 	Returns true when the question is correct - column value found in the row
		return data_row[self.column_num] == self.column_val

	def __repr__(self):
		return categories[self.column_num]

def sliceDataset(dataset, category_col):
	"""  Splits the dataset based on asked question (column header)

		For the selected header, slice the data set with similar options
		Returns a 3D list containing the sliced datasets
	"""
	category_count = classCount(dataset,category_col)

	slice_data = [[] for i in range(len(category_count))]
	for (category, value) in (category_count).items():
		category_idx = list(category_count.keys()).index(category)
		for data_row in dataset:
			if category in data_row:
				slice_data[category_idx].append(data_row)

	return slice_data

class UncertaintyCalculation():
	""" UncertaintyCalculation determines the gain in order to
		select the best question to splice the dataset.

		Calcultes the gini impurity for each row and
		information gain of the split dataset
	"""
	def __init__(self):
		# Constants for gini impurity calculations
		self.power = 2
		self.impurity_init = 1

	def giniImpurity(self, dataset):
		""" Calculates the gini impurity of the sliced data
			Most concise way (https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity)
			method: finds the duplicated decisions and then calculate the impurity.
		"""
		outcome_count = classCount(dataset, -1)

		gini_impurity = self.impurity_init
		for (outcome_name, total_appearance) in outcome_count.items():
			outcome_prob = float(total_appearance/float(len(dataset)))
			gini_impurity -= outcome_prob**self.power

		return gini_impurity

	def informationGain(self, split_dataset, current_uncertainty):
		""" Information gain: the uncertainity of the starting node
		minus the weighted impurity of the sliced child nodes.
		"""
		prob_data = []
		total_dataset = 0;
		for split_data in split_dataset:
			total_dataset += len(split_data)

		information_gain = current_uncertainty
		for split_data in split_dataset:
			p = float(len(split_data))/float(total_dataset)
			information_gain -= p*self.giniImpurity(split_data)

		return information_gain

class Leaf:
    """	A Leaf node classifies the option of a category that leads to a single decision outcome.
    	It holds a tuple with the option and decision 
    	(e.g. 1A, Y for the number of times 1A and Y show in their respective columns)
    	It holds no reference to the parent node and it has no child
    """
    def __init__(self, leaf_data, question_asked):
    	# take the first/any decision of the leaf (the leaf data should have one type of outcome)
        decision_outcome =  leaf_data[0][-1]
        # the leaf category option is not influenced by other options
        common_option = leaf_data[0][question_asked.column_num]
        self.option_decision = common_option, decision_outcome
        print("Leaf:", leaf_data)


class DecisionNode:
    """	A Decision Node asks a question.
    	This holds a reference to the question used to split, the node name, and the child nodes.
    """
    def __init__(self, split_question_, split_dataset_, split_option_):
        self.split_question = split_question_
        self.split_dataset = split_dataset_
        self.split_option = split_option_

def optimalSlice(dataset):
	"""	Finds the best question to ask.
		Iterates over every header, and determines the infromation gain.
	"""
	best_infor_gain = 0
	best_question = None
	uncertainty = UncertaintyCalculation()
	current_uncertainty = uncertainty.giniImpurity(dataset)

	 # For each header column (exclude decision)
	for category_col in range (len(categories)-1):

		# Store the column header/the question and plit the dataset
		split_question = SplitDatasetQuestion(category_col) 
		split_dataset = sliceDataset(dataset, category_col)

		# Continue to the next question (column) after an unsuccessful split
		if not split_dataset[0]:
			continue

		infor_gain = uncertainty.informationGain(split_dataset, current_uncertainty)

		if infor_gain > best_infor_gain:
			best_infor_gain, best_question = infor_gain, split_question

	return best_infor_gain, best_question


def buildOptimalTree(dataset, question_node = None, count=0):
	""" Builds the optimal tree

		Using the best question to ask at each node, it splits the dataset with it, and
		continuously repeat this method until reaching the leaf (no further question to ask).

		Returns a Question Node with question used to split, the node name, and the child nodes.

		*** Danger: Giant stack traces
	"""

	infor_gain, split_question = optimalSlice(dataset)

	if infor_gain == 0:
		return Leaf(dataset, question_node)

	print("Question -", split_question)
	split_dataset = sliceDataset(dataset, split_question.column_num)

	for dt in split_dataset:
		count += count
		print(dt, "\n")
		print(len(split_dataset),":", len(dt))

	if count == 900:
		return

	# Recursively build each split branch and keep track of the common option in the node branch
	split_data_branch = [[] for i in range(len(split_dataset))]
	for split_data_idx in range(len(split_dataset)):
		split_option = split_dataset[split_data_idx][0][split_question.column_num]
		count += 1
		print("count:", count)
		split_data_branch[split_data_idx] = buildOptimalTree(split_dataset[split_data_idx], split_question, count) 
		
	return DecisionNode(split_question, split_data_branch, split_option)


def classCount(dataset, class_col):
	# Counts the number of option occurrence in a single header/column (e.g Y: 3, N:1)
		class_count = {}
		for data_row in dataset:
			option = data_row[class_col] # class option
			if option not in class_count:
				class_count[option] = 0 # first store zero then increment 
			class_count[option] +=1

		return class_count

def printTree(node, jd,  key="", spacing = ""):
    """Tree printing function """

    # Reached the leaf: display the option and the decision then return for that branch
    if isinstance(node, Leaf):
    	print(spacing + node.option_decision[0] + ": " + node.option_decision[1])
    	jd[str(node.option_decision[0])] = node.option_decision[1]
    	return

    # recursively print every branch
    for nd in node.split_dataset:
    	if not isinstance(nd, Leaf):
    		print(spacing + "  " + nd.split_option +": " + str(nd.split_question))
    		# Json print
    		key = nd.split_option +":" + str(nd.split_question)
    		jd[key] = {}
    	else:
    		pass

    	printTree(nd, jd, key, spacing + "  ")

def jsonPrintTree(file_path, jd):
	# Json out of the tree (print jd fo)
	json_string = json.dumps(jd, indent=2)
	with open(file_path, 'w', encoding='utf-8') as json_file:
		json.dump(json_string, json_file, ensure_ascii=False, indent=4)

def drawJsonOutput(file_path):
	print("-------------------------------------- JSON FILE OUTPUT")
	with open(file_path) as json_file:
		json_data = json.load(json_file)
	print(json_data)

if __name__ == '__main__':

	# csv file name
	dataset_filepath = 'sports.csv'#
	json_output_filepath = dataset_filepath.split('.')[0]+'output.json'

	categories, options, dataset = readData(dataset_filepath)
	my_tree = buildOptimalTree(dataset)

	print("-------------------------------------- SCREEN PRINT")
	# Print the starting node header then rest of the tree
	jd = {}
	print(my_tree.split_question)

	key = str(my_tree.split_question)
	jd[key] = {}

	printTree(my_tree, jd[key])
	jsonPrintTree(json_output_filepath, jd)
	drawJsonOutput(json_output_filepath)



