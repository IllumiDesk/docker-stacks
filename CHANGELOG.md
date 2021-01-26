# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [1.1.0](https://github.com/IllumiDesk/illumidesk/compare/v1.1.0...v1.2.0) (2021-01-26)


* Adds the `nbgitpuller` dependency to base image.

### [1.1.0](https://github.com/IllumiDesk/illumidesk/compare/v1.0.1...v1.1.0) (2021-01-25)


* Removes `repo2docker` builder from base image and replaces the base image with a standard docker image based on the upstream [jupyter docker-stacks images](https://github.com/jupyter/docker-stacks).

### [1.0.1](https://github.com/IllumiDesk/illumidesk/compare/v1.0.0...v1.0.1) (2020-10-25)

* Adds `standard-version` to manage releases

## 1.0.0 (2020-10-25)


### ⚠ BREAKING CHANGES

* This repo no longer manages specific dependencies but rather a setup to run workspaces with the IllumiDesk stack.

### Features

* Convert to template repo ([#37](https://github.com/IllumiDesk/illumidesk/issues/37)) ([49c82a4](https://github.com/IllumiDesk/illumidesk/commit/49c82a4a18dabac9426b897322296b968dd0780f))


## 0.2.0 (2020-09-25)

### Features

* Add grader notebook ([#29](https://github.com/IllumiDesk/illumidesk/issues/29)) ([ff80791](https://github.com/IllumiDesk/illumidesk/commit/ff8079148a6e96f2335a4e1e6734e70e98102632))
* Add JRE and tests ([#7](https://github.com/IllumiDesk/illumidesk/issues/7)) ([952db2d](https://github.com/IllumiDesk/illumidesk/commit/952db2d4b16452c9317a7ff026b153c73371caaa))
* Consolidate role-base images ([#21](https://github.com/IllumiDesk/illumidesk/issues/21)) ([552ec6a](https://github.com/IllumiDesk/illumidesk/commit/552ec6a36899c896dd200a515dc18aadc31fdaae))
* Convert to template repo ([#37](https://github.com/IllumiDesk/illumidesk/issues/37)) ([49c82a4](https://github.com/IllumiDesk/illumidesk/commit/49c82a4a18dabac9426b897322296b968dd0780f))
* Install Julia packages in base image with install.jl file ([#6](https://github.com/IllumiDesk/illumidesk/issues/6)) ([e64e9a4](https://github.com/IllumiDesk/illumidesk/commit/e64e9a4c8fbe0145d77f4a1bc479e92b590b7a15))
* Update base image and configs ([#15](https://github.com/IllumiDesk/illumidesk/issues/15)) ([8628f03](https://github.com/IllumiDesk/illumidesk/commit/8628f03c677197a6f7d613d2dc701ff6c98c66d6))


### Bug Fixes

* Remove shell directive in build stage ([#4](https://github.com/IllumiDesk/illumidesk/issues/4)) ([4bf7e27](https://github.com/IllumiDesk/illumidesk/commit/4bf7e277d34b6dca9e3a4a2db34cb7a4494d70d5))
