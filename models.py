from dataclasses import dataclass
import random

@dataclass
class Question:
    """Data class to track question information."""
    question_text: str
    skill_code: str
    options: list
    answer: int  # 1-4 index indicating the correct answer position
    possible_distractors: list
    correct_option: str = None # will be filled in choose_distractors

    def choose_distractors(self) -> list:
        """
        Choose 3 random distractors from all possible distractors
        and assign them random positions along with the correct answer.
        
        Returns:
            list: A list of 4 options with the correct answer at a random position.
        """
        if len(self.possible_distractors) < 3:
            raise ValueError("Need at least 3 possible distractors")
        
        # Choose 3 random distractors
        chosen_distractors = random.sample(self.possible_distractors, 3)
        
        # Get the correct answer from the options at the answer index
        correct_answer = self.options[self.answer - 1]
        
        # Create a list with the correct answer and chosen distractors
        all_options = [correct_answer] + chosen_distractors
        
        # Shuffle the options
        random.shuffle(all_options)
        
        # Find the new position (1-4) of the correct answer
        new_answer_position = all_options.index(correct_answer) + 1
        
        # Update the object
        self.options = all_options
        self.answer = new_answer_position
        
        return all_options

def _rand_digit(exclude_zero=False):
    if exclude_zero:
        return random.randint(1, 9)
    return random.randint(0, 9)