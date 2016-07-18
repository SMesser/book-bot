"""Describes the BookManager class and how to parse <book_file>."""
import nltk # for sentence parsing
nltk.download('punkt') # we're only getting the bare minimum of what we need from nltk
book_file = 'book.txt'


class BookManager:
  """Manages a <book_file>, reading and editing it as needed."""

  def __init__(self):
    """Read the raw data from <book_file>."""
    text_file = open(book_file, 'r+')
    text_string = text_file.read()
    text_file.close()
    self._text_string = text_string

  def delete_message(self, message):
    """Delete the message read fromm <book file>."""
    text_file = open(book_file, 'r+')
    text_file.seek(0)
    text_file.write(self.text_without_message(message))
    text_file.truncate()
    text_file.close()

  def first_sentence(self):
    """Find the first sentence in <book_file>."""
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(self._text_string)
    return sentences[0]

  def text_without_message(self, message):
    """Remove <message> from the beginning of <self>._text_string.

    Assumes <message> is actually the beginning of <self>._text_string. If it
    is not, removes a string of length equal to <message> from
    <self>._text_string.
    """

    return self._text_string[len(message):len(self._text_string)]
