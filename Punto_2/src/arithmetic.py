"""
Peano Arithmetic Implementation.

Implements addition and multiplication of natural numbers using only
the successor function S(n) = n+1.

Based on Peano axioms: ℕ = {0, S(0), S(S(0)), ...}
"""

from typing import Callable
from dataclasses import dataclass


# ============================================================================
# SUCCESSOR FUNCTION
# ============================================================================

def S(n: int) -> int:
    """
    Successor function: S(n) = n + 1.

    This is the only primitive operation. All arithmetic is built from this.

    Args:
        n: Natural number

    Returns:
        n + 1

    Raises:
        AssertionError: If n < 0 (not a natural number)
    """
    assert n >= 0, "Successor only defined on ℕ (non-negative integers)"
    return n + 1


def pred(n: int) -> int:
    """
    Predecessor function: inverse of successor.

    pred(0) = 0 (special case)
    pred(S(n)) = n

    Args:
        n: Natural number

    Returns:
        n - 1 if n > 0, else 0

    Raises:
        AssertionError: If n < 0
    """
    assert n >= 0, "Predecessor only defined on ℕ"
    return max(0, n - 1)


# ============================================================================
# RECURSIVE ADDITION (SUMA)
# ============================================================================

def add(m: int, n: int) -> int:
    """
    Addition of two natural numbers using recursion on successor.

    Peano definition:
        add(m, 0) = m                       [base case]
        add(m, S(n)) = S(add(m, n))         [inductive case]

    This means: to add n to m, apply successor n times to m.

    Example:
        add(2, 3) = add(2, S(2))
                  = S(add(2, 2))
                  = S(S(add(2, 1)))
                  = S(S(S(add(2, 0))))
                  = S(S(S(2)))
                  = 5

    Args:
        m: First addend
        n: Second addend

    Returns:
        m + n

    Complexity:
        Time: Θ(n)  - n recursive calls and n successor applications
        Space: Θ(n) - call stack depth is n

    Raises:
        AssertionError: If m < 0 or n < 0
    """
    assert m >= 0 and n >= 0, "Addition only defined on ℕ"

    # Base case: add(m, 0) = m
    if n == 0:
        return m

    # Inductive case: add(m, S(n)) = S(add(m, n))
    return S(add(m, pred(n)))


# ============================================================================
# RECURSIVE MULTIPLICATION (MULTIPLICACIÓN)
# ============================================================================

def mul(m: int, n: int) -> int:
    """
    Multiplication of two natural numbers using addition.

    Peano definition:
        mul(m, 0) = 0                              [base case]
        mul(m, S(n)) = add(mul(m, n), m)           [inductive case]

    This means: to multiply m by n, add m a total of n times.

    Example:
        mul(2, 3) = mul(2, S(2))
                  = add(mul(2, 2), 2)
                  = add(add(mul(2, 1), 2), 2)
                  = add(add(add(mul(2, 0), 2), 2), 2)
                  = add(add(add(0, 2), 2), 2)
                  = add(add(2, 2), 2)
                  = add(4, 2)
                  = 6

    Args:
        m: Multiplicand
        n: Multiplier

    Returns:
        m * n

    Complexity:
        Time: Θ(m·n)  - n calls to add, each with Θ(m) cost
        Space: Θ(n)   - call stack depth for mul is n

    Raises:
        AssertionError: If m < 0 or n < 0
    """
    assert m >= 0 and n >= 0, "Multiplication only defined on ℕ"

    # Base case: mul(m, 0) = 0
    if n == 0:
        return 0

    # Inductive case: mul(m, S(n)) = add(mul(m, n), m)
    return add(mul(m, pred(n)), m)


# ============================================================================
# POWER FUNCTION (Built on multiplication)
# ============================================================================

def power(m: int, n: int) -> int:
    """
    Power function: m^n, defined using multiplication.

    Definition:
        power(m, 0) = 1                 [base case: anything^0 = 1]
        power(m, S(n)) = mul(power(m, n), m)  [m^(n+1) = m^n * m]

    Args:
        m: Base
        n: Exponent

    Returns:
        m^n

    Complexity:
        Time: Θ(m^n) - exponential (n calls to mul, costs scale exponentially)
        Space: Θ(n)  - call stack depth

    Raises:
        AssertionError: If m < 0 or n < 0
    """
    assert m >= 0 and n >= 0, "Power only defined on ℕ"

    # Base case: power(m, 0) = 1
    if n == 0:
        return 1

    # Inductive case: power(m, S(n)) = mul(power(m, n), m)
    return mul(power(m, pred(n)), m)


# ============================================================================
# PROPERTIES AND AXIOMS (For verification)
# ============================================================================

@dataclass
class PeanoProperties:
    """Stores verification results of Peano axioms."""

    commutativity_add: bool = False
    associativity_add: bool = False
    identity_add: bool = False

    commutativity_mul: bool = False
    associativity_mul: bool = False
    identity_mul_left: bool = False
    identity_mul_right: bool = False

    distributivity: bool = False
    induction_holds: bool = False


def verify_properties(max_n: int = 10) -> PeanoProperties:
    """
    Verify algebraic properties for small values.

    Args:
        max_n: Maximum value to test (default 10)

    Returns:
        PeanoProperties dataclass with verification results
    """
    props = PeanoProperties()

    # Test addition properties
    props.commutativity_add = all(
        add(m, n) == add(n, m)
        for m in range(max_n) for n in range(max_n)
    )

    props.associativity_add = all(
        add(add(m, n), k) == add(m, add(n, k))
        for m in range(max_n) for n in range(max_n) for k in range(max_n)
    )

    props.identity_add = all(
        add(n, 0) == n and add(0, n) == n
        for n in range(max_n)
    )

    # Test multiplication properties
    props.commutativity_mul = all(
        mul(m, n) == mul(n, m)
        for m in range(max_n) for n in range(max_n)
    )

    props.associativity_mul = all(
        mul(mul(m, n), k) == mul(m, mul(n, k))
        for m in range(max_n) for n in range(max_n) for k in range(max_n)
    )

    props.identity_mul_left = all(
        mul(1, n) == n
        for n in range(max_n)
    )

    props.identity_mul_right = all(
        mul(n, 1) == n
        for n in range(max_n)
    )

    # Test distributivity
    props.distributivity = all(
        mul(m, add(n, k)) == add(mul(m, n), mul(m, k))
        for m in range(max_n) for n in range(max_n) for k in range(max_n)
    )

    # Test induction principle (if P(0) and ∀n P(n)⟹P(S(n)) then P(ℕ))
    # P(n) = "add(n, 1) == S(n)"
    def property_P(n: int) -> bool:
        return add(n, 1) == S(n)

    props.induction_holds = (
        property_P(0) and all(property_P(n) for n in range(1, max_n))
    )

    return props


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("PEANO ARITHMETIC DEMONSTRATION")
    print("="*70 + "\n")

    # Basic operations
    print("BASIC OPERATIONS:")
    print(f"  S(5) = {S(5)}")
    print(f"  pred(5) = {pred(5)}")
    print()

    # Addition examples
    print("ADDITION (add):")
    examples_add = [(2, 3), (0, 5), (7, 0), (4, 4)]
    for m, n in examples_add:
        result = add(m, n)
        print(f"  add({m}, {n}) = {result} (expected {m + n})")
    print()

    # Multiplication examples
    print("MULTIPLICATION (mul):")
    examples_mul = [(2, 3), (0, 5), (5, 0), (4, 3)]
    for m, n in examples_mul:
        result = mul(m, n)
        print(f"  mul({m}, {n}) = {result} (expected {m * n})")
    print()

    # Power examples
    print("POWER (power):")
    examples_pow = [(2, 3), (3, 2), (5, 0), (1, 10)]
    for m, n in examples_pow:
        result = power(m, n)
        print(f"  power({m}, {n}) = {result} (expected {m ** n})")
    print()

    # Properties verification
    print("PROPERTIES VERIFICATION (testing up to n=10):")
    props = verify_properties(max_n=10)

    print(f"  Addition commutativity:     {props.commutativity_add}")
    print(f"  Addition associativity:     {props.associativity_add}")
    print(f"  Addition identity:          {props.identity_add}")
    print(f"  Multiplication commutativity: {props.commutativity_mul}")
    print(f"  Multiplication associativity: {props.associativity_mul}")
    print(f"  Multiplication identity:    {props.identity_mul_left and props.identity_mul_right}")
    print(f"  Distributivity:             {props.distributivity}")
    print(f"  Induction principle:        {props.induction_holds}")
    print()

    # Summary
    all_ok = (
        props.commutativity_add and props.associativity_add and
        props.identity_add and props.commutativity_mul and
        props.associativity_mul and props.identity_mul_left and
        props.identity_mul_right and props.distributivity and
        props.induction_holds
    )

    status = "✓ ALL PROPERTIES VERIFIED" if all_ok else "✗ SOME PROPERTIES FAILED"
    print(status)
    print("="*70 + "\n")
