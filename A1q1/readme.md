Sellers and buyers can interact with the market by running the respective seller.py and buyer.py scripts.
Sellers can register, sell items, update items, delete items, and display their items.
Buyers can search for items, buy items, add items to the wishlist, rate items, and receive notifications.
Overall, the provided code implements a basic online shopping platform using gRPC for communication between the central market and the clients. Sellers can list their products, update inventory, and receive notifications, while buyers can search for items, make purchases, rate products, and receive notifications about updates.

0. Communication:
gRPC is used for communication between the central market (server) and the clients (sellers and buyers).
Clients make remote procedure calls (RPCs) to the server to perform various actions such as registering, buying, selling, updating, etc.
The server processes these requests, performs necessary operations, updates its internal state, and sends back responses to the clients.
Communication happens over the network using protocol buffers for message serialization/deserialization.

1. Market (market.py):
This file implements the gRPC server for the central shopping platform i.e as the market.
It provides functionalities such as registering sellers, selling items, updating items, deleting items, displaying seller items, searching items, buying items, adding items to the wishlist, rating items, and notifying clients (buyers/sellers).
The MarketServicer class defines the methods corresponding to these functionalities.
Each method handles the corresponding gRPC request and performs necessary operations such as updating internal data structures (e.g., sellers, items), validation of inputs, and sending notifications.
The serve() function starts the gRPC server.


2. Seller (seller.py):
This file implements the client-side functionality for sellers.
It provides options for sellers to interact with the market, such as registering as a seller, selling items, updating items, deleting items, and displaying their items.
Sellers can choose these options from a menu provided by the seller_menu() function.
Functions like register_seller(), sell_item(), update_item(), delete_item(), and display_seller_items() interact with the market via gRPC calls.


3. Buyer (buyer.py):
This file implements the client-side functionality for buyers.
It provides options for buyers to interact with the market, such as searching for items, buying items, adding items to the wishlist, rating items, and receiving notifications.
Buyers can choose these options from a menu provided by the buyer_menu() function.
Functions like search_item(), buy_item(), add_to_wishlist(), rate_item() interact with the market via gRPC calls.


4. Protocol Buffer Definitions (shopping.proto):
This file defines the protocol buffer messages and services used for communication between the market server and the clients.
Messages like RegisterSellerRequest, SellItemRequest, UpdateItemRequest, DeleteItemRequest, DisplaySellerItemsRequest, SearchItemRequest, BuyItemRequest, AddToWishListRequest, RateItemRequest, etc., represent the data exchanged between the server and clients.
Services like Market and Notification define the RPC methods available for clients to call.



