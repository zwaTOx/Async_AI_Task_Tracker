def get_stmp(email):
    pattern = 'smtp.'
    domain_name = email.split('@')[1]   
    return pattern+domain_name, 587

