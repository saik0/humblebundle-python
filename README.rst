humblebundle-python
===================

humblebundle-python is an unofficial library for querying the undocumented Humble Bundle API.


Usage
-----
Basic usage looks something like::

    client = humblebundle.HumbleApi()
    client.login("username@example.com", "secret")
    
    order_list = client.order_list()
    
    for order in order_list:
        order.ensure_subproducts()
        for subproduct in order.subproducts:
            print(subproduct)

See examples.py for more examples

humblebundle-python is not affiliated in any way with Humble Bundle, Inc.
