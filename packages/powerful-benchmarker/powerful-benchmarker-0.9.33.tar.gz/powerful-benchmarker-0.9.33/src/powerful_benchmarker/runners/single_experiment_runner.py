#! /usr/bin/env python3
import logging
logging.info("Importing packages in single_experiment_runner")
from ..utils import common_functions as c_f, dataset_utils as d_u
from .base_runner import BaseRunner
import glob
import os
logging.info("Done importing packages in single_experiment_runner")


class SingleExperimentRunner(BaseRunner):

    def run(self):
        self.set_YR()
        if self.YR.args.reproduce_results:
            return self.reproduce_results(self.YR)
        else:
            return self.run_new_experiment_or_resume(self.YR)

    def start_experiment(self, args):
        api_parser = self.get_api_parser(args)
        run_output = api_parser.run()
        del api_parser
        return run_output

    def run_new_experiment_or_resume(self, YR):
        # merge_argparse at the beginning of training, or when evaluating
        merge_argparse = self.merge_argparse_when_resuming if YR.args.resume_training else True
        args, _, args.dict_of_yamls = YR.load_yamls(self.determine_where_to_get_yamls(YR.args), 
                                                    max_merge_depth=float('inf'),
                                                    max_argparse_merge_depth=float('inf'), 
                                                    merge_argparse=merge_argparse)
        return self.start_experiment(args)

    def reproduce_results(self, YR, starting_fresh_hook=None, max_merge_depth=float('inf'), max_argparse_merge_depth=float('inf')):
        configs_folder = os.path.join(YR.args.reproduce_results, 'configs')
        default_configs = self.get_root_config_paths(YR.args) # default configs
        experiment_config_paths = self.get_saved_config_paths(YR.args, config_folder=configs_folder) # reproduction configs
        for k, v in experiment_config_paths.items():
            if any(not os.path.isfile(filename) for filename in v):
                logging.warning("{} does not exist. Will use default config for {}".format(v,k))
                experiment_config_paths[k] = default_configs[k]
        args, _, args.dict_of_yamls = YR.load_yamls(config_paths=experiment_config_paths, 
                                                    max_merge_depth=max_merge_depth,
                                                    max_argparse_merge_depth=max_argparse_merge_depth, 
                                                    merge_argparse=self.merge_argparse_when_resuming)

        # check if there were config diffs if training was resumed
        temp_split_manager = self.pytorch_getter.get("split_manager", yaml_dict=args.split_manager)
        resume_training_dict = c_f.get_all_resume_training_config_diffs(configs_folder, temp_split_manager)

        if len(resume_training_dict) > 0:
            for sub_folder, num_epochs_dict in resume_training_dict.items():
                # train until the next config diff was made
                args.num_epochs_train = num_epochs_dict
                self.start_experiment(args)
                # Start fresh
                YR = self.setup_yaml_reader()
                if starting_fresh_hook: starting_fresh_hook(YR)
                # load the experiment configs, plus the config diffs 
                for k in glob.glob(os.path.join(sub_folder, "*")):
                    config_name = os.path.splitext(os.path.basename(k))[0]
                    experiment_config_paths[config_name].append(k)
                args, _, args.dict_of_yamls = YR.load_yamls(config_paths=experiment_config_paths, 
                                                            max_merge_depth=0, 
                                                            max_argparse_merge_depth=max_argparse_merge_depth,
                                                            merge_argparse=self.merge_argparse_when_resuming)
                args.resume_training = "latest"
        return self.start_experiment(args)