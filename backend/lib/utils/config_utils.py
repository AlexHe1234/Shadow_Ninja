from yacs.config import CfgNode as CN
import argparse
import yaml
import re
from typing import Dict


file_path = __file__
program = file_path.split('/')[-4]


def convert_module_path(path: str) -> str:
    if path[-3:] == '.py':
        path = path[:-3]
    return path.replace('/', '.')


def add_list_dict(cfg: CN, x: Dict):
    if not isinstance(x, Dict):
        return
    for k in x.keys():
        if isinstance(x[k], Dict):
            cfg[k] = CN()
            add_list_dict(cfg[k], x[k])
        else:
            cfg[k] = x[k]


class NestedLoader(yaml.Loader):
    def __init__(self, stream):
        super().__init__(stream)

    def construct_config(self, node):
        config_file = self.construct_scalar(node)
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=NestedLoader)
        return config
    

yaml.add_constructor('!config', NestedLoader.construct_config, Loader=NestedLoader)


# loader supports float rep. like 1e10
loader = NestedLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))
            

def cfg_from_file(path_to_cfg):
    cfg = CN()
    with open(path_to_cfg, 'r') as f:
        yaml_dict = yaml.load(f, Loader=loader)
    add_list_dict(cfg, yaml_dict)
    return cfg


def merge_base_config(cfg: CN, exp_cfg: CN, strict=False) -> CN:
    base_names = list(cfg.keys()) + ['exp_name']
    for k in exp_cfg:
        if exp_cfg[k] is None:
            continue
        if k not in base_names and strict:
            raise KeyError(f'Invalid key {k} in exp config')
        if isinstance(exp_cfg[k], CN):
            try:
                cfg[k] = merge_base_config(cfg[k], exp_cfg[k], strict=strict)
            except:
                if strict:
                    raise ValueError(f'Key {k} doesn\'t exist in original config and is therefore not merge-able')
                cfg[k] = exp_cfg[k]
        else:
            cfg[k] = exp_cfg[k]
    return cfg
