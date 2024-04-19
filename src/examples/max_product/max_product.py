# Given two positive integers A and B with the same amount of digits, find the maximum and minimum possible product of C and D,
# where C and D are positive integers formed by swapping the digits of A and B. Swapping can only be done on corresponding digits,
# i.e. pairs of digits that occupy the same decimal place on A and B.

# TODO: Add problem analysis and algorithm explanation
from bigint import BigInt

def calc_extreme_products_brute(a: BigInt, b: BigInt, idx: int = 0) -> tuple[BigInt, BigInt, BigInt, BigInt, BigInt, BigInt]:
    """Calculates the extremum (maximum and minimum) of the product C times D via brute force depth-first search.
    Guaranteed to find the global extrema, courtesy to the brute force algorithm.

    Args:
        a (BigNumber): The value of A.
        b (BigNumber): The value of B.
        idx (int, optional): The starting index of the search. Swapping is done on digits of this and following indices.
        Defaults to 0, which enables swapping on all digits.

    Raises:
        ValueError: A and B does not have the same amount of digits.

    Returns:
        tuple[BigNumber, BigNumber, BigNumber, BigNumber, BigNumber, BigNumber]: The value of C, D, and the product C times D,
        for both the maximum and minimum possible value of C times D.
    """
    if len(a) != len(b): raise ValueError("mismatched number length")
    if idx >= len(a):
        # Base case: Compute and return the product
        prod = a * b
        return a.clone(), b.clone(), prod, a.clone(), b.clone(), prod.clone()
    
    # Recursive case: Compare the result of the original pair and the pair that has their digits at idx swapped
    c1_max, d1_max, p1_max, c1_min, d1_min, p1_min = calc_extreme_products_brute(a, b, idx + 1)
    a.digits[idx], b.digits[idx] = b.digits[idx], a.digits[idx]
    c2_max, d2_max, p2_max, c2_min, d2_min, p2_min = calc_extreme_products_brute(a, b, idx + 1)
    a.digits[idx], b.digits[idx] = b.digits[idx], a.digits[idx]

    # Choose and return the extreme values
    cr_max, dr_max, pr_max = (c1_max, d1_max, p1_max) if p1_max >= p2_max else (c2_max, d2_max, p2_max)
    cr_min, dr_min, pr_min = (c1_min, d1_min, p1_min) if p1_min <= p2_min else (c2_min, d2_min, p2_min)

    return cr_max, dr_max, pr_max, cr_min, dr_min, pr_min

def calc_max_product(a: BigInt, b: BigInt) -> tuple[BigInt, BigInt, BigInt]:
    """Calculates the maximum of the product C and D via the above algorithm.

    Args:
        a (BigNumber): The value of A.
        b (BigNumber): The value of B.

    Raises:
        ValueError: A and B does not have the same amount of digits.

    Returns:
        tuple[BigNumber, BigNumber, BigNumber]: The value of C, D, and the product C and D.
    """
    if len(a) != len(b): raise ValueError("mismatched number length")

    c = a.clone()
    d = b.clone()
    found_diff = False
    for i in range(-1, -len(a) - 1, -1):
        curr_diff = c.digits[i] != d.digits[i]

        # If this is the first different pair of digits, choose the larger digit for A
        # Otherwise, choose the smaller digit for A
        if (not found_diff and curr_diff and c.digits[i] < d.digits[i]) or (found_diff and c.digits[i] > d.digits[i]):
            c.digits[i], d.digits[i] = d.digits[i], c.digits[i]
            
        found_diff = found_diff or c.digits[i] != d.digits[i]
        
    return c, d, c * d

def calc_min_product(a: BigInt, b: BigInt) -> tuple[BigInt, BigInt, BigInt]:
    """Calculates the minimum of the product C and D via the above algorithm.

    Args:
        a (BigNumber): The value of A.
        b (BigNumber): The value of B.

    Raises:
        ValueError: A and B does not have the same amount of digits.

    Returns:
        tuple[BigNumber, BigNumber, BigNumber]: The value of C, D, and the product C times D.
    """
    if len(a) != len(b): raise ValueError("mismatched number length")

    c = a.clone()
    d = b.clone()
    for i in range(-1, -len(a) - 1, -1):
        # Take all the largest digits for A
        if c.digits[i] < d.digits[i]:
            c.digits[i], d.digits[i] = d.digits[i], c.digits[i]
        
    return c, d, c * d

if __name__ == "__main__":
    # Compute the extreme values via the algorithm
    a = BigInt(digit_count=10)
    b = BigInt(digit_count=10)
    m1, n1, p1 = calc_max_product(a, b)
    m2, n2, p2 = calc_min_product(a, b)

    # Compute the extreme values by brute force
    m_max, n_max, p_max, m_min, n_min, p_min = calc_extreme_products_brute(a, b)

    # Display and compare the results
    print("a:", a, "\nb:", b, end="\n\n")
    print("ALGORITHM:\nMax product:\nm:", m1, "\nn:", n1, "\nm*n:", p1, "\n\nMin product:\nm:", m2, "\nn:", n2, "\nm*n:", p2, end="\n\n")
    print("BRUTE FORCE:\nMax product:\nm:", m_max, "\nn:", n_max, "\nm*n:", p_max, "\n\nMin product:\nm:", m_min, "\nn:", n_min, "\nm*n:", p_min, end="\n\n")
    print("Result is", "valid" if p1 == p_max and p2 == p_min else "not valid")
