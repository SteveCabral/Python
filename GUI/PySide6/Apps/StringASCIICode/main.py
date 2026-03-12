import sys

from PySide6.QtWidgets import QApplication

from config.config_manager import config
from themes.theme_manager import theme_manager
from app_window import AppWindow


def main():
    app = QApplication(sys.argv)
    theme_manager.apply_dark_theme(app)

    app_cfg = config.get_app_config()
    window = AppWindow()
    window.resize(app_cfg.get("window_width", 860), app_cfg.get("window_height", 640))
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
