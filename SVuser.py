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

def sanitise_input(input_string):
    # Remove any unwanted characters or patterns
    return re.sub(r'[^\w\s]', '', input_string)

def sanitise_email(input_string):
    # Remove any characters that are not allowed in email addresses
    return re.sub(r'[^a-zA-Z0-9._%+-@]', '', input_string)