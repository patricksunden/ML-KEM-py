run_tests:
	coverage run -m unittest discover tests && coverage report --show-missing \
	--fail-under=99