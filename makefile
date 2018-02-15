# Makefile for building publishing container
PROJECT = pystacks
VERSION = $(shell whoami)
REGISTRY = local
APP_IMAGE = $(PROJECT):$(VERSION)
CONTAINER_TAG = latest

imageLocal:
	docker build -t $(APP_IMAGE) .
.PHONY: imageLocal

imageOnly:
	docker build -t $(APP_IMAGE) .
.PHONY: image

image: imageOnly
	docker push $(APP_IMAGE) 
.PHONY: image

publish-image: image
	docker tag $(APP_IMAGE) $(REGISTRY)/ops/$(PROJECT):$(CONTAINER_TAG)
	docker push $(APP_IMAGE)
	docker push $(REGISTRY)/ops/$(PROJECT):$(CONTAINER_TAG)
.PHONY: publish-image

testLocal:
	docker build -f Dockerfile.test -t pystacks-local-test .
	docker build -f Dockerfile.check -t pystacks-local-check .
.PHONY: testLocal

coverageLocal:
	nosetests --with-coverage -v --cover-package=PyStacks --cover-html --cover-html-dir=coverage
	open ./coverage/index.html
.PHONY:coverageLocal

