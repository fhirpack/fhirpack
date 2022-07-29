import warnings
from pandas import DataFrame
from fhirpy import SyncFHIRClient

from fhirpack.auth import AUTH_PARAMS_PRESETS
from fhirpack.auth import Auth

import fhirpack.base
import fhirpack.extraction
import fhirpack.transformation
import fhirpack.load
import fhirpack.custom
import fhirpack.utils as utils
from fhirpack.constants import CONFIG

LOGGER = CONFIG.getLogger(__name__)


class PACK(
    fhirpack.base.BaseMixin,
    fhirpack.extraction.ExtractorMixin,
    fhirpack.transformation.TransformerMixin,
    fhirpack.load.LoaderMixin,
    fhirpack.custom.PluginMixin,
):
    def __init__(
        self,
        apiBase=None,
        client=None,
        envFile=None,
        ignoreEnvFile=False,
        unconnected=False,
        authMethod=None,
        authParams=None,
    ):

        self.logger = CONFIG.getLogger(__name__)
        self.logger.info("PACK initialization started.")

        if envFile:
            CONFIG.loadConfig(envFile)
        elif not ignoreEnvFile:
            CONFIG.loadConfig()

        if client:
            self.client = client
        elif unconnected:
            self.client = SyncFHIRClient("")
        else:
            self.__setupClient(
                apiBase=apiBase, authMethod=authMethod, authParams=authParams
            )
            
        if self.connected:
            pass
        else:
            self.logger.info("PACK is not connected to server.")
            self.client = SyncFHIRClient("")

        self.logger.info("pack initialization finished")

    def __setupClient(self, apiBase=None, authMethod=None, authParams=None):

        authorization = None

        if apiBase is not None:
            CONFIG.set("APIBASE", apiBase)
            if authMethod:
                CONFIG.set("AUTH_METHOD", authMethod)
            if isinstance(authParams, dict) and authParams:
                pass
            elif isinstance(authParams, str) and authParams:
                authParams = AUTH_PARAMS_PRESETS[authParams]
        else:
            if CONFIG.get("AUTH_PARAMS_PRESET"):
                authParams = AUTH_PARAMS_PRESETS[CONFIG.get("AUTH_PARAMS_PRESET")]
            if CONFIG.get("AUTH_METHOD") == "oauth_password":
                token = Auth.getToken("password", authParams)
                CONFIG.set("OAUTH_TOKEN", token["access_token"]),
                authorization = f"Bearer {token['access_token']}"
            elif CONFIG.get("AUTH_METHOD") == "oauth_token":
                token = CONFIG.get("OAUTH_TOKEN")
                authorization = f"Bearer {token}"
            elif authMethod is None:
                authorization = None
            else:
                raise NotImplementedError

        self.client = SyncFHIRClient(CONFIG.get("APIBASE"), authorization=authorization)

    @property
    def connected(self):
        try:
            self.client._do_request("get", f"{self.client.url}/metadata")
            return True
        except:
            return False

    def authenticate(self, force: bool = False):
        if not self.connected or force:
            self.__setupClient()

    def countServerResources(self):

        results = []
        # TODO write function in utils to retrieve current installation path
        # TODO move path with others to common location, CONFIG?
        with open(f"{utils.getInstallationPath()}/data/supported.list") as f:
            while True:
                resource = f.readline().strip()
                if not resource:
                    break

                count = self.client.execute(
                    # TODO handle and test when slash at the end of APIBASE in .env and without
                    # WARNING path must either:
                    # 1. be relative and allow FHIRPy to parametrize the URL
                    # 2. be absolute and contain the params already as they will otherwise be ignored
                    resource,
                    method="get",
                    # if _count has the value 0, this shall be treated the same as _summary=count
                    # https://www.hl7.org/fhir/search.html#count
                    params={"_count": 0},
                ).total
                results.append((resource, count))
        results = DataFrame(results, columns=["resourceType", "count"])
        return results
