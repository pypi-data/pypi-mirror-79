from functools import reduce as _reduce

def gen_cand_and_clean(votes):
	"""
	params:
	 - votes (list (dict {'a : Ord 'b})): The list of votes, which are
	   candidates mapped to a preference
	returns:
	 - candidates (set 'a): The set of candidates
	 - cleaned votes (list (dict {'a : Ord 'b}))
	
	This utility function generates a set of all candidates ranked in the
	votes cast, and returns that set along with a cleaned set of votes
	"""
	candidates = _reduce(set.union, 
						 [set(v.keys()) for v in votes], 
						 set())
	return candidates, clean_votes(candidates, votes)

def clean_votes(candidates, votes):
	"""
	params:
	 - candidates (list 'a): The list of candidates
	 - votes (list (dict {'a : Ord 'b})): The list of votes, which are
	   candidates mapped to a preference
	returns:
	 - cleaned votes (list (dict {'a : Ord 'b}))

	Cleans votes by adding a 0 for each non-present candidate, which means
	votes should be in high-preference, high rank order (1-10 worst-best)
	"""
	for vote in votes:
		for candidate in candidates:
			if candidate not in vote:
				vote[candidate] = 0
	return votes
