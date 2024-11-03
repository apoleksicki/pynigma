test:
	coverage erase
	coverage run --branch -m unittest
	coverage report

lint:
	ruff check

types:
	uv run mypy pynigma/ tests/

