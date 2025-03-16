#!/bin/bash

# Trap CTRL+C (SIGINT) and clean up background processes
trap 'echo "Stopping all servers..."; kill $(jobs -p); exit 0' SIGINT

# Installing dependencies
pip install -r administrador_usuarios_service/requirements.txt
pip install -r orden_de_pedido_service/requirements.txt
pip install -r jwt/requirements.txt
pip install -r logs_service/requirements.txt
pip install -r detector_intrusos_service/requirements.txt

# Start servers in parallel (background)
echo "Starting server administrador de usuarios"
export FLASK_APP=administrador_usuarios_service/app.py
python3 -m flask run --port=3000 &

echo "Starting server entidad autorizadora"
export FLASK_APP=jwt/app.py
python3 -m flask run --port=3001 &

echo "Starting server orden de pedidos"
export FLASK_APP=orden_de_pedido_service/app.py
python3 -m flask run --port=3002 &


echo "Starting server logs"
export FLASK_APP=logs_service/app.py
python3 -m flask run --port=3003 &

echo "Starting server intruder detector"
export FLASK_APP=detector_intrusos_service/app.py
python3 -m flask run --port=3004 &

wait
