from src.game_server.server import Server


class GameManagerServer(Server):
    pass


def main():
    server = GameManagerServer()
    server.start()


if __name__ == "__main__":
    main()
