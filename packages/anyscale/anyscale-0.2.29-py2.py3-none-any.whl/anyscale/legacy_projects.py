import argparse
import copy
import json
import os
from typing import Any, Dict, Optional

import click
import jsonschema
import yaml

PROJECT_DIR = "ray-project"
PROJECT_YAML = os.path.join(PROJECT_DIR, "project.yaml")


def make_argument_parser(name: str, params: Optional[Any], wildcards: bool) -> Any:
    """Build argument parser dynamically to parse parameter arguments.

    Args:
        name (str): Name of the command to parse.
        params (dict): Parameter specification used to construct
            the argparse parser.
        wildcards (bool): Whether wildcards are allowed as arguments.

    Returns:
        The argparse parser.
        A dictionary from argument name to list of valid choices.
    """

    parser = argparse.ArgumentParser(prog=name)
    # For argparse arguments that have a 'choices' list associated
    # with them, save it in the following dictionary.
    choices = {}
    new_params: Dict[Any, Any] = params if params else {}
    for param in new_params:
        # Construct arguments to pass into argparse's parser.add_argument.
        argparse_kwargs = copy.deepcopy(param)
        name = argparse_kwargs.pop("name")
        if wildcards and "choices" in param:
            choices[name] = param["choices"]
            argparse_kwargs["choices"] = param["choices"] + ["*"]
        if "type" in param:
            types = {"int": int, "str": str, "float": float}
            if param["type"] in types:
                argparse_kwargs["type"] = types[param["type"]]
            else:
                raise ValueError(
                    "Parameter {} has type {} which is not supported. "
                    "Type must be one of {}".format(
                        name, param["type"], list(types.keys())
                    )
                )
        parser.add_argument("--" + name, dest=name, **argparse_kwargs)

    return parser, choices


class ProjectDefinition:
    def __init__(self, current_dir: str) -> None:
        """Finds ray-project folder for current project, parse and validates it.

        Args:
            current_dir (str): Path from which to search for ray-project.

        Raises:
            jsonschema.exceptions.ValidationError: This exception is raised
                if the project file is not valid.
            ValueError: This exception is raised if there are other errors in
                the project definition (e.g. files not existing).
        """
        root = find_root(current_dir)
        if root is None:
            raise ValueError("No project root found")
        # Add an empty pathname to the end so that rsync will copy the project
        # directory to the correct target.
        self.root = os.path.join(root, "")

        # Parse the project YAML.
        project_file = os.path.join(self.root, "ray-project", "project.yaml")
        if not os.path.exists(project_file):
            raise ValueError("Project file {} not found".format(project_file))
        with open(project_file) as f:
            self.config = yaml.safe_load(f)

        check_project_config(self.root, self.config)

    def cluster_yaml(self) -> Any:
        """Return the project's cluster configuration filename."""
        return self.config["cluster"]["config"]

    def working_directory(self) -> str:
        """Return the project's working directory on a cluster session."""
        # Add an empty pathname to the end so that rsync will copy the project
        # directory to the correct target.
        directory = os.path.join("~", self.config["name"], "")
        return directory

    def get_command_info(
        self, command_name: str, args: Any, shell: Any, wildcards: bool = False
    ) -> Any:
        """Get the shell command, parsed arguments and config for a command.

        Args:
            command_name (str): Name of the command to run. The command
                definition should be available in project.yaml.
            args (tuple): Tuple containing arguments to format the command
                with.
            wildcards (bool): If True, enable wildcards as arguments.

        Returns:
            The raw shell command to run with placeholders for the arguments.
            The parsed argument dictonary, parsed with argparse.
            The config dictionary of the command.

        Raises:
            ValueError: This exception is raised if the given command is not
                found in project.yaml.
        """
        if shell or not command_name:
            return command_name, {}, {}

        command_to_run = None
        params = None
        config = None

        for command_definition in self.config["commands"]:
            if command_definition["name"] == command_name:
                command_to_run = command_definition["command"]
                params = command_definition.get("params", [])
                config = command_definition.get("config", {})
        if not command_to_run:
            raise ValueError(
                "Cannot find the command named '{}' in commmands section "
                "of the project file.".format(command_name)
            )

        parser, choices = make_argument_parser(command_name, params, wildcards)
        parsed_args = vars(parser.parse_args(list(args)))

        if wildcards:
            for key, val in parsed_args.items():
                if val == "*":
                    parsed_args[key] = choices[key]

        return command_to_run, parsed_args, config

    def git_repo(self) -> Any:
        return self.config.get("repo", None)


def find_root(directory: str) -> Optional[str]:
    """Find root directory of the ray project.

    Args:
        directory (str): Directory to start the search in.

    Returns:
        Path of the parent directory containing the ray-project or
        None if no such project is found.
    """
    prev, directory = None, os.path.abspath(directory)
    while prev != directory:
        if os.path.isdir(os.path.join(directory, "ray-project")):
            return directory
        prev, directory = directory, os.path.abspath(os.path.join(directory, os.pardir))
    return None


def validate_project_schema(project_config: Dict[Any, Any]) -> None:
    """Validate a project config against the official ray project schema.

    Args:
        project_config (dict): Parsed project yaml.

    Raises:
        jsonschema.exceptions.ValidationError: This exception is raised
            if the project file is not valid.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir, "schema.json")) as f:
        schema = json.load(f)

    jsonschema.validate(instance=project_config, schema=schema)


def check_project_config(project_root: str, project_config: Dict[Any, Any]) -> None:
    """Checks if the project definition is valid.

    Args:
        project_root (str): Path containing the ray-project
        project_config (dict): Project config definition

    Raises:
        jsonschema.exceptions.ValidationError: This exception is raised
            if the project file is not valid.
        ValueError: This exception is raised if there are other errors in
            the project definition (e.g. files not existing).
    """
    validate_project_schema(project_config)

    # Make sure the cluster yaml file exists
    cluster_file = os.path.join(project_root, project_config["cluster"]["config"])
    if not os.path.exists(cluster_file):
        raise ValueError("'cluster' file does not exist " "in {}".format(project_root))

    if "environment" in project_config:
        env = project_config["environment"]

        if sum(["dockerfile" in env, "dockerimage" in env]) > 1:
            raise ValueError(
                "Cannot specify both 'dockerfile' and " "'dockerimage' in environment."
            )

        if "requirements" in env:
            requirements_file = os.path.join(project_root, env["requirements"])
            if not os.path.exists(requirements_file):
                raise ValueError(
                    "'requirements' file in 'environment' does "
                    "not exist in {}".format(project_root)
                )

        if "dockerfile" in env:
            docker_file = os.path.join(project_root, env["dockerfile"])
            if not os.path.exists(docker_file):
                raise ValueError(
                    "'dockerfile' file in 'environment' does "
                    "not exist in {}".format(project_root)
                )


def format_command(command: str, parsed_args: Dict[Any, Any]) -> str:
    """Substitute arguments into command.

    Args:
        command (str): Shell comand with argument placeholders.
        parsed_args (dict): Dictionary that maps from argument names
            to their value.

    Returns:
        Shell command with parameters from parsed_args substituted.
    """
    for key, val in parsed_args.items():
        command = command.replace("{{" + key + "}}", str(val))
    return command


def get_session_runs(
    name: Optional[str], command: Optional[str], parsed_args: Dict[Any, Any]
) -> Any:
    """Get a list of sessions to start.

    Args:
        command (str): Shell command with argument placeholders.
        parsed_args (dict): Dictionary that maps from argument names
            to their values.

    Returns:
        List of sessions to start, which are dictionaries with keys:
            "name": Name of the session to start,
            "command": Command to run after starting the session,
            "params": Parameters for this run,
            "num_steps": 4 if a command should be run, 3 if not.
    """
    if not command:
        return [{"name": name, "command": None, "params": {}, "num_steps": 3}]

    # Try to find a wildcard argument (i.e. one that has a list of values)
    # and give an error if there is more than one (currently unsupported).
    wildcard_arg = None
    for key, val in parsed_args.items():
        if isinstance(val, list):
            if not wildcard_arg:
                wildcard_arg = key
            else:
                raise click.ClickException(
                    "More than one wildcard is not supported at the moment"
                )

    if not wildcard_arg:
        session_run = {
            "name": name,
            "command": format_command(command, parsed_args),
            "params": parsed_args,
            "num_steps": 4,
        }
        return [session_run]
    else:
        session_runs = []
        for val in parsed_args[wildcard_arg]:
            parsed_args = copy.deepcopy(parsed_args)
            parsed_args[wildcard_arg] = val
            session_run = {
                "name": "{}-{}-{}".format(name, wildcard_arg, val),
                "command": format_command(command, parsed_args),
                "params": parsed_args,
                "num_steps": 4,
            }
            session_runs.append(session_run)
        return session_runs
