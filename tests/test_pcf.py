import json

import pytest

from tally import Tally, TallyField


@pytest.fixture
def webhook_response2():
    """Load the webhook response from the JSON file."""
    with open("tests/webhook_response2.json", "r") as f:
        return json.load(f)["data"]


def test_pcf_hidden_fields(webhook_response2):
    """Test hidden fields in the webhook response."""
    tally = Tally(webhook_response2)

    assert tally.get_field_value(TallyField.HIDDEN, "booked_id", silent=True) is None
    assert tally.get_field_value(TallyField.HIDDEN, "setter_id", silent=True) is None
    assert tally.get_field_value(TallyField.HIDDEN, "closer_id", silent=True) is None
    assert tally.get_field_value(TallyField.HIDDEN, "opportunity_id", silent=True) is None
    assert tally.get_field_value(TallyField.HIDDEN, "customer_name", silent=True) is None
    assert tally.get_field_value(TallyField.HIDDEN, "customer_email", silent=True) is None


def test_pcf_text_fields(webhook_response2):
    """Test text input fields in the webhook response."""
    tally = Tally(webhook_response2)

    assert tally.get_field_value(TallyField.TEXT, "Customer Name") == "Rohit"
    assert tally.get_field_value(TallyField.TEXT, "Customer Email") == "rohit@rohit.com"


def test_pcf_multiple_choice_fields(webhook_response2):
    """Test multiple choice fields in the webhook response."""
    tally = Tally(webhook_response2)

    assert tally.get_field_value(TallyField.MULTIPLE_CHOICE, "set_by_setter") == ["Yes"]
    assert tally.get_field_value(TallyField.MULTIPLE_CHOICE, "live_transfer_call") == ["Yes"]
    assert tally.get_field_value(TallyField.MULTIPLE_CHOICE, "Call Outcome") == ["Showed"]


def test_pcf_checkboxes(webhook_response2):
    """Test checkbox fields in the webhook response."""
    tally = Tally(webhook_response2)

    assert tally.get_field_value(TallyField.CHECKBOXES, "sales_objection") == ["None (Closed)"]
    assert tally.get_field_value(TallyField.CHECKBOXES, "payment_structure") == ["PIF"]


def test_pcf_textarea_fields(webhook_response2):
    """Test textarea fields in the webhook response."""
    tally = Tally(webhook_response2)

    assert tally.get_field_value(TallyField.TEXTAREA, "notes_for_setter") == "NA"
    assert tally.get_field_value(TallyField.TEXTAREA, "customer_info") == "NA"
    assert tally.get_field_value(TallyField.TEXTAREA, "reason_for_noshow", silent=True) is None
    assert tally.get_field_value(TallyField.TEXTAREA, "reason_for_reschedule", silent=True) is None


def test_pcf_special_checkboxes(webhook_response2):
    """Test special checkboxes for blacklisting customers."""
    tally = Tally(webhook_response2)

    # No-show blacklist checkbox
    assert (
        tally.get_field_value(
            TallyField.CHECKBOXES,
            "If this customer has no-showed / cancelled more than twice, check this box to prevent them from ever booking again:",
            silent=True,
        )
        is None
    )

    # Reschedule blacklist checkbox
    assert (
        tally.get_field_value(
            TallyField.CHECKBOXES,
            "If this customer has re-scheduled more than twice, check this box to prevent them from ever booking again:",
            silent=True,
        )
        is None
    )


def test_pcf_empty_multiple_choice_fields(webhook_response2):
    """Test multiple choice fields with no value."""
    tally = Tally(webhook_response2)

    assert tally.get_field_value(TallyField.MULTIPLE_CHOICE, "customer_respond_to_calls", silent=True) is None
    assert tally.get_field_value(TallyField.MULTIPLE_CHOICE, "who_rescheduled", silent=True) is None
