import json
import jsonschema
from jsonschema import validate
from pprint import pprint
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

# Define Pydantic Model
class Transaction(BaseModel):
    InvoiceNo: int
    StockCode: int
    Description: Optional[str] = None
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: Optional[str] = None

    @field_validator('Country', mode='before')
    def set_default_country(cls, v):
        return v or "Unknown"

# JSON Schema Definition
transaction_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "InvoiceNo": {"type": "integer"},
        "StockCode": {"type": "integer"},
        "Description": {"type": "string"},
        "Quantity": {"type": "integer"},
        "InvoiceDate": {"type": "string"},
        "UnitPrice": {"type": "number"},
        "CustomerID": {"type": "integer"},
        "Country": {"type": "string"}
    },
    "required": ["InvoiceNo", "StockCode", "Quantity", "CustomerID", "InvoiceDate", "UnitPrice"]
}

# Validation Functions
def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True

def validate_json_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False, f"Given JSON data is not valid: {err.message}"
    return True, "Given JSON data is valid."

# Load JSON data from file
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

if __name__ == '__main__':
    # File path to your JSON file
    file_path = "./data/data_subset.json"
    
    # Load JSON data
    data = load_json_file(file_path)

    # Validate using Pydantic
    try:
        for record in data:
            transaction = Transaction(**record)
            print("Valid JSON with Pydantic:", transaction)
    except ValidationError as e:
        print("Validation error with Pydantic:", e.json())

    # Validate using JSON Schema
    for record in data:
        is_valid, message = validate_json_schema(record, transaction_schema)
        print(message)

    # Validate JSON strings
    valid_json_string = json.dumps(data[0])
    invalid_json_string = '{"InvoiceNo": 536370 "StockCode": 22492, "Description": "MINI PAINT SET VINTAGE", "Quantity": 36, "InvoiceDate": "12/1/2010 8:45", "UnitPrice": 0.65, "CustomerID": 12583, "Country": "France"}'

    print("Valid JSON string:", validate_json(valid_json_string))
    print("Invalid JSON string:", validate_json(invalid_json_string))

    # Additional test cases
    customer_id_missing_dict = {
        "InvoiceNo": 536370,
        "StockCode": 22492,
        "Description": "MINI PAINT SET VINTAGE",
        "Quantity": 36,
        "InvoiceDate": "12/1/2010 8:45",
        "UnitPrice": 0.65,
        "Country": "France"
    }
    invoice_no_is_a_string = {
        "InvoiceNo": "536370",
        "StockCode": 22492,
        "Description": "MINI PAINT SET VINTAGE",
        "Quantity": 36,
        "InvoiceDate": "12/1/2010 8:45",
        "UnitPrice": 0.65,
        "CustomerID": 12583,
        "Country": "France"
    }

    print("Validation result for missing CustomerID:")
    validate_json_schema(customer_id_missing_dict, transaction_schema)

    print("Validation result for InvoiceNo as a string:")
    validate_json_schema(invoice_no_is_a_string, transaction_schema)
