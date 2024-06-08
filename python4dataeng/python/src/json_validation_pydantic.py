from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

class MyDataModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = "No description provided"
    age: Optional[int]

    @field_validator('age', mode='before')
    def set_default_age(cls, v):
        return v or 0

# Valid JSON
valid_json = {
    "id": 123,
    "name": "Valid Example",
    "description": "This is a valid example.",
    "age": 30
}

# Invalid JSON
invalid_json = {
    "id": "not-an-integer",
    "name": "Invalid Example"
}

# Validate the valid JSON
try:
    valid_data = MyDataModel(**valid_json)
    print("Valid JSON:", valid_data)
except ValidationError as e:
    print("Validation error in valid JSON:", e.json())

# Validate the invalid JSON
try:
    invalid_data = MyDataModel(**invalid_json)
    print("Invalid JSON:", invalid_data)
except ValidationError as e:
    print("Validation error in invalid JSON:", e.json())

# # Save the valid JSON to a file
# with open('valid_json.json', 'w') as f:
#     json.dump(valid_json, f, indent=4)

# # Save the invalid JSON to a file
# with open('invalid_json.json', 'w') as f:
#     json.dump(invalid_json, f, indent=4)
