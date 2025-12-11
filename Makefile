.PHONY: infra gateway users statistics stop-infra logs test test-unit test-integration test-coverage test-verbose

# Start LocalStack infrastructure
infra:
	sudo docker compose up -d

# Stop LocalStack infrastructure
stop-infra:
	sudo docker compose down

# Log the container
logs:
	sudo docker logs -f pruebatecnicabeeneu-localstack-1

# Start FastAPI Gateway
gateway:
	python main.py

# Start UsersAPI microservice
users:
	cd apis/users && python main.py

# Start StatisticsAPI microservice
statistics:
	cd apis/statistics && python main.py

# Run all tests
test:
	pytest -v

# Run only unit tests
test-unit:
	pytest tests/unit -v -m unit

# Run only integration tests
test-integration:
	pytest tests/integration -v -m integration

# Run tests with coverage report
test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term-missing

# Run tests in verbose mode with detailed output
test-verbose:
	pytest -vv -s

# Install testing dependencies
install-test-deps:
	pip install -r requirements.txt
