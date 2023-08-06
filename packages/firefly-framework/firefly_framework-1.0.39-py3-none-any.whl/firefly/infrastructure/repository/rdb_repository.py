#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import List, Callable, Optional, Union

import firefly.domain as ffd
import firefly.infrastructure as ffi
import inflection
from firefly.domain.repository.repository import T


class RdbRepository(ffd.Repository[T]):
    def __init__(self, interface: ffi.RdbStorageInterface, table_name: str = None):
        super().__init__()

        self._entity_type = self._type()
        self._table = table_name or inflection.tableize(self._entity_type.get_fqn())
        self._interface = interface
        self._index = 0
        self._state = 'empty'

    def execute_ddl(self):
        self._interface.execute_ddl(self._type())

    def append(self, entity: T, **kwargs):
        self.debug('Entity added to repository: %s', str(entity))
        if entity not in self._entities:
            self._entities.append(entity)
        self._state = 'partial'

    def remove(self, entity: T, **kwargs):
        self.debug('Entity removed from repository: %s', str(entity))
        self._deletions.append(entity)
        if entity in self._entities:
            self._entities.remove(entity)

    def find(self, exp: Union[str, Callable], **kwargs) -> T:
        ret = None
        if isinstance(exp, str):
            entity = self._find_checked_out_entity(exp)
            if entity is not None:
                return entity
            ret = self._interface.find(exp, self._entity_type)
        else:
            results = self._interface.all(self._entity_type, self._get_search_criteria(exp))
            if len(results) > 0:
                ret = results[0]

        if ret:
            self._register_entity(ret)
            if self._state == 'empty':
                self._state = 'partial'

        return ret

    def raw(self, cb: Union[Callable, ffd.BinaryOp] = None, limit: int = None):
        criteria = None
        if cb is not None:
            criteria = self._get_search_criteria(cb)
        return self._interface.raw(self._entity_type, criteria, limit)

    def filter(self, cb: Union[Callable, ffd.BinaryOp], **kwargs) -> List[T]:
        if self._state == 'full':
            criteria = self._get_search_criteria(cb)
            entities = list(filter(lambda e: criteria.matches(e), self._entities))
        else:
            criteria = self._get_search_criteria(cb)
            entities = self._interface.all(self._entity_type, criteria=criteria)

            merged = []
            for entity in entities:
                if entity in self._entities:
                    merged.append(next(e for e in self._entities if e == entity))
                else:
                    merged.append(entity)
                    self._register_entity(entity)
            if self._state == 'empty':
                self._state = 'partial'
            entities = merged
        return entities

    def reduce(self, cb: Callable) -> Optional[T]:
        pass

    def __iter__(self):
        self._load_all()
        return iter(list(self._entities))

    def __next__(self):
        pass

    def __len__(self):
        self._load_all()
        return len(self._entities)

    def __getitem__(self, item):
        self._load_all()
        return self._entities[item]

    def _load_all(self):
        if self._state != 'full':
            for entity in self._interface.all(self._entity_type):
                if entity not in self._entities:
                    self._register_entity(entity)
            self._state = 'full'

    def commit(self, force_delete: bool = False):
        self.debug('commit() called in %s', str(self))
        for entity in self._deletions:
            self.debug('Deleting %s', entity)
            self._interface.remove(entity, force=force_delete)

        for entity in self._new_entities():
            self.debug('Adding %s', entity)
            self._interface.add(entity)

        for entity in self._changed_entities():
            self.debug('Updating %s', entity)
            self._interface.update(entity)
        self.debug('Done in commit()')

    def __repr__(self):
        return f'DbApiRepository[{self._entity_type}]'

    def _find_checked_out_entity(self, id_: str):
        for entity in self._entities:
            if entity.id_value() == id_:
                return entity

    def reset(self):
        super().reset()
        self._state = 'empty'
