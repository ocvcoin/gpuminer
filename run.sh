#!/bin/bash



require_root () {
	if [ "$EUID" -ne 0 ]; then
		echo "\nPlease run as root or with sudo.\n"
		exit 1
	fi
}




# Get the operating system name
os_name=$(uname -s)

if [ "$os_name" = "Darwin" ]; then
 








	set -e




	# Check if Homebrew is installed
	if ! command -v brew &> /dev/null; then
		echo "Homebrew is not installed. Installing Homebrew..."
		require_root
		NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	fi

	# Check if Python 3 is installed
	if ! command -v python3 &> /dev/null; then
		echo "Python 3 is not installed. Installing Python 3..."
		require_root
		brew install -q python@3
	fi

	# Check if Git is installed
	if ! command -v git &> /dev/null; then
		echo "Git is not installed. Installing Git..."
		require_root
		brew install -q git
	fi

	# Disable the -e option for the remaining part of the script
	set +e










 
else
 






	set -e

	if ! command -v python3 &> /dev/null
	then
		echo "Python 3 is not installed. Installing Python 3..."
		require_root
		export DEBIAN_FRONTEND=noninteractive
		apt update 
		apt -y install python3
	fi

	if ! command -v git &> /dev/null
	then
		echo "Git is not installed. Installing Git..."
		require_root
		export DEBIAN_FRONTEND=noninteractive
		apt update 
		apt -y install git
	fi

	set +e




 
fi










rm -rf ~/ocvcoin_gpuminer

git clone https://github.com/ocvcoin/gpuminer.git ~/ocvcoin_gpuminer

python3 ~/ocvcoin_gpuminer/ocvcoin_miner.py $@


