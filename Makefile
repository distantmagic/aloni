.PHONY: fmt
fmt:
	ruff format

.PHONY: lint
lint:
	ruff check && mypy ./intention
