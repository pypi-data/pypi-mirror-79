# Copyright 2020 Google LLC
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
# Lint as: python3
"""Dataclasses for representing structured output.

Classes in this file should be used for actual input/output data,
rather than in spec() metadata.

These classes can replace simple dicts or namedtuples, with two major
advantages:
- Type-checking (via pytype) doesn't work for dict fields, but does work for
  these dataclasses.
- Performance and memory use may be better, due to the use of __slots__

See the documentation for attr.s (https://www.attrs.org/) for more details.

Classes inheriting from DataTuple will be handled by serialize.py, and available
on the frontend as corresponding JavaScript objects.
"""
import abc
from typing import List, Text, Tuple, Union

import attr


@attr.s(auto_attribs=True, frozen=True, slots=True)
class DataTuple(metaclass=abc.ABCMeta):
  """Simple dataclasses.

  These are intended to be used for actual data, such as returned by
  dataset.examples and model.predict().

  Contrast with LitType and descendants, which are used in model and dataset
  /specs/ to represent types and metadata.
  """
  pass


@attr.s(auto_attribs=True, frozen=True, slots=True)
class SpanLabel(DataTuple):
  """Dataclass for individual span label preds. Can use this in model preds."""
  start: int  # inclusive
  end: int  # exclusive
  label: Text


@attr.s(auto_attribs=True, frozen=True, slots=True)
class EdgeLabel(DataTuple):
  """Dataclass for individual edge label preds. Can use this in model preds."""
  span1: Tuple[int, int]  # inclusive, exclusive
  span2: Tuple[int, int]  # inclusive, exclusive
  label: Union[Text, int, float]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class SalienceMap(DataTuple):
  """Dataclass for a salience map over tokens."""
  tokens: List[str]
  salience: List[float]  # parallel to tokens
