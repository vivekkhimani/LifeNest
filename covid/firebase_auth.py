import firebase_admin
from firebase_admin import credentials, auth, exceptions
import logging
from covid.secrets import config

logger = logging.getLogger(__name__)


def find_user(phone):
    try:
        out = auth.get_user_by_phone_number(phone)
        return True
    except auth.UserNotFoundError:
        return False
    except ValueError as ex:
        logger.error("The phone number if malformed or None: %s", ex)
        return False
    except exceptions.FirebaseError as ex:
        logger.critical("Firebase error while retrieving the data for %s", ex)
        return False


def delete_user(phone):
    user_instance = auth.get_user_by_phone_number(phone)
    try:
        auth.delete_user(user_instance.uid)
    except ValueError as ex:
        logger.error("The uid for deletion is malformed or None: %s", ex)
        return False
    except exceptions.FirebaseError as ex:
        logger.critical("Firebase error while deleting the data for uid: %s", ex)
        return False


def phone_auth_initialize():
    cred = credentials.Certificate(config)
    firebase_admin.initialize_app(cred, {'projectId': 'lifenest-315103'})


# driver
if __name__ == '__main__':
    phone_auth_initialize()
    out = find_user('+12675309712')
    print(out)
    delete_user('+12675309712')
