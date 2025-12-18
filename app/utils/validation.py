import math

# Cleanly split off of main 
def is_valid_price(value) -> bool:
    return value is not None and not math.isnan(value)