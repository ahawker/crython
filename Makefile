.DEFAULT_GOAL := help

.PHONY: test-install
test-install:  ## Install dependencies required for local test execution.
	@pip install -q -r requirements/test.txt

.PHONY: test
test: test-install  ## Run test suite.
	@py.test -v tests

.PHONY: tox-install
tox-install:  ## Install dependencies required for local test execution using tox.
	@pip install -q -r requirements/tox.txt

.PHONY: tox
tox: tox-install  ## Run test suite using tox.
	@tox

.PHONY: coveralls-install
coveralls-install:  ## Install dependencies required for coveralls.io integration.
	@pip install -q -r requirements/coveralls.txt

.PHONY: codeclimate-install
codeclimate-install:  ## Install dependencies required for codeclimate.com integration.
	@pip install -q -r requirements/codeclimate.txt

.PHONY: travis-install
travis-install: coveralls-install codeclimate-install  ## Install dependencies for travis-ci.org integration.
	@pip install -q -r requirements/travis.txt

.PHONY: travis-script
travis-script: travis-install tox  ## Entry point for travis-ci.org execution.

.PHONY: clean-pyc
clean-pyc:  ## Remove local python cache files.
	@find . -name '__pycache__' -type d -exec rm -r {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: codeclimate
codeclimate:  ## Run codeclimate analysis.
	@docker run \
		--interactive --tty --rm \
		--env CODECLIMATE_CODE="$(shell pwd)" \
		--volume "$(shell pwd)":/code \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume /tmp/cc:/tmp/cc \
		codeclimate/codeclimate analyze

.PHONY: bump-patch
bump-patch:  ## Bump package patch version, e.g. 0.0.1 -> 0.0.2.
	@bumpversion patch

.PHONY: bump-minor
bump-minor:  ## Bump package minor version, e.g. 0.1.0 -> 0.2.0.
	@bumpversion minor

.PHONY: bump-major
bump-major:  ## Bump package major version, e.g. 1.0.0 -> 2.0.0.
	@bumpversion major

.PHONY: git-push-with-tags
git-push-with-tags:  ## Push latest changes to remote with tags.
	@git push
	@git push --tags

.PHONY: push-patch
push-patch: bump-patch git-push-with-tags  ## Bump package patch version and push changes to remote.

.PHONY: push-minor
push-minor: bump-minor git-push-with-tags  ## Bump package minor version and push changes to remote.

.PHONY: push-major
push-major: bump-major git-push-with-tags  ## Bump package major version and push changes to remote.

.PHONY: docs
docs:  ## Build project documentation.
	@make -C docs html

.phony: help
help: ## Print Makefile usage.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
