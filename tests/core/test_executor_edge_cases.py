import pytest
import asyncio
from paser.core.executor import AutonomousExecutor

class MockAssistant:
    current_model = "mock-model"
    def __init__(self, responses=None):
        self.responses = responses or []
        self.call_count = 0

    def send_message(self, text):
        if self.call_count < len(self.responses):
            res = self.responses[self.call_count]
            self.call_count += 1
            return res
        return "No more responses configured."

def test_deeply_nested_json():
    """Test if the balanced brace parser can handle deeply nested structures."""
    nested_json = '{"name": "test", "args": {"a": {"b": {"c": {"d": 1}}}}}'
    tools = {"test": lambda **kwargs: "success"}
    assistant = MockAssistant(responses=[f'Here is the call: {nested_json}'])
    executor = AutonomousExecutor(assistant=assistant, tools=tools)
    result = asyncio.run(executor.execute("start"))
    assert "No more responses configured." in result

def test_malformed_json_single_quotes():
    """Test if _parse_call_content handles single quotes correctly."""
    single_quote_json = "{'name': 'test', 'args': {'val': 1}}"
    assistant = MockAssistant(responses=[single_quote_json])
    tools = {"test": lambda **kwargs: "success"}
    executor = AutonomousExecutor(assistant=assistant, tools=tools)
    result = asyncio.run(executor.execute("start"))
    assert "No more responses configured." in result

def test_braces_in_strings():
    """Test if braces inside JSON strings are handled correctly."""
    # This tests if a '}' inside a string closes the JSON prematurely
    json_with_braces = '{"name": "test", "args": {"msg": "Closing brace } here"}}'
    tools = {"test": lambda **kwargs: "success"}
    assistant = MockAssistant(responses=[f'Call: {json_with_braces}'])
    executor = AutonomousExecutor(assistant=assistant, tools=tools)
    result = asyncio.run(executor.execute("start"))
    assert "No more responses configured." in result

def test_multiple_json_objects():
    """Test if multiple JSON objects in one response are all extracted."""
    json1 = '{"name": "tool1", "args": {}}'
    json2 = '{"name": "tool2", "args": {}}'
    tools = {
        "tool1": lambda **kwargs: "res1",
        "tool2": lambda **kwargs: "res2"
    }
    assistant = MockAssistant(responses=[f'First: {json1} Second: {json2}'])
    executor = AutonomousExecutor(assistant=assistant, tools=tools)
    result = asyncio.run(executor.execute("start"))
    # The executor should process both and then move to the next response
    assert "No more responses configured." in result

def test_unbalanced_braces():
    """Test that unbalanced braces do not cause crashes and are ignored if invalid."""
    unbalanced = '{"name": "test", "args": {"a": 1}' # Missing closing brace
    tools = {"test": lambda **kwargs: "success"}
    assistant = MockAssistant(responses=[f'Call: {unbalanced}'])
    executor = AutonomousExecutor(assistant=assistant, tools=tools)
    result = asyncio.run(executor.execute("start"))
    # Should not find a valid tool call and return the text
    assert "Call: {" in result

def test_empty_json():
    """Test that empty braces are handled without crashing."""
    empty = '{}'
    tools = {"test": lambda **kwargs: "success"}
    assistant = MockAssistant(responses=[f'Call: {empty}'])
    executor = AutonomousExecutor(assistant=assistant, tools=tools)
    result = asyncio.run(executor.execute("start"))
    # {} is valid JSON but doesn't have 'name', so it should be ignored
    assert "Call: {}" in result
