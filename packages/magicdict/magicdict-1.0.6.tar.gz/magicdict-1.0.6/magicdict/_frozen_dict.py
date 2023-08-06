#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2020 Kaede Hoshikawa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import Reversible, Mapping, Generic, TypeVar, Any, Dict, List, \
    Optional, Tuple, Iterator, Iterable, Union

from ._keys_view import MagicKeysView
from ._values_view import MagicValuesView
from ._items_view import MagicItemsView

import collections
import typing

__all__ = ["FrozenMagicDict"]

_K = TypeVar("_K")

_V = TypeVar("_V")

_T = TypeVar("_T")


class FrozenMagicDict(Reversible[_K], Mapping[_K, _V], Generic[_K, _V]):
    """
    An immutable ordered, one-to-many Mapping.
    """
    __slots__ = (
        "_next_index", "_first_values", "_pair_ids", "_kv_pairs",
        "_last_values")

    @staticmethod
    def _alter_key(key: _K) -> _K:
        return key

    @staticmethod
    def _maybe_alter_key(key: Any) -> Any:
        return key

    @typing.overload
    def __init__(self, **kwargs: _V) -> None:  # pragma: no cover
        ...

    @typing.overload  # noqa: F811
    def __init__(
        self, __map: Mapping[_K, _V],
            **kwargs: _V) -> None:  # pragma: no cover
        ...

    @typing.overload  # noqa: F811
    def __init__(
        self, __iterable: Iterable[Tuple[_K, _V]],
            **kwargs: _V) -> None:  # pragma: no cover
        ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: F811
        self._next_index = 0

        self._first_values: Dict[_K, _V] = {}

        self._pair_ids: Dict[_K, List[int]] = {}
        self._kv_pairs: \
            "collections.OrderedDict[int, Tuple[_K, _V]]" = \
            collections.OrderedDict()

        self._last_values: Dict[_K, _V] = {}

        if args:
            if len(args) > 1:  # pragma: no cover
                raise TypeError(
                    ("update expected at most 1 positional argument, "
                     "got {} args.").format(len(args)))

            if isinstance(args[0], collections.abc.Mapping):
                for k, v in args[0].items():
                    self._add_one(k, v)

            elif isinstance(args[0], collections.abc.Iterable):
                for k, v in args[0]:
                    self._add_one(k, v)

            else:  # pragma: no cover
                raise TypeError(
                    ("update expected a Mapping or an Iterable "
                     "as the positional argument, got {}.")
                    .format(type(args[0])))

        for k, v in kwargs.items():
            self._add_one(k, v)

    def _get_next_index(self) -> int:
        next_index = self._next_index
        self._next_index += 1

        return next_index

    def _add_one(self, key: _K, value: _V) -> None:
        key = self._alter_key(key)

        index = self._get_next_index()

        if key not in self._first_values:
            self._first_values[key] = value
            self._pair_ids[key] = [index]

        else:
            self._pair_ids[key].append(index)

        self._kv_pairs[index] = (key, value)
        self._last_values[key] = value

    def _has_value(self, value: Any) -> bool:
        for _, _value in self._kv_pairs.values():
            if _value == value:
                return True

        else:
            return False

    def __getitem__(self, key: _K) -> _V:
        key = self._alter_key(key)

        return self._first_values[key]

    def __iter__(self) -> Iterator[_K]:
        for key, _ in self._kv_pairs.values():
            yield key

    def __len__(self) -> int:
        return len(self._kv_pairs)

    def __contains__(self, key: Any) -> bool:
        key = self._maybe_alter_key(key)

        return key in self._first_values

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, collections.abc.Mapping):
            return self.items() == obj.items()

        return False

    def __ne__(self, obj: Any) -> bool:
        return not self.__eq__(obj)

    def __str__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            repr([(key, value) for (key, value) in self._kv_pairs.values()]))

    def __reversed__(self) -> Iterator[_K]:
        for key, _ in reversed(self._kv_pairs.values()):
            yield key

    @typing.overload
    def get_first(self, key: _K) -> Optional[_V]:
        ...

    @typing.overload
    def get_first(self, key: _K, default: _T = ...) -> Union[_V, _T]:
        ...

    def get_first(self, key: _K, default: Optional[_T] = None) -> \
            Optional[Union[_V, _T]]:
        """
        Return the first value for key if key is in the dictionary,
        else default. If default is not given, it defaults to `None`,
        so that this method never raises a `KeyError`.
        """
        key = self._alter_key(key)

        try:
            return self[key]

        except KeyError:
            return default

    @typing.overload
    def get(self, key: _K) -> Optional[_V]:
        ...

    @typing.overload
    def get(self, key: _K, default: _T = ...) -> Union[_V, _T]:
        ...

    def get(self, key: _K, default: Optional[_T] = None) -> \
            Optional[Union[_V, _T]]:
        return self.get_first(key, default)

    @typing.overload
    def get_last(self, key: _K) -> Optional[_V]:
        ...

    @typing.overload
    def get_last(self, key: _K, default: _T = ...) -> Union[_V, _T]:
        ...

    def get_last(self, key: _K, default: Optional[_T] = None) -> \
            Optional[Union[_V, _T]]:
        """
        Return the last value for key if key is in the dictionary,
        else default. If default is not given, it defaults to `None`,
        so that this method never raises a `KeyError`.
        """
        key = self._alter_key(key)

        try:
            return self._last_values[key]

        except KeyError:
            return default

    def get_iter(self, key: _K) -> Iterator[_V]:
        """
        Get an iterator that iterates over all the items matching the key.
        """
        key = self._alter_key(key)

        try:
            for index in self._pair_ids.get(key, []):
                _, value = self._kv_pairs[index]

                yield value

        except KeyError as e:  # pragma: no cover
            raise RuntimeError("Dictionary modified during iteration.") from e

    def get_list(self, key: _K) -> List[_V]:
        """
        Get a list that contains all the items matching the key.
        """
        return list(self.get_iter(key))

    def copy(self) -> "FrozenMagicDict[_K, _V]":
        return self.__class__(self)

    def keys(self) -> MagicKeysView[_K]:
        return MagicKeysView(self)

    def values(self) -> MagicValuesView[_V]:
        return MagicValuesView(self)

    def items(self) -> MagicItemsView[_K, _V]:
        return MagicItemsView(self)

    @classmethod
    @typing.overload
    def fromkeys(Cls, keys: Iterable[_K]) -> "FrozenMagicDict[_K, None]":
        ...

    @classmethod
    @typing.overload
    def fromkeys(Cls, keys: Iterable[_K],
                 value: _V) -> "FrozenMagicDict[_K, _V]":
        ...

    @classmethod
    def fromkeys(
        Cls, keys: Iterable[_K], value: Optional[_V] = None) -> \
            Union["FrozenMagicDict[_K, None]", "FrozenMagicDict[_K, _V]"]:
        def _gen() -> Iterator[Tuple[_K, Optional[_V]]]:
            for k in keys:
                yield (k, value)

        return Cls(_gen())  # type: ignore

    __repr__ = __str__
