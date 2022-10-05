from datetime import datetime

import conda
from localdeps import conda_api, create_env, is_conda_environment, main, quote_package


def test_quote_package():
    p = "conda"
    assert quote_package(p) == p

    p = "conda>0.4.12"
    assert quote_package(p) == f'"{p}"'

    p = "conda<0.4.12"
    assert quote_package(p) == f'"{p}"'

    p = "conda==0.4.12"
    assert quote_package(p) == f'"{p}"'

    p = "conda pandas"
    assert quote_package(p) == "conda"


def test_conda_api():
    conda_api(conda.cli.python_api.Commands.INFO, [])


def test_create_env():
    now = datetime.now()
    env_name = f'testenv_{now.strftime("%m%d%Y%H%M%S")}'
    create_env(env_name)
    conda_api(
        conda.cli.python_api.Commands.REMOVE,
        ['--yes', '-n', env_name, '--all'],
    )


def test_is_conda_environment():
    now = datetime.now()
    env_name = f'testenv_{now.strftime("%m%d%Y%H%M%S")}'
    create_env(env_name)
    assert is_conda_environment(env_name)
    conda_api(
        conda.cli.python_api.Commands.REMOVE,
        ['--yes', '-n', env_name, '--all'],
    )


def test_is_not_conda_environment():
    now = datetime.now()
    env_name = f'testenv_{now.strftime("%m%d%Y%H%M%S")}'
    assert not is_conda_environment(env_name)
