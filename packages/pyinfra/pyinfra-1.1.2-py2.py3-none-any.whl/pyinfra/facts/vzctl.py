import json

from pyinfra.api import FactBase


class OpenvzContainers(FactBase):
    '''
    Returns a dict of running OpenVZ containers by CTID:

    .. code:: python

        {
            666: {
                'ip': [],
                'ostemplate': 'ubuntu...',
                ...
            },
            ...
        }
    '''

    command = 'vzlist -a -j'
    default = dict
    use_default_on_error = True

    @staticmethod
    def process(output):
        combined_json = ''.join(output)
        vz_data = json.loads(combined_json)

        return {
            int(vz.pop('ctid')): vz
            for vz in vz_data
        }
