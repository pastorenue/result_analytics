from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    """
    Used during JSON serialization to convert Decimal() types to a float JSON representation.
    """
    def default(self, obj):
        from decimal import Decimal
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)