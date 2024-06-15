.PHONY: fmt
fmt:
	ruff format

.PHONY: lint
lint:
	ruff check && mypy \
		--disallow-any-decorated \
		--disallow-any-explicit \
		--disallow-any-expr \
		--disallow-any-generics \
		--disallow-any-unimported \
		--disallow-subclassing-any \
		--disallow-untyped-calls \
		--disallow-untyped-decorators \
		--disallow-untyped-defs \
		--extra-checks \
		--pretty \
		--strict \
		--strict-equality \
		--warn-redundant-casts \
		--warn-return-any \
		--warn-unreachable \
		--warn-unused-ignores \
		./intention

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
