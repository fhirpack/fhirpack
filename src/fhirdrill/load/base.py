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


    def sendDICOMToFiles(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        combine: bool = False,
        params: dict = None,
        ignoreFrame: bool = False,
    ):
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        
        if input:
            raise NotImplementedError
            # input = self.castOperand(input, SyncFHIRReference, "replace")
            # result = self.getResources(input, resourceType="replace", raw=True)

        elif self.isFrame and not ignoreFrame:
            input = self
            paths = self.path.values
        
            n = len(input)
            if len(paths) == 1 and combine:
                paths = [paths[0]] * n
            elif len(paths) == len(input):
                pass
            else:
                raise Exception("number of paths and number of data blobs must be equal")
            
            if self.resourceTypeIs("ImagingStudy"):

                input.path.apply(
                    lambda x: os.makedirs(x, exist_ok=True)
                )
                
                results=input.apply(
                    lambda x: x.data.save_as(x.path+'/'+x.data.SOPInstanceUID),
                    axis=1
                )
                
        #             newStudyInstanceUID = str(instance.StudyInstanceUID)

        #             try:
        #                 desc = str(instance.SeriesDescription)
        #             except:
        #                 desc = "No Description"
        #             save_dir = f"oliver/{newStudyInstanceUID}/{desc}"
        #             os.makedirs(save_dir, exist_ok=True)
        #             instance.save_as(f"{save_dir}/{instance.SOPInstanceUID}.dcm")
            
        #     except KeyboardInterrupt: raise 
        #     except Exception as e:
        #         print(e)
        #         pass

        #     time.sleep(0.5)
        #     results.append(data)
        # if resultInCol:
        #     result = self.assign(**{resultInCol: results})
        # else:
        #     result = se


                # result = input.apply(
                #     lambda x: self.searchResources(
                #         searchParams=dict(searchParams, **{"replace": x.id}),
                #         resourceType="replace",
                #         raw=True,
                #     )
                # )
                # result = result.values

            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

        result = self.prepareOutput(result)

        return result

