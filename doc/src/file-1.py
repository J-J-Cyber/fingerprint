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
      # every x words, add average length 
      # of words until then
      if word_count == x:
        result.append(0 if word_count == \
            0 else word_len / x)
        word_len = 0
        word_count = 0
    # add average words of remainder of words
    result.append(0 if word_count == 0 else \
        word_len / word_count)

  return result