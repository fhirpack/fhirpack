import logging
import dotenv
import requests
from pathlib import Path
from enum import Enum
from typing import Union
import magic


from fhirpy import SyncFHIRClient
import fhirpack.exceptions as exceptions
import fhirpack as fp

logger = logging.getLogger(__name__)


def valuesForKeys(data: Union[dict, list], lookupKeys: list):

    lookup_keys = list(set(lookupKeys))

    if isinstance(data, dict):
        for k, v in data.items():
            if k in lookup_keys and not isinstance(v, list) and not isinstance(v, dict):
                yield v
            else:
                yield from valuesForKeys(v, lookupKeys)

    elif isinstance(data, list):
        for item in data:
            yield from valuesForKeys(item, lookupKeys)


def keys(obj, prefix=""):

    separator = ""
    if prefix:
        separator = "."
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{prefix}{separator}{k}"
            yield from keys(v, f"{prefix}{separator}{k}")
    elif isinstance(obj, list):
        for item in obj:
            yield from keys(item, prefix)


def getInstallationPath():
    return Path(fp.__file__).parent


def clientFromEnv():

    DOTENVPATH = dotenv.find_dotenv()
    CONFIG = dotenv.dotenv_values(DOTENVPATH)
    logger.info(f"found .env file at {DOTENVPATH}")
    logger.info(f"found {len(CONFIG)} key-value pairs in .env file")
    logger.info(f"found .env file at {DOTENVPATH}")
    logger.info(f"found {CONFIG} key-value pairs in .env file")

    LOGINURL = CONFIG["LOGINURL"]

    basicAuth = requests.auth.HTTPBasicAuth(CONFIG["USERNAME"], CONFIG["PASSWORD"])

    OAUTHTOKEN = requests.get(LOGINURL, auth=basicAuth).text
    dotenv.set_key(DOTENVPATH, "OAUTHTOKEN", OAUTHTOKEN)

    logger.info(f"acquired OAuth token: {False if OAUTHTOKEN is None else True}")

    AUTHHEADER = f"Bearer {OAUTHTOKEN}"
    logger.info(f"FHIR authorization header: {AUTHHEADER[:-30]}")

    APIBASE = CONFIG["APIBASE"]
    client = SyncFHIRClient(APIBASE, authorization=AUTHHEADER)
    return client


# TODO implement


def textToAscii():
    return None


def guessBufferMIMEType(bytes: bytes):

    guessedType = magic.from_buffer(bytes, mime=True).split("/")
    if len(guessedType) == 2:
        return guessedType[1]
    else:
        return None


def flattenList(input: list):
    for i in input:
        if isinstance(i, list):
            yield from flattenList(i)
        else:
            yield i


def validateFrame(frame):

    if frame.client is None:
        raise exceptions.ServerConnectionException(
            "No server connection. For this operation, a server connection is required."
        )
    if frame.isnull().values.any():
        raise exceptions.InvalidInputDataException(
            "Frame must not contain null values."
        )
    if not "data" in frame.columns:
        raise exceptions.InvalidInputDataException(
            "Frame must contain a 'data' column."
        )
    if isinstance(frame.data.values[0], list):
        raise exceptions.InvalidInputDataException(
            "Frame object must not contain lists. Most likely, use .explode()"
        )


# TODO decide whether we need an alternative not in Frame/PACK

# def getURLBytes(
#         input: list[str]= None,
#         params: dict = {},
#     ):
#         if not params:
#             params = {}

#         print(input)

#         results=[]
#         for i,url in zip(range(len(input)),input):
#             response = requests.get(
#                 url[0],
#                 # headers=params['headers'],
#                 headers=self.client._build_request_headers(),
#                 stream=True
#             )

#             data=bytearray()

#             if not response.ok:
#                 raise Exception(f"{response}")
#             for block in response.iter_content(1024):
#                 data.extend(block)
#                 if not block:
#                     break
#             results.append(data)

#         return data
