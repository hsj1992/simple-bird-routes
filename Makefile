.PHONY: generate_routes use_for_bird

all: generate_routes use_for_bird

generate_routes:
	#python3 make.py ./src eth0
	python3 make.py ./src "192.168.31.55;fdac::55"

use_for_bird:
	cp routes4.conf /etc/bird/routes4.conf
	cp routes6.conf /etc/bird/routes6.conf
	birdc configure
