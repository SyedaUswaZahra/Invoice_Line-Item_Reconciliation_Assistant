from typing import Optional

from pydantic import BaseModel, Field


class LineItemSchema(BaseModel):
    """Canonical line-item record schema (FR-2)."""

    quantity: int = Field(..., gt=0, description="Quantity of the line item")
    unit_price: float = Field(..., description="Unit price in the invoice currency")
    tax_rate: float = Field(
        0.0, ge=0, description="Applicable tax rate as a percentage"
    )
    line_total: float = Field(
        ..., description="Computed line total (qty * unit_price * (1 + tax_rate/100))"
    )
    po_reference: Optional[str] = Field(
        None, description="Purchase order reference if present"
    )

    def recompute_line_total(self) -> float:
        """Recompute line_total from qty, unit_price, and tax_rate (pure Python)."""
        self.line_total = self.quantity * self.unit_price * (
            1 + self.tax_rate / 100
        )
        return self.line_total
