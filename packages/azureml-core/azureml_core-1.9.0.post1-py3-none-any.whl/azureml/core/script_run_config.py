# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality to manage configuration for submitting training runs in Azure Machine Learning."""
import logging
from copy import deepcopy

from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._logging import ChainedIdentity
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data._dataset import _Dataset
from azureml.data._loggerfactory import collect_datasets_usage
from azureml.data.constants import _SCRIPT_RUN_SUBMIT_ACTIVITY, _DATASET_ARGUMENT_TEMPLATE, _SKIP_VALIDATE_DATASETS
from azureml.core.runconfig import Data
from azureml.exceptions import UserErrorException

from ._experiment_method import experiment_method
from .runconfig import RunConfiguration


module_logger = logging.getLogger(__name__)


def submit(script_run_config, workspace, experiment_name, run_id=None, _parent_run_id=None):
    """Submit and return a script run.

    This function creates an :class:`azureml.core.Experiment`, applies the run configuration,
    submits the run, and returns a :class:`azureml.core.script_run.ScriptRun` object.

    :param script_run_config: The configuration information for the run.
    :type script_run_config:  azureml.core.script_run_config.ScriptRunConfig
    :param workspace: A workspace in which to create the experiment.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The name of the experiment.
    :type experiment_name: str
    :param run_id: An optional ID of the run.
    :type run_id: str
    :param _parent_run_id: Internal use only.
    :type _parent_run_id: str
    :return: A script run object.
    :rtype: azureml.core.script_run.ScriptRun
    """
    from azureml.core import Experiment
    from azureml._execution import _commands
    from azureml._project.project import Project

    experiment = Experiment(workspace, experiment_name, _create_in_cloud=False)
    project = Project(directory=script_run_config.source_directory, experiment=experiment)

    run_config = get_run_config_from_script_run(script_run_config)
    dataset_consumptions = _update_args_and_inputs(workspace, run_config)
    collect_datasets_usage(module_logger, _SCRIPT_RUN_SUBMIT_ACTIVITY, dataset_consumptions,
                           workspace, run_config.target)
    run = _commands.start_run(project, run_config,
                              telemetry_values=script_run_config._telemetry_values,
                              run_id=run_id, parent_run_id=_parent_run_id)
    run.add_properties(global_tracking_info_registry.gather_all(script_run_config.source_directory))

    return run


def get_run_config_from_script_run(script_run_config):
    """Get the RunConfiguration object with parameters copied from the ScriptRunConfig.

    :param script_run_config: The ScriptRunConfig from which to get the run configuration.
    :type script_run_config:  azureml.core.script_run_config.ScriptRunConfig
    :return: The run configuration.
    :rtype: azureml.core.runconfig.RunConfiguration
    """
    # Gets a deep copy of run_config
    run_config = RunConfiguration._get_run_config_object(
        path=script_run_config.source_directory, run_config=script_run_config.run_config)

    if script_run_config.arguments:
        # Gets a deep copy of arguments as arguments contains not only simple type (e.g. DatasetConsumptionConfig)
        run_config.arguments = deepcopy(script_run_config.arguments)

    if script_run_config.script:
        run_config.script = script_run_config.script

    return run_config


def _update_args_and_inputs(workspace, run_config):
    def update_args_and_data(args, data):
        for index in range(len(args)):
            if isinstance(args[index], _Dataset):
                raise UserErrorException("Dataset cannot be used without providing a name for the run. Please provide "
                                         "a name by calling the as_named_input instance method on dataset.")
            if isinstance(args[index], Data):
                raise UserErrorException("azureml.core.runconfig.Data is not supported in arguments. Only "
                                         "DatasetConsumptionConfig is supported. It can be created by calling "
                                         "dataset.as_named_input('my_dataset')")
            if isinstance(args[index], DatasetConsumptionConfig):
                dataset = args[index]
                args[index].dataset._ensure_saved(workspace)
                if dataset.name in data:
                    module_logger.warning(("Dataset with the name {} is already defined in the data section of the "
                                           "RunConfiguration. The DatasetConsumptionConfig in the data section will "
                                           "be used to materialized the data").format(dataset.name))
                else:
                    data[dataset.name] = dataset
                if dataset.mode == 'direct':
                    args[index] = run_config.arguments[index].dataset.id
                    if not args[index]:
                        # Execution service will retrieve latest dataset by name
                        args[index] = _DATASET_ARGUMENT_TEMPLATE.format(dataset.name)
                else:
                    # the value will be replaced in the execution service with the path on compute
                    args[index] = _DATASET_ARGUMENT_TEMPLATE.format(dataset.name)

                # Set the environment variable for mount validation
                if dataset.dataset._consume_latest:
                    env_vars = run_config.environment.environment_variables
                    if _SKIP_VALIDATE_DATASETS not in env_vars:
                        env_vars[_SKIP_VALIDATE_DATASETS] = dataset.name
                    else:
                        env_vars[_SKIP_VALIDATE_DATASETS] = ",".join([env_vars[_SKIP_VALIDATE_DATASETS], dataset.name])

    dataset_consumptions = []

    def update_data(data):
        if data and not workspace:
            raise UserErrorException("Datasets cannot be used in experiments where workspace is not provided. "
                                     "Please make sure you create the experiment with a valid workspace.")
        for key, value in data.items():
            if isinstance(value, _Dataset):
                raise UserErrorException("Dataset cannot be used without providing a name for the run. Please provide "
                                         "a name by calling the as_named_input instance method on dataset.")
            elif isinstance(value, DatasetConsumptionConfig):
                value.dataset._ensure_saved(workspace)
                data[key] = Data.create(value)
                dataset_consumptions.append(value)
            elif not isinstance(value, Data):
                raise UserErrorException("{} cannot be used as data.".format(type(value).__name__))

    update_args_and_data(run_config.arguments, run_config.data)
    update_data(run_config.data)

    return dataset_consumptions


class ScriptRunConfig(ChainedIdentity):
    """Represents configuration information for submitting a training run in Azure Machine Learning.

    A ScriptRunConfig packages together environment configuration of :class:`azureml.core.runconfig.RunConfiguration`
    with a script for training to create a `script run`. In most typical scenarios, you will create
    a ScriptRunConfig object and then access RunConfiguration with the
    :func:`azureml.core.script_run_config.get_run_config_from_script_run` function.

    Once a script run is configured and submitted with the :meth:`azureml.core.Experiment.submit`
    method or with the :func:`azureml.core.script_run_config.submit` function, a
    :class:`azureml.core.script_run.ScriptRun` is returned.

    For examples of run configurations, see `Select and use a compute target to train your
    model <https://docs.microsoft.com/azure/machine-learning/how-to-set-up-training-targets>`_.

    .. remarks::

        The Azure Machine Learning SDK provides you with a series of interconnected classes, that are
        designed to help you train and compare machine learning models that are related by the shared
        problem that they are solving.

        An :class:`azureml.core.Experiment` acts as a logical container for these training runs. A
        :class:`azureml.core.RunConfiguration` object is used to codify the information necessary to
        submit a training run in an experiment. A ScriptRunConfig object is a helper class that packages
        the RunConfiguration object with an execution script for training.

        A ScriptRunConfig object is used to submit a training run as part of an Experiment.
        When a training run is submitted using a ScriptRunConfig object, the submit method returns an
        object of type :class:`azureml.core.ScriptRun`. The returned ScriptRun object gives you
        programmatic access to information about the training run. ScriptRun is a child class
        of :class:`azureml.core.Run`.

        The key concept to remember is that there are different configuration objects that are used to
        submit an experiment, based on what kind of run you want to trigger. The type of the configuration object
        then informs what child class of Run you get back from the submit method. When you pass a
        ScriptRunConfig object in a call to Experiment's submit method, you get back a ScriptRun object.
        Examples of other run objects returned include :class:`azureml.train.automl.run.AutoMLRun` (returned for
        an AutoML run) and :class:`azureml.pipeline.core.PipelineRun` (returned for a Pipeline run).

        The following sample shows how to submit a training script on your local machine.

        .. code-block:: python

                from azureml.core import ScriptRunConfig, RunConfiguration, Experiment

                # create or load an experiment
                experiment = Experiment(workspace, "MyExperiment")
                # By setting the user_managed_dependencies = True, the run uses the current python environment
                # in your local machine
                run_config=RunConfiguration()
                runconfig.environment.python.user_managed_dependencies = True
                # run a trial from the train.py code in your current directory
                config = ScriptRunConfig(source_directory='.', script='train.py', run_config=run_config)
                script_run = experiment.submit(config)

        For more examples showing how to work with ScriptRunConfig, see:

        * the article `Select and use a compute target to train your
          model <https://docs.microsoft.com/azure/machine-learning/how-to-set-up-training-targets>`_
        * these `training
          notebooks <https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/training>`_

    :param source_directory: The directory that contains the training script.
    :type source_directory: str
    :param script: The name of the training script, for example 'train.py'.
    :type script: str
    :param arguments: Optional command line arguments to pass to the training script.
        Arguments are passed in pairs, for example, ['--arg1', arg1_val, '--arg2', arg2_val].
    :type arguments: builtin.list[str]
    :param run_config: Optional run configuration to use.
    :type run_config: azureml.core.runconfig.RunConfiguration
    :param _telemetry_values: Internal use only.
    :type _telemetry_values: dict
    """

    @experiment_method(submit_function=submit)
    def __init__(self, source_directory, script=None, arguments=None, run_config=None, _telemetry_values=None):
        """Class ScriptRunConfig constructor.

        :param source_directory: The directory that contains the training script.
        :type source_directory: str
        :param script: The name of the training script, for example 'train.py'.
        :type script: str
        :param arguments: Optional command line arguments to pass to the training script.
            Arguments are passed in pairs, for example, ['--arg1', arg1_val, '--arg2', arg2_val].
        :type arguments: builtin.list[str]
        :param run_config: Optional run configuration to use.
        :type run_config: azureml.core.runconfig.RunConfiguration
        :param _telemetry_values: Internal use only.
        :type _telemetry_values: dict
        """
        self.source_directory = source_directory
        self.script = script
        self.arguments = arguments
        self.run_config = run_config if run_config else RunConfiguration()
        self._telemetry_values = _telemetry_values
