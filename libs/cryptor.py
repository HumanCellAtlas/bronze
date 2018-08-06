import pickle
import codecs


__all__ = ['decrypt_from_environment_variable_with_base64',
           'encrypt_dict_to_string_with_base64']


def decrypt_from_environment_variable_with_base64(env):
    raw_env = env.replace(r'\n', '\n')
    return pickle.loads(codecs.decode(raw_env.encode(), 'base64'))


def encrypt_dict_to_string_with_base64(dic):
    return codecs.encode(pickle.dumps(dic), 'base64').decode()
