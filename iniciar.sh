#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
if [ ! -f config.json ]; then
  cp config.example.json config.json
  echo "Configura el client_id en config.json y vuelve a iniciar."
  exit 1
fi
python3 main.py
