version := 0.1

.PHONY: black
black:
	find . -name '*.py' | xargs black --check --line-length=90

.PHONY: pylint
pylint:
	find . -name '*.py' | xargs pylint --output-format=colorized

.PHONY: misspell
MISSPELL := $(shell command -v misspell 2> /dev/null)
misspell:
ifndef MISSPELL
	$(error "Misspell was not found on your path. It is considered a provided dependency since it's not a Python library. Please install and add to your path: https://github.com/client9/misspell.")
endif
	find . -name '*.py' -or -name "*.md" | xargs misspell

.PHONY: pytest
pytest:
	pytest tests/

.PHONY: hadolint
hadolint:
	docker run --rm -i hadolint/hadolint < Dockerfile

.PHONY: build
build:
	docker build -t basph/airflow-rocket:$(version) .
	docker tag basph/airflow-rocket:$(version) basph/airflow-rocket:latest

.PHONY: ci
ci: | black pylint misspell pytest hadolint build

.PHONY: push
push:
	docker push basph/airflow-rocket:$(version)
	docker push basph/airflow-rocket:latest
