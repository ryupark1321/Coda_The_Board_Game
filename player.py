import gameengine

class Player:
	def __init__(self, cards, num):
		self.cards = cards
		self.shown_cards = dict()
		self.num = num
		self.not_yet_mine = None
		self.new_card = None

	def show_to_others(self):
		s = ''
		for c in self.cards:
			to_show = c[0] if c[0] != 'j' else c[1]
			if c == self.not_yet_mine: s += to_show.upper() + ' | '
			elif self.shown_cards.get(c) == None: 
				s += to_show + ' | '
			else: s += c + ' | '
		print('player'+str(self.num)+'\n' + s + '\n')

	def show_to_self(self):
		s = ''
		for c in self.cards: 
			if c == self.not_yet_mine: s += c.upper() + ' | '
			else: s += c + ' | '
		print('player' + str(self.num) + ' (me)\n' + s + '\n')

	def guessed_by_other(player, pos, card):
		if player.cards[pos] == card and (player.shown_cards.get(card) == None): player.shown_cards.update({card: True}); return True
		else: return False

	def incorporate_card(self, new_card):
		# if the card isn't in the deck
		if self.cards.count(new_card) != 0:
			self.cards.sort(key = lambda c : gameengine.get_val(c))
			self.not_yet_mine = None
		return self.cards.index(new_card)	

	def is_over(self):
		return len(self.cards) == len(self.shown_cards)

	def get_joker_val(self):
		return input('What value do you want your joker to be? : ')

	def has_joker(self):
		if self.cards.count('jw') != 0:
			return 'jw'
		elif self.cards.count('jb') != 0:
			return 'jb'
		else: return ''
	
	def where_joker(self, color):
		return self.cards.index(color)
	
	def joker_handler(self):
		color = self.has_joker() # this returns the color of the joker or an empty string, in which case it will move to the else statement
		if color:
			pos = self.where_joker(color)
			self.cards[pos] = color + self.get_joker_val()
			color = self.has_joker() # if there is a second joker, we must check this case.
			if color:
				pos = self.where_joker(color)
				self.cards[pos] = color + self.get_joker_val()
			return True
		else:
			return False
