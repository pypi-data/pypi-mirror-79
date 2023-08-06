"""
rankedpairs

This is a module that implements a lightweight ranked pairs voting algorithm. 

There are two main components to this, the Ranked Pairs module (rp) and the
Election class (Election). rp contains all the logic for Ranked Pairs, and 
Election is a wrapper class to make working with the data a bit easier. 

A common way to import this module would be:

import rankedpairs as pyrp

There is more documentation in each module (ie help(rp.Election))

Written by Simon Lequar, Dabney '22
"""
from .rp import *
from .election import Election
