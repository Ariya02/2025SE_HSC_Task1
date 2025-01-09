import re  #import regular expression 

def validate_password(password):
    if len(password) < 8 or len(password) > 12:
        return "Password must be between 8 and 12 characters long."
    if not re.search(r'\d', password):
        return "Password must contain at least one digit."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    return None

def validate_email(email):
    email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if not re.match(email_regex, email):
        return "Invalid email address."
    return None

def sanitise_input(input_data):
    # Removes potentially harmful characters (<>), scripts cannot be injected 
    sanitized_data = re.sub(r'[<>]', '', input_data)
    return sanitized_data