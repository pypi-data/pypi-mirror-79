import datetime
import requests
import time

from crowdcurio_client.crowdcurio import CrowdCurioObject

class Annotation(CrowdCurioObject):
    _api_slug = 'annotation'
    _link_slug = 'annotation'
    _edit_attributes = (
        'created',
        'updated',
        'label',
        'position',
        'group',
        'sequence',
        'experiment',
        'data',
        'condition',
        'paid',
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id:
            return None
        return cls.where(id=id, slug=slug).next()

    def destroy(self):
        self.delete('{}'.format(self.id), json={'data': {'type':'Annotation', 'id': self.id}})
