# generate distractiors
# distractor function: takes a number (correct ans) and generates required number of distractors for that number

import random

# extract terms from the question string
def get_terms(question):
    terms = question.split()
    num1 = int(terms[0])
    num2 = int(terms[-1])
    return [num1, num2]

# off by one distractor function
def off_by_one(question, correct_ans, num_distractors=2):
    if num_distractors > 2:
        raise ValueError("Can only generate up to 2 distractors for off_by_one.")
    distractors = set()
    offsets = [-1, 1]
    random.shuffle(offsets)
    for i in range(num_distractors):
        distractor = correct_ans + offsets[i]
        distractors.add(distractor)
    return list(distractors)

# added wrong place value for second number
def add_wrong_place_value(question, correct_ans, num_distractors=2):
    num1, num2 = get_terms(question)
    print(num1, num2)
    distractors = set()

    # num2 added at wrong place value
    digits_difference = len(str(num1)) - len(str(num2))
    # print(f"{len(str(num2))} - {len(str(num1))} = {digits_difference}")
    for i in range(digits_difference):
        distractors.add(num1 + (num2 * 10**(i+1)))

    return list(distractors)