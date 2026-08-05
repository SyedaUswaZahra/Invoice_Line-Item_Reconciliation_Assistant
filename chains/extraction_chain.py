from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from schemas.line_item import LineItemSchema


class LineItemExtractionChain:
    """Layout-aware parsing chain coercing raw invoice text into canonical LineItemSchema records (FR-2)."""

    def __init__(self, model_name: str = "gpt-4o") -> None:
        self.model = ChatOpenAI(model=model_name, temperature=0)

        self.parser = PydanticOutputParser(pydantic_object=List[LineItemSchema])

        self.prompt = PromptTemplate(
            template=(
                "You are an expert invoice parser. Extract all line items from the "
                "raw invoice text below and return them as a JSON list conforming to "
                "the canonical LineItemSchema.\n\n"
                "Each item must have: quantity (int > 0), unit_price (float), "
                "tax_rate (float percentage, default 0.0), line_total (float computed "
                "as qty * unit_price * (1 + tax_rate/100)), and optional po_reference.\n\n"
                "If no line items are present, return an empty list.\n\n"
                "{format_instructions}\n\n"
                "RAW INVOICE TEXT:\n{raw_text}"
            ),
            input_variables=["raw_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.chain = self.prompt | self.model | self.parser

    def extract(self, raw_text: str) -> List[LineItemSchema]:
        """Coerce raw invoice text into a list of canonical line-item records."""
        return self.chain.invoke({"raw_text": raw_text})
