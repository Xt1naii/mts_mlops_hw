.PHONY: *

APP_PORT := 5000
SERVICE_PORT := 3000
DOCKER_TAG := latest
DOCKER_IMAGE := mts_hw_service

run_app:
	PYTHONPATH=. ./venv/bin/python3 -m uvicorn src.main:app \
			   --port=$(APP_PORT) \
			   --host='0.0.0.0'

run_app_docker:
	PYTHONPATH=. python3 -m uvicorn src.main:app \
			   --port=$(APP_PORT) \
			   --host='0.0.0.0'

build_image:
	docker build -f Dockerfile . --force-rm=true -t $(DOCKER_IMAGE):$(DOCKER_TAG)

run_container:
	docker run --rm -p $(SERVICE_PORT):$(APP_PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)
