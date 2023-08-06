# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import uuid



from .log import logger
from .parser import Parser
from .display import Display
from .ipython_api import IPythonAPI
from .constants import Constants, CryptoParam, SsoStorageParam, SsoEnvVarParam, SsoStorage, SsoCrypto

from .dict_db_storage import DictDbStorage


_SUPPORTED_STORAGE = [
    SsoStorage.IPYTHON_DB
]


_SUPPORTED_CRYPTO = [
    SsoCrypto.DPAPI
]


def get_sso_store(cache_selector_key:str=None, **options) -> SsoStorage: #pylint: disable=no-method-argument
    encryption_keys_string = os.getenv(Constants.SSO_ENV_VAR_NAME)
    if not encryption_keys_string:
        # Display.showWarningMessage(f"Warning: SSO is not activated because environment variable {SSO_ENV_VAR_NAME} is not set")
        return

    key_vals = Parser.parse_and_get_kv_string(encryption_keys_string, {})
    cache_name = key_vals.get(SsoEnvVarParam.CACHE_NAME)  
    secret_key = key_vals.get(SsoEnvVarParam.SECRET_KEY)
    secret_salt_uuid = key_vals.get(SsoEnvVarParam.SECRET_SALT_UUID)
    crypto = key_vals.get(SsoEnvVarParam.CRYPTO)
    storage = key_vals.get(SsoEnvVarParam.STORAGE)

    if storage in _SUPPORTED_STORAGE:
        pass
    elif storage is None:
        Display.showWarningMessage(f"Warning: SSO is not activated due to environment variable {Constants.SSO_ENV_VAR_NAME} is missing {SsoEnvVarParam.STORAGE} key/value")
        return
    else:
        Display.showWarningMessage(f"Warning: SSO is not activated due to {storage} storage is not supported")
        return

    if storage == SsoStorage.IPYTHON_DB:
        if not(cache_name):
            Display.showWarningMessage(f"Warning: SSO is not activated due to environment variable {Constants.SSO_ENV_VAR_NAME} is missing {SsoEnvVarParam.CACHE_NAME} key/value")
            return  

    if crypto in _SUPPORTED_CRYPTO:
        pass
    elif crypto is None:
        Display.showWarningMessage(f"Warning: SSO is not activated due to environment variable {Constants.SSO_ENV_VAR_NAME} is missing {SsoEnvVarParam.CRYPTO} key/value")
        return
    else:
        Display.showWarningMessage(f"Warning: SSO is not activated due to {crypto} cryptography is not supported")
        return

    crypto_obj = None
    if crypto == SsoCrypto.DPAPI:
        # from .dpapi_crypto import DpapiCrypto, dpapi_installed
        from .dpapi_crypto_msal import DpapiCrypto, dpapi_installed
        if  not dpapi_installed:
            Display.showWarningMessage(f"Warning: SSO is not activated due to {SsoCrypto.DPAPI} cryptography failed to install")
            return
        crypto_obj = DpapiCrypto()

    elif crypto == SsoCrypto.FERNET:
        from .fernet_crypto import FernetCrypto, fernet_installed, check_password_strength
        if  not fernet_installed:
            Display.showWarningMessage(f"Warning: SSO is not activated due to {SsoCrypto.FERNET} cryptography and/or password-strength modules are not found")
            return

        if not(secret_key):
            Display.showWarningMessage(f"Warning: SSO is not activated due to environment variable {Constants.SSO_ENV_VAR_NAME} is missing {SsoEnvVarParam.SECRET_KEY} key/value")
            return

        if not(secret_salt_uuid):
            Display.showWarningMessage(f"Warning: SSO is not activated due to environment variable {Constants.SSO_ENV_VAR_NAME} is missing {SsoEnvVarParam.SECRET_SALT_UUID} key/value")
            return

        hint = check_password_strength(secret_key)
        if hint:
            message = f"Warning: SSO could not be activated due to {SsoEnvVarParam.SECRET_KEY} key in environment variable {Constants.SSO_ENV_VAR_NAME} is too simple. It should contain: \n{hint}" 
            Display.showWarningMessage(message)
            return

        try:
            salt = uuid.UUID(secret_salt_uuid, version=4)            
        except:
            Display.showWarningMessage(f"Warning: SSO is not activated due to {SsoEnvVarParam.SECRET_SALT_UUID} key in environment variable {Constants.SSO_ENV_VAR_NAME} is not set to a valid uuid")
            return

        crypto_options = {
            CryptoParam.PASSWORD: f"{cache_name or ''}-{secret_key}",
            CryptoParam.SALT: salt,
            CryptoParam.LENGTH: 32
        }
        crypto_obj = FernetCrypto(crypto_options)
       
    if crypto_obj is not None:
        gc_ttl_in_secs = options.get('sso_db_gc_interval', 0) * Constants.HOUR_SECS #convert from hours to seconds
        storage_options = {
            SsoStorageParam.CACHE_SELECTOR_KEY: cache_selector_key,
            SsoStorageParam.CRYPTO_OBJ: crypto_obj,
            SsoStorageParam.CACHE_NAME: cache_name,
            SsoStorageParam.GC_TTL_IN_SECS: gc_ttl_in_secs
        }

        if storage == SsoStorage.IPYTHON_DB:
            db = IPythonAPI._get_ipython_db(**options)
            return DictDbStorage(db, storage_options)
