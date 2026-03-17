from dataclasses import dataclass
import random


def _is_non_negative_option(value):
    """Return True only for non-negative answer/option values."""
    if isinstance(value, int):
        return value >= 0
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return False
        if "R" in s:
            q, sep, r = s.partition("R")
            if not sep:
                return False
            try:
                return int(q) >= 0 and int(r) >= 0
            except ValueError:
                return False
        try:
            return int(s) >= 0
        except ValueError:
            return False
    return False

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
        # Get the correct answer from the options at the answer index
        correct_answer = self.options[self.answer - 1]

        # Keep only non-negative distractors and avoid duplicates of the correct answer.
        filtered_distractors = [
            d for d in self.possible_distractors
            if _is_non_negative_option(d) and d != correct_answer
        ]

        if len(filtered_distractors) < 3:
            raise ValueError("Need at least 3 non-negative possible distractors")

        # Choose 3 random distractors
        chosen_distractors = random.sample(filtered_distractors, 3)
        
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