"""Reverse Polish calculator.

This RPN calculator creates an expression tree from
the input.  It prints the expression in algebraic
notation and then prints the result of evaluating it.
"""

import lex
import expr
import io
from expr import *

BINOPS = { lex.TokenCat.PLUS: expr.Plus,
           lex.TokenCat.TIMES: expr.Times,
           lex.TokenCat.DIV: expr.Div,
           lex.TokenCat.MINUS: expr.Minus
        }

UNOPS = { lex.TokenCat.ABS: expr.Abs,
          lex.TokenCat.NEG: expr.Neg
         }


def calc(text: str):
    """Read and evaluate a single line formula."""
    try:
        stack = rpn_parse(text)
        if len(stack) == 0:
            print("(No expression)")
        else:
            # For a balanced expression there will be one Expr object
            # on the stack, but if there are more we'll just print
            # each of them
            for exp in stack:
                print(f"{exp} => {exp.eval()}")
    except Exception as e:
        print(e)


def rpn_calc():
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")


def rpn_parse(text: str) -> list[expr.Expr]:
    """Parse text in reverse Polish notation
    into a list of expressions (exactly one if
    the expression is balanced).
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input
    """
    tokens = text.split()
    stack = []
    tokens = list(tokens)
    for token in tokens:
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(expr.Plus(a, b))
            elif token == "-":
                stack.append(expr.Minus(a, b))
            elif token == "*":
                stack.append(expr.Times(a, b))
            else:
                stack.append(expr.Div(a, b))
        elif token.isdigit():
            stack.append(expr.IntConst(int(token)))
        elif token in "==":
            name, value = token.split("=")
            stack.append(expr.Assign(expr.Var(name, stack.pop())))
        else:
            if token == "x":
                stack.append(expr.Var(token))
            else:
                raise Exception("Invalid varaible name" + token)
    return stack






if __name__ == "__main__":
    """RPN Calculator as main program"""
    rpn_calc()










