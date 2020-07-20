# inspiration from https://github.com/jupyter/docker-stacks
.PHONY: build

# Use bash for inline if-statements in target
SHELL:=bash
OWNER:=illumidesk
VENV_NAME?=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_BIN}/activate

PYTHON=${VENV_BIN}/python3

# Need to list the images in build dependency order
ALL_STACKS:=base-notebook \
    learner-notebook \
	instructor-notebook \
	grader-notebook \
	rstudio \
	theia \
	vscode

ALL_IMAGES:=$(ALL_STACKS)

# Linter
HADOLINT="${HOME}/hadolint"

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# http://github.com/jupyter/docker-stacks
	@echo "illumidesk/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build/base-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build/%: DARGS?=
build/%: ## build the latest image for a stack
	docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@)
	@echo -n "Built image size: "
	@docker images $(OWNER)/$(notdir $@):latest --format "{{.Size}}"

build-all: $(foreach I,$(ALL_IMAGES), build/$(I) ) ## build all stacks

dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%: ## run one of the containers (stacks) on port 8888
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

lint/%: ARGS?=--config .hadolint.yml
lint/%: ## lint the dockerfile(s) for a stack
	@echo "Linting Dockerfiles with Hadolint in $(notdir $@)..."
	@git ls-files --exclude='Dockerfile*' --ignored $(notdir $@) | grep -v ppc64 | xargs -L 1 $(HADOLINT) $(ARGS)
	@echo "Linting with Hadolint done!"
	@echo "Linting tests with flake8 in in $(notdir $@)..."
	${VENV_BIN}/flake8 $(notdir $@)
	@echo "Linting with flake8 done!"
	@echo "Applying black updates to test files in $(notdir $@)..."
	${VENV_BIN}/black $(notdir $@)
	@echo "Source formatting with black done!"

lint-all: $(foreach I,$(ALL_IMAGES),lint/$(I) ) ## lint all stacks

lint-build-all: $(foreach I,$(ALL_IMAGES),lint/$(I) build/$(I) test/$(I) ) ## lint, build and test all stacks

lint-install: ## install hadolint
	@echo "Installing hadolint at $(HADOLINT) ..."
	@curl -sL -o $(HADOLINT) "https://github.com/hadolint/hadolint/releases/download/v1.18.0/hadolint-$(shell uname -s)-$(shell uname -m)"
	@chmod 700 $(HADOLINT)
	@echo "Hadolint nstallation done!"
	@$(HADOLINT) --version

venv:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -r dev-requirements.txt

tests: venv
	${PYTHON} -m pytest -vv tests
