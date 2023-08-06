"""
CLI Command
"""
import asyncio
import logging
import sys
from typing import Optional

import pyperclip
import typer

from .reader import CSVTableReader
from .renderer import HTMLRenderer
from .ui import UserColumnSettings
from .utils import save_to_file


logger = logging.getLogger(__name__)


app = typer.Typer()


@app.command("tablify")
def tablify(
    csv_file: str = typer.Argument(..., help="Filename of CSV data file"),
    output_file: Optional[str] = typer.Option(
        "", help="Filename of output file"
    ),
    clip: Optional[bool] = typer.Option(
        False, help="Copy HTML table to clipboard"
    ),
) -> None:
    """Converts CSV into HTML table and saves it to output file and/or copies it to clipboard."""
    try:
        csv_table = CSVTableReader(csv_file)
        user_input = UserColumnSettings(csv_table.columns)
        user_input.get_input()

        html_renderer = HTMLRenderer(csv_table.data, user_input)
        html_table = asyncio.run(html_renderer.render())

        fpath = output_file if output_file else f"{csv_file}.html"

        if not clip:
            save_to_file(html_table, fpath)
            logger.info(f"Finished writing converted table to {fpath}")
        else:
            pyperclip.copy(html_table)
            logger.info("Copied HTML table to clipboard")

            if output_file:
                save_to_file(html_table, fpath)
                logger.info(f"Finished writing converted table to {fpath}")
    except KeyboardInterrupt:
        logger.warning("Canceled")
    except Exception as e:
        logger.error(f"An unhandled error occurred: {e}")
        sys.exit(1)
