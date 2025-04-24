#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 /path/to/input_dir /path/to/output_dir [--max_depth N]"
    exit 1
fi

# Проверим, установлен ли Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing..."
    sudo apt update && sudo apt install -y python3
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/collect_files.py"

# Вызов Python скрипта с передачей всех аргументов
python3 "$PYTHON_SCRIPT" "$@"
