"""
Ranked Pairs

This module can run the Ranked Pairs election method given a set of votes
represented as preferences. The implementation was taken from the wikipedia
article on Ranked Pairs, with a few performance based modifications

This module is the lightweight version with no dependencies 

Written by Simon Lequar, Dabney '22
"""
from . import utils as _utils

def _pair_ranker(pairs, comp):
	"""
	helper function for _gen_pairs(), sorts a list of pairs based on some
	comparison
	notably, it doesn't include any ties, since this would be an irrelevant
	edge in the graph later. (if comp[(1, 3)] == comp[(3, 1)], which means
	there is no preference between 1 and 3, then neither (1, 3) nor (3, 1)
	will be in the list of pairs returned)
	"""
	# Makes sure only one of (a, b) or (b, a) is in the ranking
	# Also doesn't include ties since they are irrelevant for this method
	ranked_pairs = [p for p in pairs if comp[p] > comp[p[::-1]]]
	# Sorts first for win strength, then for loss weakness 
	ranked_pairs.sort(reverse=True, key=(lambda x: (comp[x], -comp[x[::-1]])))
	return ranked_pairs

def _gen_pairs(candidates, votes):
	"""
	Helper function for run(), used to generate the ordered pairs of
	candidates. The returned pairs are already in strength order
	"""
	# We need to compare each pair (Ranked Pairs, duh) of candidates
	pairs = [(i, j) for i in candidates for j in candidates if i != j]
	votes = _utils.clean_votes(candidates, votes)

	# This calculates the strength of each pairwise election
	comp = {}
	for i, j in pairs:
		temp = 0
		for vote in votes:
			if vote[i] > vote[j]:
				temp += 1
		comp[(i, j)] = temp

	# This helper function can be changed for different tiebreakers
	return _pair_ranker(pairs, comp)


def _faster_comp(candidates, pairs):
	"""
	helper function for run(), evaluates winner of pairs, but faster (by
	about two orders of magnitude) than _graph() (now deprecated)
	"""
	# This computation doesn't create the whole graph, but relies on the idea
	# that the winner will never have an edge pointing to it
	edges = set()
	children = set()
	for (i, j) in pairs:
		if i in candidates and j in candidates and \
		   i not in children and (j, i) not in edges:
			children.add(j)
			edges.add((i, j))
	winners = set()
	for c in candidates:
		if c not in children:
			winners.add(c)
	return winners

def _check_bad_input(candidates, votes):
	"""
	helper function for run(), checks for errors in inputs
	"""
	# Some light error checking, may be expanded
	if len(candidates) == 0:
		raise ValueError("No candidates")
	if len(votes) == 0:
		raise ValueError("No votes")
	if len(candidates) != len(set(candidates)):
		raise ValueError("Repeated Candidates")


def run(candidates, votes):
	"""
	params:
	 - candidates (iterable 'a): The list or set of *unique* candidates
	 - votes (list (dict {'a : Ord 'b})): The list of votes, which are
	   candidates mapped to a preference
	returns:
	 - winners (set 'a): This is a set of all winners (more than 1 iff tied)

	Runs RP on a list of candidates and a list of dictionaries of votes

	Repeated candidates are not allowed, repeated votes are allowed

	Votes are in high-preference, high rank (ie 1-10, 1 worst, 10 best), and
	all ranks are positive

	Conditions of typical use:
		number of candidates small (~10 for original application)
		number of votes can be any size

	Linear in number of votes, O(N^2) in number of candidates
	"""
	_check_bad_input(candidates, votes)

	candidates = set(candidates)
	pairs = _gen_pairs(candidates, votes)
	winners = _faster_comp(candidates, pairs)
	return winners

def full_order(candidates, votes):
	"""
	params:
	 - candidates (iterable 'a): The list or set of *unique* candidates
	 - votes (list (dict {'a : Ord 'b})): The list of votes, which are
	   candidates mapped to a preference
	returns:
	 - ordered results (list (set 'a)): A list representing the finish order

	Runs RP on a list of candidates and a list of dictionaries of votes, but
	returns the result for each candidate, as opposed to run(), which only
	returns first place.

	A return of [{2}, {1, 3}, {4}] would represent 2 in first, 1 and 3 tied
	for second, and 4 in third place.

	See documentation of run() for more details
	"""
	_check_bad_input(candidates, votes)

	candidates = set(candidates)
	pairs = _gen_pairs(candidates, votes)
	order = []
	while(len(candidates) > 0):
		winners = _faster_comp(candidates, pairs)
		order.append(winners)
		candidates -= winners
	return order
