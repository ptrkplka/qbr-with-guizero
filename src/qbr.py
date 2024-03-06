#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import sys
import kociemba
import argparse
from video import webcam
import i18n
import os
from config import config
from constants import (
    ROOT_DIR,
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)
from guizero import App, Window, Text, PushButton

# Set default locale.
locale = config.get_setting('locale')
if not locale:
    config.set_setting('locale', 'en')
    locale = config.get_setting('locale')

# Init i18n.
i18n.load_path.append(os.path.join(ROOT_DIR, 'translations'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')
i18n.set('locale', locale)
i18n.set('fallback', 'en')

class Qbr:

    def __init__(self, normalize):
        self.normalize = normalize

    def run(self):
        """The main function that will run the Qbr program."""
        state = webcam.run()

        # If we receive a number then it's an error code.
        if isinstance(state, int) and state > 0:
            self.print_E_and_exit(state)

        try:
            algorithm = kociemba.solve(state)
            length = len(algorithm.split(' '))
        except Exception:
            self.print_E_and_exit(E_INCORRECTLY_SCANNED)

        # guizero setup
        app = App(text = "QBR: Start", height = 400, width = 400)
        app.show()

        window_sol = Window(app, text = "QBR: Instructions", height = 400, width = 400)
        window_sol.hide()

        window_hrs = Window(window_sol, text = "QBR: Human Readable Solution", height = 800, width = 800)
        window_hrs.hide()

        window_cs = Window(window_hrs, text = "QBR: Cheat Sheet")
        window_cs.hide()

        # functions for guizero

        # open
        def open_window_sol():
            window_sol.show()
            app.hide()

        def open_window_hrs():
            window_hrs.show()
            window_sol.hide()

        def open_window_cs():
            window_cs.show()

        # close

        def close_app():
            os.exit()

        def close_window_sol():
            app.show()
            window_sol.hide()

        def close_window_hrs():
            window_sol.show()
            window_hrs.hide()

        def close_window_cs():
            window_cs.hide()

        # Buttons
        button_next = PushButton(app, text = "-->", command = open_window_sol)
        button_close = PushButton(app, text = i18n.t('close'), command = close_app)

        button_next_sol = PushButton(window_sol, text = i18n.t('hrs'), command = open_window_hrs)
        button_close_sol = PushButton(window_sol, text = i18n.t('close'), command = close_window_sol)
        
        button_next_hrs = PushButton(window_hrs, text = i18n.t('cs'), command = open_window_cs)
        button_close_hrs = PushButton(window_hrs, text = i18n.t('close'), command = close_window_hrs)

        # Text in windows
        starting_pos = Text(app, text = i18n.t('startingPosition'))
        moves = Text(window, text = i18n.t('moves', moves=length))
        solution = Text(window, text = i18n.t('solution', algorithm=algorithm))

        if self.normalize:
            for index, notation in enumerate(algorithm.split(' ')):
                text = i18n.t('solveManual.{}'.format(notation))
                human_readable_solution = Text(window_hrs, text = '{}. {}'.format(index + 1, text))

    def print_E_and_exit(self, code):
        """Print an error message based on the code and exit the program."""
        if code == E_INCORRECTLY_SCANNED:
            print('\033[0;33m[{}] {}'.format(i18n.t('error'), i18n.t('haventScannedAllSides')))
            print('{}\033[0m'.format(i18n.t('pleaseTryAgain')))
        elif code == E_ALREADY_SOLVED:
            print('\033[0;33m[{}] {}'.format(i18n.t('error'), i18n.t('cubeAlreadySolved')))
        sys.exit(code)

if __name__ == '__main__':
    # Define the application arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--normalize',
        default=False,
        action='store_true',
        help='Shows the solution normalized. For example "R2" would be: \
              "Turn the right side 180 degrees".'
    )
    args = parser.parse_args()

    # Run Qbr with all arguments.
    Qbr(args.normalize).run()
