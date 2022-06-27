
all:run

install-ns3:
	@cd scripts; bash install.sh

build:
	@cd scripts; ./build.py --full

fast-build:
	@cd scripts; ./build.py --fast

