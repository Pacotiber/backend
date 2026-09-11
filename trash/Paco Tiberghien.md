#Paco Tiberghien 

    ...<5 lines>...
        tags=tags
    )
  File "C:\Users\Paco Tiberghien\iCloudDrive\Esilv\année 4\computerscience\backend\.venv\Lib\site-packages\pydantic\main.py", line 263, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 2 validation errors for Article
tags
  Input should be a valid list [type=list_type, input_value='Animal', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/list_type
category
  Input should be a valid string [type=string_type, input_value=['urine'], input_type=list]
    For further information visit https://errors.pydantic.dev/2.13/v/string_type
