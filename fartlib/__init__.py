import importlib.resources

from fartlib.HttpWorker import *
from fartlib.FartLooper import *
from fartlib.types.FartRequest import *
from fartlib.types.FartResponse import *
from fartlib.types.ResponseCallback import *
from . import wordlists

usernames = importlib.resources.read_text(wordlists, "usernames.txt").splitlines()
passwords = importlib.resources.read_text(wordlists, "passwords.txt").splitlines()
