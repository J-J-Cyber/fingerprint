import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, TextTilingTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

punctuations = [",", ".", ":", ";", "(", ")", "[", "]", "{", "}"]

in_file = "./Juilius Caesar.txt"


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

	def __init__(self, exclude_stop_words = False, stem_words = False, filter_integers = False, exclude_duplicates = False, avg_word_len_per_sentence = False, sentence_length = False, avg_word_len_per_x_words = False, avg_word_len_per_x_sent = False, richness_per_x_words = False, richness_per_x_sent = False, sentiment = False, digit_count_per_x_words = False, digit_count_per_x_sent = False):
		self.exclude_stop_words = exclude_stop_words
		self.stem_words = stem_words
		self.filter_integers = filter_integers
		self.exclude_duplicates = exclude_duplicates
		self.avg_word_len_per_sentence = avg_word_len_per_sentence
		self.sentence_length = sentence_length
		self.avg_word_len_per_x_words = avg_word_len_per_x_words
		self.avg_word_len_per_x_sent = avg_word_len_per_x_sent
		self.richness_per_x_words = richness_per_x_words
		self.richness_per_x_sent = richness_per_x_sent
		self.sentiment = sentiment
		self.digit_count_per_x_words = digit_count_per_x_words
		self.digit_count_per_x_sent = digit_count_per_x_sent

		self.ps = PorterStemmer()
		
	# Helper functions
	def tokenize(self, text):
		if self.stem_words:
			text = self.ps.stem(text)
		if self.exclude_duplicates:
			text = removeDuplicates(text)
		if self.exclude_stop_words:
			text = filterStopWords(text)
		else:
			text = word_tokenize(text)

		return text

	def removeDuplicates(self, text):
		return list(dict.fromkeys(text.split()))

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


	def getFeaturesFromFile(self, file):
		# read file and extract sentences (clumped together)
		f = open(file, "r")
		text = f.read().replace("-\r\r", "").replace("-\n", "")
		f.close()

		self.average_word_length_per_sentence = self.getAverageWordLengthPerSentence(text)

		self.average_word_length_per_x_words = self.getAverageWordLengthPerXWords(text, 100)

	# average length of words total
	#f_avgwordlen = getAverageWordLength(text)

def main():
	fe = FeatureExtractor()
	fe.getFeaturesFromFile(in_file)

if __name__ == "__main__":
	main()