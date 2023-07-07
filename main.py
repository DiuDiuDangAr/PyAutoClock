from unicodedata import name
from aurora_ui import UIClock
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('misc/history.log', 'w', 'utf-8')])
    ui = UIClock()