
all:run

install-ns3:
	@cd scripts; bash install.sh

build:
	@cd scripts; bash build.sh

run:build
	@python3 main.py
