from enum import Enum


class TallyField(Enum):
    TEXT = "INPUT_TEXT"
    NUMBER = "INPUT_NUMBER"
    HIDDEN = "HIDDEN_FIELDS"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    EMAIL = "INPUT_EMAIL"
    PHONE_NUMBER = "INPUT_PHONE_NUMBER"
    FORM_NAME = "formName"
    TEXTAREA = "TEXTAREA"
    LINK = "INPUT_LINK"
    CHECKBOXES = "CHECKBOXES"
    DROPDOWN = "DROPDOWN"
    MULTI_SELECT = "MULTI_SELECT"
    FILE_UPLOAD = "FILE_UPLOAD"
    DATE = "INPUT_DATE"
    TIME = "INPUT_TIME"