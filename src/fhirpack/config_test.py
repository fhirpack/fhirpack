from calendar import c
from charset_normalizer import detect
import pytest
import dotenv
from fhirpack.config import Config
from unittest import mock


@pytest.fixture()
def envFile(tmp_path):
    """Crates a temporary dot env file so the original one is not manipulated"""

    tempDir = tmp_path / "tmp"
    tempDir.mkdir()
    tempFile = tempDir / ".env"

    return tempFile


def test_initFromEmptyDic():
    """Tests configuration from default .env.example"""

    config = Config()
    configDic = config.data

    assert len(configDic) != 0


def test_loadConfig(envFile):

    dotenv.set_key(envFile, "test_one", "1")
    config = Config()
    config.loadConfig(envFile)

    assert "test_one" in dotenv.dotenv_values(envFile)


def test_get(envFile):

    dotenv.set_key(envFile, "test_one", "1")
    config = Config()
    config.loadConfig(envFile)

    assert config.get("test_one") == "1"


def test_set(envFile):

    config = Config()
    config.loadConfig(envFile)
    config.set("test_two", "2", saveToEnv=True)

    assert "test_two" in dotenv.dotenv_values(envFile)


def test_getLogger():
    config = Config()
    logger = config.getLogger(__name__)

    assert logger.name == __name__
