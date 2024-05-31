import os
from llm import LLM
from utils.config_utils import *


def replace_last_path(fp, replace):
    splits = fp.split('/')[:-1]
    splits.append(replace)
    return os.path.join(splits)


# read config
lib_path = __file__
config_dir = replace_last_path(lib_path, 'config')

global_config = cfg_from_file(os.path.join(config_dir, 'global.yaml'))
llm_config = cfg_from_file(os.path.join(config_dir, 'llm.yaml'))
rs_config = cfg_from_file(os.path.join(config_dir, 'rec_sys.yaml'))

# initialize global objects
# NOTE: please don't re-initialize them
foundation_model = LLM(**llm_config)
