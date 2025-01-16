#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import PoolMeta


class Location(metaclass=PoolMeta):
    __name__ = 'stock.location'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.warehouse.searcher = 'search_warehouse'

    @classmethod
    def search_warehouse(cls, name, clause):
        warehouse_child_locations = cls.search([
            ('parent.type', '=', 'warehouse'),
            ('type', '=', 'storage'),
            ('parent', clause[1], clause[2]),
            ])
        found_warehouse_ids = []
        storage_location_ids = []
        for location in warehouse_child_locations:
            storage_location_ids.append(location.id)
            found_warehouse_ids.append(location.parent.id)
        warehouse_location_ids = []
        for location in cls.search([
                ('parent', 'child_of', storage_location_ids),
                ]):
            if (location.warehouse and location.warehouse.id in
                    found_warehouse_ids):
                warehouse_location_ids.append(location.id)
        return [('id', 'in', warehouse_location_ids)]
