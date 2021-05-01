import random
import player

'''
get_val assigns value to each card by adding the numerical value of the card with 0(b) or 0.5(w) depending on which color block it is. 
In case of a joker, it calls the joker_handler method to let the player decide which color card it is.
'''
def get_val(card):
	# Joker handling: if the card is joker, ignore the first letter, which is j.
	if card[0] == 'j':
		color = 0 if card[1] == 'b' else 0.5
		val = int(card[2:])
	else:
		color = 0 if card[0] == 'b' else 0.5
		val = int(card[1:])
	return color + val

def init_state(num_p):
    # Initial state of remaining deck
	rem_deck = ['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','b10','b11','w0','w1','w2','w3','w4','w5','w6','w7','w8','w9','w10','w11','jb','jw']
    # Different initial number of cards given to each player depending on the # of players
	num_cards = 3 if num_p == 4 else 4
    # player_card[i] => list of cards ith player has
	player_cards = [[0] * num_cards] * num_p
	players = []
    # shuffling the deck
	random.shuffle(rem_deck)
	for i in range(num_p):
		print('Player ' + str(i) + ' is drawing initial set of cards.')
        # each player draws a set of cards from the deck
		player_cards[i] = [rem_deck.pop(0) for j in range(num_cards)]
		# becomes a player
		player_i = player.Player(player_cards[i], i + 1)
		print(player_i.cards)
		# check for joker and sort the cards afterward
		player_i.joker_handler()
		# sort ith player's cards according to the game's rule
		player_i.cards.sort(key = get_val)
		# append it to players
		players.append(player_i)
	return [rem_deck, players]

def show_all(me, players):
	for p in players:
		if me == p: me.show_to_self()
		else: p.show_to_others()
        
'''
	[turn] method simulates a player's turn in the following manner:
	
	1. If [curr_player] wants to guess, it checks whether the target_player is still in play and compares the [target_player]'s card with [pos] and [card]
	-- If all returns True, the turn method prints the new_state and returns True
	2. If one of the three things laid out fails, the [new_card] is incorporated into [curr_player]'s deck. Then,
		a. if [guess] was False,
			- prints skipped
		b. if anything else,
			- prints guessed wrong, shows the [new_card] to all other players
	   	--> prints all cards, then retuns False

'''
def turn(players, curr_player, new_card, guess, target_player, pos, card):
	# if the curr_player wants to guess, the target_player is not over, and if guess was successful(guessed_by_other handles updating shown_cards) 
	if guess and not (target_player.is_over()) and target_player.guessed_by_other(pos,card):  
		print('\n' + 'Guessed Right!') 
		show_all(curr_player, players) 
		return True  
	else:
		# if skipped or guessed wrong
		new_card_pos = curr_player.incorporate_card(new_card) # add new_card into curr_player's cards(sorted now) 
		curr_player.not_yet_mine = None #the card is now fully curr_player's card
		if not guess: #if didn't guess, the player skipped
			print('\n' + "skip")
		else:
			print('\n' + 'Guessed Wrong!')
			curr_player.guessed_by_other(new_card_pos, new_card) # show the card
		show_all(curr_player, players)
		return False

'''
	[draw_cards] pops a card from [deck] and appends it to [player].cards
	and then sets [player].not_yet_mine gets the new_card
'''
def draw_card(deck, player):
	new_card = deck.pop(0)
	player.cards.append(new_card)
	if player.joker_handler(): new_card = player.cards[-1] # if the new cards was a joker, it handles it and then new_card gets the newly assigned value
	player.not_yet_mine = new_card
	return new_card
