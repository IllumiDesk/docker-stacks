# inspiration from https://github.com/jupyter/docker-stacks
.PHONY: test

# Use bash for inline if-statements in target
SHELL:=bash
OWNER:=illumidesk
ARCH:=$(shell uname -m)
DIFF_RANGE?=master...HEAD

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
	@echo "Replace % with a stack directory name (e.g., make build/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build/%: DARGS?=
build/%: ## build the latest image for a stack
	docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@)
	@echo -n "Built image size: "
	@docker images $(OWNER)/$(notdir $@):latest --format "{{.Size}}"

build-all: $(foreach I,$(ALL_IMAGES), build/$(I) ) ## build all stacks
build-test-all: $(foreach I,$(ALL_IMAGES), build/$(I) test/$(I) ) ## build and test all stacks

cont-clean-all: cont-stop-all cont-rm-all ## clean all containers (stop + rm)

cont-stop-all: ## stop all containers
	@echo "Stopping all containers ..."
	-docker stop -t0 $(shell docker ps -a -q) 2> /dev/null

cont-rm-all: ## remove all containers
	@echo "Removing all containers ..."
	-docker rm --force $(shell docker ps -a -q) 2> /dev/null

dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%: ## run a foreground container for a stack
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

dev-env: ## install libraries required to build docs and run tests
	pip install -r requirements-dev.txt

lint/%: ARGS?=
lint/%: ## lint the dockerfile(s) for a stack
	@echo "Linting Dockerfiles in $(notdir $@)..."
	@git ls-files --exclude='Dockerfile*' --ignored $(notdir $@) | grep -v ppc64 | xargs -L 1 $(HADOLINT) $(ARGS)
	@echo "Linting done!"

lint-all: $(foreach I,$(ALL_IMAGES),lint/$(I) ) ## lint all stacks

lint-build-test-all: $(foreach I,$(ALL_IMAGES),lint/$(I) build/$(I) test/$(I) ) ## lint, build and test all stacks

lint-install: ## install hadolint
	@echo "Installing hadolint at $(HADOLINT) ..."
	@curl -sL -o $(HADOLINT) "https://github.com/hadolint/hadolint/releases/download/v1.18.0/hadolint-$(shell uname -s)-$(shell uname -m)"
	@chmod 700 $(HADOLINT)
	@echo "Installation done!"
	@$(HADOLINT) --version	

img-clean: img-rm-dang img-rm ## clean dangling and jupyter images

img-list: ## list jupyter images
	@echo "Listing $(OWNER) images ..."
	docker images "$(OWNER)/*"

img-rm:  ## remove jupyter images
	@echo "Removing $(OWNER) images ..."
	-docker rmi --force $(shell docker images --quiet "$(OWNER)/*") 2> /dev/null

img-rm-dang: ## remove dangling images (tagged None)
	@echo "Removing dangling images ..."
	-docker rmi --force $(shell docker images -f "dangling=true" -q) 2> /dev/null

pull/%: DARGS?=
pull/%: ## pull a jupyter image
	docker pull $(DARGS) $(OWNER)/$(notdir $@)

run/%: DARGS?=
run/%: ## run a bash in interactive mode in a stack
	docker run -it --rm $(DARGS) $(OWNER)/$(notdir $@) $(SHELL)

run-sudo/%: DARGS?=
run-sudo/%: ## run a bash in interactive mode as root in a stack
	docker run -it --rm -u root $(DARGS) $(OWNER)/$(notdir $@) $(SHELL)

tx-en: ## rebuild en locale strings and push to master (req: GH_TOKEN)
	@git config --global user.email "travis@travis-ci.org"
	@git config --global user.name "Travis CI"
	@git checkout master

	@make -C docs clean gettext
	@cd docs && sphinx-intl update -p _build/gettext -l en

	@git add docs/locale/en
	@git commit -m "[ci skip] Update en source strings (build: $$TRAVIS_JOB_NUMBER)"

	@git remote add origin-tx https://$${GH_TOKEN}@github.com/IllumiDesk/docker-stacks.git
	@git push -u origin-tx master

test/%: ## run tests against a stack (only common tests or common tests + specific tests)
	@if [ ! -d "$(notdir $@)/test" ]; then TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest -m "not info" test; \
	else TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest -m "not info" test $(notdir $@)/test; fi

test-all: $(foreach I,$(ALL_IMAGES),test/$(I)) ## test all stacks
