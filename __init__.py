# varhandler/__init__.py

from .load import load
from .save import save
from .get import get
from .save import search as vh_save_search
from .get import search as vh_get_search
from .get import valueOf as vh_get_valueOf
from .get import exists as vh_get_exists

# Alias
save_search = vh_save_search
get_search = vh_get_search
get_valueOf = vh_get_valueOf
get_exists = vh_get_exists
