import re 

def read_file():
    with open("samplepythonquestions.txt") as x:
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

            if provided_answer == actual_answer: #Correct answer
                print("Correct!")
                del dict_of_qs[parent_key]
            else: #Incorrect answer
                print(f"Incorrect. The correct answer is {actual_answer}.")


def run():
    rawtext = read_file()
    split_by_questions = rawtext.split("\n\n")

    dict_of_qs = {}

    dict_of_qs = assign_qs_to_dicts(split_by_questions, dict_of_qs)
    iterate_through_questions(dict_of_qs)



if __name__ == "__main__":
    run()