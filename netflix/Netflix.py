#!/usr/bin/env python3

# ---------------------------
# projects/netflix/Netflix.py
# Copyright (C) 2015
# Glenn P. Downing
# --------------------------- 

import pickle
import os
import json
from pprint import pprint

from urllib.request import urlopen, urlretrieve
from math  import sqrt
from numpy import mean, sqrt, square, subtract

import warnings

# ------------
# netflix_rmse
# ------------

def netflix_rmse (actual_ratings, predicted_ratings) :
    """
    computes the root mean square error of two lists
    returns the floating point value
    """

    warnings.simplefilter("error") # turns warnings into exceptions

    try :
        return sqrt(mean(square(subtract(actual_ratings, predicted_ratings))))
    except :
        # exception could be thrown if either of the lists are empty
        return 0.0

def netflix_rmse_from_dictionary(actual_ratings_dictionary, predicted_ratings_dictionary) :
    """
    convert two dictionaries into lists, then compute the rmse
    actual_ratings_dictionary dictionary with correct answers
    predicted_ratings_dictionary dictionary with predicted answers
    return the rmse value (int/float)
    """
    actual_ratings_list    = []
    predicted_ratings_list = []

    for movie_number in predicted_ratings_dictionary :

        for user_number in actual_ratings_dictionary[movie_number] :
            actual_ratings_list    += [user_number,]

        for user_number in predicted_ratings_dictionary[movie_number] :
            predicted_ratings_list += [user_number,]

    return netflix_rmse(actual_ratings_list, predicted_ratings_list)

# ------------
# netflix_read
# ------------

def netflix_read (input_stream) :
    """
    read from stream, build dictionary object
    input_stream the input
    return a dictionary object
    """

    dictionary_result = {}
    movie_number = 0

    for current_line in input_stream :
        if ':' in current_line : # contains a movie title
            movie_number = int(current_line[:-2]) # remove last two characters :\n
            dictionary_result[movie_number] = ()
        else :
            if '\n' in current_line :
                current_line = current_line[:-1] # remove last character \n
            dictionary_result[movie_number] += (int(current_line),)

    return dictionary_result

# ----------------------
# netflix_get_heuristics
# ----------------------

# def netflix_get_heuristics (user_number, movie_number, average_movie_rating, average_user_rating, movie_decades, user_decades) :
#     """
#     computes averages of various ratings which are used to compute final guess
#     user_number the customer's ID number
#     movie_number the movie's ID number
#     average_movie_rating the movie's average rating given by all customers
#     average_user_rating the average rating given to any movie by this particular customer
#     movie_decades dictionary detailing which movie is from which decade
#     user_decades the average rating given by a user to movies in a given decade
#     return the max cycle length of the range [input_dictionary, j]
#     """

#     return_value = [average_movie_rating[str(movie_number)], average_user_rating[str(user_number)]]

#     try :
#         # if customer hasn't rated a movie from that era, it will raise a keyerror
#         decade = movie_decades[str(movie_number)]
#         this_dict = user_decades.get(str(user_number))
#         count = this_dict.get(str(decade)).get('count')
#         total = this_dict.get(str(decade)).get('total')
#         average = float(total)/count
#         return_value += [average]
#     except :
#         pass

#     return return_value

# ------------
# netflix_eval
# ------------

def netflix_eval (input_dictionary) :
    """
    reads the input, creates a new dictionary populated with guesses
    input_dictionary the dictionary holding the input values
    return the dictionary of guesses
    """

    # load the cache files

    urlretrieve("http://www.cs.utexas.edu/~ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json", "BRG564-Average_Movie_Rating_Cache.json")

    with open('BRG564-Average_Movie_Rating_Cache.json') as data_file:    
        average_movie_rating = json.load(data_file)

    urlretrieve("http://www.cs.utexas.edu/~ebanner/netflix-tests/ezo55-Average_Viewer_Rating_Cache.json", "ezo55-Average_Viewer_Rating_Cache.json")
    
    with open('ezo55-Average_Viewer_Rating_Cache.json') as data_file:    
        average_user_rating = json.load(data_file)

    urlretrieve("http://www.cs.utexas.edu/~ebanner/netflix-tests/pra359-Movie_Decades_Cache.json", "pra359-Movie_Decades_Cache.json")
    
    with open('pra359-Movie_Decades_Cache.json') as data_file:    
        movie_decades = json.load(data_file)

    urlretrieve("http://www.cs.utexas.edu/~ebanner/netflix-tests/drc2582-customer_decade_dict.json", "drc2582-customer_decade_dict.json")
    
    with open('drc2582-customer_decade_dict.json') as data_file:    
        user_decades = json.load(data_file)

    predictions_dictionary = {}

    for movie_number in input_dictionary :
        # initialize the dictionary entry
        predictions_dictionary[movie_number] = ()

        # iterate over users, filling in the predicted ratings
        for user_number in input_dictionary[movie_number] :
            
            # create list of estimation heuristics

            heuristics_list = [average_movie_rating[str(movie_number)], average_user_rating[str(user_number)]]

            try :
                # if customer hasn't rated a movie from that era, it will raise a keyerror
                decade = movie_decades[str(movie_number)]
                this_dict = user_decades.get(str(user_number))
                count = this_dict.get(str(decade)).get('count')
                total = this_dict.get(str(decade)).get('total')
                average = float(total)/count
                heuristics_list += [average]
            except :
                pass

            # use heuristics to predict rating
            predicted_rating = mean(heuristics_list)

            # place the prediction into the predictions_dictionary
            predictions_dictionary[movie_number] += (predicted_rating,)

    return predictions_dictionary

# -------------
# netflix_print
# -------------

def netflix_print (output_stream, output_dictionary, rmse_value) :
    """
    print the guess dictionary and rmse
    output_stream a writer
    output_dictionary the dictionary to output
    rmse_value the rmse value
    """

    for movie_number in output_dictionary :
        # write the movie number
        output_stream.write(str(movie_number) + ":\n")

        for rating in output_dictionary[movie_number] :
            # write the user rating
            output_stream.write("%.1f" % rating + "\n")

    # write the RMSE
    output_stream.write("RMSE: %.2f" % rmse_value + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (input_stream, output_stream) :
    """
    input_stream a reader
    output_stream a writer
    """

    # parse dictionary from input
    input_dictionary = netflix_read(input_stream)

    # acquire dictionary of predicted ratings
    predictions_dictionary = netflix_eval(input_dictionary)

    urlretrieve("http://www.cs.utexas.edu/users/ebanner/netflix-tests/jmt3675-probe_solution.txt", "jmt3675-probe_solution.txt")

    solutions_file = open('./jmt3675-probe_solution.txt')
    solutions_dictionary = netflix_read(solutions_file)
    solutions_file.close()

    # calculate rmse
    rmse_value = netflix_rmse_from_dictionary(solutions_dictionary, predictions_dictionary)

    # print the results
    netflix_print(output_stream, predictions_dictionary, rmse_value)



