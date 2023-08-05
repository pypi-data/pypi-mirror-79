import datetime
import json
import operator
import hashlib

import pytest


def sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()


@pytest.mark.skip('datasets')
def test_export_json(app, mocker):
    mocker.patch('spinta.backends.postgresql.sqlalchemy.utcnow', return_value=datetime.datetime(2019, 3, 6, 16, 15, 0, 816308))

    app.authorize(['spinta_set_meta_fields'])
    app.authmodel('country/:dataset/csv/:resource/countries', ['upsert', 'getall'])

    resp = app.post('/country/:dataset/csv/:resource/countries', json={'_data': [
        {
            '_op': 'upsert',
            '_type': 'country/:dataset/csv/:resource/countries',
            '_id': sha1('1'),
            '_where': '_id="' + sha1('1') + '"',
            'code': 'lt',
            'title': 'Lithuania',
        },
        {
            '_op': 'upsert',
            '_type': 'country/:dataset/csv/:resource/countries',
            '_id': sha1('2'),
            '_where': '_id="' + sha1('2') + '"',
            'code': 'lv',
            'title': 'LATVIA',
        },
        {
            '_op': 'upsert',
            '_type': 'country/:dataset/csv/:resource/countries',
            '_id': sha1('2'),
            '_where': '_id="' + sha1('2') + '"',
            'code': 'lv',
            'title': 'Latvia',
        },
    ]})
    assert resp.status_code == 200, resp.json()
    data = resp.json()['_data']
    revs = [d['_revision'] for d in data]

    resp = app.get('country/:dataset/csv/:resource/countries/:format/jsonl')
    data = sorted([json.loads(line) for line in resp.text.splitlines()], key=operator.itemgetter('code'))
    assert data == [
        {
            'code': 'lt',
            '_id': sha1('1'),
            '_revision': revs[0],
            'title': 'Lithuania',
            '_type': 'country/:dataset/csv/:resource/countries'
        },
        {
            'code': 'lv',
            '_id': sha1('2'),
            '_revision': revs[2],
            'title': 'Latvia',
            '_type': 'country/:dataset/csv/:resource/countries',
        },
    ]


@pytest.mark.skip('datasets')
def test_export_jsonl_with_all(app):
    app.authorize(['spinta_set_meta_fields'])
    app.authmodel('continent/:dataset/dependencies/:resource/continents', ['insert', 'getall'])
    app.authmodel('country/:dataset/dependencies/:resource/continents', ['insert', 'getall'])
    app.authmodel('capital/:dataset/dependencies/:resource/continents', ['insert', 'getall'])

    resp = app.post('/', json={'_data': [
        {
            '_type': 'continent/:dataset/dependencies/:resource/continents',
            '_op': 'insert',
            '_id': sha1('1'),
            'title': 'Europe',
        },
        {
            '_type': 'country/:dataset/dependencies/:resource/continents',
            '_op': 'insert',
            '_id': sha1('2'),
            'title': 'Lithuania',
            'continent': sha1('1'),
        },
        {
            '_type': 'capital/:dataset/dependencies/:resource/continents',
            '_op': 'insert',
            '_id': sha1('3'),
            'title': 'Vilnius',
            'country': sha1('2'),
        },
    ]})
    assert resp.status_code == 200, resp.json()

    resp = app.get('/:all/:dataset/dependencies/:resource/continents?format(jsonl)')
    assert resp.status_code == 200, resp.json()
    data = [json.loads(d) for d in resp.text.splitlines()]
    assert sorted(((d['_id'], d['title']) for d in data), key=lambda x: x[1]) == [
        (sha1('1'), 'Europe'),
        (sha1('2'), 'Lithuania'),
        (sha1('3'), 'Vilnius')
    ]
