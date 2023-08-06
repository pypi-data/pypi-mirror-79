import json
import os
import pickle
from collections import OrderedDict
from enum import Enum

import mlflow
import yaml
from mlflow.tracking import MlflowClient
from mlflow.utils.autologging_utils import try_mlflow_log

from pypads import logger


def add_to_store_object(source, obj, store=True):
    from pypads.app.pypads import get_current_pads
    pads = get_current_pads()
    if not pads.cache.run_exists(id(source)):
        pads.cache.run_add(id(source), OrderedDict())

    objects_store: OrderedDict = pads.cache.run_get(id(source))

    if id(obj) not in objects_store:
        objects_store[id(obj)] = (obj, store)
    else:
        logger.warning("Object already added to the store")


def get_temp_folder(run=None):
    """
    Get the base folder to log tmp files to. For now it can't be changed. Todo make configurable
    :return:
    """
    from pypads.app.pypads import get_current_pads
    pads = get_current_pads()
    run = run if run else pads.api.active_run()
    if run is None:
        raise ValueError("No active run is defined.")
    return os.path.join(pads.folder, "tmp", run.info.experiment_id, run.info.run_id) + os.path.sep


def get_run_folder():
    """
    Get the folder holding the run information.
    :return:
    """
    run = mlflow.active_run()
    if run is None:
        raise ValueError("No active run is defined.")
    # TODO use artifact download if needed or load artifact.
    return os.path.join(mlflow.get_tracking_uri(), run.info.experiment_id, run.info.run_id)


class WriteFormats(Enum):
    pickle = 'pickle'
    text = 'text'
    yaml = 'yaml'
    json = 'json'


class ReadFormats(Enum):
    pickle = 'pickle'
    txt = 'txt'
    yaml = 'yaml'
    json = 'json'


# extract all tags of runs by experiment id
def all_tags(experiment_id):
    client = MlflowClient(mlflow.get_tracking_uri())
    ds_infos = client.list_run_infos(experiment_id)
    for i in ds_infos:
        yield mlflow.get_run(i.run_id).data.tags


def try_read_artifact(file_name, folder_lookup=True):
    """
    Function to read an artifact from disk
    :param file_name:
    :return:
    """
    # TODO make defensive
    path = file_name
    if folder_lookup:
        base_path = get_run_folder()
        path = os.path.join(base_path, "artifacts", file_name)

    # Functions for the options to read
    def read_text(p):
        with open(p, "r") as fd:
            return fd.read()

    def read_pickle(p):
        try:
            with open(p, "rb") as fd:
                return pickle.load(fd)
        except Exception as e:
            logger.warning("Couldn't read pickle file. " + str(e))

    def read_yaml(p):
        try:
            with open(p, "r") as fd:
                return yaml.full_load(fd)
        except Exception as e:
            logger.warning("Couldn't read artifact as yaml. Trying to read it as text instead. " + str(e))
            return read_text(p)

    def read_json(p):
        try:
            with open(p, "r") as fd:
                return json.load(fd)
        except Exception as e:
            logger.warning("Couldn't read artifact as json. Trying to read it as text instead. " + str(e))
            return read_text(p)

    options = {
        ReadFormats.pickle: read_pickle,
        ReadFormats.txt: read_text,
        ReadFormats.yaml: read_yaml,
        ReadFormats.json: read_json
    }

    read_format = path.split('.')[-1]
    if ReadFormats[read_format]:
        read_format = ReadFormats[read_format]
    else:
        logger.warning("Configured read format " + read_format + " not supported! ")
        return
    try:
        data = options[read_format](path)
    except Exception as e:
        logger.warning("Reading artifact failed for '" + path + "'. " + str(e))
        data = "Cannot view content"
    return data


def try_write_artifact(file_name, obj, write_format, preserve_folder=True):
    """
    Function to write an artifact to disk.
    :param preserve_folder:
    :param write_format:
    :param file_name:
    :param obj:
    :return:
    """
    base_path = get_temp_folder()
    path = os.path.join(base_path, file_name)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # Functions for the options to write to
    def write_text(p, o):
        with open(p + ".txt", "w+") as fd:
            fd.write(str(o))
            return fd.name

    def write_pickle(p, o):
        try:
            with open(p + ".pickle", "wb+") as fd:
                pickle.dump(o, fd)
                return fd.name
        except Exception as e:
            logger.warning("Couldn't pickle output. Trying to save toString instead. " + str(e))
            return write_text(p, o)

    def write_yaml(p, o):
        try:
            with open(p + ".yaml", "w+") as fd:
                if isinstance(o, str):
                    fd.write(o)
                    # TODO check if valid json?
                else:
                    yaml.dump(o, fd)
                return fd.name
        except Exception as e:
            logger.warning("Couldn't write meta as yaml. Trying to save it as json instead. " + str(e))
            return write_json(p, o)

    def write_json(p, o):
        try:
            with open(p + ".json", "w+") as fd:
                if isinstance(o, str):
                    fd.write(o)
                    # TODO check if valid json?
                else:
                    json.dump(o, fd)
                return fd.name
        except Exception as e:
            logger.warning("Couldn't write meta as json. Trying to save it as text instead. " + str(e))
            return write_text(p, o)

    # Options to write to
    options = {
        WriteFormats.pickle: write_pickle,
        WriteFormats.text: write_text,
        WriteFormats.yaml: write_yaml,
        WriteFormats.json: write_json
    }

    # Write to disk
    if isinstance(write_format, str):
        if WriteFormats[write_format]:
            write_format = WriteFormats[write_format]
        else:
            logger.warning("Configured write format " + write_format + " not supported! ")
            return

    path = options[write_format](path, obj)
    if preserve_folder:
        in_folder = os.path.join(base_path, file_name.split(os.sep)[0])
        # Log artifact to mlflow
        if os.path.isdir(in_folder):
            try_mlflow_log(mlflow.log_artifact, in_folder)
        else:
            try_mlflow_log(mlflow.log_artifact, path)
    else:
        try_mlflow_log(mlflow.log_artifact, path)


def _to_artifact_meta_name(name):
    return name + ".artifact"


def _to_metric_meta_name(name):
    return name + ".metric"


def _to_param_meta_name(name):
    return name + ".param"
