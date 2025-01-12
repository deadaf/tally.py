from tally.types import TallyField


class Tally:
    def __init__(self, webhook_body: dict):
        self.webhook_body = webhook_body

    @property
    def form_name(self) -> str | None:
        """Get the name of the form from the tally webhook body."""
        return self.webhook_body.get("formName")

    def get_field_value(self, field_type: TallyField, field_label: str, silent: bool = False):
        """
        Get the value of a field from the tally webhook body.

        :param field_type: The type of the field to get the value of.
        :param field_label: The label of the field to get the value of.
        :param silent: If True, the function will not raise an error if the field is not found.

        :return: The value / values of the field if found, otherwise None.

        :raises ValueError: If the field is not found and silent is False.
        """

        for field in self.webhook_body.get("fields", []):
            if field_type == TallyField.CHECKBOXES:
                # Special case for CHECKBOXES: Aggregate all sub-checkboxes with value=True
                return self._get_checkbox_values(field_label)

            elif field.get("type") == field_type.value and field.get("label") == field_label:
                return self._extract_field_value(field)

        if not silent:
            raise ValueError(f"Field with label '{field_label}' and type '{field_type}' not found.")
        return None

    def _extract_field_value(self, field: dict):
        """
        Extract the value from a field, handling field-specific cases.

        :param field: The field dictionary.
        :return: The extracted value.
        """
        field_type = field.get("type")

        if field_type in (TallyField.MULTIPLE_CHOICE.value, TallyField.DROPDOWN.value, TallyField.MULTI_SELECT.value):
            return self._get_option_texts(field)

        if field_type == TallyField.FILE_UPLOAD.value:
            return self._get_file_info(field)

        return field.get("value")

    def _get_checkbox_values(self, main_label: str) -> list[str] | None:
        """
        Extract the 'text' values of selected checkboxes from the main checkbox field.

        :param main_label: The label of the main checkbox field.
        :return: A list of texts for selected checkboxes or None if no matching checkboxes are found.
        """
        # Step 1: Find the main checkbox field
        for field in self.webhook_body.get("fields", []):
            if field.get("label") == main_label and field.get("type") == TallyField.CHECKBOXES.value:
                options = field.get("options", [])
                option_map = {option["id"]: option["text"] for option in options}

                # Step 2: Match sub-checkboxes' values (True) to option IDs
                selected_texts = []
                for sub_field in self.webhook_body.get("fields", []):
                    if sub_field.get("key").startswith(field.get("key")) and sub_field.get("value") is True:
                        option_id = sub_field.get("key").split("_")[-1]
                        if option_id in option_map:
                            selected_texts.append(option_map[option_id])

                return selected_texts if selected_texts else None  # Explicitly return None if no selections

        # Raise an error if the main checkbox field is not found
        raise ValueError(f"Main checkbox with label '{main_label}' not found.")

    def _get_option_texts(self, field: dict) -> list[str] | None:
        """
        Extract the text of selected options for fields like MULTIPLE_CHOICE, DROPDOWN, and MULTI_SELECT.

        :param field: The field dictionary.
        :return: A list of texts corresponding to selected options, or None if no value is provided.
        """
        value_ids = field.get("value", [])
        if value_ids is None:  # Handle case where value is None
            return None

        options = field.get("options", [])
        return [option["text"] for option in options if option["id"] in value_ids]

    def _get_file_info(self, field: dict) -> list[dict]:
        """Extract file information from a FILE_UPLOAD field."""
        return field.get("value", [])
