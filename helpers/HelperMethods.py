def relationship_status_calculator(points):
    status = ''
    if -100 <= points <= -50:
        status = 'enemies'
    elif -51 <= points <= -31:
        status = 'cold'
    elif -31 <= points <= 31:
        status = 'acquaintances'
    elif 31 <= points <= 51:
        status = 'warm'
    elif 51 <= points <= 81:
        status = 'friends'
    elif 81 <= points <= 101:
        status = 'crushes'
    elif 101 <= points <= 111:
        status = 'lovers'

    return status