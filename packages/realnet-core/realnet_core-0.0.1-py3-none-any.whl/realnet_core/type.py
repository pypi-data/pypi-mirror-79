import json

import realnet_core.item


class Type:

    def __init__(self, id, name, items=[], attributes=None):
        self.id = id
        self.name = name
        self.items = items
        self.attributes = attributes

    def create_item(self, id, name, attributes=None):
        return realnet_core.item.Item(id,
                                      name,
                                      self,
                                      attributes if attributes else {})

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'items': [item.to_dict() for item in self.items],
                'attributes': self.attributes if isinstance(self.attributes, dict) else {}}

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return Type(data['id'],
                    data['name'],
                    [realnet_core.item.Item.from_dict(item) for item in data['items']],
                    data['attributes'])

    @classmethod
    def from_json(cls, data):
        t = json.loads(data)
        return Type(t['id'],
                    t['name'],
                    [realnet_core.item.Item.from_dict(item) for item in t['items']],
                    t['attributes'])
