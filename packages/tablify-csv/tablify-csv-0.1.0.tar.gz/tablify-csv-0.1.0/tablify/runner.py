"""
Script entry point
"""
import logging

from .cli import app

LOGLEVEL = "INFO"


def main():
    logging.basicConfig(format="%(message)s", level=getattr(logging, LOGLEVEL))
    logging.debug("Initializing")
    app()
