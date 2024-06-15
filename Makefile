.PHONY: fmt
fmt:
	ruff format

.PHONY: lint
lint:
	ruff check
	mypy \
		--disallow-any-generics \
		--disallow-any-unimported \
		--disallow-subclassing-any \
		--disallow-untyped-calls \
		--disallow-untyped-decorators \
		--disallow-untyped-defs \
		--extra-checks \
		--follow-imports=normal \
		--pretty \
		--strict \
		--strict-equality \
		--warn-redundant-casts \
		--warn-return-any \
		--warn-unreachable \
		--warn-unused-ignores \
		./intention
