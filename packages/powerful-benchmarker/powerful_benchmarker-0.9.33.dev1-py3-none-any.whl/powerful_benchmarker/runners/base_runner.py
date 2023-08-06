#! /usr/bin/env python3
import logging
logging.info("Importing packages in base_runner")
from easy_module_attribute_getter import YamlReader, PytorchGetter, utils as emag_utils
from ..utils import common_functions as c_f
import argparse
import glob
import os
from collections import defaultdict
logging.info("Done importing packages in base_runner")


class BaseRunner:
    def __init__(self, 
                dataset_root="datasets", 
                root_experiment_folder="experiments", 
                pytorch_home=None, 
                root_config_folder=None, 
                global_db_path=None,
                merge_argparse_when_resuming=False):
        self.dataset_root = dataset_root
        self.root_experiment_folder = root_experiment_folder
        self.global_db_path = global_db_path
        self.merge_argparse_when_resuming = merge_argparse_when_resuming
        self.pytorch_home = pytorch_home
        if pytorch_home is not None:
            os.environ["TORCH_HOME"] = self.pytorch_home
        if root_config_folder is not None:
            self.root_config_folder = root_config_folder
        else:
            self.root_config_folder = os.path.join(os.path.dirname(__file__), "../configs")
        self.config_foldernames_base = "config_foldernames"
        self.init_pytorch_getter()
        
    def register(self, module_type, module):
        self.pytorch_getter.register(module_type, module)

    def unregister(self, module_type, module):
        self.pytorch_getter.unregister(module_type, module)

    def init_pytorch_getter(self):
        from pytorch_metric_learning import trainers, distances, losses, miners, reducers, regularizers, samplers, testers, utils
        from .. import architectures, datasets, factories, api_parsers, split_managers, aggregators, ensembles
        from sklearn.manifold import TSNE
        import torch
        self.pytorch_getter = PytorchGetter(use_pretrainedmodels_package=True)
        self.pytorch_getter.register('model', architectures.misc_models)
        self.pytorch_getter.register('model', utils.common_functions.Identity)
        self.pytorch_getter.register('loss', losses)
        self.pytorch_getter.register('miner', miners)
        self.pytorch_getter.register('regularizer', regularizers)
        self.pytorch_getter.register('sampler', samplers)
        self.pytorch_getter.register('trainer', trainers)
        self.pytorch_getter.register('tester', testers)
        self.pytorch_getter.register('dataset', datasets)
        self.pytorch_getter.register('api_parser', api_parsers)
        self.pytorch_getter.register('accuracy_calculator', utils.accuracy_calculator.AccuracyCalculator)
        self.pytorch_getter.register('split_manager', split_managers)
        self.pytorch_getter.register('hook_container', utils.logging_presets.HookContainer)
        self.pytorch_getter.register('factory', factories)
        self.pytorch_getter.register('aggregator', aggregators)
        self.pytorch_getter.register('ensemble', ensembles)
        self.pytorch_getter.register('visualizer', TSNE)
        self.pytorch_getter.register('distance', distances)
        self.pytorch_getter.register('reducer', reducers)
        self.pytorch_getter.register('weight_init_func', torch.nn.init)


    def set_YR(self):
        self.YR = self.setup_yaml_reader()


    def run(self):
        raise NotImplementedError


    def get_api_parser(self, args):
        api_parser_kwargs = {"args": args, "pytorch_getter": self.pytorch_getter, "global_db_path": self.global_db_path}
        if args.api_parser:
            AP, AP_params = self.pytorch_getter.get('api_parser', yaml_dict=args.api_parser, return_uninitialized=True)
            AP_params = emag_utils.merge_two_dicts(api_parser_kwargs, AP_params)
            AP = AP(**AP_params)
        else:
            class_name = "API"+c_f.first_key_of_dict(args.trainer)
            try:
                AP = self.pytorch_getter.get('api_parser', class_name=class_name, params=api_parser_kwargs)
            except AttributeError:
                logging.warning("Couldn't find api_parser named {}. Using BaseAPIParser instead.".format(class_name))
                AP = self.pytorch_getter.get('api_parser', class_name="BaseAPIParser", params=api_parser_kwargs)
        return AP

    def setup_argparser(self):
        parser = argparse.ArgumentParser(allow_abbrev=False)
        parser.add_argument("--experiment_name", type=str, required=True)
        parser.add_argument("--resume_training", type=str, default=None, choices=["latest", "best"])
        parser.add_argument("--evaluate", action="store_true")
        parser.add_argument("--evaluate_ensemble", action="store_true")
        parser.add_argument("--reproduce_results", type=str, default=None)
        return parser


    def setup_yaml_reader(self):
        argparser = self.setup_argparser()
        YR = YamlReader(argparser=argparser)
        YR.args.dataset_root = self.dataset_root
        YR.args.experiment_folder = os.path.join(self.root_experiment_folder, YR.args.experiment_name)
        YR.args.place_to_save_configs = os.path.join(YR.args.experiment_folder, "configs")
        config_foldernames_yaml = "{}.yaml".format(self.config_foldernames_base)
        foldername_info = None
        if not hasattr(YR.args, self.config_foldernames_base):
            # first try loading config_foldernames from "place_to_save_configs", in case we're resuming
            already_saved_config_foldernames = os.path.join(YR.args.place_to_save_configs, config_foldernames_yaml)
            if os.path.isfile(already_saved_config_foldernames):
                foldername_info = c_f.load_yaml(already_saved_config_foldernames)
            else:
                foldername_info = c_f.load_yaml(os.path.join(self.root_config_folder, config_foldernames_yaml))
            YR.args.config_foldernames = foldername_info[self.config_foldernames_base]

        for subfolder in YR.args.config_foldernames:
            if not hasattr(YR.args, subfolder):
                yaml_names = ["default"] if foldername_info is None else foldername_info[subfolder]
                setattr(YR.args, subfolder, yaml_names)
        return YR


    def determine_where_to_get_yamls(self, args):
        if args.resume_training or args.evaluate or args.evaluate_ensemble:
            config_paths = self.get_saved_config_paths(args)
        else:
            config_paths = self.get_root_config_paths(args)
        return config_paths


    def get_saved_config_paths(self, args, config_folder=None):
        folder = args.place_to_save_configs if config_folder is None else config_folder
        return {v: [os.path.join(folder,'%s.yaml'%v)] for v in self.get_list_of_yaml_names_to_load(args)}


    def get_root_config_paths(self, args):
        config_paths = defaultdict(list)
        for subfolder in self.get_list_of_yaml_names_to_load(args):
            without_subfolder = os.path.join(self.root_config_folder, "%s.yaml"%subfolder)
            if os.path.isfile(without_subfolder):
                config_paths[subfolder].append(without_subfolder)
            else:
                for curr_yaml in getattr(args, subfolder):
                    with_subfolder = os.path.join(self.root_config_folder, subfolder, "%s.yaml"%curr_yaml)
                    config_paths[subfolder].append(with_subfolder)
        return config_paths


    def get_list_of_yaml_names_to_load(self, args):
        return args.config_foldernames + [self.config_foldernames_base]
