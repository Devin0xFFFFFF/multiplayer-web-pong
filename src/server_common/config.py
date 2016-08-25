MATCHMAKER_IP = "localhost"
GAME_MANAGER_IP = "localhost"
LOGGER_IP = "localhost"

MATCHMAKER_PORT = "5556"
GAME_MANAGER_PORT = "5557"
LOGGER_PORT = "5558"

MATCHMAKER_ADDR = "tcp://" + MATCHMAKER_IP + ":" + MATCHMAKER_PORT
GAME_MANAGER_ADDR = "tcp://" + GAME_MANAGER_IP + ":" + GAME_MANAGER_PORT
LOGGER_ADDR = "tcp://" + LOGGER_IP + ":" + LOGGER_PORT

GAME_MANAGER_ADDR_INTERNAL = "inproc://mpwp_game_manager.ipc"

# TO RUN WEBSOCKETD:
# cd into multiplayer-web-pong/src
# ./client_handler/websocketd.exe --port=8080 python -m client_handler.client_handler
