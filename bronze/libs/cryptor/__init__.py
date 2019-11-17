import pickle
import codecs
import json


__all__ = [
    'decrypt_from_environment_variable_with_base64',
    'encrypt_dict_to_string_with_base64',
]


def decrypt_from_environment_variable_with_base64(base64string: str):
    """Decrypt from a string."""
    raw_env = base64string.replace(r'\n', '\n')
    return pickle.loads(codecs.decode(raw_env.encode(), 'base64'))


def encrypt_dict_to_string_with_base64(dic: dict):
    """This is a helper function for creating the string from a credential dictionary."""
    return codecs.encode(pickle.dumps(dic), 'base64').decode()


def encrypt_file_to_string_with_base64(path_to_json_file: str):
    """This is a helper function for creating the string from a credential file."""
    with open(path_to_json_file) as f:
        dic = json.load(f)
    return encrypt_dict_to_string_with_base64(dic)
