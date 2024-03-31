.PHONY: all

all: settings.json
	python download.py

settings.json: settings.dhall
	dhall-to-json --file settings.dhall --output settings.json
