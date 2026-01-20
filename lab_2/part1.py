# Lab 2 (part 1)
# student name: Gyan Edbert Zesiro
# student number: 38600060

from __future__ import annotations  # helps with type hints
from tkinter import *
# do not import any more modules


# do not change the skeleton of the program. Only add code where it is requested.
class Rational:
    """
    this class implements the rational number type
    it stores the rational number in its lowest from
    two data fields:
        numerator and denominator
        (numerator stores the sign of the rational)
    Operation:
        add, subtract, multiply and divide
        toString
    """

    def __init__(self, numerator: int, denominator: int) -> None:
        """initializer stores the rational number in the lowest form"""

        def greatestCommonDivisor(n: int, d: int):
            """local method for the greatest common divisor calculation"""
            n1 = abs(n)
            d1 = abs(d)
            result = 1
            k = 1
            while k <= n1 and k <= d1:
                if n1 % k == 0 and d1 % k == 0:
                    result = k
                k += 1
            return result

        # rational number must be in the lowest form (numerator and denominator have no other common factor other than 1)
        gcd: int = greatestCommonDivisor(numerator, denominator)
        # numerator stores the sign of the rational
        signFactor: int = 1 if denominator > 0 else -1
        self.numerator = signFactor * numerator // gcd
        self.denominator = abs(denominator) // gcd

    def add(self, secondRational: Rational) -> Rational:
        """
        adds 'this' rational to secondRational
        returns the result as a rational number (type Rational)
        """
        # to implement
        # Check for NaN
        if self.denominator == 0 or secondRational.denominator == 0:
            return Rational(0, 0)

        numerator = (self.numerator * secondRational.denominator) + (
            secondRational.numerator * self.denominator
        )
        denominator = self.denominator * secondRational.denominator
        return Rational(numerator, denominator)

    def subtract(self, secondRational: Rational) -> Rational:
        """
        subtracts secondRational from 'this' rational to
        returns the result as a rational number (type Rational)
        """
        # to implement
        if self.denominator == 0 or secondRational.denominator == 0:
            return Rational(0, 0)

        numerator = (self.numerator * secondRational.denominator) - (
            secondRational.numerator * self.denominator
        )
        denominator = self.denominator * secondRational.denominator
        return Rational(numerator, denominator)

    def multiply(self, secondRational: Rational) -> Rational:
        """
        multiplies 'this' rational to secondRational
        returns the result as a rational number (type Rational)
        """
        # to implement
        if self.denominator == 0 or secondRational.denominator == 0:
            return Rational(0, 0)

        numerator = self.numerator * secondRational.numerator
        denominator = self.denominator * secondRational.denominator
        return Rational(numerator, denominator)

    def divide(self, secondRational: Rational) -> Rational:
        """
        divides 'this' rational by secondRational
        returns the result as a rational number (type Rational)
        """
        # to implement
        if self.denominator == 0 or secondRational.denominator == 0:
            return Rational(0, 0)

        numerator = self.numerator * secondRational.denominator
        denominator = self.denominator * secondRational.numerator
        return Rational(numerator, denominator)

    def toString(self) -> str:
        """
        returns a string representation of 'this' rational
        the general output format is: numerator/denominator
        especial cases:
            if 'this' rational is an integer, it must not show any denominator
            if denominator is 0, it returns "NaN" (not a number)
            if numerator or the denominator is not an integer, it returns "NaN"
        """
        # to implement
        if self.denominator == 0:
            return "NaN"

        if not (
            isinstance(self.numerator, int) and isinstance(self.denominator, int)
        ):  # if not integer, return NaN as well
            return "NaN"

        # This checks for both case when add/subtract = 0 and division results in a whole number
        if self.numerator % self.denominator == 0:
            return str(self.numerator // self.denominator)

        return f"{self.numerator}/{self.denominator}"


class GUI:
    """
    this class implements the GUI for our program
    use as is.
    The add, subtract, multiply and divide methods invoke the corresponding
    methods from the Rational class to calculate the result to display.
    """

    def __init__(self):
        """
        The initializer creates the main window, label and entry widgets,
        and starts the GUI mainloop.
        """
        window = Tk()
        window.title("Rational Numbers")
        window.geometry("190x180")

        # Labels and entries for the first rational number
        frame1 = Frame(window)
        frame1.grid(row=1, column=1, pady=10)
        Label(frame1, text="Rational 1:").pack(side=LEFT)
        self.rational1Numerator = StringVar()
        Entry(
            frame1,
            width=5,
            textvariable=self.rational1Numerator,
            justify=RIGHT,
            font=("Calibri 13"),
        ).pack(side=LEFT)
        Label(frame1, text="/").pack(side=LEFT)
        self.rational1Denominator = StringVar()
        Entry(
            frame1,
            width=5,
            textvariable=self.rational1Denominator,
            justify=RIGHT,
            font=("Calibri 13"),
        ).pack(side=LEFT)

        # Labels and entries for the second rational number
        frame2 = Frame(window)
        frame2.grid(row=3, column=1, pady=10)
        Label(frame2, text="Rational 2:").pack(side=LEFT)
        self.rational2Numerator = StringVar()
        Entry(
            frame2,
            width=5,
            textvariable=self.rational2Numerator,
            justify=RIGHT,
            font=("Calibri 13"),
        ).pack(side=LEFT)
        Label(frame2, text="/").pack(side=LEFT)
        self.rational2Denominator = StringVar()
        Entry(
            frame2,
            width=5,
            textvariable=self.rational2Denominator,
            justify=RIGHT,
            font=("Calibri 13"),
        ).pack(side=LEFT)

        # Labels and entries for the result rational number
        # an entry widget is used as the output here
        frame3 = Frame(window)
        frame3.grid(row=4, column=1, pady=10)
        Label(frame3, text="Result:     ").pack(side=LEFT)
        self.result = StringVar()
        Entry(
            frame3,
            width=10,
            textvariable=self.result,
            justify=RIGHT,
            font=("Calibri 13"),
        ).pack(side=LEFT)

        # Buttons for add, subtract, multiply and divide
        frame4 = Frame(window)  # Create and add a frame to window
        frame4.grid(row=5, column=1, pady=5, sticky=E)
        Button(frame4, text="Add", command=self.add).pack(side=LEFT)
        Button(frame4, text="Subtract", command=self.subtract).pack(side=LEFT)
        Button(frame4, text="Multiply", command=self.multiply).pack(side=LEFT)
        Button(frame4, text="Divide", command=self.divide).pack(side=LEFT)

        mainloop()

    def add(self):
        (rational1, rational2) = self.getBothRational()
        result = rational1.add(rational2)
        self.result.set(result.toString())

    def subtract(self):
        (rational1, rational2) = self.getBothRational()
        result = rational1.subtract(rational2)
        self.result.set(result.toString())

    def multiply(self):
        (rational1, rational2) = self.getBothRational()
        result = rational1.multiply(rational2)
        self.result.set(result.toString())

    def divide(self):
        (rational1, rational2) = self.getBothRational()
        result = rational1.divide(rational2)
        self.result.set(result.toString())

    def getBothRational(self):
        """Helper method used by add, subtract, multiply and divide methods"""
        try:
            numerator1 = eval(self.rational1Numerator.get())
            denominator1 = eval(self.rational1Denominator.get())
            rational1 = Rational(numerator1, denominator1)

            numerator2 = eval(self.rational2Numerator.get())
            denominator2 = eval(self.rational2Denominator.get())
            rational2 = Rational(numerator2, denominator2)
            return (rational1, rational2)
        except:
            return (
                Rational(0, 0),
                Rational(0, 0),
            )  # if an entry value is missing, cause NaN


if __name__ == "__main__":
    GUI()
