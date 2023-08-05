import hashlib

import bson
import requests

from .common import getToken, read_in_chunks, MID_VERBOSITY, getVerbosity
from .Task import Task
from .saving.saving import determine_model, hash_model
from .web.urls import RETRIEVE_MODEL_URL, HASH_URL, COMPILE_URL
from .saving import save_model


def compile(model, input_shape, library, model_label, asynchronous=False):
    if model_label != "" and model is None:
        print(model_label)
        params = {"token": getToken(), "input_shape": input_shape, "label": model_label}
        response = requests.get(RETRIEVE_MODEL_URL, params=params)
        if response.status_code == 200:
            return response
        else:
            raise LookupError("Model not found. " + str(response))
    if bson.ObjectId.is_valid(model):
        return model
    if library == "":
        library = determine_model(model)
    hash = hash_model(model, library)
    params = {"token": getToken(), "input_shape": input_shape, "given_name": model_label, "hash": hash,
              "collection": 2, "modelType": library}
    response = requests.get(HASH_URL, params=params)
    if response.status_code == 200:
        if getVerbosity() >= MID_VERBOSITY:
            print("Model already on server. Returning result...")
        return response.json()
    elif response.status_code != 204:
        raise ConnectionAbortedError("Checking hash not worked. {0}".format(response.content))
    else:
        if getVerbosity() >= MID_VERBOSITY:
            print("Model not found on server.")
            print("Saving model locally...")
        file_path = save_model(model, library)
        with open(file_path, "rb") as file:
            size = 0
            for piece in read_in_chunks(file):
                size += len(piece)
            if model_label == "":
                model_label = file_path
            params["given_name"] = model_label
            if getVerbosity() >= MID_VERBOSITY:
                print("Model saved locally.")
            print("Model file size is {} bytes. Uploading model now...".format(size))
            task = Task(compileApi(file, params))
            if not asynchronous:
                task.wait()
                print("Model compiled successfully.")
            return task


def compileApi(file, params):
    file.seek(0)
    files = {'file': file}
    response = requests.post(COMPILE_URL, files=files, params=params)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response.json()

