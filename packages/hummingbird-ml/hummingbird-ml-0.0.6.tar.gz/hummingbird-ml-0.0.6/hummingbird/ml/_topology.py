# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Converters for topology IR are stored in this file.
"""
from distutils.version import LooseVersion
import os
import torch
from uuid import uuid4

from onnxconverter_common.registration import get_converter
import onnx

from ._container import (
    PyTorchBackendModel,
    PyTorchSklearnContainerRegression,
    PyTorchSklearnContainerClassification,
    PyTorchSklearnContainerTransformer,
    PyTorchSklearnContainerAnomalyDetection,
    TorchScriptSklearnContainerRegression,
    TorchScriptSklearnContainerClassification,
    TorchScriptSklearnContainerTransformer,
    TorchScriptSklearnContainerAnomalyDetection,
    ONNXSklearnContainerRegression,
    ONNXSklearnContainerClassification,
    ONNXSklearnContainerTransformer,
    ONNXSklearnContainerAnomalyDetection,
)
from .exceptions import MissingConverter
from .operator_converters import constants


def convert(topology, backend, device, extra_config={}):
    """
    This function is used to convert a `onnxconverter_common.topology.Topology` object into a *backend* model.

    Args:
        topology: The `onnxconverter_common.topology.Topology` object that will be converted into a backend model
        backend: Which backend the model should be run on
        device: Which device the translated model will be run on
        extra_config: Extra configurations to be used by individual operator converters

    Returns:
        A model implemented in the selected backend
    """
    assert topology is not None, "Cannot convert a Topology object of type None."
    assert backend is not None, "Cannot convert a Topology object into backend None."
    assert device is not None, "Cannot convert a Topology object into device None."

    operator_map = {}

    for operator in topology.topological_operator_iterator():
        try:
            converter = get_converter(operator.type)

            if backend == onnx.__name__:
                # vers = LooseVersion(torch.__version__)
                # allowed_min = LooseVersion("1.6.0")
                # Pytorch <= 1.6.0 has a bug with exporting GEMM into ONNX.
                # For the moment only tree_trav is enabled for pytorch <= 1.6.0
                # if vers < allowed_min:
                extra_config[constants.TREE_IMPLEMENTATION] = "tree_trav"

            operator_map[operator.full_name] = converter(operator, device, extra_config)
        except ValueError:
            raise MissingConverter(
                "Unable to find converter for {} type {} with extra config: {}.".format(
                    operator.type, type(getattr(operator, "raw_model", None)), extra_config
                )
            )
        except Exception as e:
            raise e

    operators = list(topology.topological_operator_iterator())
    torch_model = PyTorchBackendModel(
        topology.raw_model.input_names, topology.raw_model.output_names, operator_map, operators, extra_config
    ).eval()

    if backend == onnx.__name__:
        onnx_model_name = output_model_name = None
        target_opset = 11

        # Set optional configuration options for ONNX if any.
        if constants.ONNX_OUTPUT_MODEL_NAME in extra_config:
            onnx_model_name = extra_config[constants.ONNX_OUTPUT_MODEL_NAME]
            output_model_name = onnx_model_name + ".onnx"
        if constants.ONNX_TARGET_OPSET in extra_config:
            target_opset = extra_config[constants.ONNX_TARGET_OPSET]
        if output_model_name is None:
            output_model_name = str(uuid4().hex) + ".onnx"

        # Put the tracing test input into the right format.
        trace_input = extra_config[constants.TEST_INPUT]
        if type(trace_input) is tuple:
            trace_input = tuple([torch.from_numpy(i) for i in trace_input])
        else:
            trace_input = torch.from_numpy(trace_input)

        # Generate the ONNX models
        torch.onnx.export(
            torch_model,
            trace_input,
            output_model_name,
            input_names=topology.raw_model.input_names,
            output_names=topology.raw_model.output_names,
            keep_initializers_as_inputs=False,
            opset_version=target_opset,
            do_constant_folding=True,
        )
        hb_model = onnx.load(output_model_name)
        os.remove(output_model_name)

        # Set the ONNX model name if any.
        if onnx_model_name is not None:
            hb_model.graph.name = onnx_model_name

        # Fix the model to use arbitrary batch dimensions
        def fix_dim(dim):
            updated = False
            if dim.HasField("dim_value"):
                dim.Clear()
                updated = True
                dim.dim_param = "sym"

            return updated

        def fix_value_info(value):
            num_fixed = 0
            if value.type.HasField("tensor_type"):
                shape = value.type.tensor_type.shape
                if shape:
                    dim = shape.dim[0]
                    if fix_dim(dim):
                        num_fixed += 1

            return num_fixed

        def fix_graph(graph):
            num_fixed = 0
            for input in graph.input:
                num_fixed += fix_value_info(input)

            for output in graph.output:
                num_fixed += fix_value_info(output)

            for node in graph.node:
                for attr in node.attribute:
                    if attr.HasField("g"):
                        num_fixed += fix_graph(attr.g)

            return num_fixed

        fix_graph(hb_model.graph)
    else:
        # Set the device for the model.
        if device != "cpu":
            if backend == torch.__name__ or torch.jit.__name__:
                torch_model = torch_model.to(device)

        # If the backend is tochscript, jit the model.
        if backend == torch.jit.__name__:
            test_data = torch.from_numpy(extra_config[constants.TEST_INPUT])
            if device != "cpu":
                test_data.to(device)
            torch_model = torch.jit.trace(torch_model, test_data).eval()
            torch.jit.optimized_execution(torch_model)
        hb_model = torch_model

    # Return if the container is not needed.
    if constants.CONTAINER in extra_config and not extra_config[constants.CONTAINER]:
        return hb_model

    # We scan the operators backwards until we find an operator with a defined type
    # This is necessary because ONNX models can have arbitrary operators doing casting, reshaping etc.
    idx = len(operators) - 1
    while (
        idx >= 0
        and not operator_map[operators[idx].full_name].regression
        and not operator_map[operators[idx].full_name].classification
        and not operator_map[operators[idx].full_name].anomaly_detection
        and not operator_map[operators[idx].full_name].transformer
    ):
        idx -= 1

    assert idx >= 0, "Cannot detect container type. Please fill an issue at https://github.com/microsoft/hummingbird."

    # If is a transformer, we need to check whether there is another operator type before.
    # E.g., normalization after classification.
    tmp_idx = idx
    if operator_map[operators[idx].full_name].transformer:
        while (
            idx > 0
            and not operator_map[operators[idx].full_name].regression
            and not operator_map[operators[idx].full_name].classification
            and not operator_map[operators[idx].full_name].anomaly_detection
        ):
            idx -= 1
        if idx < 0:
            idx = tmp_idx

    if operator_map[operators[idx].full_name].regression:
        # We are doing a regression task.
        if backend == torch.jit.__name__:
            container = TorchScriptSklearnContainerRegression
        elif backend == onnx.__name__:
            container = ONNXSklearnContainerRegression
        else:
            container = PyTorchSklearnContainerRegression
    elif operator_map[operators[idx].full_name].anomaly_detection:
        # We are doing anomaly detection.
        if backend == torch.jit.__name__:
            container = TorchScriptSklearnContainerAnomalyDetection
        elif backend == onnx.__name__:
            container = ONNXSklearnContainerAnomalyDetection
        else:
            container = PyTorchSklearnContainerAnomalyDetection
    elif operator_map[operators[idx].full_name].transformer:
        # We are just transforming the input data.
        if backend == torch.jit.__name__:
            container = TorchScriptSklearnContainerTransformer
        elif backend == onnx.__name__:
            container = ONNXSklearnContainerTransformer
        else:
            container = PyTorchSklearnContainerTransformer
    else:
        # We are doing a classification task.
        if backend == torch.jit.__name__:
            container = TorchScriptSklearnContainerClassification
        elif backend == onnx.__name__:
            container = ONNXSklearnContainerClassification
        else:
            container = PyTorchSklearnContainerClassification

    hb_model = container(hb_model, extra_config)

    return hb_model
