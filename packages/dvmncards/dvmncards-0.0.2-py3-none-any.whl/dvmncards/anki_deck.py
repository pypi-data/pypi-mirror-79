from anki.exporting import *
from anki import Collection as aopen
import tempfile


col = None
ds = None
testDir = os.path.dirname(__file__)


def getEmptyCol():
    if len(getEmptyCol.master) == 0:
        (fd, nam) = tempfile.mkstemp(suffix=".anki2")
        os.close(fd)
        os.unlink(nam)
        col = aopen(nam)
        col.close(downgrade=False)
        getEmptyCol.master = nam
    (fd, nam) = tempfile.mkstemp(suffix=".anki2")
    shutil.copy(getEmptyCol.master, nam)
    col = aopen(nam)
    return col

getEmptyCol.master = ""


def add_new_card(deck, front, back,
                css=None, explination=None):
    if explination:
        deck.models.setCurrent(deck.models.byName("Basic (type in the answer)"))
        m = deck.models.current()
        if css:
            m['css'] = css
        field = deck.models.newField("Explination")
        deck.models.addField(m, field)
        card = deck.newNote()
        card['Front'] = front
        card['Back'] = back
        card['Explination'] = explination
        m['tmpls'][0]['afmt'] = '{{Front}}\n\n<hr id=answer>\n\n{{type:Back}}\n{{Explination}}'
    else:
        card = deck.newNote()
        card['Front'] = front
        card['Back'] = back
        if css:
            m = deck.models.current()
            m['css'] = css
    deck.addNote(card)


def add_image(deck,image,image_name='deck',extension_image='.jpeg'):
    image_path = f'{image_name}.{extension_image}'
    with open(image_path, 'wb') as f:
        f.write(image)
    deck.media.addFile(image_path)


def export_ankipkg(deck,path):
    export = AnkiPackageExporter(deck)
    export_path = os.path.normpath(path)
    export.includeHTML = True
    export.exportInto(export_path)


def test_export_ankipkg():
    deck = getEmptyCol()

    n = deck.newNote()
    #check Front card
    assert n["Front"] == ''
    n["Front"] = 'test'
    assert n["Front"] == 'test'

    # check Back card
    assert n["Back"] == ''
    n["Back"] = 'Тест'
    assert n["Back"] == 'Тест'

    #check css style of card
    current_models = deck.models.current()
    new_css = """.card {
                      font-family: arial;
                      font-size: 12px;
                      text-align: left;
                      color: yellow;
                      background-color: black;
                    }
                """
    current_models['css'] = new_css
    assert current_models['css'] == new_css

