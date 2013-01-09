import csv, sys, os
 
thisFile = os.path.abspath(__file__)
thisDir = os.path.dirname(thisFile)
QUOTES_FILEPATH = os.path.join(thisDir, 'data', 'gratitude-quotes.csv')

class Quote:
   def __init__(self, day=None, text=None, author=None):
      self.day = day
      self.text = text
      self.author = author

   def __repr__(self):
      return "Day %s: %s --%s" % (self.day, self.text, self.author)


class Quotes:
   quotes = None
   def __init__(self):
      if Quotes.quotes is None:
         Quotes.quotes = {}
         quotesCsv = csv.reader(open(QUOTES_FILEPATH))
         quotesCsv.next() # skip header line
         for row in quotesCsv:
            day = int(row[0])
            quote = Quote(day=day, text=row[1], author=row[2])
            Quotes.quotes[day] = quote

   def getQuote(self, day):
      try:
         result = Quotes.quotes[day]
      except:
         result = Quote()
      return result

   def getQuotes(self):
      return Quotes.quotes

