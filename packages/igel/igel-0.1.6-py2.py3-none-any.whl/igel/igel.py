"""Main module."""

import pandas as pd
import pickle
import os
import json
import warnings
import logging

try:
    from igel.utils import read_yaml, extract_params, _reshape
    from igel.data import evaluate_model
    from igel.configs import configs
    from igel.data import models_dict, metrics_dict
    from igel.preprocessing import update_dataset_props
    from igel.preprocessing import handle_missing_values
except ImportError:
    from utils import read_yaml, extract_params, _reshape
    from data import evaluate_model
    from configs import configs
    from data import models_dict, metrics_dict
    from preprocessing import update_dataset_props
    from preprocessing import handle_missing_values, encode, normalize

from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class IgelModel(object):
    """
    IgelModel is the base model to use the fit, evaluate and predict functions of the sklearn library
    """
    supported_types = ('regression', 'classification')  # supported types that can be selected in the yaml file
    results_path = configs.get('results_path')  # path to the results folder
    default_model_path = configs.get('default_model_path')  # path to the pre-fitted model
    description_file = configs.get('description_file')  # path to the description.json file
    evaluation_file = configs.get('evaluation_file')  # path to the evaluation.json file
    prediction_file = configs.get('prediction_file')  # path to the predictions.csv
    default_dataset_props = configs.get('dataset_props')  # dataset props that can be changed from the yaml file
    default_model_props = configs.get('models_props')  # model props that can be changed from the yaml file
    model = None

    def __init__(self, command: str, **cli_args):
        logger.info(f"Entered CLI args:         {cli_args}")
        logger.info(f"Chosen command:           {command}")
        self.data_path: str = cli_args.get('data_path')  # path to the dataset

        if command == "fit":
            self.yml_path = cli_args.get('yaml_path')
            self.yaml_configs = read_yaml(self.yml_path)
            logger.info(f"your chosen configuration: {self.yaml_configs}")

            # dataset options given by the user
            self.dataset_props: dict = self.yaml_configs.get('dataset', self.default_dataset_props)
            # model options given by the user
            self.model_props: dict = self.yaml_configs.get('model', self.default_model_props)
            # list of target(s) to predict
            self.target: list = self.yaml_configs.get('target')

            self.model_type = self.model_props.get('type')
            logger.info(f"dataset_props: {self.dataset_props} \n"
                        f"model_props: {self.model_props} \n "
                        f"target: {self.target} \n")

        else:
            self.model_path = cli_args.get('model_path', self.default_model_path)
            logger.info(f"path of the pre-fitted model => {self.model_path}")
            with open(self.description_file, 'r') as f:
                dic = json.load(f)
                self.target: list = dic.get("target")  # target to predict as a list
                self.model_type: str = dic.get("type")  # type of the model -> regression or classification

    def _create_model(self):
        """
        fetch a model depending on the provided type and algorithm by the user and return it
        @return: class of the chosen model
        """
        model_type = self.model_props.get('type')
        model_algorithm = self.model_props.get('algorithm')
        if not model_type or not model_algorithm:
            raise Exception(f"model_type and algorithm cannot be None")
        algorithms = models_dict.get(model_type)  # extract all algorithms as a dictionary
        model = algorithms.get(model_algorithm)  # extract model class depending on the algorithm
        logger.info(f"Solving a {model_type} problem using ===> {model_algorithm}")
        if not model:
            raise Exception("Model not found in the algorithms list")
        else:
            return model

    def _save_model(self, model):
        """
        save the model to a binary file
        @param model: model to save
        @return: bool
        """
        try:
            if not os.path.exists(self.results_path):
                os.mkdir(self.results_path)
            else:
                logger.info(f"Folder {self.results_path} already exists")
                logger.warning(f"data in the {self.results_path} folder will be overridden. If you don't"
                               f"want this, then move the current {self.results_path} to another path")

        except OSError:
            logger.exception(f"Creating the directory {self.results_path} failed ")
        else:
            logger.info(f"Successfully created the directory in {self.results_path} ")
            pickle.dump(model, open(self.default_model_path, 'wb'))
            return True

    def _load_model(self, f: str = ''):
        """
        load a saved model from file
        @param f: path to model
        @return: loaded model
        """
        try:
            if not f:
                logger.info(f"result path: {self.results_path} ")
                logger.info(f"loading model form {self.default_model_path} ")
                model = pickle.load(open(self.default_model_path, 'rb'))
            else:
                logger.info(f"loading from {f}")
                model = pickle.load(open(f, 'rb'))
            return model
        except FileNotFoundError:
            logger.error(f"File not found in {self.default_model_path} ")

    def _prepare_fit_data(self):
        return self._process_data(fit=True)

    def _prepare_val_data(self):
        return self._process_data(fit=False)

    def _process_data(self, fit=True):
        """
        read and return data as x and y
        @return: list of separate x and y
        """
        assert isinstance(self.target, list), "provide target(s) as a list in the yaml file"
        assert len(self.target) > 0, "please provide at least a target to predict"
        try:
            dataset = pd.read_csv(self.data_path)
            logger.info(f"dataset shape: {dataset.shape}")
            attributes = list(dataset.columns)
            logger.info(f"dataset attributes: {attributes}")

            # handle missing values in the dataset
            preprocess_props = self.dataset_props.get('preprocess', None)
            if preprocess_props:
                # handle encoding
                encoding = preprocess_props.get('encoding')
                if encoding:
                    encoding_type = encoding.get('type', None)
                    column = encoding.get('column', None)
                    dataset = encode(df=dataset,
                                     encoding_type=encoding_type.lower(),
                                     column=column)
                    logger.info(f"shape of the dataset after encoding => {dataset.shape}")

                # preprocessing strategy: mean, median, mode etc..
                strategy = preprocess_props.get('missing_values')
                if strategy:
                    dataset = handle_missing_values(dataset,
                                                    strategy=strategy)
                    logger.info(f"shape of the dataset after handling missing values => {dataset.shape}")


            if any(col not in attributes for col in self.target):
                raise Exception("chosen target(s) to predict must exist in the dataset")

            y = pd.concat([dataset.pop(x) for x in self.target], axis=1)
            x = _reshape(dataset.to_numpy())
            y = _reshape(y.to_numpy())
            logger.info(f"y shape: {y.shape} and x shape: {x.shape}")

            # handle data scaling
            if preprocess_props:
                scaling_props = preprocess_props.get('scale', None)
                if scaling_props:
                    scaling_method = scaling_props.get('method', None)
                    scaling_target = scaling_props.get('target', None)
                    if scaling_target == 'all':
                        x = normalize(x, method=scaling_method)
                        y = normalize(y, method=scaling_method)
                    elif scaling_target == 'inputs':
                        x = normalize(x, method=scaling_method)
                    elif scaling_target == 'outputs':
                        y = normalize(y, method=scaling_method)

            if not fit:
                return x, y

            split_options = self.dataset_props.get('split')
            test_size = split_options.get('test_size')
            shuffle = split_options.get('shuffle')
            stratify = split_options.get('stratify')
            x_train, x_test, y_train, y_test = train_test_split(x,
                                                                y,
                                                                test_size=test_size,
                                                                shuffle=shuffle,
                                                                stratify=None if not stratify or stratify.lower() == "none" else stratify)
            return x_train, y_train, x_test, y_test

        except Exception as e:
            logger.exception(f"error occured while preparing the data: {e.args}")

    def _prepare_predict_data(self):
        """
        read and return x_pred
        @return: x_pred
        """
        try:
            x_val = pd.read_csv(self.data_path)
            logger.info(f"shape of the prediction data: {x_val.shape}")

            return _reshape(x_val)
        except Exception as e:
            logger.exception(f"exception while preparing prediction data: {e}")

    def fit(self, **kwargs):
        """
        fit a machine learning model and save it to a file along with a description.json file
        @return: None
        """
        x_train, y_train, x_test, y_test = self._prepare_fit_data()
        model_class = self._create_model()
        self.model = model_class(**kwargs)
        logger.info(f"executing a {self.model.__class__.__name__} algorithm ..")

        self.model.fit(x_train, y_train)

        saved = self._save_model(self.model)
        if saved:
            logger.info(f"model saved successfully and can be found in the {self.results_path} folder")
        test_predictions = self.model.predict(x_test)
        eval_results = evaluate_model(model_type=self.model_type,
                                      y_pred=test_predictions,
                                      y_true=y_test,
                                      **kwargs)
        fit_description = {
            "model": self.model.__class__.__name__,
            "type": self.model_props['type'],
            "algorithm": self.model_props['algorithm'],
            "data path": self.data_path,
            "train data shape": x_train.shape,
            "test data shape": x_test.shape,
            "train data size": x_train.shape[0],
            "test data size": x_test.shape[0],
            "results path": str(self.results_path),
            "model path": str(self.default_model_path),
            "target": self.target,
            "results on test data": eval_results
        }

        try:
            logger.info(f"saving fit description to {self.description_file}")
            with open(self.description_file, 'w', encoding='utf-8') as f:
                json.dump(fit_description, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.exception(f"Error while storing the fit description file: {e}")

    def evaluate(self, **kwargs):
        """
        evaluate a pre-fitted model and save results to a evaluation.json
        @return: None
        """
        try:
            model = self._load_model()
            x_val, y_true = self._prepare_val_data()
            y_pred = model.predict(x_val)
            eval_results = evaluate_model(model_type=self.model_type,
                                          y_pred=y_pred,
                                          y_true=y_true,
                                          **kwargs)

            logger.info(f"saving fit description to {self.evaluation_file}")
            with open(self.evaluation_file, 'w', encoding='utf-8') as f:
                json.dump(eval_results, f, ensure_ascii=False, indent=4)

        except Exception as e:
            logger.exception(f"error occured during evaluation: {e}")

    def predict(self):
        """
        use a pre-fitted model to make predictions and save them as csv
        @return: None
        """
        try:
            model = self._load_model(f=self.model_path)
            x_val = self._prepare_predict_data()
            y_pred = model.predict(x_val)
            y_pred = _reshape(y_pred)
            logger.info(f"predictions array type: {type(y_pred)}")
            logger.info(f"predictions shape: {y_pred.shape} | shape len: {len(y_pred.shape)}")
            logger.info(f"predict on targets: {self.target}")
            df_pred = pd.DataFrame.from_dict(
                {self.target[i]: y_pred[:, i] if len(y_pred.shape) > 1 else y_pred for i in range(len(self.target))})

            logger.info(f"saving the predictions to {self.prediction_file}")
            df_pred.to_csv(self.prediction_file)

        except Exception as e:
            logger.exception(f"Error while preparing predictions: {e}")


if __name__ == '__main__':
    mock_params = {'data_path': '/home/nidhal/my_projects/igel/examples/data/Iris.csv',  # '/home/nidhal/my_projects/igel/examples/data/indians-diabetes.csv',
                   'yaml_path': '/home/nidhal/my_projects/igel/examples/iris_example.yaml'}
    reg = IgelModel('fit', **mock_params)
    reg.fit()
    # reg.predict()
