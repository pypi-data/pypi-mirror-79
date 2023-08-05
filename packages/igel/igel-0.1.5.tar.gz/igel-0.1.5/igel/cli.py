"""Console script for igel."""
import sys
import argparse
from igel import IgelModel


class CLI(object):
    """CLI describes a command line interface for interacting with igel, there
    are several different functions that can be performed. These functions are:

    - fit - fits a model on the input file specified to it
    - predict - Given a list of $hat{y}$ values, compute $d(\\hat{y}, y) under a
      specified metric

    """

    available_args = {
        "dp": "data_path",
        "yml": "yaml_path",
    }

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Igel CLI Runner',
            usage='''

                    igel <command> [<args>]
                    - Available sub-commands at the moment are:
                       fit                 fits a model
                       evaluate            evaluate the performance of a pre-fitted model
                       predict             Predicts using a pre-fitted model

                    - Available arguments:
                        --data_path         Path to your dataset
                        --yaml_file         Path to your yaml file
                        ------------------------------------------
                        or for a short version
                        -dp                 Path to your dataset
                        -yml                Path to your yaml file
''')

        self.parser.add_argument('command', help='Subcommand to run')
        self.cmd = self.parse_command()
        self.args = sys.argv[2:]
        self.dict_args = self.convert_args_to_dict()
        getattr(self, self.cmd.command)()

    def validate_args(self, dict_args: dict) -> dict:
        """
        validate arguments entered by the user and transform short args to the representation needed by igel
        @param dict_args: dict of arguments
        @return: new validated and transformed args

        """
        d_args = {}
        for k, v in dict_args.items():
            if k not in self.available_args.keys() and k not in self.available_args.values():
                print(f'Unrecognized argument -> {k}')
                self.parser.print_help()
                exit(1)

            elif k in self.available_args.values():
                d_args[k] = v

            else:
                d_args[self.available_args[k]] = v

        return d_args

    def convert_args_to_dict(self) -> dict:
        """
        convert args list to a dictionary
        @return: args as dictionary
        """

        dict_args = {self.args[i].replace('-', ''): self.args[i + 1] for i in range(0, len(self.args) - 1, 2)}
        dict_args = self.validate_args(dict_args)
        return dict_args

    def parse_command(self):
        """
        parse command, which represents the function that will be called by igel
        @return: command entered by the user
        """
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        cmd = self.parser.parse_args(sys.argv[1:2])
        if not hasattr(self, cmd.command):
            print('Unrecognized command')
            self.parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        return cmd

    def fit(self):
        IgelModel(self.cmd.command, **self.dict_args).fit()

    def predict(self):
        IgelModel(self.cmd.command, **self.dict_args).predict()

    def evaluate(self):
        IgelModel(self.cmd.command, **self.dict_args).evaluate()

    def algorithms(self):
        print(f"\n\n"
              f"{'*'*60}  Supported machine learning algorithms  {'*'*60} \n\n"
              f"1 - Regression algorithms: \n"
              f"{'-'*50} \n"
              f"{list(IgelModel.models_dict.get('regression').keys())} \n\n"
              f"{'='*120} \n"
              f"2 - Classification algorithms: \n"
              f"{'-'*50} \n"
              f"{list(IgelModel.models_dict.get('classification').keys())} \n"
              f" \n")

    def help(self):
        self.parser.print_help()


def main():
    CLI()


if __name__ == "__main__":
    main()
