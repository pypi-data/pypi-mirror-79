"""
HTML renderer

Classes:
    HTMLRenderer
"""
import logging
from typing import Dict, List

from lxml import etree

from .ui import UserColumnSettings


logger = logging.getLogger(__name__)


class HTMLRenderer:
    """Converts table data into HTML table."""

    def __init__(self, data: List[Dict], cols: UserColumnSettings) -> None:
        self.data = data
        self.cols = cols

    async def render(self) -> str:
        """Renders data table as HTML."""
        try:
            table = etree.Element("table")
            thead = await self._render_thead()
            table.append(thead)
            tbody = await self._render_tbody()
            table.append(tbody)
            return etree.tostring(table, pretty_print=True).decode("utf-8")
        except Exception as e:
            logger.warning(f"Error rendering table: {e}")

    async def _render_thead(self) -> etree._Element:
        """Renders thead element and all children therein."""
        thead = etree.Element("thead")
        tr = etree.Element("tr")

        for col in self.cols.columns:
            th = etree.Element("th")
            th.text = self.cols.settings[col].get("heading", col)
            tr.append(th)

        thead.append(tr)
        return thead

    async def _render_tbody(self) -> etree._Element:
        """Renders tbody element and all children therein."""
        tbody = etree.Element("tbody")

        for row in self.data:
            try:
                tr = self._render_data_row(row)
                tbody.append(tr)
            except Exception as e:
                logger.warning(f"Error rendering row: {e}")

        return tbody

    def _render_data_row(self, row_data: dict) -> etree._Element:
        """Renders given data row."""
        tr = etree.Element("tr")

        for col in self.cols.columns:
            td = etree.Element("td")
            td.text = str(row_data.get(col, ""))
            class_name = self.cols.settings[col].get("class_name")
            if class_name:
                td.set("class", class_name)
            tr.append(td)

        return tr
