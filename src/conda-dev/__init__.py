"""
Allows the installation of dependencies extracted from the conda.recipe/meta.yaml file
"""
import argparse
import logging
import os
import subprocess
import sys

import conda.cli.python_api
import conda.exceptions
import conda_build.api
import conda_build.environ


CUR_DIR = os.getcwd()
PACKAGE_NAME = os.path.basename(CUR_DIR)
_LOGGER = logging.getLogger(PACKAGE_NAME)
_LOGGER.handlers = list()
_ch = logging.StreamHandler(sys.stdout)
_ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
_LOGGER.addHandler(_ch)


def quote_package(d):
    """Need to wrap packages with quote marks"""
    if '>' in d or '=' in d or '<' in d:
        d = '"{}"'.format(d)
    elif ' ' in d:
        d = d.split(' ')[0]
    return d


def conda_api(cmd_type, cmd_list):
    stdout, stderr, return_code = conda.cli.python_api.run_command(cmd_type, *cmd_list)
    _LOGGER.debug(
        '\n  cmd type: %s\n  cmd: %s\n  stdout: %s\n  stderr: %s\n  return_code: %s',
        cmd_type,
        ' '.join(cmd_list),
        stdout,
        stderr,
        return_code,
    )


def create_env(env_name):
    """Create the env, and clear it out if it already exists"""
    assert env_name != 'base'
    try:
        conda_api(
            conda.cli.python_api.Commands.REMOVE,
            ['--yes', '-n', env_name, '--all'],
        )
    except conda.exceptions.PackagesNotFoundError:
        # this happens when the env is already empty
        pass
    print("Creating env at: %s" % env_location)
    conda_api(
        conda.cli.python_api.Commands.CREATE,
        ['--yes', '-n', env_name],
    )


def is_conda_environment(env_name):
    stdout = subprocess.check_output("conda env list", shell=True).decode()
    stdout_lst = stdout.split()
    for item in stdout_lst[1::2]:
        if item == env_name:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description=('Create a conda environment with all dependencies'
                     ' for developing'),
    )
    parser.add_argument(
        '--env',
        type=str,
        default='dev-' + PACKAGE_NAME.replace(' ', '-'),
        help='The name of the development environment to be created',
    )
    parser.add_argument(
        '--conda_dir',
        type=str,
        default=os.path.join(CUR_DIR, '..', '.conda'),
        help='Path to the conda recipe',
    )
    parser.add_argument(
        '--replace_env',
        type=bool,
        default=False,
        help='Whether to destroy and recreate the passed environment',
    )
    parser.add_argument(
        '--conda_version',
        type=str,
        default='',
        help='Version to pin conda to',
    )
    parser.add_argument(
        '--conda_build_version',
        type=str,
        default='',
        help='Version to pin conda-build to',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Switch on debugging',
    )
    parser.add_argument(
        '--ignore_test_deps',
        action='store_true',
        help='If true, test dependencies will be ignored',
    )
    parser.add_argument(
        '--include_build_deps',
        action='store_true',
        help='If true, build and host dependencies will be included',
    )
    args = parser.parse_args()

    if args.debug:
        _LOGGER.setLevel(logging.DEBUG)
    else:
        _LOGGER.setLevel(logging.WARNING)
    _LOGGER.debug(args)

    # clear out and re-create the env if it already exists
    env_name = args.env
    if not is_conda_environment(env_name) or replace_env:
        create_env(env_name)

    # get the dependencies from meta.yaml
    metadata = conda_build.api.render(args.conda_dir)[0][0]
    deps = metadata.get_value('requirements/run')
    if args.include_build_deps:
        deps += metadata.get_value('requirements/build')
        deps += metadata.get_value('requirements/host')
    if not args.ignore_test_deps:
        deps += metadata.get_value('test/requires')
    if len(args.conda_version) > 0:
        deps.append(f'conda={args.conda_version}')
    if len(args.conda_build_version) > 0:
        deps.append(f'conda-build={args.conda_build_version}')
    # else:
    #     deps.append('conda-build')

    # convert to space separated string
    deps = [quote_package(d) for d in deps]
    _LOGGER.info('Dependencies for env=%s: %s', args.env, ' '.join(deps))

    # install dependecies into a conda env
    command_args = ['--yes']
    if args.env != 'base':
        command_args.extend(['-n', args.env])
    command_args.extend(deps)
    conda_api(
        conda.cli.python_api.Commands.INSTALL,
        command_args,
    )


if __name__ == '__main__':
    main()
