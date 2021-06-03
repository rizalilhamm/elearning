class SchemaValidationError(Exception):
    pass

class ExtentionError(Exception):
    pass

errors = {
    "SchemaValidationError": {
        "message": "Something was wrong",
        "status": 400
    },
    "ExtentionError": {
        "message": "Extention not Allowed",
        "status": 400
    } 
}