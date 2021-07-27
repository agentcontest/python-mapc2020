.PHONY: test

test:
	python -m mypy --strict mapc2020
	flake8 mapc2020 setup.py
	python setup.py --long-description | rst2html --strict --no-raw > /dev/null
