import pytest
from paser.tools.file_tools import read_file, replace_string_at_line, verify_file_hash
from paser.tools.core_tools import context
import os

@pytest.fixture
def temp_file(tmp_path):
    f = tmp_path / "test_val.txt"
    f.write_text("Line 1\nLine 2\nLine 3")
    return str(f)

def test_invalid_type_enforcement():
    """Verify that passing an integer where a string is expected triggers a validation error."""
    # read_file expects a string path. Passing an int should be caught by Pydantic.
    result = read_file(path=12345)
    assert "Error de validación" in result

def test_out_of_range_enforcement(temp_file):
    """Verify that line_number <= 0 is caught by the schema (gt=0)."""
    # replace_string_at_line schema has line_number: int = Field(..., gt=0)
    result = replace_string_at_line(path=temp_file, line_number=0, search_text="Line", replace_text="Row")
    assert "Error de validación" in result
    assert "greater than 0" in result.lower()

def test_hash_length_enforcement(temp_file):
    """Verify that an invalid SHA-256 hash length is caught by the schema."""
    # verify_file_hash schema has expected_hash: str = Field(..., min_length=64, max_length=64)
    result = verify_file_hash(path=temp_file, expected_hash="too-short")
    assert "Error de validación" in result
    assert "string_too_short" in result or "length" in result.lower()
