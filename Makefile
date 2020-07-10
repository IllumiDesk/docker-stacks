# inspiration from https://github.com/jupyter/docker-stacks
.PHONY: build

# Use bash for inline if-statements in target
SHELL:=bash
OWNER:=illumidesk

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
	@echo "jupyter/docker-stacks"
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
	@echo "Linting Dockerfiles in $(notdir $@)..."
	@git ls-files --exclude='Dockerfile*' --ignored $(notdir $@) | grep -v ppc64 | xargs -L 1 $(HADOLINT) $(ARGS)
	@echo "Linting done!"

lint-all: $(foreach I,$(ALL_IMAGES),lint/$(I) ) ## lint all stacks

lint-build-all: $(foreach I,$(ALL_IMAGES),lint/$(I) build/$(I) test/$(I) ) ## lint, build and test all stacks

lint-install: ## install hadolint
	@echo "Installing hadolint at $(HADOLINT) ..."
	@curl -sL -o $(HADOLINT) "https://github.com/hadolint/hadolint/releases/download/v1.18.0/hadolint-$(shell uname -s)-$(shell uname -m)"
	@chmod 700 $(HADOLINT)
	@echo "Installation done!"
	@$(HADOLINT) --version	
