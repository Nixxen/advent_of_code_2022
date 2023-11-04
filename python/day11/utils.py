def lcm(a: int, b: int) -> int:
    """Find the least common multiple of two numbers.

    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: least common multiple
    """
    gcd_res, _, _ = gcd(a, b)
    # if gcd_res == 1:
    #     print(f"{a} and {b} are relatively prime")
    # print(f"LCM of {a} and {b} is {a} * {b} // {gcd_res} = {a * b // gcd_res}")
    return (a * b) // gcd_res


def gcd(a: int, b: int):
    """Return the greatest common divisor of a and b.

    Args:
        a (int): first number
        b (int): second number

    Returns:
        tuple(int, int, int): (gcd, x, y) such that gcd = ax + by
    """
    # Returns gcd(a,b) and integers x and y such that
    # xa + yb = gcd(a,b)
    x = 1
    y = 0
    z = 0
    w = 1
    while a != b:
        if a > b:
            a -= b
            x -= z
            y -= w
        else:
            b -= a
            z -= x
            w -= y
    return (a, x, y)
