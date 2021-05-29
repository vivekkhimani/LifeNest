import firebase_admin
from firebase_admin import credentials, auth, exceptions
import logging

logger = logging.getLogger(__name__)

config = {
    "type": "service_account",
    "project_id": "lifenest-315103",
    "private_key_id": "8c309a82e9fcc8a438a1b65642eef41af3e320b7",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3sbYGXYISiUFT\nOZ+PNgyzNUJ3wjTq4kmPpiRWnFkwKc2MiTc5XFHLPk9J1NHcKuyKB3MU40LlS8kP\n/pX7awaeZWFlEHPlwNs8YeR6kfZ4KrL5kkTo81IlU3M7fwdBlXcEii6c/3pOdXaq\nFOsKPLoyR/nS3z4ZCHYHJ24pLJmYv+xQQHkqvsCQUPzWAAI/HtkHkN77sON66a56\nfNGHBt7SrPuszwRx6KdcCWjyj8oIcOgjzafZtqTwKWRSGJWlSf5GjJD2ATIzkEbr\nmYPpS5rZ0vBpdhoCNL5kduW4P65BOq9gasA7q+VtqF9mXqL/AZ5XYmssHbB9A4J6\nBWlxaUJtAgMBAAECggEAVo7ZYHd4fsaJby+UdbW410st9mOfbtzRX+yga+WBi1Xv\nYx0XViKf8j76uqYbe30Id+QZwMpz77s905kZ0F52wHWyJp7Rlf5B8FqKgI0+EBLC\nwiI/8WsSlr8TagIqB6fn7M42N8mUttrX3z47INhLvry2xjxmtQINJ8LXQHShLd3X\nCWiw3dhctP9qZJYXRl6fjG6Zc1lS9cDRGauw2XPIk1U8q6xrf04yPbFP2RA2MeUn\nKwl/a07BQa6Ydw3zQaBN1UjldZkjjdVmO/TJWzB2UX+nn01l5EpjSQSC6m3HWktu\nwPEoKE4GMO5mYGSgczRJS/xshECLW0JvGBWiIJqbawKBgQD+H5pAvlnEa2Ebo1ZS\n2r8TjRCpDfaBgFExSuWx1boE27dAySwqfXl+UNuj6aMvF5pth681ps/75Y73eLrZ\nhJrPcaQTE8POgXrtv6Wlw6KcOCN5zvFzAE2ZV4SIWp5VQVcwyh2Z7Dqo7zW/k6ye\n+/e61jSdtyvLTmoDRFFVC1CajwKBgQC5DPfjhguTS/GFnvkE6vR3IsCn+r6trAb4\nzpO7rf7hxc2eusqx1a6I/G0+dLYU1iiTc+EMY80C4/MHbDc2xiBlfDsUnLq6rzP9\np22lUjCm+d88c4oialjqtDTlCU0XqLxx+J1LTby+WWEeMZiwCK+mjDxRYfPb6EzS\ncnDJLgXBQwKBgQDpzBt3q2kdPAmIivrVmakoDKWiU1VSicKpThYLSe4toBN2CF+Y\n6/3GCBA7Oq3GmrmaQbYh70n0n5ur9Kg7jTN83Tmtz4ZbTGbTq3l0C4xkm4WQAKPF\nQScjiBBH/s8i8s2L9rfLMDo7yHCzw+KSFpExlPetjqM9FfSU8tq9Gn7a4wKBgErx\ns5tT+HApO6GwJo4VUfjF/FyLspnHp/MwRqil6Soq4AG/CMRJFCyqftvijLOXoEtH\njQdli+v1wcFp1Fq8lvZC//JzHzToLBg4rLFdvhKB9CUZbgJOK8CyRxHTWIOSdO97\njsimrSAyNqDx2TLB8dFzziHvl8GiLSq16nOvzejdAoGBAMxspjSfYpMe0yAAaPkl\nVyDdsnOVp/gNwxKODdOmB+r0gfFKqhImFdcGkKYEjrNM2BJF4k/lp166jqE2tTsf\n8n5CXqvVuBJuIMpIwdp6Ra7/hoTYyg9fZVUz0FZ7p4qp3VMlIbRbtm2ABHPYSuPu\nckOHRi8Ho+vc2QhY9dBsCRX0\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-7kmot@lifenest-315103.iam.gserviceaccount.com",
    "client_id": "109233227251753806901",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7kmot%40lifenest-315103.iam.gserviceaccount.com"
}


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
