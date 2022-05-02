import logging
import dotenv
import requests
import os
from enum import Enum
from typing import Union
import magic

from fhirpy import SyncFHIRClient
import fhirdrill as fd

logger = logging.getLogger(__name__)


def valuesForKeys(data: Union[dict, list], lookup_keys: list):

    lookup_keys = list(set(lookup_keys))

    if isinstance(data, dict):
        for k, v in data.items():
            if k in lookup_keys and not isinstance(v, list) and not isinstance(v, dict):
                yield v
            else:
                yield from valuesForKeys(v, lookup_keys)

    elif isinstance(data, list):
        for item in data:
            yield from valuesForKeys(item, lookup_keys)


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
    return os.path.dirname(fd.__file__)


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
    if input == []:
        return input
    if isinstance(input[0], list):
        return flattenList(input[0]) + flattenList(input[1:])
    return input[:1] + flattenList(input[1:])


# TODO decide whether we need an alternative not in Frame/Drill

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
