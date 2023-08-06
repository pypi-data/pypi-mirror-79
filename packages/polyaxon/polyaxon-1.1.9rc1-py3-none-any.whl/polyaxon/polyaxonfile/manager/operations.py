#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy

from collections.abc import Mapping
from typing import Dict, Union

from polyaxon import pkg
from polyaxon.env_vars.getters.queue import get_queue_info
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
    get_specification,
    kinds,
)
from polyaxon.polyflow import V1Component, V1Operation


def get_op_specification(
    config: Union[V1Component, V1Operation] = None,
    hub: str = None,
    params: Dict = None,
    preset: str = None,
    queue: str = None,
    nocache: bool = None,
    path_context: str = None,
    validate_params: bool = True,
) -> V1Operation:
    job_data = {
        "version": config.version if config else pkg.SCHEMA_VERSION,
        "kind": kinds.OPERATION,
    }
    if params:
        if not isinstance(params, Mapping):
            raise PolyaxonfileError(
                "Params: `{}` must be a valid mapping".format(params)
            )
        job_data["params"] = params
    if preset:
        job_data["preset"] = preset
    if queue:
        # Check only
        get_queue_info(queue)
        job_data["queue"] = queue
    if nocache is not None:
        job_data["cache"] = {"disable": nocache}

    if config and config.kind == kinds.COMPONENT:
        job_data["component"] = config.to_dict()
        config = get_specification(data=[job_data])
    elif config and config.kind == kinds.OPERATION:
        config = get_specification(data=[config.to_dict(), job_data])
    elif hub:
        job_data["hubRef"] = hub
        config = get_specification(data=[job_data])

    if hub and config.hub_ref is None:
        config.hub_ref = hub
    hub = config.hub_ref
    public_hub = config.has_public_hub_reference
    params = copy.deepcopy(config.params)
    # Sanity check if params were passed and we are not dealing with a hub component
    if validate_params and not (hub and not public_hub):
        # Avoid in-place patch
        run_config = get_specification(config.to_dict())
        run_config = OperationSpecification.compile_operation(run_config)
        run_config.validate_params(params=params, is_template=False)
        if run_config.is_dag_run:
            run_config.run.set_path_context(path_context)
            CompiledOperationSpecification.apply_operation_contexts(run_config)
    return config
