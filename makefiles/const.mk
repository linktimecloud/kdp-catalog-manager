# Setting SHELL to bash allows bash commands to be executed by recipes.
SHELL = /usr/bin/env bash -o pipefail
.SHELL_FLAGS = -ec


# Git Repo info
BUILD_DATE            := $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

GIT_COMMIT            ?= git-$(shell git rev-parse --short HEAD)
GIT_COMMIT_LONG       ?= $(shell git rev-parse HEAD)
GIT_COMMIT_MESSAGE    := $(shell git log -1 --pretty=format:"%s" | sed 's/"/\\"/g')
GIT_REMOTE            := origin
GIT_BRANCH            := $(shell git rev-parse --symbolic-full-name --verify --quiet --abbrev-ref HEAD)
GIT_TAG               := $(shell git describe --exact-match --tags --abbrev=0  2> /dev/null || echo untagged)
GIT_TREE_STATE        := $(shell if [[ -z "`git status --porcelain`" ]]; then echo "clean" ; else echo "dirty"; fi)
RELEASE_TAG           := $(shell if [[ "$(GIT_TAG)" =~ ^[.\|v][0-9]{1,}.[0-9]{1,}[.\|-][0-9]{1,} ]]; then echo "true"; else echo "false"; fi)

VERSION               := latest
ifeq ($(RELEASE_TAG),true)
VERSION               := $(GIT_TAG)
endif

$(info GIT_COMMIT=$(GIT_COMMIT) GIT_COMMIT_MESSAGE=$(GIT_COMMIT_MESSAGE) GIT_BRANCH=$(GIT_BRANCH) GIT_TAG=$(GIT_TAG) GIT_TREE_STATE=$(GIT_TREE_STATE) RELEASE_TAG=$(RELEASE_TAG) VERSION=$(VERSION))

ARTIFACTS_SERVER ?= ""