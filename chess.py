# Chess class for the main GUI

import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton

from Components.chessboard import Chessboard


class Chess(object):
    def main(self):
        app = QApplication(sys.argv)
        self.chessboard = Chessboard()
        chess_ui_layout = QGridLayout()
        chess_ui_layout.addWidget(self.chessboard, 0, 0, 1, 1)
        
        self.restart_button = QPushButton("New Game")
        self.restart_button.clicked.connect(self.chessboard.setup_pieces)
        chess_ui_layout.addWidget(self.restart_button, 1, 0, 1, 1)

        chess_ui = QWidget()
        chess_ui.setLayout(chess_ui_layout)
        chess_ui.setVisible(True)
        sys.exit(app.exec_())


if __name__ == "__main__":
    Chess().main()