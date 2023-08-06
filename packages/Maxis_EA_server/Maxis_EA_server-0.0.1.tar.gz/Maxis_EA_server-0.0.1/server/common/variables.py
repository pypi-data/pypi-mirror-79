"""
Constants
"""
import socket
import logging

DEFAULT_PORT = 2222
DEFAULT_IP_ADDRESS = '127.0.0.1'
# DEFAULT_IP_ADDRESS = socket.gethostbyname(socket.gethostname())
MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 4096
ENCODING = 'utf-8'

LOGGING_FORMATTER = logging.Formatter("%(asctime)s %(levelname)-8s %(filename)-12s %(message)s")

LOGGING_LEVEL = logging.DEBUG

SERVER_CONFIG = 'server.ini'

# Base keys

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Another keys

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_202 = {
    RESPONSE: 202,
    LIST_INFO: None
}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
RESPONSE_205 = {
    RESPONSE: 205
}

RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
