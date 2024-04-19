import math, random as rand

class BigInt:
    """
    Represents a big integer, that can have an arbitrary amount of digits.
    """

    def __init__(
            self, *,
            value: int | None = None,
            digit_count: int | None = None
        ) -> None:
        """Creates an instance of `BigInt`.

        Args:
            value (int | None, optional): The integral value of the `BigInt`. Defaults to None.
            digit_count (int | None, optional): The amount of random digits to allocate to this `BigInt`. Defaults to None.

        Raises:
            ValueError: Not enough information is given to create the big integer object.
            NotImplementedError: The given argument values are not currently supported.
        """

        self._digits: list[int] = []
        if value is not None:
            if value < 0: raise NotImplementedError("negative value not implemented")
            if value != 0:
                val_dc = int(math.log10(value)) + 1
                num_dc = val_dc if digit_count is None else min(val_dc, digit_count)

                for _ in range(num_dc):
                    self._digits.append(value % 10)
                    value //= 10
        else:
            if digit_count is None: raise ValueError("provide at least a value or a digit count")
            for i in range(digit_count):
                self._digits.append(rand.randint(0 if i < digit_count - 1 else 1, 9))
    
    def clone(self):
        """Creates a clone of this `BigInt` instance.

        Returns:
            BigInt: A deep copy of the instance.
        """
        c = BigInt(digit_count=0)
        for digit in self._digits: c._digits.append(digit)
        return c

    def add_at(self, idx: int, value: int) -> None:
        """Adds a value at the specified decimal position. Supports carry computation.

        Args:
            idx (int): The index at which to add the value.
            value (int): The value to add to the number.

        Raises:
            NotImplementedError: The given argument values are not currently supported.
        """
        if value < 0: raise NotImplementedError("negative value not implemented")
        if value == 0: return

        while idx >= len(self): self._digits.append(0)
        
        new_val = self._digits[idx] + value
        self._digits[idx] = new_val % 10
        self.add_at(idx + 1, new_val // 10)

    @property
    def digits(self) -> list[int]:
        """The digits of this big integer.

        Returns:
            list[int]: A list containing the digits of this big integer.
        """
        return self._digits

    def __len__(self) -> int:
        """Returns the number of digits in this big integer.

        Returns:
            int: The number of digits in this big integer.
        """
        return len(self._digits)

    def __eq__(self, other: object) -> bool:
        """Checks whether this big integer is equal (in integral value) to another big integer.

        Args:
            other (object): The object to compare.

        Returns:
            bool: `False` if `object` is not a `BigInt` or `object` represents a different integral value. Otherwise, returns `True`.
        """
        if not isinstance(other, BigInt): return False
        if len(self) != len(other): return False

        eq = True
        for i in range(len(self)):
            eq = self._digits[i] == other._digits[i]
            if not eq: break
        return eq

    def __gt__(self, other: object) -> bool:
        """Returns whether this big integer is greater than another big integer.

        Args:
            other (object): The object to compare.

        Raises:
            TypeError: `other` is not a `BigInt`.

        Returns:
            bool: `True` if this big integer represents a value greater than `other`. Otherwise, returns `False`.
        """
        if not isinstance(other, BigInt): raise TypeError("not a BigNumber")
        if len(self) != len(other): return len(self) > len(other)

        nlt, gt = True, False
        for i in range(len(self) - 1, -1, -1):
            d1, d2 = self._digits[i], other._digits[i]
            nlt = d1 >= d2
            gt = d1 > d2
            if gt or not nlt: break
        return gt

    def __ge__(self, other: object) -> bool:
        """Returns whether this big integer is greater than or equal to another big integer.

        Args:
            other (object): The object to compare.

        Raises:
            TypeError: `other` is not a `BigInt`.

        Returns:
            bool: `True` if this big integer represents a value greater than or equal to `other`. Otherwise, returns `False`.
        """
        if not isinstance(other, BigInt): raise TypeError("not a BigNumber")
        return not self < other

    def __le__(self, other: object) -> bool:
        """Returns whether this big integer is less than or equal to another big integer.

        Args:
            other (object): The object to compare.

        Raises:
            TypeError: `other` is not a `BigInt`.

        Returns:
            bool: `True` if this big integer represents a value less than or equal to `other`. Otherwise, returns `False`.
        """
        if not isinstance(other, BigInt): raise TypeError("not a BigNumber")
        return not self > other

    def __add__(self, other: object):
        """Computes the sum of two big integers.

        Args:
            other (object): The object to add by.

        Raises:
            TypeError: `other` is not a `BigInt`.

        Returns:
            BigInt: The sum of the two big integers.
        """
        if not isinstance(other, BigInt): raise TypeError("not a BigNumber")
        
        result = BigInt(digit_count=0)
        for i in range(max(len(self), len(other))):
            a = self._digits[i] if i < len(self) else 0
            b = other._digits[i] if i < len(other) else 0

            result.add_at(i, a + b)
        
        return result
    
    def __mul__(self, other: object):
        """Computes the product of two big integers.

        Args:
            other (object): The object to multiply by.

        Raises:
            TypeError: `other` is not a `BigInt`.

        Returns:
            BigInt: The product of the two big integers.
        """
        if not isinstance(other, BigInt): raise TypeError("not a BigNumber")

        result = BigInt(digit_count=0)
        for j in range(len(other)):
            carry = 0
            for i in range(len(self)):
                product = self._digits[i] * other._digits[j] + carry
                carry = product // 10
                product %= 10

                result.add_at(j + i, product)
            if carry != 0: result.add_at(j + len(self), carry)
        
        return result

    def __int__(self) -> int:
        """Returns the integral value of this big integer.

        Returns:
            int: The integral value of this big integer.
        """
        val = 0
        for i in range(len(self)):
            digit = self._digits[i]
            val += digit * 10**i
        return val
    
    def __str__(self) -> str:
        """Returns the string representation of this big integer.

        Returns:
            str: The string representation of this big integer.
        """
        s = ""
        for digit in self._digits:
            s = f"{digit}" + s
        return s

    def __repr__(self) -> str:
        """Returns the canonical string representation of this big integer, such that `eval(repr(obj)) == obj`.

        Returns:
            str: The canonical string representation of this big integer.
        """
        return f"BigInt(value={str(self)})"
