from setuptools import _install_setup_requires
from setuptools.command.develop import develop as DevelopCmd
from setuptools.command.install import install as InstallCmd
from setuptools.command.sdist import sdist as SDistCmd
from distutils.dist import Distribution
from setuptools.config import read_configuration

from wheel.bdist_wheel import bdist_wheel as BDistWheelCmd

import logging
from pathlib import Path
import codecs
import os
import subprocess
import time
import stat
import sys
import shutil
import requests
from inspect import getmembers, isfunction

from cookiecutter.main import cookiecutter
from twine.commands.upload import main as twine_main

from proma.require import requires


def load_project_param(with_opts=False):
    """

    Examples:
      >>> p = load_project_param()
      >>> p['name']
      'proma'

    """
    conf_pth = "setup.cfg"
    conf_dict = read_configuration(conf_pth)

    param = {}
    param.update(**conf_dict["option"])
    param.update(**conf_dict["metadata"])
    if with_opts:
        param.update(**conf_dict["options"])

    param["script_name"] = "setup.py"

    return param


def update_status(func):
    param = load_project_param()

    status_pth = os.path.join(".proma", "status")

    t_ns = time.time_ns()

    f = open(status_pth, "w")
    f.write("%s@%i" % (func, t_ns))
    f.close()


def init_proma_dir():
    os.makedirs(".proma", exist_ok=True)

    clean_pth = os.path.join(".proma", "clean.sh")
    if not os.path.exists(clean_pth):
        os.rename("clean.sh", clean_pth)

    param = load_project_param(with_opts=True)
    if "install_requires" in param.keys():
        deps = param["install_requires"]
    else:
        deps = []

    req_pth = os.path.join(".proma", "requirements.txt")
    f = open(req_pth, "w")
    for r in deps:
        f.write("%s\n" % r)
    f.close()


def print_help():
    import proma
    print("proma v" + proma.__version__)
    print()
    from proma import proma as p
    functions_list = [o[1] for o in getmembers(p) if isfunction(o[1])]
    for f in functions_list:
        if hasattr(f, 'proma_command') and f.proma_command:
            print("%s\n   %s" % (f.__name__, f.__doc__.strip()))

@requires()
def create(name):
    """
    Package creation : proma create [name]
    """
    print("Creating '%s'" % name)

    params = {
        "full_name": "Yann de The",
        "email": "ydethe@gmail.com",
        "github_username": "ydethe",
        "project_name": name,
        "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.",
        "version": "0.1.0",
        "add_pyup_badge": "y",
        "command_line_interface": "y",
    }

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter(
        "https://gitlab.com/ydethe/cookiecutter-proma.git",
        checkout=None,  # The branch, tag or commit ID to checkout after clone.
        no_input=True,  # Prompt the user at command line for manual configuration?
        extra_context=params,  # A dictionary of context that overrides default and user configuration.
        replay=False,
        overwrite_if_exists=True,  # Overwrite the contents of output directory if it exists
        output_dir=".",  # Where to output the generated project dir into.
        config_file=None,  # User configuration file path
        default_config=False,  # Use default values rather than a config file
        password=None,  # The password to use when extracting the repository
        directory=None,  # Relative path to a cookiecutter template in a repository
        skip_if_file_exists=False,
    )

    wd = os.getcwd()
    os.chdir(name)
    init_proma_dir()
    os.chdir(wd)


@requires()
def init(param):
    """
    Package initialization for an existing package : proma init
    """
    pth = os.getcwd()
    name = os.path.split(pth)[-1]

    print("Initializing '%s'" % name)

    init_proma_dir()


@requires()
def build(args):
    """
    Creation of distributable files in the dist folder : proma build
    """
    param = load_project_param()

    name = param["name"]

    print("Building '%s' --> whl and tar.gz" % name)

    _install_setup_requires(param)
    dist = Distribution(param)

    cmd = SDistCmd(dist)
    cmd.finalize_options()

    cmd.run()

    cmd = BDistWheelCmd(dist)
    cmd.finalize_options()

    cmd.run()


@requires()
def develop(args):
    """
    Locally installs the package for developpement purpose : proma develop
    """
    param = load_project_param()

    if len(args) == 0:
        uninst = False
    else:
        uninst = "--uninstall" in args[0]

    name = param["name"]

    if uninst:
        print("Removing develop '%s'" % name)
    else:
        print("Develop '%s'" % name)

    _install_setup_requires(param)
    dist = Distribution(param)

    cmd = DevelopCmd(dist, uninstall=uninst)
    cmd.finalize_options()

    cmd.run()


@requires([develop])
def test(args):
    """
    Tests the package with tox : proma test
    """
    param = load_project_param()

    name = param["name"]

    print("Testing '%s'" % name)

    cmd = ["tox", "-e", "py"]
    cmd.extend(args)

    # In case the requirements in setup.cfg have changed
    init_proma_dir()
    process = subprocess.run(cmd, universal_newlines=True)


@requires([test])
def install(args):
    """
    Installs the package : proma install
    """
    param = load_project_param()

    name = param["name"]

    print("Installing '%s'" % name)

    _install_setup_requires(param)
    dist = Distribution(param)

    cmd = InstallCmd(dist)
    cmd.finalize_options()

    cmd.run()


@requires()
def clean(args):
    """
    Cleans the package working directory : proma clean
    """
    param = load_project_param()

    name = param["name"]

    print("Cleaning '%s'" % name)

    cmd = [".proma/clean.sh"]
    cmd.extend(args)

    process = subprocess.run(cmd, universal_newlines=True)


@requires()
def doc(args):
    """
    Builds the package's documentation with sphinx : proma doc
    """
    param = load_project_param()

    name = param["name"]

    print("Building doc for '%s'" % name)

    command = ["sphinx-build"]
    command.append("-T")
    command.append("-b")
    command.append("html")
    command.append("-D")
    command.append("language=fr")
    command.append(".")
    command.append("_build/html")

    wd = os.getcwd()
    os.chdir("docs")
    os.makedirs("_build", exist_ok=True)
    process = subprocess.run(command, universal_newlines=True)
    os.chdir(wd)


@requires()
def uninstall(param):
    """
    Uninstall the package (developpement mode and final mode) : proma uninstall
    """
    param = load_project_param()

    name = param["name"]

    print("Uninstalling '%s'" % name)

    wd = Path(os.getcwd())

    def rm_func(d: Path):
        print("   Removing '%s'" % d)
        if d.is_dir():
            shutil.rmtree(d)
        else:
            os.remove(d)

    for d in sys.path:
        pd = Path(d)
        n = os.path.split(d)[-1].split(".")[0]
        if n == name and not wd in pd.parents and wd != pd:
            rm_func(pd)
        else:
            for dirpath, dirnames, filenames in os.walk(d):
                pc = Path(dirpath)
                for sd in dirnames:
                    spth = Path(os.path.join(dirpath, sd))
                    n = os.path.split(sd)[-1].split(".")[0]
                    if n == name and not wd in spth.parents and wd != spth:
                        rm_func(spth)

                for sd in filenames:
                    spth = Path(os.path.join(dirpath, sd))
                    n = os.path.split(sd)[-1].split(".")[0]
                    if n == name and not wd in spth.parents and wd != spth:
                        rm_func(spth)


@requires([test, build])
def upload(args):
    """
    Upload the package with twine : proma upload
    """
    log = logging.getLogger("proma_logger")

    param = load_project_param()

    name = param["name"]

    print("Uploading '%s'" % name)

    try:
        twine_main(["dist/*"])
    except requests.HTTPError as e:
        log.error(e.args[0])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
