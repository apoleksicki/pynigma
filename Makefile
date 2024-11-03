test:
	coverage erase
	coverage run --branch -m unittest
	coverage report
