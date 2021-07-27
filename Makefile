.PHONY: test

test:
	python -m mypy --strict mapc2020
	flake8 mapc2020 setup.py
	python setup.py --long-description | rst2html --strict --no-raw > /dev/null

publish: test
	rm -rf build dist mapc2020.egg-info
	python setup.py sdist bdist_wheel
	twine check dist/*
	#twine upload --skip-existing --sign dist/*
