#Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Reflectance module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import sys

from tensorflow_graphics.reflectance import blinn_phong
from tensorflow_graphics.reflectance import lambertian
from tensorflow_graphics.reflectance import phong

# API contains submodules of tensorflow_graphics.transformation.
__all__ = [
    obj_name for obj_name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.ismodule(obj) and obj.__name__.rsplit(".", 1)[0] == __name__
]