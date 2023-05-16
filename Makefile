.PHONY: help build setup benchmark

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Display this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Generate and package required data files for using in Hemingway
	python build/generate_pos_data.py
	python build/package_data.py

setup: ## Setup NLTK for data generation
	python setup/nltk_setup.py

benchmark: ## Benchmark Hemingway against annotated Brown corpus
	pip install .
	python tests/benchmark/main.py
