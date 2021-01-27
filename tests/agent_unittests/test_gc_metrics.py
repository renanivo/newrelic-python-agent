# Copyright 2010 New Relic, Inc.
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

import os
import gc
import platform

import pytest

from newrelic.packages import six
from newrelic.samplers.gc_data import garbage_collector_data_source


@pytest.fixture
def data_source():
    sampler = garbage_collector_data_source(settings=())["factory"](environ=())
    sampler.start()
    yield sampler
    sampler.stop()


PID = os.getpid()

if six.PY2:
    EXPECTED_METRICS = (
        "GC/objects/%d/all" % PID,
        "GC/objects/%d/0" % PID,
        "GC/objects/%d/1" % PID,
        "GC/objects/%d/2" % PID,
    )
else:
    EXPECTED_METRICS = (
        "GC/objects/%d/all" % PID,
        "GC/objects/%d/0" % PID,
        "GC/objects/%d/1" % PID,
        "GC/objects/%d/2" % PID,
        "GC/collections/%d/all" % PID,
        "GC/collections/%d/0" % PID,
        "GC/collections/%d/1" % PID,
        "GC/collections/%d/2" % PID,
        "GC/collected/%d/all" % PID,
        "GC/collected/%d/0" % PID,
        "GC/collected/%d/1" % PID,
        "GC/collected/%d/2" % PID,
        "GC/uncollectable/%d/all" % PID,
        "GC/uncollectable/%d/0" % PID,
        "GC/uncollectable/%d/1" % PID,
        "GC/uncollectable/%d/2" % PID,
        "GC/time/%d/all" % PID,
        "GC/time/%d/0" % PID,
        "GC/time/%d/1" % PID,
        "GC/time/%d/2" % PID,
    )


@pytest.mark.xfail(
    platform.python_implementation() == "PyPy",
    reason="Not implemented on PyPy yet",
    strict=True,
    raises=AssertionError,
)
def test_gc_metrics_collection(data_source):
    gc.collect()
    metrics_table = dict(data_source() or ())

    for metric in EXPECTED_METRICS:
        assert metric in metrics_table