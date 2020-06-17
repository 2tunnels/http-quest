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

helm-upgrade:
	helm upgrade \
		--atomic \
		--install \
		--namespace http-quest \
		--set image.tag=v0.1.3 \
		--set secrets.BUGSNAG_API_KEY=secret \
		http-quest \
		./charts/http-quest/

patch:
	bump2version patch
	git push --follow-tags
