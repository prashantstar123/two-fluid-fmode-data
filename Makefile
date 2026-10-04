.PHONY: reproduce verify test
reproduce:
	bash reproduce.sh
verify:
	.venv/bin/python -m reproduction --verify-only
test:
	.venv/bin/python -m unittest discover -s tests -v
