import os
from functools import reduce
from collections import OrderedDict
import yaml

from dipor.jinja.extensions import RoutesExtension

def get_structural_context(prefix, app_name, content_root):
    ctx = {}
    directory = OrderedDict()

    rootdir = os.path.join(prefix, content_root)
    start = content_root.rstrip(os.sep).rfind(os.sep) + 1

    routes_file = os.path.join(prefix, app_name, "routes.yml")
    overridden_route_names = {}
    if os.path.exists(routes_file) and os.path.getsize(routes_file) > 0:
        with open(routes_file) as f:
            overridden_route_names = yaml.load(f, Loader=yaml.FullLoader)
            print(overridden_route_names)
    for path, dirs, files in os.walk(rootdir):
        path = os.path.relpath(path, prefix)
        folders = path[start:].split(os.sep)
        subdir = {}
        if '_branches' in folders:
            folders.remove('_branches')
        parent = reduce(dict.get, folders[:-1], directory)
        parent[folders[-1]] = subdir
    processed_path = process_paths(directory['content'], overridden_route_names=overridden_route_names)
    return processed_path

def process_paths(directory, overridden_route_names, prefix="", is_subpath=False):
    ## this is the default path. allow overriding later
    route_dir = {}
    for k, v in directory.items():
        if not v:
            if prefix+"/"+k in overridden_route_names.keys():
                route_dir[prefix+"/"+k] = (overridden_route_names[prefix+"/"+k], None)
            else:
                route_dir[prefix+"/"+k] = (k, None)
        else:
            sub_paths = process_paths(v, overridden_route_names=overridden_route_names, prefix="/"+k, is_subpath=True)
            if "/"+k in overridden_route_names.keys():
                route_dir["/"+k] = (overridden_route_names["/"+k], sub_paths)
            else:
                route_dir["/"+k] = (k, sub_paths)
    if is_subpath:
        return route_dir

    if "/" in overridden_route_names.keys():
        final_route = {'/': (overridden_route_names["/"], route_dir)}
    else:
        final_route = {'/': ('home', route_dir)}
    return final_route

        