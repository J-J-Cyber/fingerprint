import numpy as np
import nltk
import sys
import os
import platform
import glob
from nltk.tokenize import sent_tokenize, word_tokenize, TextTilingTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# additional libs for heatmaps
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

punctuations = [",", ".", ":", ";", "(", ")", "[", "]", "{", "}"]

suptitles = ["LEL",
             "Average Word Length", "Words per Sentence",
             "Length per Sentence", "Richness per Sentence",
             "Richness per 100 Words", "Richness per Sentence-stemm",
             "Richness per 100 words stemm", "Sentiment per Sentence",
              "Digit Count per Sentence"]
# ==================================================================
#                          IMPORTANT
# ==================================================================
#nltk.download() # downloads NLTK library if not previously installed
# uncomment line 16 to download NLTK library
# ==================================================================


def test_call():
	print("Hello from Feature Extractor!")


# function to be called from server.py
def handle_feature_call(filenames, features):
	sentiment_flag = 0
	result_dict = {}
	result_name_list = []
	for filename in filenames:
		file_name = filename
		file_feature = int(features[0])
		result = ""
		path_to_file = ""
		data_path = ""

		platform_name = platform.system()
		if platform_name == "Darwin":
			data_path = os.getcwd() + "/data"
		if platform_name == "Windows":
			data_path = os.getcwd() + "\\data"

		for x in os.walk(data_path):
			for y in glob.glob(os.path.join(x[0], file_name)):
				path_to_file = y

		if path_to_file == "":
			print("no file with given name found!")
			exit(-2)

		if (file_feature > 8) and (file_feature < 1):
			print("no feature with given number available!")
			exit(-3)

		fe = FeatureExtractor()
		fe.getFeaturesFromFile(path_to_file, 20)

		for feature in features:
			file_feature = int(feature)
			if file_feature == 1:
				result = fe.average_word_length_per_sentence
			if file_feature == 2:
				result = fe.words_per_sentence
			if file_feature == 3:
				result = fe.length_per_sentence
			if file_feature == 4:
				result = fe.richness_per_sentence
			if file_feature == 5:
				result = fe.richness_per_x_words
			if file_feature == 6:
				result = fe.richness_per_sentence_stemmed
			if file_feature == 7:
				result = fe.richness_per_x_words_stemmed
			if file_feature == 8:
				sentiment_flag = 1
				result = fe.sentiment_per_sentence
				result_1 = []
				result_2 = []
				result_3 = []
				for i in result:
					tmp_result_1 = []
					tmp_result_2 = []
					tmp_result_3 = []
					for item in i:
						tmp_result_1.append(item["neg"])
						tmp_result_2.append(item["neu"])
						tmp_result_3.append(item["pos"])
					result_1.append(tmp_result_1)
					result_2.append(tmp_result_2)
					result_3.append(tmp_result_3)
				result_dict[str(filename[:-4]) + " Neg" + str(feature) + ".png"] = result_1
				result_name_list.append(str(filename[:-4]) + " Neg" + str(feature) + ".png")
				result_dict[str(filename[:-4]) + " Neu" + str(feature) + ".png"] = result_2
				result_name_list.append(str(filename[:-4]) + " Neu" + str(feature) + ".png")
				result_dict[str(filename[:-4]) + " Pos" + str(feature) + ".png"] = result_3
				result_name_list.append(str(filename[:-4]) + " Pos" + str(feature) + ".png")
				continue

			if file_feature == 9:
				result = fe.digit_count_per_sentence

			#if len(result) < 20:
			#	result.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
			result_dict[str(filename[:-4]) + str(feature) + ".png"] = result
			result_name_list.append(str(filename[:-4]) + str(feature) + ".png")

	# handle image creation
	tmp_idx = 0
	for name in result_dict:
		data = result_dict[name]
		df = pd.DataFrame(data, columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"])
		sns.heatmap(df, annot=False, cmap="viridis", cbar=True)
		#if os.path.isfile("img/" + name):
			#sns.heatmap.clf()
			#continue
		global suptitles
		plt.suptitle(result_name_list[tmp_idx][:-5] + " " + suptitles[int(name[-5])])
		tmp_idx += 1
		sentiment_flag = 0
		plt.savefig("img/" + name)
		plt.clf()

	return result_dict


class FeatureExtractor(object):
	exclude_stop_words = 		True
	stem_words = 				True
	filter_integers = 			True
	exclude_duplicates =		True

	ps = None

	average_word_length_per_sentence = None
	words_per_sentence = None
	length_per_sentence = None
	richness_per_sentence = None
	richness_per_x_words = None
	richness_per_sentence_stemmed = None
	richness_per_x_words_stemmed = None
	sentiment_per_sentence = None
	digit_count_per_sentence = None

	def __init__(self, exclude_stop_words = False, stem_words = False, filter_integers = False, exclude_duplicates = False):
		self.exclude_stop_words = exclude_stop_words
		self.stem_words = stem_words
		self.filter_integers = filter_integers
		self.exclude_duplicates = exclude_duplicates

		self.ps = PorterStemmer()
		
	def removeDuplicates(self, text):
		return list(dict.fromkeys(text.split()))

	def removeStopWords(self, text):
		result = []

		word_tokens = word_tokenize(text)

		stop_words = set(stopwords.words('english'))

		for word in word_tokens:
			if word not in stop_words:
				result.append(word)
		return result

	def getAverageWordLengthPerSentence(self, text):
		result = []
		word_len = 0
		word_count = 0

		tokens = self.tokenize(text)

		for sentence in tokens:
			sentence = sentence.replace("\n", " ")
			tokens = self.tokenize(sentence)
			for word in tokens:
				# punctuations arent words
				if not word in punctuations: 
					word_count += 1
					word_len += len(word)
			# remove divide by 0
			result.append(0 if word_count == 0 else word_len / word_count)
			word_len = 0
			word_count = 0
		return result

	def getAverageWordLengthPerXWords(self, text, x):
		result = []
		word_len = 0
		word_count = 0

		tokens = self.tokenize(text)

		for word in tokens:
			# punctiations arent words
			if not word in punctuations:
				word_count += 1
				word_len += len(word)
			# every x words, add average length of words until then
			if word_count == x:
				result.append(0 if word_count == 0 else word_len / x)
				word_len = 0
				word_count = 0
		# add average words of remainder of words
		result.append(0 if word_count == 0 else word_len / word_count)

		return result

	def getAmountOfWordsInSentencesAndSentenceLength(self, text):
		result1 = [] # amount of words in sentence
		result2 = [] # length of sentence (character-wise)
		sentence_length = 0
		word_count = 0

		tokens = sent_tokenize(text)

		for sentence in tokens:
			sentence = sentence.replace("\n", " ")
			word_tokens = self.tokenize(sentence)
			for word in word_tokens:
				# punctuations arent words
				if not word in punctuations:
					word_count += 1
					sentence_length += len(word)
			result1.append(0 if word_count == 0 else word_count)
			result2.append(0 if word_count == 0 else sentence_length)
			word_count = 0 
			sentence_length = 0

		return result1, result2

	def getRichnessPerSentence(self, text):
		result = []
		richness = 0
		word_stems = []

		tokens = sent_tokenize(text)

		for sentence in tokens:
			sentence = sentence.replace("\n", " ")
			word_tokens = self.tokenize(sentence)
			for word in word_tokens:
				# punctuations arent words
				if not word in punctuations:
					if not word in word_stems:
						richness += 1
						word_stems.append(word)
			result.append(richness)
			word_stems = []
			richness = 0
		return result

	def getRichnessPerXWords(self, text, x):
		result = []
		richness = 0
		word_count = 0
		word_stems = []

		tokens = sent_tokenize(text)

		for sentence in tokens:
			sentence = sentence.replace("\n", " ")
			word_tokens = self.tokenize(sentence)
			for word in word_tokens:
				# punctiations arent words
				if not word in punctuations:
					word_count += 1
					if not word in word_stems:
						richness += 1
						word_stems.append(word)
				# every x words, append richness of X words
				if word_count == x:
					result.append(richness)
					richness = 0
					word_count = 0
					word_stems = []
		result.append(richness)

		return result

	def getSentimentPerSentence(self, text):
		result = []

		tokens = sent_tokenize(text)
		sentiment_analyzer = SentimentIntensityAnalyzer()

		for sentence in tokens:
			sentence = sentence.replace("\n", " ")
			result.append(sentiment_analyzer.polarity_scores(sentence))
		return result

	def getDigitCountPerSentence(self, text):
		result = []
		digit_count = 0

		tokens = sent_tokenize(text)

		for sentence in tokens:
			sentence = sentence.replace("\n", "")
			word_tokens = self.tokenize(sentence)
			for word in word_tokens:
				# punctuations arent words
				if not word in punctuations:
					for char in word:
						if char.isdigit():
							digit_count += 1
			result.append(digit_count)
		return result

	# Helper functions
	def tokenize(self, text):
		if self.stem_words:
			text = self.ps.stem(text)
		if self.exclude_duplicates:
			text = self.removeDuplicates(text)
		if self.exclude_stop_words:
			text = self.removeStopWords(text)
		else:
			text = word_tokenize(text)

		return text

	def chunkList(self, n, array):
		avg = len(array) / float(n * n)
		result = []
		row = []
		last = 0.0

		while last < len(array):
			tmp = array[int(last):int(last + avg)]
			row.append(0 if not tmp else round(sum(tmp)/len(tmp), 2))
			if len(row) == n and (last + avg) < len(array):
				result.append(row)
				row = []
			last += avg
		if len(result) == 19:
			result.append(row)

		return result

	def chunkDict(self, n, array):
		avg = len(array) / float(n * n)
		result = []
		row = []
		last = 0.0

		while last < len(array):
			tmp = array[int(last):int(last + avg)]
			tmpdict = {}
			neg = 0.0
			neu = 0.0
			pos = 0.0
			compound = 0.0

			for d in tmp:
				neg += list(d.values())[0]
				neu += list(d.values())[1]
				pos += list(d.values())[2]
				compound += list(d.values())[3]

			tmpdict['neg'] = round(neg / len(tmp), 2)
			tmpdict['neu'] = round(neu / len(tmp), 2)
			tmpdict['pos'] = round(pos / len(tmp), 2)
			tmpdict['compound'] = round(compound / len(tmp), 2)

			row.append(tmpdict)
			if len(row) == n and (last + avg) < len(array):
				result.append(row)
				row = []
			last += avg
		if len(result) == 19:
			result.append(row)
		return result

	def getFeaturesFromFile(self, file, n = -1):
		# read file and extract sentences (clumped together)
		f = open(file, "r")
		text = f.read().replace("-\r\r", "").replace("-\n", "")
		f.close()

		self.average_word_length_per_sentence = self.getAverageWordLengthPerSentence(text)

		self.average_word_length_per_x_words = self.getAverageWordLengthPerXWords(text, 100)

		self.words_per_sentence, self.length_per_sentence = self.getAmountOfWordsInSentencesAndSentenceLength(text)

		self.richness_per_sentence = self.getRichnessPerSentence(text)

		self.richness_per_x_words = self.getRichnessPerXWords(text, 100)

		self.stem_words = True
		self.richness_per_sentence_stemmed = self.getRichnessPerSentence(text)
		self.richness_per_x_words_stemmed = self.getRichnessPerXWords(text, 100)
		self.stem_words = False

		self.sentiment_per_sentence = self.getSentimentPerSentence(text)

		self.digit_count_per_sentence = self.getDigitCountPerSentence(text)
		if n != -1:
			print(f"Dividing into {n}x{n} matrix!")
			self.average_word_length_per_sentence = self.chunkList(n, self.average_word_length_per_sentence)
			self.average_word_length_per_x_words = self.chunkList(n, self.average_word_length_per_x_words)
			self.words_per_sentence = self.chunkList(n, self.words_per_sentence)
			self.length_per_sentence = self.chunkList(n, self.length_per_sentence)
			self.richness_per_sentence = self.chunkList(n, self.richness_per_sentence)
			self.richness_per_x_words = self.chunkList(n, self.richness_per_x_words)
			self.richness_per_sentence_stemmed = self.chunkList(n, self.richness_per_sentence_stemmed)
			self.richness_per_x_words_stemmed = self.chunkList(n, self.richness_per_x_words_stemmed)
			self.sentiment_per_sentence = self.chunkDict(n, self.sentiment_per_sentence)
			self.digit_count_per_sentence = self.chunkList(n, self.digit_count_per_sentence)

def main():
	# handleing command line arguments:
	if len(sys.argv) <= 2:
		print("Call with arg1=NameStringOfFile, arg2=FeatureNumber(1-8)")
		exit(-1)

	file_name = sys.argv[1]
	file_feature = int(sys.argv[2])

	platform_name = platform.system();
	if platform_name == "Darwin":
		data_path = os.getcwd()[:-3] + "/data"
	if platform_name == "Windows":
		data_path = os.getcwd()[:-3] + "\\data"

	path_to_file = ""
	for x in os.walk(data_path):
		for y in glob.glob(os.path.join(x[0], file_name)):
			path_to_file = y

	if path_to_file == "":
		print("no file with given name found!")
		exit(-2)

	if (file_feature > 8) and (file_feature < 1):
		print("no feature with given number available!")
		exit(-3)
	
	fe = FeatureExtractor()
	fe.getFeaturesFromFile(path_to_file, 20)

	if file_feature == 1:
		print(fe.average_word_length_per_sentence)
	if file_feature == 2:
		print(fe.words_per_sentence)
	if file_feature == 3:
		print(fe.length_per_sentence)
	if file_feature == 4:
		print(fe.richness_per_sentence)
	if file_feature == 5:
		print(np.array(fe.richness_per_x_words).shape)
	if file_feature == 6:
		print(fe.richness_per_sentence_stemmed)
	if file_feature == 7:
		print(fe.richness_per_x_words_stemmed)
	if file_feature == 8:
		print(fe.sentiment_per_sentence)
	if file_feature == 9:
		print(np.array(fe.digit_count_per_sentence).shape)

if __name__ == "__main__":
	main()
