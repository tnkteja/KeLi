.PHONY: docsclean-pyc clean-build docs

init:
	python setup.py install

test:
	python setup.py test

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	rm -f docs/viper.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ -d 2 viper/
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html
