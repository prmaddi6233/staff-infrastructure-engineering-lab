.PHONY: test demo verify
test:
	python3 -m unittest discover -s tests -v
demo:
	python3 -m reliability
verify: test
	python3 scripts/check_repository.py
