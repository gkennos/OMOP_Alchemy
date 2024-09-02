from .episode import Episode
from .episode_event import Episode_Event
from .joined_mappers import Condition_Episode, Systemic_Therapy_Episode, Person_Episodes

for concept_linked_table in [Episode]:
    concept_linked_table.add_concepts()

__all__ = [Episode, Episode_Event, Condition_Episode, Systemic_Therapy_Episode, Person_Episodes]