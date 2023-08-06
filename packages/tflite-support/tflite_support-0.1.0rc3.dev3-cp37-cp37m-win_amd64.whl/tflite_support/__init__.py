# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""An import entry for the TFLite Support project.

In the original project structure, all python targets are accessed by paths like
tensorflow_lite_support.metadata.metadata.MetadataDisplayer, which is verbose
and deep. This file provides some shortcuts. It's also compatible with our first
version Pip package.

In pip build, this file will be renamed as tflite_support/__init__.py.
"""


import sys as _sys

import flatbuffers as _flatbuffers
from tensorflow_lite_support.metadata import metadata as _metadata
from tensorflow_lite_support.metadata import metadata_schema_py_generated as _metadata_schema_py_generated
from tensorflow_lite_support.metadata import schema_py_generated as _schema_py_generated

# Shortcut metadata and schemas.
_current_module = _sys.modules[__name__]

setattr(_current_module, "metadata", _metadata)
setattr(_current_module, "metadata_schema_py_generated", _metadata_schema_py_generated)
setattr(_current_module, "schema_py_generated", _schema_py_generated)

# Compatible shortcut for Flatbuffers because we previously package flatbuffers
# in our pip package.
setattr(_current_module, "flatbuffers", _flatbuffers)
