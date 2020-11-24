import numpy as np
import nltk
import sys
import os
import glob
from nltk.tokenize import sent_tokenize, word_tokenize, TextTilingTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

punctuations = [",", ".", ":", ";", "(", ")", "[", "]", "{", "}"]

in_file = "./Julius Caesar.txt"


# ==================================================================
#                          IMPORTANT
# ==================================================================
#nltk.download() # downloads NLTK library if not previously installed
# uncomment line 16 to download NLTK library
# ==================================================================





class FeatureExtractor(object):
	exclude_stop_words = 		True
	stem_words = 				True
	filter_integers = 			True
	exclude_duplicates =		True
	avg_word_len_per_sentence = True
	sentence_length = 			True
	avg_word_len_per_x_words = 	True
	avg_word_len_per_x_sent = 	True
	richness_per_x_words = 		True
	richness_per_x_sent = 		True
	sentiment = 				True
	digit_count_per_x_words = 	True
	digit_count_per_x_sent = 	True
	ps = None

	average_word_length_per_sentence = None
	words_per_sentence = None
	length_per_sentence = None
	richness_per_sentence = None
	richness_per_x_words = None
	richness_per_sentence_stemmed = None
	sentiment_per_sentence = None
	digit_count_per_sentence = None

	def __init__(self, exclude_stop_words = False, stem_words = False, filter_integers = False, exclude_duplicates = False, avg_word_len_per_sentence = False, sentence_length = False, avg_word_len_per_x_words = False, avg_word_len_per_x_sent = False, sentiment = False, digit_count_per_x_words = False, digit_count_per_x_sent = False):
		self.exclude_stop_words = exclude_stop_words
		self.stem_words = stem_words
		self.filter_integers = filter_integers
		self.exclude_duplicates = exclude_duplicates
		self.avg_word_len_per_sentence = avg_word_len_per_sentence
		self.sentence_length = sentence_length
		self.avg_word_len_per_x_words = avg_word_len_per_x_words
		self.avg_word_len_per_x_sent = avg_word_len_per_x_sent
		self.sentiment = sentiment
		self.digit_count_per_x_words = digit_count_per_x_words
		self.digit_count_per_x_sent = digit_count_per_x_sent

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

	def getFeaturesFromFile(self, file):
		# read file and extract sentences (clumped together)
		f = open(file, "r")
		text = f.read().replace("-\r\r", "").replace("-\n", "")
		f.close()

		self.average_word_length_per_sentence = self.getAverageWordLengthPerSentence(text)

		self.average_word_length_per_x_words = self.getAverageWordLengthPerXWords(text, 100)

		self.words_per_sentence, self.length_per_sentence = self.getAmountOfWordsInSentencesAndSentenceLength(text)

		self.richness_per_sentence = self.getRichnessPerSentence(text)

		self.stem_words = True
		self.richness_per_sentence_stemmed = self.getRichnessPerSentence(text)
		self.stem_words = False

		self.sentiment_per_sentence = self.getSentimentPerSentence(text)

		self.digit_count_per_sentence = self.getDigitCountPerSentence(text)

def main():
	# handleing command line arguments:
	if len(sys.argv) <= 1:
		print("Call with Name of file as string")
		exit(-1)

	file_name = sys.argv[1]
	data_path = os.getcwd()[:-3] + "\\data"

	path_to_file = ""
	for x in os.walk(data_path):
		for y in glob.glob(os.path.join(x[0], file_name)):
			path_to_file = y

	fe = FeatureExtractor()
	fe.getFeaturesFromFile(path_to_file)

if __name__ == "__main__":
	main()
