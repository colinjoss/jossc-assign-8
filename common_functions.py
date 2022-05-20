import re
from constants import *


name_pattern = re.compile("^[a-zA-Z0-9.' ]*$")
type_pattern = re.compile("^[a-zA-Z ]*$")


def get_entity(client, type, id):
    key = client.key(type, int(id))
    return client.get(key)


def new_boat(datastore, client, content):
    boat = datastore.entity.Entity(key=client.key(BOAT))
    boat.update({
        'name': content['name'],
        'type': content['type'],
        'length': content['length']
    })
    client.put(boat)
    boat['id'] = boat.key.id
    boat['self'] = URL + '/boats/' + str(boat.key.id)
    client.put(boat)
    return boat


def is_nonexistent(entity):
    return entity is None


def name_in_use(client, type, name):
    query = client.query(kind=type)
    results = list(query.fetch())
    for entity in results:
        if str(entity['name']) == str(name):
            return True
    return False


def valid(prop, input):
    if prop == 'name':
        return valid_name(str(input))
    elif prop == 'type':
        return valid_type(str(input))
    elif prop == 'length':
        return valid_length(input)
    else:
        return False


def valid_name(name):
    if len(name) > 33:          # Boat name cannot exceed 33 characters
        return False
    if name_pattern.match(name) is None:     # Boat name can only use letters, spaces, numbers, and periods
        return False
    return True


def valid_type(type):
    if len(type) > 255:         # Boat type cannot exceed 255 characters
        return False
    if type_pattern.match(type) is None:      # Boat type can only use letters and spaces
        return False
    return True


def valid_length(length):
    try:
        int(length)
        return True
    except:
        return False


def response_object(res, type, code, location=None):
    if location is not None:
        res.location = location
    res.mimetype = type
    res.status_code = code
    return res
