#!/bin/bash



set -e

if ! command -v python3 &> /dev/null
then

	if (( $EUID != 0 )); then
		echo "
		Please run as root
		"
		exit
	fi

    apt update 
	apt -y install python3
fi

if ! command -v git &> /dev/null
then

	if (( $EUID != 0 )); then
		echo "
		Please run as root
		"
		exit
	fi

    apt update 
	apt -y install git
fi

set +e

rm -rf ~/ocvcoin_gpuminer

git clone https://github.com/ocvcoin/gpuminer.git ~/ocvcoin_gpuminer

python3 ~/ocvcoin_gpuminer/ocvcoin_miner.py


