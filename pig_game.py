#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""week 7"""
import random
import time
import argparse


class Die(object):
    """ Object for a Die (single dice)"""
    def __init__(self, sides):
        self.sides = sides
    def roll(self, seed):
        random.seed(seed)
        rando_roll = random.randint(1,self.sides)
        # game logic
        if rando_roll == 1:
            rando_roll = -1
        return rando_roll

class Player(object):
    def __init__(self):
        self.players = []
    def create_player_list(self, num_of_players):
        start_score = 0 # starting score is always zero for everyone
        for x in range(num_of_players):
            self.players.append(start_score)
    def return_player_list(self):
        return self.players
    def update_player_score(self, player_position, result):
        self.players[player_position] += result
        return self.players[player_position]

class Game (object):
    """ Object for the stage of a game"""
    def __init__(self, sides):
        self.game_die = Die(sides)
        self.game_players = Player()
    def roll(self, seed):
        return self.game_die.roll(seed)
    def create_player_list(self,num_of_players):
        self.game_players.create_player_list(num_of_players)
    def return_player_list(self):
        return self.game_players.return_player_list()
    def update_player_score(self, player_position, result):
        return self.game_players.update_player_score(player_position, result)

def game_loop(games,num_of_players,winning_score):
    """The loop of the game for single game

    Args:
        games (Class): Instance of class Game
        num_of_players (int): the number of player in this game
        winning_score (int): The score that determines a winner

    Attributes:
        updated_score (int): the current score of the player after each hold
        game_continue (bool): controls game loop

    Returns:

    Examples:
    """
    updated_score = 0
    game_continue = True

    # Assign player list
    games.create_player_list(num_of_players)

    # Game Loop
    while game_continue:
        # cycle between players
        for player_position in range (num_of_players):
            print "\nPlayer {} Turn".format(player_position + 1)

            # Clear temp score each round
            temp_score = 0

            # Turns loop
            while True:
                # User input
                user_input = raw_input("Enter (r)ole or (h)old:")

                # roll dice, get value
                if user_input == "r":
                    # roll dice using class Game.roll with random seed (time)
                    roll_result = games.roll(time.time())
                    # if roll a 1 end Turns for this player
                    if roll_result < 0:
                        print "\nPlayer {} rolled a 1. End turn.".format((player_position + 1))
                        break
                    # continue game logic
                    else:
                        print "Player {} rolled a {}".format((player_position + 1),roll_result)
                        # incriment temp score
                        temp_score += roll_result

                # hold dice and bank temp score
                elif user_input == "h":
                    print "Player {} Holds".format((player_position + 1))
                    # assign value to score using class Game
                    updated_score = games.update_player_score((player_position),temp_score)
                    break

                else:
                    print "Whoops! Enter correct selection (r or h)"

            print "Score List:",games.return_player_list()

            # determine if a winner
            if updated_score >= winning_score:
                print 'Player {} wins!'.format(player_position + 1)
                game_continue = False
                break


def input_int(question):
    """Function to ask a int question

    Args:
        question (string): the question to ask user

    Attributes:

    Returns:
        Returns int from user
    Examples:
    """
    while True:
        try:
            value = int(input(question))
        except (SyntaxError, NameError) as exception:
            print("Invalid entry. Try again.")
            continue

        if value <= 0:
            print("Invalid entry. Try again.")
            continue
        else:
            break

    return value


def main():
    """Main function that runs at start of program.

    Args:
        --numPlayers (int): number of players in each game

    Attributes:
        winning_score (int): the score to determine a winner
        counter (int): counter
        game_state_list (list): a list of games

    Returns:

    Examples:
        >>> $ python pig_game.py --numPlayers 3
        >>> How many games do you want to play?: 1
        Starting Game 1

        Player 1 Turn
        Enter (r)ole or (h)old:r
    """
    winning_score = 100
    counter = 1
    game_state_list = []

    # Enable command-line arguments
    parser = argparse.ArgumentParser()
    # Add command-line argmuemnt
    parser.add_argument('--numPlayers', type=int)
    args =  parser.parse_args()

    # Get number of games from user input
    num_of_games = input_int("How many games do you want to play?: ")

    # Get number of players in each game
    for x in range(num_of_games):
        # Note. Use this commented code below if you want to also let the user define the number of players in each game
        #game_state_list.append((Game(6) ,(input_int("How many players in Game {}?: ".format((x + 1))))))

        # list of tuples (Game class instnace, num_of_plauyers)
        game_state_list.append((Game(6) ,args.numPlayers))

    # Play all games. Note that the games are not aware of each other
    for game_state, num_users in game_state_list:
        print "\nStarting Game",counter
        game_loop(game_state,num_users,winning_score)
        counter += 1

    print "Completed all the games!"


# Run main if file direcrly executed
if __name__ == '__main__':
    main()
