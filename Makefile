test:
	pytest -vv --cov=http_quest --cov-report=term-missing

isort:
	isort --recursive .

black:
	black .

format: isort black

lint-isort:
	isort --recursive --check-only .

lint-black:
	black --check .

lint-mypy:
	mypy .

lint-safety:
	safety check --full-report

lint: lint-isort lint-black lint-mypy lint-safety

uvicorn:
	uvicorn http_quest.asgi:application --reload

docker-build:
	docker image build -t http-quest .

docker-run:
	docker container run -it -p 8000:8000 http-quest

patch:
	bump2version patch
	git push --follow-tags
