from dataclasses import dataclass, replace
from functools import cached_property, lru_cache
from typing import List, Mapping

import jmespath


@lru_cache(maxsize=512)
def compile_expression(expression: str):
    return jmespath.compile(expression)


@dataclass
class Agon:
    expression: str

    @cached_property
    def compiled(self):
        return compile_expression(self.expression)

    def search(self, obj):
        return self.compiled.search(obj)

    def __or__(self, other):
        # self | other
        if isinstance(other, Agon):
            expression = " | ".join([self.expression, other.expression])
            return replace(self, expression=expression)
        if isinstance(other, str):
            expression = " | ".join([self.expression, other])
            return replace(self, expression=expression)
        return NotImplemented

    def __ror__(self, other):
        # other | self
        if isinstance(other, (List, Mapping)):
            return self.search(other)
        return NotImplemented
