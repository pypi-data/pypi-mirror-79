#! /usr/bin/env python3

""" example module: extra.iota """

from good.beta import FunB

def FunI():
	return FunB() + "_Iota"

if __name__ == "__main__":
	print("I prefer to be a module")
