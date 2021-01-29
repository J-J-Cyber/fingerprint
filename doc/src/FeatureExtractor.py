class FeatureExtractor(object):
  exclude_stop_words =   True
  stem_words =     True
  filter_integers =   True
  exclude_duplicates =  True

  ps = None

  average_word_length_per_sentence =  None
  words_per_sentence =                None
  length_per_sentence =               None
  richness_per_sentence =             None
  richness_per_x_words =              None
  richness_per_sentence_stemmed =     None
  richness_per_x_words_stemmed =      None
  sentiment_per_sentence =            None
  digit_count_per_sentence =          None

  def __init__(self, exclude_stop_words = False, \
        stem_words = False,  filter_integers = False, 
        exclude_duplicates = False):
    self.exclude_stop_words = exclude_stop_words 
    self.stem_words = stem_words 
    self.filter_integers = filter_integers
    self.exclude_duplicates = exclude_duplicates

    self.ps = PorterStemmer()