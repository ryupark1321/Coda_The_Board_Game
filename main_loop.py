import gameengine
while 1:
    # define the numnber of players: Back to having the option of more than two-player game
	num_p = int(input("How many players will be playing the game? \n (choose from   2   |   3   |  4) \n"))
	num_losers = 0
	rem_p = num_p - num_losers # remaining alive player

    # initialize players and remaining deck
	rem_deck, players = gameengine.init_state(num_p)
    # false if ith player is still playing, true if ith player lost and is out of the game
	losers = [False] * num_p
	deck_is_empty = False
	round_counter = 1
	
	while rem_p >= 2: # if there are more than 2 players remaining, the game continues
		for i in range(num_p):
			print('\n\nRound ' + str(round_counter) + '  :  Player ' + str(i + 1) +
                  ' Turn to play')
			print(' '.center(140, '-'))
			curr_player = players[i]
			gameengine.show_all(curr_player, players)
			'''
            if remaining deck is not empty
            - take one tile & place the tile into the lineup
            - guess
                -- succeed => targeted player reveals the tile
                    --> another guess
                    --> pass
                -- failed
                    --> reveal the tile

            if remaining deck is empty
            - guess
                -- succeed => targeted player reveals the tile
                    --> another guess
                    --> pass
                -- failed
                    --> reveal any tile the player wants from the lineup
                
            '''
			if not deck_is_empty:
                # draw a new card from the remaing deck and sort the lineup accordingly
				new_card = gameengine.draw_card(rem_deck, curr_player)
			else:
                # if rem_deck is empty, player must choose a tile to reveal if the guess is wrong
				new_card = input(
                    'which card of yours are you willing to sacrifice? : ')
			gameengine.show_all(curr_player, players)
			guess_is_successful = True
			first_time = True
			while guess_is_successful:
				if first_time:
					first_time = False  # no longer first time guessing
					will_guess = True  # has to guess since it's the first time drawing a new card
				else:
					will_guess = input('will you guess? (y/n) : ') == 'y'
                # had to unindent because if first time, it will guess without defining target_player, pos, and player_guess_card
				if will_guess:
					target_player = int(
                        input(
                            'Which player do you want to target? \n put one digit number for the player \n do not choose someone who is out of the game : '
                        ))
					pos = int(
                        input(
                            "\n Tell us the position of the card you want to guess : (starts from 0) : "
                        ))
					player_guess_card = input(
                        "\n Tell us the card: if black1 then b1 if white 4 then w4 :   \n if joker, put j before w4      "
                    )
                # got rid of the else and break because we stil need to incorporate the new_card if the player wants to skip.
				guess_is_successful = gameengine.turn(
                    players, players[i], new_card, will_guess,
                    players[target_player - 1], pos, player_guess_card)
				if guess_is_successful and players[target_player - 1].is_over(
                ):  # if the guess was successful and the target player has no unshown cards
					losers[target_player - 1] = True  #update losers list --> for the prevention of overkilling an already lost player + finding out the winner
					num_losers += 1  #update number of losers
				if num_losers == num_p - 1:
					break  # if end condition is met break out of for-loop
			if num_losers == num_p - 1:
				break  # if end condition is met break out of for-loop
			deck_is_empty = len(
                rem_deck) == 0  # if not done update deck_is_empty
		round_counter += 1  # round count number goes up
		if num_losers == num_p - 1:
			break
	print('Player ' + str(losers.index(False) + 1) + ' is the winner')
	break
