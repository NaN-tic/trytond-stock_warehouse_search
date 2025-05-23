# This file is part stock_warehouse_search module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import stock

def register():
    Pool.register(
        stock.Location,
        module='stock_warehouse_search', type_='model')
