from os import path
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow

from argparse import ArgumentParser
from oauth2client import tools
from .service import Service

DIR_NAME = path.abspath(__file__)
DIR_NAME = path.dirname(DIR_NAME)

import logging
import sys

def walk(directory, media=('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            if not filename.endswith(media):
                continue
            filename = path.join(dirpath, filename)
            yield filename

def auth(t):
    return open(path.join(DIR_NAME, '.auth-flow.p'), t)

def authenticate():
    scope = 'https://picasaweb.google.com/data/'
    client_info = path.join(DIR_NAME, 'client_info.json')
    return InstalledAppFlow.from_client_secrets_file(client_info, scopes=[scope])

auth_error = False

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def load_flow(load=True):
    try:
        if load:raise Exception 
        with auth('rb') as f:
            flow = pickle.load(f)
    except:
        global auth_error
        auth_error = True
        return authenticate()
    else:
        return flow

def dump_flow(flow):
    with auth('wb') as f:
        pickle.dump(flow, f)

import requests

def save_session(session):
    pass

def login(flags):
    """Returns a Service that wraps API requests.

    Throws on failure.

    "flags" is an ArgumentParser's returned args.
    """
    flow = load_flow()
    # flow.run_local_server()

    logger = logging.getLogger('GOOGLE_PHOTOS_UPLOAD')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stderr))

    # is_session = isinstance(flow, requests.Session)
    try:
        # flow.run_local_server()
        flow.run_console()
    except:
        return Service(flow, logger)
    try:
        session = flow.authorized_session()
        session.headers['GData-Version'] = '3'
        save_session(session)
    except:
        return login(flags)
    
    return Service(session, logger)

def parser():
    return ArgumentParser(description='Upload photos to Google Photos', parents=[ tools.argparser ])