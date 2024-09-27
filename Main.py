from AppManager import AppManager


def main() -> None:
    app_manager = AppManager()
    app_manager.start()
    app_manager.main()
    app_manager.end()


if __name__ == "__main__":
    main()
