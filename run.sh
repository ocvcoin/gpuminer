#!/bin/bash

PYTHON_EXEC=$(command -v python3 || command -v python || echo "")
IS_VALID_PY=false

check_python_version() {
    local exec_path="$1"
    
    if [ -n "$exec_path" ] && [ -x "$exec_path" ]; then
        local version
        version=$("$exec_path" -c 'import sys; print(sys.version_info[0])' 2>/dev/null || echo "")
        
        if [[ "$version" =~ ^[0-9]+$ ]] && [ "$version" -ge 3 ]; then
            return 0
        fi
    fi
    return 1
}

if check_python_version "$PYTHON_EXEC"; then
    IS_VALID_PY=true
fi

if [ "$IS_VALID_PY" = false ]; then
    echo "Valid Python 3+ not found. Trying to install..."
    os_name=$(uname -s)

    if [ "$os_name" = "Darwin" ]; then
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            
            if [ -x "/opt/homebrew/bin/brew" ]; then
                eval "$(/opt/homebrew/bin/brew shellenv)"
            elif [ -x "/usr/local/bin/brew" ]; then
                eval "$(/usr/local/bin/brew shellenv)"
            fi
        fi
        
        echo "Trying to install python@3 via Homebrew..."
        brew install python@3
        
        CURRENT_CHECK=$(command -v python3 || command -v python || echo "")
        if [ -z "$CURRENT_CHECK" ] || ! check_python_version "$CURRENT_CHECK"; then
            echo "python@3 validation failed. Trying alternative: brew install python..."
            brew install python
        fi
    else
        SUDO_CMD=""
        if [ "$(id -u)" -ne 0 ]; then
            if command -v sudo &> /dev/null; then
                SUDO_CMD="sudo"
            else
                echo "WARNING: Root privileges are required to install Python, but 'sudo' is missing!"
                
            fi
        fi

        if command -v apt-get &> /dev/null; then
            $SUDO_CMD apt-get update && $SUDO_CMD apt-get -y install python3
        elif command -v dnf &> /dev/null; then
            $SUDO_CMD dnf -y install python3
        elif command -v yum &> /dev/null; then
            $SUDO_CMD yum -y install python3
        elif command -v pacman &> /dev/null; then
            $SUDO_CMD pacman -S --noconfirm python
        elif command -v zypper &> /dev/null; then
            $SUDO_CMD zypper -n install python3
        elif command -v apk &> /dev/null; then
            $SUDO_CMD apk add python3
        fi
    fi

    PYTHON_EXEC=$(command -v python3 || command -v python || echo "")
    if check_python_version "$PYTHON_EXEC"; then
        IS_VALID_PY=true
    fi
fi

if [ "$IS_VALID_PY" = false ] || [ -z "$PYTHON_EXEC" ]; then
    echo "Error: Python 3 or higher is required but could not be found or installed."
    exit 1
fi

TARGET_DIR="$HOME/ocvcoin_gpuminer"
PARENT_DIR="$HOME"
ARCHIVE_PATH="$PARENT_DIR/gpuminer_main.tar.gz"
URL="https://github.com/ocvcoin/gpuminer/archive/refs/heads/main.tar.gz"

if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR"
fi

if [ -d "$PARENT_DIR/gpuminer-main" ]; then
    rm -rf "$PARENT_DIR/gpuminer-main"
fi

if [ -f "$ARCHIVE_PATH" ]; then
    rm -f "$ARCHIVE_PATH"
fi

echo "-> Downloading archive to disk..."

DOWNLOAD_SUCCESS=false

if command -v curl &> /dev/null; then
    if curl -sSfL -o "$ARCHIVE_PATH" "$URL"; then
        DOWNLOAD_SUCCESS=true
    fi
elif command -v wget &> /dev/null; then
    if wget -q --tries=3 -O "$ARCHIVE_PATH" "$URL"; then
        DOWNLOAD_SUCCESS=true
    fi
else
    echo "Error: Neither curl nor wget was found."
    exit 1
fi

if [ "$DOWNLOAD_SUCCESS" = false ] || [ ! -f "$ARCHIVE_PATH" ]; then
    echo "Error: Failed to download the archive."
    rm -f "$ARCHIVE_PATH" 2>/dev/null
    exit 1
fi

echo "-> Extracting archive from disk..."

if ! tar -xzf "$ARCHIVE_PATH" -C "$PARENT_DIR"; then
    echo "Error: Failed to extract the archive."
    rm -f "$ARCHIVE_PATH" 2>/dev/null
    exit 1
fi

rm -f "$ARCHIVE_PATH"

if [ -d "$PARENT_DIR/gpuminer-main" ]; then
    if ! mv "$PARENT_DIR/gpuminer-main" "$TARGET_DIR"; then
        echo "Error: Failed to move extracted directory to target destination."
        exit 1
    fi
else
    echo "Error: Extraction completed but 'gpuminer-main' directory was not found."
    exit 1
fi

RAW_PATH="$TARGET_DIR/ocvcoin_miner.py"

if [ ! -f "$RAW_PATH" ]; then
    echo "Error: Miner script not found at $RAW_PATH"
    exit 1
fi

CMD=("$PYTHON_EXEC" "$RAW_PATH")

"${CMD[@]}" "$@"