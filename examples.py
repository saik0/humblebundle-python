__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

import humblebundle

# Start a new session.
# It's not a RESTful api, we must store an auth token in out session cookies.
client = humblebundle.HumbleApi()

# Login and store the auth cookie in the session
client.login("username@example.com", "secret")

# Download the list of orders for the current user
order_list = client.order_list()

# Download the subproduct listing for each order
# An order has information about a purchase, but not its contents
for order in order_list:
    # Fill in the subproducts (the titles purchased in the order)
    order.ensure_subproducts()
    # Print every game, ebook, audiobook, etc. for each order
    for subproduct in order.subproducts:
        print(subproduct.machine_name)

