import json

import pytest

from tally import Tally, TallyField


@pytest.fixture
def webhook_response():
    """Load the webhook response from the JSON file."""
    with open("tests/webhook_response.json", "r") as f:
        return json.load(f)["data"]


def test_form_name(webhook_response):
    """Test that the form name is correctly retrieved."""
    tally = Tally(webhook_response)
    assert tally.form_name == "Test  Form", "Form name mismatch"


@pytest.mark.parametrize(
    "field_type,field_label,expected_value",
    [
        (TallyField.TEXT, "Short Text", "Short Text xyz"),
        (TallyField.TEXTAREA, "Long Text", "Long Text xyz"),
        (TallyField.MULTIPLE_CHOICE, "Multiple Choice", ["B"]),
        (TallyField.DROPDOWN, "Dropdown", ["B"]),
        (TallyField.MULTI_SELECT, "Multi Select", ["A", "B"]),
        (TallyField.NUMBER, "Number", 3),
        (TallyField.EMAIL, "Email", "rohit@test.com"),
        (TallyField.PHONE_NUMBER, "Phone Number", "+919996071403"),
        (TallyField.LINK, "Link", "https://google.com"),
        (
            TallyField.FILE_UPLOAD,
            "File Upload",
            [
                {
                    "id": "V5Ny0v",
                    "name": "README.md",
                    "url": "https://storage.tally.so/private/README.md?id=V5Ny0v&accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlY1TnkwdiIsImZvcm1JZCI6Im5QdmJPMSIsImlhdCI6MTczNjY2NzU2OX0.9hW03_SP8A3Am4WvGsCS70SBTkw8j_xBa8H8wlaOnok&signature=c0117fbfbd79b5bfab6dd509dbc4338076c45e776f2394295cc85f1b502f1c24",
                    "mimeType": "text/markdown",
                    "size": 9,
                }
            ],
        ),
        (TallyField.DATE, "Date", "2025-01-12"),
        (TallyField.TIME, "Time", "00:02"),
    ],
)
def test_get_field_value(webhook_response, field_type, field_label, expected_value):
    """Test getting the value of specific fields."""
    tally = Tally(webhook_response)
    assert tally.get_field_value(field_type, field_label) == expected_value


def test_get_checkbox_values(webhook_response):
    """Test retrieving checkbox values."""
    tally = Tally(webhook_response)
    checkbox_values = tally.get_field_value(TallyField.CHECKBOXES, "Checkbox")
    assert checkbox_values == ["A", "B"]


def test_missing_field(webhook_response):
    """Test behavior when a field is missing."""
    tally = Tally(webhook_response)
    with pytest.raises(ValueError, match="Field with label 'Nonexistent' and type 'TallyField.TEXT' not found."):
        tally.get_field_value(TallyField.TEXT, "Nonexistent")


def test_silent_mode(webhook_response):
    """Test that silent mode suppresses errors for missing fields."""
    tally = Tally(webhook_response)
    assert tally.get_field_value(TallyField.TEXT, "Nonexistent", silent=True) is None


def test_invalid_webhook_body():
    """Test behavior when an invalid webhook body is provided."""
    tally = Tally({})
    assert tally.form_name is None
    assert tally.get_field_value(TallyField.TEXT, "Some Label", silent=True) is None
