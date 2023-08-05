import pytest

from ..utils import get_valid_identifier, load_metaschema
from ..schemaperfect import _FromDict, set_metaschema_version


@pytest.fixture
def refschema():
    return {
        '$ref': '#/definitions/Foo',
        'definitions': {
            'Foo': {'$ref': '#/definitions/Bar'},
            'Bar': {'$ref': '#/definitions/Baz'},
            'Baz': {'type': 'string'}
        }
    }


def test_get_valid_identifier():
    assert get_valid_identifier('$schema') == 'schema'
    assert get_valid_identifier('$ref') == 'ref'
    assert get_valid_identifier('foo-bar') == 'foobar'
    assert get_valid_identifier('$as') == 'as_'
    assert get_valid_identifier('for') == 'for_'
    assert get_valid_identifier('--') == '_'


@pytest.mark.parametrize('use_json', [True, False])
def test_hash_schema(refschema, use_json):
    copy = refschema.copy()
    copy['description'] = "A schema"
    copy['title'] = "Schema to test"
    assert _FromDict.hash_schema(refschema) == _FromDict.hash_schema(copy)


@pytest.mark.parametrize('draft_no', ['07', '06', '04', '03'])
def test_metaschema_version(draft_no):
    set_metaschema_version('draft' + str(int(draft_no)))
    metaschema = load_metaschema()
    id_key = "$id" if int(draft_no) >= 6 else "id"
    assert metaschema[id_key].split('//')[1].startswith("json-schema.org/draft-{0}".format(draft_no))
