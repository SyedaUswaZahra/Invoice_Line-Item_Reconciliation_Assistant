from typing import List, Dict


class ReportAssembler:
    """Assembles the final variance report table with all columns and explanations (FR-8)."""

    HEADER = [
        "description",
        "expected qty",
        "actual qty",
        "expected price",
        "actual price",
        "variance",
        "explanation",
    ]

    def assemble(self, rows: List[Dict]) -> str:
        """Build a formatted variance report table string."""
        if not rows:
            return self._render_table([])

        lines = [self._format_header()]
        lines.append(self._format_separator())
        for row in rows:
            lines.append(self._format_row(row))
        return "\n".join(lines)

    def _format_row(self, row: Dict) -> str:
        """Format a single report row."""
        description = str(row.get("description", ""))
        expected_qty = self._format_number(row.get("expected_qty"))
        actual_qty = self._format_number(row.get("actual_qty"))
        expected_price = self._format_currency(row.get("expected_price"))
        actual_price = self._format_currency(row.get("actual_price"))
        variance = self._format_percent(row.get("variance"))
        explanation = str(row.get("explanation", ""))

        cells = [
            description,
            expected_qty,
            actual_qty,
            expected_price,
            actual_price,
            variance,
            explanation,
        ]
        return " | ".join(cells)

    def _format_header(self) -> str:
        return " | ".join(self.HEADER)

    def _format_separator(self) -> str:
        return "-+-".join("-" * len(header) for header in self.HEADER)

    @staticmethod
    def _format_number(value) -> str:
        if value is None:
            return ""
        try:
            return f"{float(value):.2f}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_currency(value) -> str:
        if value is None:
            return ""
        try:
            return f"${float(value):.2f}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_percent(value) -> str:
        if value is None:
            return ""
        try:
            return f"{float(value) * 100:.2f}%"
        except (TypeError, ValueError):
            return str(value)
