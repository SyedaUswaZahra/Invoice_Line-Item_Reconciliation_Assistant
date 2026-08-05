import argparse
import json

from graph.workflow_graph import WorkflowGraph
from schemas.line_item import LineItemSchema
from typing import List


def parse_args() -> argparse.Namespace:
    """Parse CLI args: invoice file path, PO data path, optional tolerance."""
    parser = argparse.ArgumentParser(
        description="Run the invoice reconciliation workflow and print the variance report."
    )
    parser.add_argument(
        "--invoice",
        required=True,
        help="Path to the invoice file (PDF, image, or HTML).",
    )
    parser.add_argument(
        "--po-data",
        required=True,
        help="Path to the JSON file containing PO line items.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.05,
        help="Variance tolerance fraction (default: 0.05).",
    )
    return parser.parse_args()


def load_po_items(po_path: str) -> List[LineItemSchema]:
    """Load PO line items from a JSON file."""
    with open(po_path, "r", encoding="utf-8") as f:
        raw_items = json.load(f)
    return [LineItemSchema(**item) for item in raw_items]


def main() -> None:
    """Entry point: build graph, run workflow, print report."""
    args = parse_args()

    po_items = load_po_items(args.po_data)

    graph = WorkflowGraph()
    graph.build()

    final_state = graph.run(args.invoice, po_items)

    print(final_state.get("report", "No report generated."))


if __name__ == "__main__":
    main()
