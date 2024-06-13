.PHONY: fmt
fmt:
	ruff format

.PHONY: lint
lint:
	ruff check && mypy ./intention

.PHONY: start
start:
	granian \
		--interface asgi \
		--loop uvloop \
		--workers 1 \
		./app.py
