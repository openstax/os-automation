clean:
	rm -rf .eggs/ build/ dist/ docs/_build/ htmlcov/ *.egg-info/ .coverage
	-find . -name '__pycache__' -prune -exec rm -rf "{}" \;
	-find . -name '*.pyc' -delete

.PHONY: docs
docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs at docs/_build/html/index.html\n\n\033[0m"
