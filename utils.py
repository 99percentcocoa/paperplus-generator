def number_to_letter(num):
    """
    Convert numeric answer (1, 2, 3, 4) to letter (A, B, C, D).
    
    Args:
        num: int or str representing the answer position (1-4)
    
    Returns:
        str: The corresponding letter (A, B, C, or D)
    
    Raises:
        ValueError: If input is not 1-4
    """
    # Convert to int if string
    if isinstance(num, str):
        try:
            num = int(num)
        except ValueError:
            raise ValueError(f"Invalid input: {num}. Must be '1', '2', '3', or '4'")
    
    # Map number to letter
    mapping = {1: "A", 2: "B", 3: "C", 4: "D"}
    
    if num not in mapping:
        raise ValueError(f"Invalid answer number: {num}. Must be 1, 2, 3, or 4")
    
    return mapping[num]


def letter_to_index(letter):
    """
    Convert letter answer (A, B, C, D) to index (0, 1, 2, 3).
    
    Args:
        letter: str representing the answer letter (A-D, case-insensitive)
    
    Returns:
        int: The corresponding index (0, 1, 2, or 3)
    
    Raises:
        ValueError: If input is not A-D
    """
    # Convert to uppercase if needed
    if isinstance(letter, str):
        letter = letter.upper()
    else:
        raise ValueError(f"Invalid input type: {type(letter)}. Must be a string")
    
    # Map letter to index
    mapping = {"A": 0, "B": 1, "C": 2, "D": 3}
    
    if letter not in mapping:
        raise ValueError(f"Invalid answer letter: {letter}. Must be A, B, C, or D")
    
    return mapping[letter]
