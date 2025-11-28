Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

...     def __len__(self):
...         return len(self._cards)
... 
...     def __getitem__(self, position):
...         return self._cards[position]
... 
SyntaxError: multiple statements found while compiling a single statement
>>> import collections
>>> Card = collections.namedtuple('Card', ['rank', 'suit'])
>>> class FrenchDeck:
...     ranks = [str(n) for n in range(2, 11)] + list('JQKA')
...     suits = 'spades diamonds clubs hearts'.split()
... 
...     def __init__(self):
...         self._cards = [Card(rank, suit) for suit in self.suits
...                                         for rank in self.ranks]
... 
...     def __len__(self):
...         return len(self._cards)
... 
...     def __getitem__(self, position):
...         return self._cards[position]
... 
...     
>>> beer_card = Card('7', 'diamonds')
>>> beer_card
Card(rank='7', suit='diamonds')
>>> deck = FrenchDeck()
>>> len(deck)
52
>>> deck[0]
Card(rank='2', suit='spades')
>>> str(n) for n in range(2, 11)
SyntaxError: invalid syntax
>>> ranks = [str(n) for n in range(2, 11)] + list('JQKA')
>>> ranks
['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
>>> [str(n) for n in range(2, 11)]
['2', '3', '4', '5', '6', '7', '8', '9', '10']
>>> ['A' + str(n) for n in range(2, 11)]
['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
