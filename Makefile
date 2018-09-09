.PHONY:	
	tests
	clean
	coverage

coverage:
	coverage run -m unittest discover -s test
	coverage html
	coverage xml
 
tests:
	python -m unittest discover -v -s test

clean:
	find -name \*.pyc -delete
	find -name \*.pyo -delete
	find -name __pycache__ -delete
	find -name \*.so -delete
