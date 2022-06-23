
all:run

install-ns3:
	@cd scripts; bash install.sh

run:
	@ns3 run main.py
