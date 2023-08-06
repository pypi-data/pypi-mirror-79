from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class DefaultValidator(Validator):

  def __init__(self, default_value: Any) -> None:
    self.default_value = default_value

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
    pass

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
    if value is None:
      if callable(self.default_value):
        return self.default_value()
      else:
        return self.default_value
    else:
      return value
