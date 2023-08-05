from typing import List, Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator

class OneOfValidator(Validator):

  def __init__(self, str_list: List[str]) -> None:
    self.str_list = str_list

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
    if value is not None and value not in self.str_list:
      raise ValidationException(
        { key_path: f'Value \'{value}\' at \'{key_path}\' should be one of {self.str_list}.' },
        root
      )
