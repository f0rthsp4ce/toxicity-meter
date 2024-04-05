.PHONY: download bot

download: settings.json .venv
	python download.py

bot: .venv
	python tg-bot.py

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
