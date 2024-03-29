# Docker image info
IMG			   ?= linktimecloud/kdp-catalog-manager:$(VERSION)
IMG_REGISTRY   ?= ""

.PHONY: set-build-info
set-build-info:
	git log -1 --pretty=format:"{ \"GitVersion\": {%n  \"branch\": \"$(GIT_BRANCH)\",%n  \"commit\": \"%H\",%n  \"author\": \"%an <%ae>\",%n  \"date\": \"%ai\",%n  \"message\": \"$(GIT_COMMIT_MESSAGE)\",%n  \"tag\": \"$(GIT_TAG)\"%n},\"Version\": \"$(VERSION)\"%n,\"BuildDate\": \"$(BUILD_DATE)\"%n}" > kdp_catalog_manager/git.json

.PHONY: docker-build
docker-build: docker-build-image
	@echo "Docker build complete."

.PHONY: docker-build-image
docker-build-image:
	docker build -t $(IMG_REGISTRY)/$(IMG) -f Dockerfile .

.PHONY: docker-push
docker-push: docker-push-image
	@echo "Docker push complete."

.PHONY: docker-push-image
docker-push-image:
	docker push $(IMG_REGISTRY)/$(IMG)
