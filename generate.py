import random
from typing import Tuple, Union
from dataclasses import dataclass

# Type for answers: either an int (for most), or (quotient, remainder) tuple for divisions with remainder
Answer = Union[int, Tuple[int, int]]

# -----------------------
# Addition / Subtraction
# -----------------------

def gen_1A() -> Tuple[str, Answer]:
    """1-digit addition - no carry"""
    a = random.randint(1, 8)
    b = random.randint(0, 9 - a)  # ensure a+b < 10
    q = f"{a} + {b}"
    return q, a + b

def gen_1S() -> Tuple[str, Answer]:
    """1-digit subtraction - no borrow (minuend >= subtrahend)"""
    a = random.randint(1, 9)
    b = random.randint(0, a)
    q = f"{a} - {b}"
    return q, a - b

def gen_T5() -> Tuple[str, Answer]:
    """Multiplication tables - up to 5 (i.e., pick 1..5)"""
    a = random.randint(1, 10)
    b = random.randint(1, 5)
    q = f"{a} × {b}"
    return q, a * b

def gen_2A1() -> Tuple[str, Answer]:
    """2 + 1 digit addition - no carry (two-digit + one-digit, units sum < 10)"""
    tens = random.randint(1, 9)
    units = random.randint(0, 8)
    one = random.randint(0, 9 - units)  # ensure units + one < 10
    a = 10 * tens + units
    q = f"{a} + {one}"
    return q, a + one

def gen_2A2() -> Tuple[str, Answer]:
    """2 + 2 digit addition - no carry (units sum < 10)"""
    t1 = random.randint(1, 9)
    u1 = random.randint(0, 9)
    t2 = random.randint(1, 9)
    u2 = random.randint(0, 9 - u1)  # ensure unit-digit no carry
    a = 10 * t1 + u1
    b = 10 * t2 + u2
    return f"{a} + {b}", a + b

def gen_2S1() -> Tuple[str, Answer]:
    """2 - 1 digit subtraction - no borrow (two-digit minuend minus one-digit subtrahend; units >= subtrahend)"""
    tens = random.randint(1, 9)
    units = random.randint(0, 9)
    one = random.randint(0, units)  # ensure no borrow
    a = 10 * tens + units
    return f"{a} - {one}", a - one

def gen_1AC() -> Tuple[str, Answer]:
    """1-digit addition - carry (sum >= 10)"""
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    # ensure carry
    while a + b < 10:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
    return f"{a} + {b}", a + b

def gen_2A1C() -> Tuple[str, Answer]:
    """2-digit addition - carry (2-digit + ? single carry occurs in units)"""
    tens = random.randint(1, 9)
    u1 = random.randint(0, 9)
    one = random.randint(0, 9)
    # ensure units produce carry
    while (u1 + one) < 10:
        u1 = random.randint(0, 9)
        one = random.randint(0, 9)
    a = 10 * tens + u1
    return f"{a} + {one}", a + one

def gen_2A2C() -> Tuple[str, Answer]:
    """2 + 2 digit addition - double carry (carry from units to tens AND tens to hundreds)"""
    # select digits such that:
    # units sum >= 10 -> carry1 = 1
    # tens sum + carry1 >= 10 -> carry2 = 1
    while True:
        u1 = random.randint(0, 9)
        u2 = random.randint(0, 9)
        c1 = 1 if (u1 + u2) >= 10 else 0
        t1 = random.randint(1, 9)
        t2 = random.randint(1, 9)
        if (t1 + t2 + c1) >= 10:
            a = 10 * t1 + u1
            b = 10 * t2 + u2
            return f"{a} + {b}", a + b

def gen_2S1B() -> Tuple[str, Answer]:
    """2 - 1 digit subtraction - borrow (units < subtrahend -> borrow occurs)"""
    tens = random.randint(1, 9)
    units = random.randint(0, 8)
    # choose subtrahend > units to force borrow
    sub = random.randint(units + 1, 9)
    a = 10 * tens + units
    return f"{a} - {sub}", a - sub

def gen_2S2() -> Tuple[str, Answer]:
    """2 - 2 digit subtraction - no borrow (digitwise minuend >= subtrahend)"""
    t1 = random.randint(1, 9)
    u1 = random.randint(0, 9)
    t2 = random.randint(1, t1)  # ensure tens >=
    u2 = random.randint(0, u1)  # ensure units >=
    a = 10 * t1 + u1
    b = 10 * t2 + u2
    return f"{a} - {b}", a - b

def gen_2S2B() -> Tuple[str, Answer]:
    """2 - 2 digit subtraction - single borrow (units place requires borrow, tens does not)"""
    while True:
        t1 = random.randint(1, 9)
        u1 = random.randint(0, 9)
        t2 = random.randint(1, 9)
        u2 = random.randint(0, 9)
        a = 10 * t1 + u1
        b = 10 * t2 + u2
        if a <= b:
            continue
        # Single borrow: units requires borrow but tens doesn't
        # Units borrow if u1 < u2
        # After borrowing for units, tens has (t1 - 1), which must be >= t2
        if u1 < u2 and (t1 - 1) >= t2:
            return f"{a} - {b}", a - b

def gen_T10() -> Tuple[str, Answer]:
    """Multiplication tables - 5 to 10 (i.e., choose multiplier 5..10)"""
    a = random.randint(6, 10)
    b = random.randint(2, 10)
    return f"{a} × {b}", a * b

def gen_3A() -> Tuple[str, Answer]:
    """3-digit addition - no carry (no digit pair sums >= 10)"""
    d1 = random.randint(1, 9)
    d2 = random.randint(0, 9)
    d3 = random.randint(0, 9)
    while True:
        e1 = random.randint(1, 9)
        e2 = random.randint(0, 9)
        e3 = random.randint(0, 9)
        if d3 + e3 < 10 and d2 + e2 < 10 and d1 + e1 < 10:
            a = 100 * d1 + 10 * d2 + d3
            b = 100 * e1 + 10 * e2 + e3
            return f"{a} + {b}", a + b

def gen_3AC() -> Tuple[str, Answer]:
    """3-digit addition - single carry (exactly one column causes carry)"""
    # build digits such that exactly one of the three columns has sum >= 10
    while True:
        A = [random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)]
        B = [random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)]
        carries = 0
        # unit
        if A[2] + B[2] >= 10:
            carries += 1
            c1 = 1
        else:
            c1 = 0
        # tens
        if A[1] + B[1] + c1 >= 10:
            carries += 1
            c2 = 1
        else:
            c2 = 0
        # hundreds
        if A[0] + B[0] + c2 >= 10:
            carries += 1
        if carries == 1:
            a = 100 * A[0] + 10 * A[1] + A[2]
            b = 100 * B[0] + 10 * B[1] + B[2]
            return f"{a} + {b}", a + b

def gen_3S() -> Tuple[str, Answer]:
    """3-digit subtraction - no borrow (digitwise minuend >= subtrahend)"""
    A0 = random.randint(1, 9)
    A1 = random.randint(0, 9)
    A2 = random.randint(0, 9)
    B0 = random.randint(1, A0)
    B1 = random.randint(0, A1)
    B2 = random.randint(0, A2)
    a = 100 * A0 + 10 * A1 + A2
    b = 100 * B0 + 10 * B1 + B2
    return f"{a} - {b}", a - b

def gen_3AC2() -> Tuple[str, Answer]:
    """3-digit addition - double carry (exactly two columns cause a carry)"""
    while True:
        A = [random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)]
        B = [random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)]
        carries = 0
        c1 = 1 if A[2] + B[2] >= 10 else 0
        if c1: carries += 1
        c2 = 1 if (A[1] + B[1] + c1) >= 10 else 0
        if c2: carries += 1
        c3 = 1 if (A[0] + B[0] + c2) >= 10 else 0
        if c3: carries += 1
        # double carry -> exactly 2 columns produced carry
        if carries == 2:
            a = 100 * A[0] + 10 * A[1] + A[2]
            b = 100 * B[0] + 10 * B[1] + B[2]
            return f"{a} + {b}", a + b

def gen_3SB() -> Tuple[str, Answer]:
    """3-digit subtraction - single borrow (exactly one borrow occurs)"""
    while True:
        A = [random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)]
        B = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
        # require A >= B overall
        a = 100 * A[0] + 10 * A[1] + A[2]
        b = 100 * B[0] + 10 * B[1] + B[2]
        if a <= b:
            continue
        # compute borrows by simulating column subtraction
        borrows = 0
        A2, A1, A0 = A[2], A[1], A[0]  # units, tens, hundreds (we'll treat reversed)
        # units
        if A2 < B[2]:
            borrows += 1
            # simulate borrow: tens reduced by 1
            t1 = A1 - 1
        else:
            t1 = A1
        # tens
        if t1 < B[1]:
            borrows += 1
            h = A0 - 1
        else:
            h = A0
        # hundreds
        if h < B[0]:
            borrows += 1
        if borrows == 1:
            return f"{a} - {b}", a - b

def gen_3SB2() -> Tuple[str, Answer]:
    """3-digit subtraction - double borrow (exactly two borrows occur)"""
    while True:
        A = [random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)]
        B = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
        a = 100 * A[0] + 10 * A[1] + A[2]
        b = 100 * B[0] + 10 * B[1] + B[2]
        if a <= b:
            continue
        borrows = 0
        A2, A1, A0 = A[2], A[1], A[0]
        if A2 < B[2]:
            borrows += 1
            t1 = A1 - 1
        else:
            t1 = A1
        if t1 < B[1]:
            borrows += 1
            h = A0 - 1
        else:
            h = A0
        if h < B[0]:
            borrows += 1
        if borrows == 2:
            return f"{a} - {b}", a - b

# -----------------------
# Multiplication
# -----------------------

def gen_2M1() -> Tuple[str, Answer]:
    """2x1 multiplication - no carry (each digit * multiplier < 10)"""
    while True:
        multiplier = random.randint(2, 9)
        tens = random.randint(1, 9)
        units = random.randint(0, 9)
        if multiplier * units < 10 and multiplier * tens < 10:
            a = 10 * tens + units
            return f"{a} × {multiplier}", a * multiplier

def gen_3M1() -> Tuple[str, Answer]:
    """3x1 multiplication - no carry (each digit * multiplier < 10)"""
    while True:
        multiplier = random.randint(2, 9)
        h = random.randint(1, 9)
        t = random.randint(0, 9)
        u = random.randint(0, 9)
        if multiplier * u < 10 and multiplier * t < 10 and multiplier * h < 10:
            a = 100 * h + 10 * t + u
            return f"{a} × {multiplier}", a * multiplier

def gen_2M1C() -> Tuple[str, Answer]:
    """2x1 multiplication - carry (at least one digit*multiplier >= 10)"""
    while True:
        multiplier = random.randint(2, 9)
        tens = random.randint(1, 9)
        units = random.randint(0, 9)
        if multiplier * units >= 10 or multiplier * tens >= 10:
            a = 10 * tens + units
            return f"{a} × {multiplier}", a * multiplier

def gen_3M1C() -> Tuple[str, Answer]:
    """3x1 multiplication - single carry (exactly one digit*multiplier produces carry)"""
    while True:
        multiplier = random.randint(2, 9)
        h = random.randint(1, 9)
        t = random.randint(0, 9)
        u = random.randint(0, 9)
        prod_flags = [multiplier * u >= 10, multiplier * t >= 10, multiplier * h >= 10]
        if sum(prod_flags) == 1:
            a = 100 * h + 10 * t + u
            return f"{a} × {multiplier}", a * multiplier

def gen_3M1C2() -> Tuple[str, Answer]:
    """3x1 multiplication - double carry (exactly two digit*multiplier produces carry)"""
    while True:
        multiplier = random.randint(2, 9)
        h = random.randint(1, 9)
        t = random.randint(0, 9)
        u = random.randint(0, 9)
        prod_flags = [multiplier * u >= 10, multiplier * t >= 10, multiplier * h >= 10]
        if sum(prod_flags) == 2:
            a = 100 * h + 10 * t + u
            return f"{a} × {multiplier}", a * multiplier

def gen_2M2() -> Tuple[str, Answer]:
    """2x2 multiplication - no carry. (each single-digit product < 10)"""
    while True:
        a1 = random.randint(1, 9)
        a0 = random.randint(0, 9)
        b1 = random.randint(1, 9)
        b0 = random.randint(0, 9)
        if (a0 * b0 < 10) and (a0 * b1 < 10) and (a1 * b0 < 10) and (a1 * b1 < 10):
            a = 10 * a1 + a0
            b = 10 * b1 + b0
            return f"{a} × {b}", a * b

def gen_2M2C() -> Tuple[str, Answer]:
    """2x2 multiplication - carry (at least one single-digit product >= 10)"""
    while True:
        a1 = random.randint(1, 9)
        a0 = random.randint(0, 9)
        b1 = random.randint(1, 9)
        b0 = random.randint(0, 9)
        cond = (a0 * b0 >= 10) or (a0 * b1 >= 10) or (a1 * b0 >= 10) or (a1 * b1 >= 10)
        if cond:
            a = 10 * a1 + a0
            b = 10 * b1 + b0
            return f"{a} × {b}", a * b

def gen_3M2C() -> Tuple[str, Answer]:
    """3x2 multiplication - carry (three-digit times two-digit where at least one single-digit product >= 10)"""
    while True:
        a2 = random.randint(1, 9)
        a1 = random.randint(0, 9)
        a0 = random.randint(0, 9)
        b1 = random.randint(1, 9)
        b0 = random.randint(0, 9)
        cond = any(x >= 10 for x in [a0*b0, a1*b0, a2*b0, a0*b1, a1*b1, a2*b1])
        if cond:
            a = 100 * a2 + 10 * a1 + a0
            b = 10 * b1 + b0
            return f"{a} × {b}", a * b

# -----------------------
# Division
# -----------------------

def gen_2D1() -> Tuple[str, Answer]:
    """
    2-digit ÷ 1-digit division WITHOUT remainder.
    e.g., 48 ÷ 6 = 8
    """
    divisor = random.randint(2, 9)
    quotient = random.randint(1, 9)     # ensures dividend remains 2-digit
    tens = random.randint(1, 9)         # create 2-digit quotient indirectly
    dividend = (10 * tens + quotient) * divisor
    if dividend < 10 or dividend > 99:
        return gen_2D1()                # retry if not 2-digit
    return f"{dividend} ÷ {divisor}", dividend // divisor

def gen_3D1() -> Tuple[str, Answer]:
    """3/1 division without remainder (three-digit dividend divided by one-digit divisor evenly)"""
    while True:
        dividend = random.randint(100, 999)
        divisor = random.randint(2, 9)
        if dividend % divisor == 0:
            return f"{dividend} ÷ {divisor}", dividend // divisor

def gen_2D1R() -> Tuple[str, Answer]:
    """2/1 division with remainder (two-digit dividend divided by one-digit divisor with remainder)"""
    while True:
        dividend = random.randint(10, 99)
        divisor = random.randint(2, 9)
        if dividend % divisor != 0:
            return f"{dividend} ÷ {divisor}", (dividend // divisor, dividend % divisor)

def gen_3D1R() -> Tuple[str, Answer]:
    """3/1 division with remainder (three-digit dividend divided by one-digit divisor with remainder)"""
    while True:
        dividend = random.randint(100, 999)
        divisor = random.randint(2, 9)
        if dividend % divisor != 0:
            return f"{dividend} ÷ {divisor}", (dividend // divisor, dividend % divisor)

def gen_3D1Z() -> Tuple[str, Answer]:
    """3/1 division with 0 in quotient (we produce a division where quotient's middle digit is 0, no remainder)"""
    while True:
        divisor = random.randint(2, 9)
        # construct quotient as a0b with 3-digit quotient
        a = random.randint(1, 4)  # keep product in 3-digit
        b = random.randint(0, 9)
        quo = 100 * a + 0 * 10 + b  # a0b
        dividend = divisor * quo
        if 100 <= dividend <= 999:
            return f"{dividend} ÷ {divisor}", quo

def gen_4D1R() -> Tuple[str, Answer]:
    """4/1 division with remainder (four-digit dividend divided by one-digit divisor with remainder)"""
    while True:
        dividend = random.randint(1000, 9999)
        divisor = random.randint(2, 9)
        if dividend % divisor != 0:
            return f"{dividend} ÷ {divisor}", (dividend // divisor, dividend % divisor)

# -----------------------
# Dispatcher and helpers
# -----------------------

_gen_map = {
    "1A": gen_1A,
    "1S": gen_1S,
    "T5": gen_T5,
    "2A1": gen_2A1,
    "2A2": gen_2A2,
    "2S1": gen_2S1,
    "1AC": gen_1AC,
    "2A1C": gen_2A1C,
    "2A2C": gen_2A2C,
    "2S1B": gen_2S1B,
    "2S2": gen_2S2,
    "T10": gen_T10,
    "3A": gen_3A,
    "3AC": gen_3AC,
    "3S": gen_3S,
    "2S2B": gen_2S2B,
    "3AC2": gen_3AC2,
    "3SB": gen_3SB,
    "3SB2": gen_3SB2,
    "2M1": gen_2M1,
    "3M1": gen_3M1,
    "2M1C": gen_2M1C,
    "3M1C": gen_3M1C,
    "3M1C2": gen_3M1C2,
    "2M2": gen_2M2,
    "2D1": gen_2D1,
    "3D1": gen_3D1,
    "2M2C": gen_2M2C,
    "2D1R": gen_2D1R,
    "3D1R": gen_3D1R,
    "3M2C": gen_3M2C,
    "3D1Z": gen_3D1Z,
    "4D1R": gen_4D1R,
}

def gen_questions(code: str, n: int):
    """
    Generate n questions for the given skill code.
    Returns a list of (question_str, answer) tuples.
    """
    code = code.strip()
    if code not in _gen_map:
        raise ValueError(f"Unknown code: {code}")
    
    generator = _gen_map[code]
    out = []
    for _ in range(n):
        out.append(generator())
    return out

# Backwards-compatible single-question call
def gen_question(code: str):
    return gen_questions(code, 1)[0]

# -----------------------
# Quick demo when run as script
# -----------------------
if __name__ == "__main__":
    # show one example for each code in the mapping
    for k in sorted(_gen_map.keys()):
        q, a = _gen_map[k]()
        print(f"{k}: {q} -> {a}")
