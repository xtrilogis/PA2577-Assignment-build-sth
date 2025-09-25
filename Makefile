SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup Commands
activate_venv: ## Activate the virtual environment
	..\..\..\..\..\DataHeap\venvs\ccvenv\Scripts\Activate.ps1


##@ Publish Commands
build-backend: # Build the backend image
	docker build -t juliawin/as1backend backend/.

publish-backend: build-backend # Push the backend image to docker hub
	docker push juliawin/as1backend

deploy-backend: build-backend # Deploy only the backend service
	kubectl apply -f ./backend/kube-backend.yml


build-frontend: # Build the frontend image
	docker build -t juliawin/as1frontend frontend/.


publish-frontend: build-frontend # Push the frontend image to docker hub
	docker push juliawin/as1frontend


deploy-frontend: build-frontend # Deploy only the frontend service
	kubectl apply -f ./frontend/kube-frontend.yml


deploy-postgres:
	kubectl apply -f ./postgres/kube-postgres.yml


publish: publish-backend publish-frontend # Publish Microservices to docker hub


deploy-individual: deploy-backend deploy-frontend deploy-postgres # Deploy the services one by one


deploy-one: # Deploy the application in on go
	kubectl apply -f kube-config.yml


clean-up: # Remove all resources
	kubectl delete -f .\kube-config.yml
	docker image rm juliawin/as1backend
	docker image rm juliawin/as1frontend
	kubectl delete pvc -l app=postgres

# Delete Images, Volumnes


##@ Dev Commands
postgres-connect:
	kubectl exec -it $$(kubectl get pods -l app=postgres -o jsonpath="{.items[0].metadata.name}") -- psql -h localhost -U ps_user --password -p 5432 ps_db