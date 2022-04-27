import json
import importlib
from typing import Union
import os

import pandas as pd
import magic

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import numpy as np
import fhirdrill.utils as utils

# LOGGER = CONFIG.getLogger(__name__)


class BaseLoaderMixin:
    def sendResourcesToFiles(
        self,
        # TODO if None save to os.getcwd
        paths: list[str] = None,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        combine: bool = False,
    ):

        result = []
        if not input and self.isFrame:
            input = self.data
            if not paths:
                paths = self.paths
        elif input and not self.isFrame:
            input = self.prepareOperationInput(input, SyncFHIRResource)
        elif input and self.isFrame:
            # TODO raise error references and isFrame not allowed
            raise NotImplementedError

        n = len(input)
        paths = [os.path.abspath(e) for e in paths]

        if len(paths) == 1 and combine:
            with open(paths[0], "w", encoding="utf-8") as f:
                sobj = json.dumps(
                    input.apply(lambda x: x.serialize()).to_list(),
                    indent=4,
                    sort_keys=True,
                )
                f.write(sobj)
        elif len(paths) == len(input):
            pass
        else:
            raise Exception("number of paths and number of data blobs must be equal")

        successes = np.full(n, True)

        if not combine:
            for i, res, path in zip(range(n), input, paths):
                try:
                    with open(path, "a+", encoding="utf-8") as f:
                        sobj = json.dumps(res.serialize(), indent=4, sort_keys=True)
                        f.write(sobj)
                except Exception as e:
                    # TODO raise or log?
                    successes[i] = False

        return successes

    def sendBytesToFile(
        self,
        input: list[bytearray] = None,
        paths: list[str] = None,
        guessExtension: bool = False,
        combine: bool = False,
        params: dict = None,
    ):

        if not params:
            params = {}

        if not input and self.isFrame:
            input = self.data.values
            paths = self.path.values
        elif input and not self.isFrame:
            pass
        elif input and self.isFrame:
            raise NotImplementedError

        n = len(input)
        if len(paths) == 1 and combine:
            paths = [paths[0]] * n
        elif len(paths) == len(input):
            pass
        else:
            raise Exception("number of paths and number of data blobs must be equal")

        successes = np.full(n, True)

        for i, data, path in zip(range(n), input, paths):
            try:
                extension = utils.guessBufferMIMEType(bytes(data[:50]))
                abspath = os.path.abspath(path)
                if guessExtension:
                    abspath += "." + extension
                with open(abspath, "wb+") as f:
                    f.write(data)
            except Exception as e:
                successes[i] = False
                # TODO raise or log?

        return successes
