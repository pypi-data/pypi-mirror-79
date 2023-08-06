from . import utils as _utils
from . import rp as _rp
import json as _json
from functools import reduce as _reduce
import ast as _ast

class Election:
	"""
	This is a wrapper class to store votes, it allows for easy use of the
	methods in rp.py without having to track inputs. 

	Initialize as an empty Election(), or with a list of dicts of votes. 
	Candidates will be automatically filled in from the votes. (Note, this can
	lead to missing candidates if no one ranked that candidate). 
	"""

	def __init__(self, votes=[], method=_rp):
		"""
		constructor, optionally takes a vote list of dicts, will eventually
		be able to accept multiple voting methods once implemented
		"""
		self.method = method
		self.votes = votes
		self._update_on_vote()

	def _update_on_vote(self):
		"""
		Helper to reset state when votes change
		"""
		self.single_winner = None
		self.full_order = None
		self.candidates, self.votes = _utils.gen_cand_and_clean(self.votes)

	def set_votes(self, new_votes):
		"""
		Public method to change the votes in an Election
		"""
		self.votes = new_votes
		self._update_on_vote()
	
	def get_candidates(self):
		return self.candidates
	
	def get_votes(self):
		return self.votes

	def get_winner(self):
		"""
		Computes and stores the single winner of an election using the
		method specified (ranked pairs is the only method at present)
		"""
		if self.single_winner is not None:
			return self.single_winner
		temp = self.method.run(self.candidates, self.votes)
		self.single_winner = temp
		return self.single_winner

	def get_full_order(self):
		"""
		Computes and stores the full results of an election using the 
		specified method of the Election
		"""	
		if self.full_order is not None:
			return self.full_order
		temp = self.method.full_order(self.candidates, self.votes)
		self.full_order = temp
		return self.full_order

	def load(self, votes):
		"""
		This method loads a JSON string representing a list of dicts into
		the votes of the Election object. It can also accept a list of dicts
		"""
		# Case of JSON string, otherwise assume list
		if type(votes) == str:
			try:
				votes = _json.loads(votes)
			except ValueError as e:
				raise e
		
		try:
			assert(type(votes) == list and type(votes[0]) == dict)
		except AssertionError:
			raise ValueError("Votes not formatted correctly, must be \
							  list of dicts")
		except IndexError:
			self.set_votes([])
			return

		self.votes = votes
		self._update_on_vote()


	def load_from_file(self, filename):
		"""
		This method can load a file into the Election object, the file must
		contain one dictionary per line, formatted as a literal dictionary
		or as a JSON object
		"""
		with open(filename, 'r') as f:
			try:
				votes = list(map(_ast.literal_eval, f.readlines()))
				assert(type(votes) == list and type(votes[0]) == dict)
				self.votes = votes
				self._update_on_vote()
			except (SyntaxError, ValueError):
				raise ValueError("Votes not formatted correctly, cannot \
								  be evaluated to list of dict")
			except AssertionError:
				raise ValueError("Votes not formatted correctly, must be \
								  one dictionary per line, not separated")






