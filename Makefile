NAME = mhworth/matt-resume
VERSION = 0.0.1

.PHONY: all build test tag_latest release ssh

all: build

build:
	docker build -t $(NAME):$(VERSION) --rm .
	docker tag -f $(NAME):$(VERSION) $(NAME):latest

tag_latest:
	docker tag -f $(NAME):$(VERSION) $(NAME):latest

run:
	docker run --rm -it -p 8000:8000 mhworth/matt-cv

release: tag_latest
	@if ! docker images $(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(NAME) version $(VERSION) is not yet built. Please run 'make build'"; false; fi
	docker push $(NAME)

