import json
from typing import Union
import os

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import numpy as np
import fhirpack.utils as utils

# LOGGER = CONFIG.getLogger(__name__)


class BaseLoaderMixin:
    # TODO rename sendResourcesToJSON
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
        """Serializes the input to JSON and saves it to the specified paths.

        Args:
            paths (list[str], optional): Paths to save the JSON files to. Defaults to None.
            input (list[str], list[SyncFHIRReference], list[SyncFHIRResource], optional): Input to serialize. Defaults to None.
            combine (bool, optional): If True, all input is combined into one file. Defaults to False.

        Raises:
            NotImplementedError: If input is a DataFrame and ignoreFrame is False.
            Exception: If the number of paths and the number of input blobs do not match.

        Returns:
            list[bool]: List of booleans indicating whether the operation was successful.
        """

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
        """Saves the input to the specified paths.

        Args:
            input (list[bytearray], optional): Input to save. Defaults to None.
            paths (list[str], optional): Paths to save the input to. Defaults to None.
            guessExtension (bool, optional): If True, the extension is guessed from the first 50 bytes of the input. Defaults to False.
            combine (bool, optional): If True, all input is combined into one file. Defaults to False.
            params (dict, optional): Additional parameters. Defaults to None.

        Raises:
            NotImplementedError: If input is a DataFrame and ignoreFrame is False.
            Exception: If the number of paths and the number of input blobs do not match.

        Returns:
            list[bool]: List of booleans indicating whether the operation was successful.
        """
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

    def sendToTable(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        # combine: bool = False,
        params: dict = None,
        ignoreFrame: bool = False,
        fileType: str = "csv",
        # TODO enforce existence of paths in checks
        paths: list[str] = None,
    ):
        """Saves the input in csv format to the specified paths.

        Args:
            input (Union[ list[str], list[SyncFHIRReference], list[SyncFHIRResource], ], optional): Input to save. Defaults to None.
            params (dict, optional): Additional parameters. Defaults to None.
            ignoreFrame (bool, optional): If True, the input is ignored if the object is a DataFrame. Defaults to False.
            fileType (str, optional): The file type to save the input as. Defaults to "csv".
            paths (list[str], optional): Paths to save the input to. Defaults to None.

        Raises:
            NotImplementedError: If input is a DataFrame and ignoreFrame is False.
            NotImplementedError: If the number of paths and the number of input blobs do not match.
            ValueError: If fileType is not csv or xls.
            NotImplementedError: If more than one path is specified.
        """
        params = {} if params is None else params
        input = [] if input is None else input
        paths = [] if paths is None else paths
        result = []

        if len(input):
            raise NotImplementedError
            # input = self.castOperand(input, SyncFHIRReference, "replace")
            # result = self.getResources(input, resourceType="replace", raw=True)
        try:
            if self.isFrame and not ignoreFrame:
                input = self

                if len(paths) > 1:
                    raise NotImplementedError

                if fileType not in ["csv", "xls"]:
                    raise ValueError(str(fileType) + " not supported. Use csv, xls.")

                path = f"{paths[0]}.{fileType}"

                if "/" in path:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                else:
                    path = f"./{path}"

                if fileType == "xls":
                    raise ValueError("XLS not yet supported.")
                    # TODO: disabled until the env has an xls engine
                    # inFrame.to_excel(path, engine="xlsxwriter", sheet_name="cohort")
                elif fileType == "csv":
                    input.to_csv(path_or_buf=path, index=False)
                else:
                    raise NotImplementedError

            else:
                raise NotImplementedError

            result = [True]

        except Exception as e:
            raise e

        result = self.prepareOutput(result)

        return result

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
        """Saves the input in the dicom format to the specified paths.

        Args:
            input (Union[ list[str], list[SyncFHIRReference], list[SyncFHIRResource], ], optional): Input to save. Defaults to None.
            combine (bool, optional): If True, all input is combined into one file. Defaults to False.
            params (dict, optional): Additional parameters. Defaults to None.
            ignoreFrame (bool, optional): If True, the input is ignored if the object is a DataFrame. Defaults to False.

        Raises:
            NotImplementedError: If input is a DataFrame and ignoreFrame is False.
            Exception: If the number of paths and the number of input blobs do not match.
            NotImplementedError: If more than one path is specified.
            NotImplementedError: If the resource type is not ImagingStudy.
        """
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
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
                raise Exception(
                    "number of paths and number of data blobs must be equal"
                )

            if self.resourceTypeIs("ImagingStudy"):
                input.path.apply(lambda x: os.makedirs(x, exist_ok=True))

                result = input.apply(
                    lambda x: x.data.save_as(x.path + "/" + x.data.SOPInstanceUID),
                    axis=1,
                )

            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

        result = self.prepareOutput(result)

        return result
