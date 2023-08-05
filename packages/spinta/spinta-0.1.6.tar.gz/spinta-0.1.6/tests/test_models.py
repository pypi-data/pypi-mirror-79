import traceback

import pytest

from spinta.testing.utils import create_manifest_files
from spinta.testing.context import create_test_context


def check_store(rc, tmpdir, files):
    create_manifest_files(tmpdir, files)
    context = create_test_context(rc)
    context.load({
        'manifests': {
            'default': {
                'path': str(tmpdir),
            }
        }
    })


def test_engine_name_overshadow(rc, tmpdir):
    with pytest.raises(Exception) as e:
        check_store(rc, tmpdir, {
            'models/report.yml': {
                'type': 'model',
                'name': 'report',
                'endpoint': 'report',
            },
        })
    assert "Endpoint name can't overshadow existing model names and 'report' is already a model name." in str(e.value)


@pytest.mark.skip('datasets')
def test_engine_name_overshadow_other(rc, tmpdir):
    with pytest.raises(Exception) as e:
        check_store(rc, tmpdir, {
            'models/report.yml': {
                'type': 'model',
                'name': 'report',
            },
            'datasets/report.yml': {
                'type': 'dataset',
                'name': 'report',
                'resources': {
                    'res': {
                        'objects': {
                            '': {
                                'rep': {
                                    'endpoint': 'report',
                                }
                            }
                        }
                    }
                }
            },
        })
    traceback.print_exception(e.type, e.value, e.tb)
    assert "Endpoint name can't overshadow existing model names and 'report' is already a model name." in str(e.value)
