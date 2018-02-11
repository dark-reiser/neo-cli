import click
import getpass
import subprocess
import requests
import os
import re
from json import dumps
from .base import Base
from docopt import docopt
from neo.libs import network as network_lib
from neo.libs import utils
from neo.libs import orchestration as orch
from tabulate import tabulate


class Ls(Base):
    """
usage: 
        ls [-f PATH] [-a]

List all stack

Options:
-h --help               Print usage
-f PATH --file=PATH     Set neo manifest file
-a --all                List all stacks

Run 'neo ls COMMAND --help' for more information on a command.
"""

    def execute(self):
        headers = ["ID", "Name", "Status", "Created", "Updated"]
        if self.args["--all"]:
            print(tabulate(orch.get_list(), headers=headers, tablefmt="grid"))
            exit()

        set_file = self.args["--file"]
        default_file = orch.check_manifest_file()

        if set_file:
            real_path = os.path.dirname(os.path.realpath(set_file))
            if os.path.exists(real_path):
                default_file = "{}/{}".format(real_path, set_file)
            else:
                utils.log_err("{} file is not exists!".format(set_file))
                exit()

        if not default_file:
            utils.log_err("Can't find neo.yml manifest file!")
            exit()

        projects = utils.get_project(default_file)

        project_list = list()
        for project in projects:
            proj = orch.get_stack(project)
            if proj:
                project_list.append(proj)

        if len(project_list) > 0:
            print(tabulate(project_list, headers=headers, tablefmt="grid"))
        else:
            utils.log_warn("No Data...")
