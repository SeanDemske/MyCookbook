# Utility Functions

def password_confirmed(password, password_confirmation):
    """Checks to see if passwords match"""

    if password == password_confirmation:
        return True
    else:
        return False