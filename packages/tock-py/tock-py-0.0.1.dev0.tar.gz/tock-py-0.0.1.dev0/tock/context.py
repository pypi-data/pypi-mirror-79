# -*- coding: utf-8 -*-
from typing import Type, Optional

from tock.intent import Intent
from tock.models import Entity


class Context:

    def __init__(self, previous_intent: Optional[Intent] = None, current_story: Optional[Type] = None):
        self.current_story: Optional[Type] = current_story
        self.entities = []
        self.__previous_intent: Optional[Intent] = previous_intent

    def entity(self, entity_type: str) -> Optional[Entity]:
        for entity in reversed(self.entities):
            if entity.type == entity_type:
                return entity

    @property
    def previous_intent(self):
        return self.__previous_intent
