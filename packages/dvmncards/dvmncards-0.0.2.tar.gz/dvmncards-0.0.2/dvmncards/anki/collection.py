# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from __future__ import annotations

import os
import time
import weakref


from anki.consts import *
from anki.decks import DeckManager
from anki.media import MediaManager
from anki.notes import Note


class Collection:

    def __init__(
        self,
        path: str,
        server: bool = False,
        log: bool = False,
    ) -> None:
        self._should_log = log
        self.server = server
        self.path = os.path.abspath(path)
        self.reopen()

        self._lastSave = time.time()
        self.media = MediaManager(self, server)
        self.decks = DeckManager(self)


    def name(self) -> Any:
        return os.path.splitext(os.path.basename(self.path))[0]

    def weakref(self) -> Collection:
        "Shortcut to create a weak reference that doesn't break code completion."
        return weakref.proxy(self)




    # Notes
    ##########################################################################

    def newNote(self, forDeck: bool = True) -> Note:
        "Return a new note with the current model."
        return Note(self, self.models.current(forDeck))

    def add_note(self, note: Note, deck_id: int) -> None:
        note.id = self.backend.add_note(note=note.to_backend_note(), deck_id=deck_id)

    # legacy

    def addNote(self, note: Note) -> int:
        self.add_note(note, note.model()["did"])
        return len(note.cards())




# legacy name
_Collection = Collection
