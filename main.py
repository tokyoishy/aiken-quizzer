import re 
import os
import sys

def exit_program(message=""):
    print(f"Exiting. {message}")
    sys.exit(0)

def get_list_of_files(dir_to_questions):
    raw_list_of_files = os.listdir(dir_to_questions)
    list_of_files = []
    for file in raw_list_of_files:
        split_name = file.split('.')
        if split_name[len(split_name)-1] == 'txt':
            list_of_files.append(file)
    
    return list_of_files

def check_files_in_dir(dir_to_questions):
    list_of_files = get_list_of_files(dir_to_questions)
    if len(list_of_files) == 0:
        exit_program("There are no files in the given directory")
    print("\nWelcome! Which question file would you like to quiz on?\n")
    question_files = {}
    for index, f in enumerate(list_of_files): # Fill dict with file number and name
        question_files[str(index+1)] = f
        print(f"{index+1}. {f}")
    print("\nAfter answering with the letter option, you can use the following commands:")
    print(":q -> quit\n:d -> don't ask this question again (will do this by default if the answer is correct)\nNo answer will continue to the next question.\n")
    return question_files

def get_file_selection(question_files):
    while True: # Keeps asking until valid question file is selected
        question_file_chosen = input("Enter number of question file: ")
        if question_file_chosen in question_files.keys():
            file_name = question_files[question_file_chosen]
            break
        else:
            print("That was not a valid option. Please input the # associated with the file.")
    return file_name

def read_file(file_name):
    with open(f"question_files/{file_name}") as x:
        rawtext = x.read()

    return rawtext

def assign_qs_to_dicts(split_questions, dict_of_qs):
    for index,value in enumerate(split_questions): # Go through each question (as a str)
        broken_down_q = value.split("\n")
        temp_dict = {}
        temp_dict["Question"] = broken_down_q[0] # The first line of the block should be the question
        answer = broken_down_q[len(broken_down_q)-1].split(" ") # The last line of the block should be the answer
        answer = answer[1]
        temp_dict["Answer"] = answer
        options = broken_down_q[1:len(broken_down_q)-1] # Lines between first and last should be the options
        for k in options:
            if ')' in k: # Either ')' or '.' is used as a postfix to the letter
                split_option = k.split(") ")
            elif '.' in k:
                split_option = k.split(". ")
            else:
                raise Exception("Error")
            option_letter = split_option[0]
            option_q = split_option[1]
            temp_dict[option_letter] = option_q
        dict_of_qs[index] = temp_dict # The dict allows to remove questions if they're answered correctly
    return dict_of_qs

def iterate_through_questions(dict_of_qs):
    mistakes_count = 0
    correct_count = 0
    while len(dict_of_qs) > 0: # As long as we have questions to go thru...
        for parent_key,value in dict_of_qs.copy().items():
            print("\n")
            for key,value in value.items():
                if key != 'Answer':
                    if key == "Question":
                        print(f"{key}: {value}")
                    else:
                        print(f"{key}. {value}")
                else:
                    actual_answer = value
            provided_answer = input("Enter your answer: ")
            if provided_answer == actual_answer:
                print("Correct!")
                correct_count += 1
                del dict_of_qs[parent_key]
            else:
                print(f"Incorrect. The correct answer is {actual_answer}.")
                mistakes_count += 1
            print("Enter choice (:q to quit, :d to ignore this question)")
            post_choice = input("")
            match post_choice:
                case ":q":
                    print("Quitting...")
                    return dict_of_qs, mistakes_count, correct_count
                case ":d":
                    print("I won't ask this again")
                    del dict_of_qs[parent_key]
    return dict_of_qs, mistakes_count, correct_count

def final_summary(dict_of_qs, mistakes_count, correct_count):
    if len(dict_of_qs) == 0:
        print(f"You finished! You had {mistakes_count} mistakes and {correct_count} correct answers.")
    else:
        print(f"You ended early, but you had {mistakes_count} mistakes and {correct_count} correct answers.")


def run():
    question_files = check_files_in_dir("./question_files/")
    file_name = get_file_selection(question_files)

    rawtext = read_file(file_name)
    split_by_questions = rawtext.split("\n\n")

    dict_of_qs = {}
    try:
        dict_of_qs = assign_qs_to_dicts(split_by_questions, dict_of_qs)
    except Exception as e:
        print(f"This file may not be formatted correctly: {e}")
        exit_program()
    dict_of_qs, mistakes_count, correct_count = iterate_through_questions(dict_of_qs)
    final_summary(dict_of_qs, mistakes_count, correct_count)


if __name__ == "__main__":
    run()