#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.transaction import inactive_records


class Location(metaclass=PoolMeta):
    __name__ = 'stock.location'
    # Restore warehouse as a Function field in this module because stock
    # replaced it with a property and search_warehouse requires a searcher.
    warehouse = fields.Function(
        fields.Many2One('stock.location', 'Warehouse'),
        'get_warehouse', searcher='search_warehouse')

    @classmethod
    def __setup__(cls):
        super().__setup__()

    def get_warehouse(self, name):
        # Order by descending left to get the first one in the tree
        with inactive_records():
            locations = self.search([
                    ('parent', 'parent_of', [self.id]),
                    ('type', '=', 'warehouse'),
                    ], order=[('left', 'DESC')])
        if locations:
            return locations[0].id

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
