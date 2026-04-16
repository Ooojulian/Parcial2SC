"""
Unit tests for Peano arithmetic operations.

Tests correctness of addition, multiplication, and related functions.
"""

import pytest
from src.arithmetic import S, pred, add, mul, power, verify_properties


class TestSuccessor:
    """Test successor function."""

    def test_successor_basic(self):
        """Test basic successor operation."""
        assert S(0) == 1
        assert S(1) == 2
        assert S(5) == 6
        assert S(100) == 101

    def test_successor_negative_fails(self):
        """Successor not defined for negative numbers."""
        with pytest.raises(AssertionError):
            S(-1)

    def test_successor_chain(self):
        """Test chained successors."""
        assert S(S(S(0))) == 3
        assert S(S(S(S(2)))) == 6


class TestPredecessor:
    """Test predecessor function."""

    def test_predecessor_basic(self):
        """Test basic predecessor operation."""
        assert pred(1) == 0
        assert pred(2) == 1
        assert pred(5) == 4

    def test_predecessor_zero(self):
        """Predecessor of 0 is 0 (by definition)."""
        assert pred(0) == 0

    def test_predecessor_negative_fails(self):
        """Predecessor not defined for negative numbers."""
        with pytest.raises(AssertionError):
            pred(-1)

    def test_successor_predecessor_inverse(self):
        """S(pred(n)) = n for n > 0, and S(pred(0)) = 1."""
        for n in range(1, 10):
            assert S(pred(n)) == n

    def test_predecessor_successor_inverse(self):
        """pred(S(n)) = n for all n."""
        for n in range(10):
            assert pred(S(n)) == n


class TestAddition:
    """Test addition operation."""

    def test_addition_basic(self):
        """Test basic addition cases."""
        assert add(0, 0) == 0
        assert add(2, 3) == 5
        assert add(5, 2) == 7
        assert add(10, 0) == 10

    def test_addition_zero_identity(self):
        """Zero is additive identity."""
        for n in range(10):
            assert add(n, 0) == n
            assert add(0, n) == n

    def test_addition_correctness(self):
        """Test correctness against expected arithmetic."""
        test_cases = [
            (1, 1, 2),
            (2, 3, 5),
            (5, 7, 12),
            (0, 5, 5),
            (10, 0, 10),
            (3, 4, 7),
        ]
        for m, n, expected in test_cases:
            assert add(m, n) == expected

    def test_addition_commutativity(self):
        """Addition is commutative: add(m,n) = add(n,m)."""
        for m in range(8):
            for n in range(8):
                assert add(m, n) == add(n, m), f"Failed for ({m}, {n})"

    def test_addition_associativity(self):
        """Addition is associative: add(add(m,n),k) = add(m,add(n,k))."""
        for m in range(6):
            for n in range(6):
                for k in range(6):
                    left = add(add(m, n), k)
                    right = add(m, add(n, k))
                    assert left == right, f"Failed for ({m}, {n}, {k})"

    def test_addition_negative_fails(self):
        """Addition not defined for negative numbers."""
        with pytest.raises(AssertionError):
            add(-1, 5)
        with pytest.raises(AssertionError):
            add(5, -1)

    def test_addition_large_numbers(self):
        """Test addition with larger numbers."""
        assert add(100, 200) == 300
        assert add(1000, 500) == 1500


class TestMultiplication:
    """Test multiplication operation."""

    def test_multiplication_basic(self):
        """Test basic multiplication cases."""
        assert mul(0, 0) == 0
        assert mul(2, 3) == 6
        assert mul(5, 2) == 10
        assert mul(10, 0) == 0

    def test_multiplication_zero(self):
        """Zero is multiplicative annihilator."""
        for n in range(10):
            assert mul(n, 0) == 0
            assert mul(0, n) == 0

    def test_multiplication_one_identity(self):
        """One is multiplicative identity."""
        for n in range(10):
            assert mul(n, 1) == n
            assert mul(1, n) == n

    def test_multiplication_correctness(self):
        """Test correctness against expected arithmetic."""
        test_cases = [
            (1, 1, 1),
            (2, 3, 6),
            (5, 4, 20),
            (0, 7, 0),
            (7, 0, 0),
            (3, 3, 9),
            (2, 5, 10),
        ]
        for m, n, expected in test_cases:
            assert mul(m, n) == expected, f"mul({m}, {n}) failed"

    def test_multiplication_commutativity(self):
        """Multiplication is commutative: mul(m,n) = mul(n,m)."""
        for m in range(8):
            for n in range(8):
                assert mul(m, n) == mul(n, m), f"Failed for ({m}, {n})"

    def test_multiplication_associativity(self):
        """Multiplication is associative: mul(mul(m,n),k) = mul(m,mul(n,k))."""
        for m in range(5):
            for n in range(5):
                for k in range(5):
                    left = mul(mul(m, n), k)
                    right = mul(m, mul(n, k))
                    assert left == right, f"Failed for ({m}, {n}, {k})"

    def test_multiplication_negative_fails(self):
        """Multiplication not defined for negative numbers."""
        with pytest.raises(AssertionError):
            mul(-1, 5)
        with pytest.raises(AssertionError):
            mul(5, -1)

    def test_multiplication_distributivity(self):
        """Multiplication distributes over addition."""
        # m * (n + k) = m*n + m*k
        for m in range(5):
            for n in range(5):
                for k in range(5):
                    left = mul(m, add(n, k))
                    right = add(mul(m, n), mul(m, k))
                    assert left == right, f"Failed for ({m}, {n}, {k})"

    def test_multiplication_large_numbers(self):
        """Test multiplication with larger numbers."""
        assert mul(10, 20) == 200
        assert mul(15, 12) == 180


class TestPower:
    """Test power operation."""

    def test_power_basic(self):
        """Test basic power cases."""
        assert power(2, 0) == 1
        assert power(2, 1) == 2
        assert power(2, 3) == 8
        assert power(3, 2) == 9

    def test_power_one_exponent(self):
        """Anything to the power of 1 equals itself."""
        for n in range(10):
            assert power(n, 1) == n

    def test_power_zero_exponent(self):
        """Anything to the power of 0 equals 1."""
        for n in range(1, 10):
            assert power(n, 0) == 1

    def test_power_base_one(self):
        """1 to any power equals 1."""
        for n in range(10):
            assert power(1, n) == 1

    def test_power_correctness(self):
        """Test correctness against expected arithmetic."""
        test_cases = [
            (2, 2, 4),
            (2, 3, 8),
            (3, 2, 9),
            (5, 2, 25),
            (2, 4, 16),
        ]
        for m, n, expected in test_cases:
            assert power(m, n) == expected, f"power({m}, {n}) failed"

    def test_power_negative_fails(self):
        """Power not defined for negative numbers."""
        with pytest.raises(AssertionError):
            power(-1, 5)
        with pytest.raises(AssertionError):
            power(5, -1)


class TestAlgebraicProperties:
    """Test algebraic properties of arithmetic."""

    def test_induction_principle(self):
        """
        Test induction principle: if P(0) and ∀n P(n)⟹P(S(n)), then P(ℕ).

        Property P(n): add(n, 1) = S(n)
        """
        def property_P(n: int) -> bool:
            return add(n, 1) == S(n)

        # Base case: P(0)
        assert property_P(0)

        # Inductive cases: if P(n) then P(S(n))
        for n in range(20):
            assert property_P(n)
            # If P(n) holds, P(S(n)) should also hold
            assert property_P(S(n))

    def test_verify_properties(self):
        """Test the property verification function."""
        props = verify_properties(max_n=8)

        assert props.commutativity_add
        assert props.associativity_add
        assert props.identity_add
        assert props.commutativity_mul
        assert props.associativity_mul
        assert props.identity_mul_left
        assert props.identity_mul_right
        assert props.distributivity
        assert props.induction_holds


class TestComplexity:
    """
    Test complexity characteristics.

    Note: These are sanity checks, not rigorous complexity tests.
    """

    def test_addition_linear_growth(self):
        """Addition time should grow linearly with second argument."""
        # For Peano arithmetic, larger n should require more recursive calls
        # This is a sanity check that add actually uses recursion

        # add(m, 10) requires 10 recursive calls
        # add(m, 100) requires 100 recursive calls
        result_10 = add(5, 10)
        result_100 = add(5, 100)

        assert result_10 == 15
        assert result_100 == 105

    def test_multiplication_quadratic_growth(self):
        """Multiplication time should grow quadratically."""
        # mul(m, n) calls add m times, each call is O(n)
        # Total: O(m·n)

        import time

        def timed_mul(m: int, n: int) -> float:
            start = time.perf_counter()
            mul(m, n)
            return time.perf_counter() - start

        # Just sanity check: larger inputs take longer
        time_mul_5_5 = timed_mul(5, 5)
        time_mul_10_10 = timed_mul(10, 10)

        assert time_mul_10_10 >= time_mul_5_5


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_operands(self):
        """Test operations with zero."""
        assert add(0, 0) == 0
        assert mul(0, 0) == 0
        assert power(0, 1) == 0  # 0^1 = 0

    def test_single_element(self):
        """Test operations with 1."""
        assert add(1, 1) == 2
        assert mul(1, 1) == 1
        assert power(1, 1) == 1

    def test_commutative_operations_order_independence(self):
        """Commutative operations should not depend on order."""
        values = [0, 1, 2, 5, 10]
        for m in values:
            for n in values:
                assert add(m, n) == add(n, m)
                assert mul(m, n) == mul(n, m)
