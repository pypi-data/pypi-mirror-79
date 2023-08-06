from ..interfaces.GraphQLInterface import GraphQLInterface

from ..steps.AuthAndConnectStep import AuthAndConnectStep
from ..steps.CreateVersionStep import CreateVersionStep
from ..steps.UploadModelStep import UploadModelStep
from ..steps.UploadNotebookStep import UploadNotebookStep
from ..steps.InitiateDeployStep import InitiateDeployStep
from ..steps.MonitorDeployStep import MonitorDeployStep

from ..helpers.colorprint import *



def deploy(project_name, model_path, notebook, auth_token):
    """DeployCommand deploy func"""
    return DeployCommand(project_name, model_path, notebook, auth_token).call()


class DeployCommand(object):
    """DeployCommand"""

    def __init__(self, project_name, model_path, notebook_path=None, api_key=None):
        self.project_name   = project_name
        self.model_path     = model_path
        self.notebook_path  = notebook_path
        self.graphql        = GraphQLInterface(api_key)

        if not (isinstance(notebook_path, str) or notebook_path == None):
            redp('You must provide a path to the notebook if you use the --notebook flag', n=2)
            defaultp('Usage: ', n=1)
            cyanp('--notebook ./path/to/notebook.ipnb', n=2, t=1)
            exit()

    def call(self):
        """DeployCommand.call."""

        user = AuthAndConnectStep(self.graphql).call(self.project_name)
        version = CreateVersionStep(self.graphql).call(self.project_name, self.notebook_path)
        UploadModelStep(self.graphql).call(version, self.model_path)
        if self.notebook_path:
            UploadNotebookStep(self.graphql).call(version, self.notebook_path)
        version = InitiateDeployStep(self.graphql).call(version)
        MonitorDeployStep(self.graphql).call(version)
