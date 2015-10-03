import os

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec, NoteFilter
import evernote.edam.type.ttypes as ttypes


OUTPUT_DIR = '/Users/dan/src/1p/evernote'

def make_file_name(note, resource):
    suffix = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
    }[resource.mime]

    file_name = '%s-%s.%s' % (
        note.title.replace(' ', '-'),
        resource.guid,
        suffix)

    return os.path.join(OUTPUT_DIR, file_name)

auth_token = None
sandbox = False

client = EvernoteClient(token=auth_token, sandbox=sandbox)
note_store = client.get_note_store()

count = 100

notes_meta_list = note_store.findNotesMetadata(auth_token, NoteFilter(), 0, count, NotesMetadataResultSpec())

for note_meta in notes_meta_list.notes:
    note = note_store.getNote(auth_token, note_meta.guid, True, True, False, False)
    for resource in note.resources:
        with open(make_file_name(note, resource), 'wb') as fp:
            fp.write(resource.data.body)
