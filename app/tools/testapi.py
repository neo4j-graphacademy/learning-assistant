import requests
from typing import Optional
from langchain.tools import StructuredTool


def post_message(url: str, body: dict, parameters: Optional[dict] = None) -> str:
    """Sends a POST request to the given url with the given body and parameters."""
    # print((url, body, parameters))
    result = requests.post(url, json=body, params=parameters)
    return f"Status: {result.status_code} - {result.text}"


post_message_tool = StructuredTool.from_function(post_message)
