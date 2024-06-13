.PHONY: fmt
fmt:
	ruff format

.PHONY: lint
lint:
	ruff check

.PHONY: start.asgi
start.asgi:
	granian \
		--interface asgi \
		--loop uvloop \
		--workers 1 \
		./app_asgi.py

.PHONY: start.rsgi
start.rsgi:
	granian \
		--interface rsgi \
		--loop uvloop \
		--workers 1 \
		./app_rsgi.py
