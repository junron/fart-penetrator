import importlib.resources

from lib.HttpWorker import *
from lib.types.FartRequest import *
from lib.types.FartResponse import *
from lib.types.AttackConfig import *
from lib.types.ResponseCallback import *
from . import wordlists

usernames = importlib.resources.read_text(wordlists, "usernames.txt").splitlines()
passwords = importlib.resources.read_text(wordlists, "passwords.txt").splitlines()
