# tally.py

Tally.py is a lightweight Python wrapper designed to parse and process form responses from Tally.so. It simplifies handling webhook payloads by providing methods to extract form metadata, field values, and other key information.

## Installation

You can install the package directly from GitHub:

```
pip install git+https://github.com/deadaf/tally.py.git
```

Or add it to your Poetry project:
```
poetry add git+https://github.com/deadaf/tally.py.git
```

## Usage

```py
from tally import Tally, TallyField

# Simulate webhook payload
webhook_payload = {
    "formName": "Test Form",
    "fields": [
        {
            "key": "question_1",
            "label": "Short Text",
            "type": "INPUT_TEXT",
            "value": "Hello World"
        },
        {
            "key": "question_2",
            "label": "Checkbox",
            "type": "CHECKBOXES",
            "value": ["option_1", "option_2"],
            "options": [
                {"id": "option_1", "text": "Option 1"},
                {"id": "option_2", "text": "Option 2"}
            ]
        }
    ]
}

# Initialize Tally wrapper
tally = Tally(webhook_payload)

# Extract form name
print(tally.form_name)  # Output: "Test Form"

# Get values for specific fields
short_text = tally.get_field_value(TallyField.TEXT, "Short Text")
print(short_text)  # Output: "Hello World"

checkbox_values = tally.get_field_value(TallyField.CHECKBOXES, "Checkbox")
print(checkbox_values)  # Output: ["Option 1", "Option 2"]
```
