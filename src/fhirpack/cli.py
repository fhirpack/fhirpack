import argparse
import logging
import sys
import click
import fhirpack as fpack
import fhirpy as fp
import json
import warnings

from fhirpack import __version__

__author__ = "Jayson Salazar"
__copyright__ = "Jayson Salazar"
__license__ = ""

LOGGERPREFIX = "FHIRDRILL:"


logger = logging.getLogger(__name__)


def info(msg):
    logger.info(f"{LOGGERPREFIX} {msg}")


def processParams(string: str) -> dict:
    string = string.split(",")
    params = {}
    for s in string:
        s = s.replace(" ", "")
        p = s.split("=")
        params[p[0]] = p[1]
    return params


def setupLogging():
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="The pack for your FHIR server.",
)
@click.version_option()
@click.option(
    "-s",
    "--source",
    type=str,
    default=None,
    help="URL of the FHIR server or path to json files.",
)
@click.option(
    "-d",
    "--destination",
    type=str,
    default=None,
    help="Location of the output.",
)
@click.option(
    "-o",
    "--operation",
    type=str,
    default=[],
    multiple=True,
    help="Operations to retrieve data.",
)
@click.option(
    "-p",
    "--params",
    type=str,
    default=[],
    help="Provide additional search parameters.",
    multiple=True,
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    help="Print results in verbose format.",
    show_default=True,
    is_flag=True,
)
def main(source, params, operation, destination, verbose):

    setupLogging()
    info("execution started")

    fromFile = False

    # build client from source argument
    # if not source argument is passed, .env.example is used
    if not source:
        pack = fpack.PACK()

    # only json files are supported as source
    elif "json" in source:
        warnings.warn(
            "When operating on Files, only transformation functions will work."
        )
        fromFile = True
        client = fp.SyncFHIRClient("")
        pack = fpack.PACK(client)
        source = source.replace(",", "").split(" ")
    else:
        client = fp.SyncFHIRClient(source)
        pack = fpack.PACK(client)

    result = None

    # build searchParams for operations from input params
    searchParamsList = []
    if params:
        for p in params:
            # processParams() creates a key:value pair from the input param
            searchParamsList.append(processParams(p))

    # execute operations
    if operation:
        if fromFile:
            # this pack does not have client connection
            # only transformations can be performed
            pack = pack.getFromFiles(source)

        for op in operation:
            searchParams = {}
            if params and searchParamsList:
                searchParams["searchParams"] = searchParamsList.pop(0)

            # turn argument into respecive method
            desiredOperation = op.replace(",", "").split(" ")
            packEquivalentFunc = getattr(pack, desiredOperation.pop(0))

            # exectue method, with associated search parameters
            result = packEquivalentFunc(desiredOperation, **searchParams)
            pack = result

    if destination:

        destination = destination.replace(",", "").split(" ")
        jsonString = result.to_json(date_format="iso")
        jsonParsed = json.loads(jsonString)

        for d in destination:
            with open(d, "w") as f:
                json.dump(jsonParsed, f, ensure_ascii=False, indent=4)
    else:
        if verbose:
            try:
                click.echo(result.pretty)
            except:
                click.echo(result.to_json())

        else:
            click.echo(result)

    info("execution ended.")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
