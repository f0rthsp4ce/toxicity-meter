.PHONY: telegram-download build-bot bot

telegram-download: settings.json .venv
	python telegram-download.py

build-bot:
	docker buildx build . -f tg-bot.Dockerfile -q -t toxicity-bot

run-bot:
	docker run --mount type=bind,source=$(pwd)/settings.json,target=/home/nonroot/settings.json,ro --env-file=.env --gpus all --rm -it toxicity-bot

.venv: conda.yml
	@if [ -d $@ ]; then \
		echo "Updating environment using $<..."; \
		micromamba update -p ./.venv -f $<; \
	else \
		echo "Creating environment using $<..."; \
		micromamba create -p ./.venv -f $<; \
	fi
	@touch $@

settings.json: settings.dhall
	dhall-to-json --file settings.dhall --output settings.json
