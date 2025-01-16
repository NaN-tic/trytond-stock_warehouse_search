# This file is part stock_warehouse_search module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction


class StockWarehouseSearchTestCase(ModuleTestCase):
    'Test Stock Warehouse Search module'
    module = 'stock_warehouse_search'

    @with_transaction()
    def test_warehouse_search(self):
        'Test Warehouse Search'
        pool = Pool()
        Location = pool.get('stock.location')

        supplier, = Location.search([('code', '=', 'SUP')])
        storage, = Location.search([('code', '=', 'STO')])
        warehouse, = Location.search([('code', '=', 'WH')])
        self.assertNotEqual(len(Location.search([('warehouse.code', '=', 'WH')])), 0)


del ModuleTestCase
