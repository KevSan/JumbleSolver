import json
import enchant
import os
from pyspark import SparkContext
from pytrends.request import TrendReq

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
freq_file = os.path.join(THIS_FOLDER, 'freq_dict.json')


enchant_dict_global = enchant.Dict()
freq_dict_global = dict()

with open(freq_file, 'r') as fp:
    freq_dict_global = json.load(fp)


def solve_jumble_puzzle(jumble_puzzle_list):

    chars_for_final_puzzle = get_circled_chars_list(jumble_puzzle_list[0])

    all_possible_solutions = []
    for str in chars_for_final_puzzle:
        possible_solutions(jumble_puzzle_list[1], 0, str, [], all_possible_solutions)

    final_solution = get_final_answer(all_possible_solutions)

    return final_solution


#returns a list of all possible strings that can be used to solve the final puzzle
def get_circled_chars_list(scrambled_words_dict):

    all_unscrambled_words = all_possible_words(scrambled_words_dict)

    strings_of_circled_chars = []
    all_possible_circled_char_strs(all_unscrambled_words, 0, [], strings_of_circled_chars)

    return strings_of_circled_chars


def all_possible_words(scrambled_words):

    all_unscrambled_words = []

    for str in scrambled_words:
        current_word_solutions_set = set()
        unscramble_word(list(str), 0, len(str), current_word_solutions_set)

        word_solutions_dict = dict()
        for word in current_word_solutions_set:
            word_solutions_dict[word] = scrambled_words[str]

        all_unscrambled_words.append(word_solutions_dict)

    return all_unscrambled_words


def unscramble_word(scrambled_chars, starting_index, end_index, possible_word_set):

    if starting_index == end_index:
        possible_word = "".join(scrambled_chars)

        if enchant_dict_global.check(possible_word) and possible_word in freq_dict_global:
            possible_word_set.add(possible_word)

    else:
        for i in range(starting_index, end_index):
            scrambled_chars[starting_index], scrambled_chars[i] = scrambled_chars[i], scrambled_chars[starting_index]
            unscramble_word(scrambled_chars, starting_index + 1, end_index, possible_word_set)
            scrambled_chars[starting_index], scrambled_chars[i] = scrambled_chars[i], scrambled_chars[starting_index]


def all_possible_circled_char_strs(all_unscrambled_words, starting_index, possible_circled_chars, list_of_str):

    #print(all_unscrambled_words)
    if starting_index == len(all_unscrambled_words):
        list_of_str.append("".join(possible_circled_chars))
    else:
        for key in all_unscrambled_words[starting_index]:
            curr_list = []
            for index in all_unscrambled_words[starting_index][key]:
                curr_list.append(key[index])
            curr_list.extend(possible_circled_chars)
            all_possible_circled_char_strs(all_unscrambled_words, starting_index+1, curr_list, list_of_str)


def str_combo_of_len_k(str_combo_list, curr_str, left, k, str):

    if k == 0:
        str_combo_list.append("".join(curr_str))

    else:
        for i in range(left, len(str)):
            curr_str.append(str[i])
            str_combo_of_len_k(str_combo_list, curr_str, i + 1, k - 1, str)
            curr_str.pop()


def dict_of_char_count(str):
    strDict = dict()

    for char in str:
        if char in strDict:
            strDict[char] += 1
        else:
            strDict[char] = 1

    return strDict


def remove_chars_from_dict(str, strDict):
    for char in str:
        if strDict[char] == 1:
            strDict.pop(char)
        else:
            strDict[char] -= 1


def create_str_from_dict(strDict):
    currWord = []

    for key in strDict:
        tempList = [key] * strDict[key]
        currWord.extend(tempList)

    return "".join(currWord)


def possible_solutions(solution_word_lengths, index, str_of_circled_chars, curr_solution, all_solutions):

    if index == len(solution_word_lengths):
        #curr_str = ' '.join(word for word in curr_solution)
        #all_solutions.append(curr_str)
        all_solutions.append(curr_solution)

    else:
        combo_list = []
        str_combo_of_len_k(combo_list, [], 0, solution_word_lengths[index], str_of_circled_chars)

        combo_dict = set()
        for combo in combo_list:
            unscramble_word(list(combo), 0, len(combo), combo_dict)

        for word in combo_dict:
            temp_answer = []
            temp_answer.extend(curr_solution)
            temp_answer.append(word)

            temp_dict = dict_of_char_count(str_of_circled_chars)

            remove_chars_from_dict(word, temp_dict)

            temp_str = create_str_from_dict(temp_dict)
            possible_solutions(solution_word_lengths, index+1, temp_str, temp_answer, all_solutions)


def get_final_answer(all_possible_solutions):

    sc = SparkContext("local", "Filter app")
    all_solutions_rdd = sc.parallelize(all_possible_solutions)

    zeros_filterd_out_rdd = all_solutions_rdd.filter(phrase_not_mostly_zeroes)
    good_scoring_phrases_rdd = zeros_filterd_out_rdd.filter(phrase_scores_well)

    string_rdd = good_scoring_phrases_rdd.map(lambda a: " ".join(a))

    g_trend_score_rdd = string_rdd.map(lambda a: google_trend_score_of_phrase(a))


    g_trends = g_trend_score_rdd.collect()

    g_trends.sort(key = lambda x: x[1], reverse=True)


    if g_trends[0][1] < 200:

        str_phrases = [x[0].split(" ") for x in g_trends]
        str_phrases_rdd = sc.parallelize(str_phrases)
        str_and_freq_score_rdd = str_phrases_rdd.map(lambda a: phrase_and_score_getter(a))
        str_and_freq_list = str_and_freq_score_rdd.collect()

        str_and_freq_list.sort(key=lambda x: x[1])

        return " ".join(str_and_freq_list[0][0])

    else:
        return g_trends[0][0]


def phrase_and_score_getter(phrase):

    return [phrase, phrase_score(phrase)]


def google_trend_score_of_phrase(phrase):

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([phrase], cat=0, timeframe='today 5-y', geo='', gprop='')
    popularity_of_phrase_by_state = pytrends.interest_by_region(resolution='USA')
    popularity_score = popularity_of_phrase_by_state.sum().values[0]

    return [phrase, popularity_score]



def phrase_not_mostly_zeroes(phrase):

    if len(phrase) == 1 or len(phrase) == 2:
        return True

    else:
        num_of_zero_frequencies = 0
        for word in phrase:
            if freq_dict_global[word] == 0:
                num_of_zero_frequencies += 1

        if num_of_zero_frequencies + 1 == len(phrase) or num_of_zero_frequencies == len(phrase):
            return False

        return True


def phrase_score(phrase):

    score = 0
    for word in phrase:
        score+= freq_dict_global[word]

    return score


def phrase_scores_well(phrase):

    score_of_phrase = phrase_score(phrase)

    if score_of_phrase >= 3000:
        return False

    else:
        for word in phrase:
            if freq_dict_global[word] > 1500:
                return False

        return True