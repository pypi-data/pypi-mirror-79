"""
User Interface
"""
from collections import defaultdict
import logging
from typing import Dict, List

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator


logger = logging.getLogger(__name__)


# Validators
is_required_validator = Validator.from_callable(
    lambda x: bool(str(x)),
    error_message="This field is required.",
    move_cursor_to_end=True,
)


# UI class
class UserColumnSettings:
    """Captures and stores user-specified column settings."""

    def __init__(self, columns: List[str]) -> None:
        self.columns = columns
        self.settings = defaultdict(lambda: dict())

    def get_input(self) -> None:
        """Shows input prompt and gets user input."""
        for col in self.columns:
            try:
                col_settings = self._process_column(col)
                if not col_settings:
                    raise ValueError("No settings entered")
                self.settings[col].update(col_settings)
            except Exception as e:
                logger.warning(f"Error getting settings for column {col}: {e}")

    def _process_column(self, column_name: str) -> Dict[str, str]:
        """Captures user settings for given column."""
        heading = prompt(
            f"Column heading for {column_name}",
            validator=is_required_validator,
            validate_while_typing=False,
        )
        class_name = prompt(f"Class name for {column_name} (optional)")
        return {"heading": heading, "class_name": class_name}
