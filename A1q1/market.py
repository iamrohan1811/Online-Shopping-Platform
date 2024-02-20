# market.py
import grpc
from concurrent import futures
import shopping_pb2 as pb2
import shopping_pb2_grpc as pb2_grpc

items_number=1

class MarketServicer(pb2_grpc.MarketServicer):
    def __init__(self):
        self.sellers = {}
        self.items = {}
        self.wait_list = {}
        self.ratings = {}

    def _calculate_average_rating(self, item_id):
        total_ratings = sum(self.ratings[item_id].values())
        num_ratings = len(self.ratings[item_id])
        return total_ratings / num_ratings if num_ratings != 0 else 0

    def _notify_buyer(self, buyer_address, notification_message):
        with grpc.insecure_channel(buyer_address) as channel:
            stub = pb2_grpc.NotificationStub(channel)
            response = stub.NotifyClient(pb2.NotifyClientRequest(notification_message=notification_message))
            print("Notification sent to buyer:", response.message)

    def _notify_seller(self, seller_address, notification_message):
        with grpc.insecure_channel(seller_address) as channel:
            stub = pb2_grpc.NotificationStub(channel)
            response = stub.NotifyClient(pb2.NotifyClientRequest(notification_message=notification_message))
            print("Notification sent to seller:", response.message)

    def SearchItem(self, request, context):
        
        print("Search request for Item name:", request.item_name, "Category:", request.category)
        response = pb2.SearchItemResponse()
        for item_id, item_info in self.items.items():
            if request.item_name == "" or request.item_name==item_info['product_name']:
                if request.category == "ANY" or request.category == item_info['category']:
                    item = response.items.add()
                    item.item_id = item_id
                    item.product_name = item_info['product_name']
                    item.category = item_info['category']
                    item.quantity = item_info['quantity']
                    item.description = item_info['description']
                    item.price_per_unit = item_info['price_per_unit']
                    item.seller= item_info['seller_address']
        return response
        #pass

    def BuyItem(self, request, context):
        # Your existing code for buying items
        print(f"Buy request {request.quantity} of item {request.item_id}, from {request.buyer_address}")
        
        # Check if the item exists
        if request.item_id not in self.items:
            return pb2.BuyItemResponse(message="FAIL: Invalid item ID")
        
        item = self.items[request.item_id]
        
        # Check if there is enough stock
        if item['quantity'] < request.quantity:
            return pb2.BuyItemResponse(message="FAIL: Not enough stock available")
        
        # Update the item quantity
        item['quantity'] -= request.quantity
        
       
        return pb2.BuyItemResponse(message="SUCCESS")

    def UpdateItem(self, request, context):
        # Your existing code for updating items
        print("Update Item", request.item_id, "request from", request.seller_address)
        if request.seller_address not in self.sellers or self.sellers[request.seller_address] != request.seller_uuid:
            return pb2.UpdateItemResponse(message="FAIL: Invalid seller credentials")
        
        # verify credentials done above...................

        if request.item_id not in self.items:
            return pb2.UpdateItemResponse(message="FAIL: Item not found")
        
        self.items[request.item_id]['price_per_unit'] = request.price_per_unit
        self.items[request.item_id]['quantity'] = request.quantity

        
        return pb2.UpdateItemResponse(message="SUCCESS")

    def RateItem(self, request, context):
        # Your existing code for rating items
        print(f"{request.buyer_address} rated item {request.item_id} with {request.rating} stars.")

        # Check if the item exists
        if request.item_id not in self.items:
            return pb2.RateItemResponse(message="FAIL: Invalid item ID")

        # Check if the rating is valid
        if request.rating < 1 or request.rating > 5:
            return pb2.RateItemResponse(message="FAIL: Invalid rating. Rating must be between 1 and 5.")

        # Check if the buyer has already rated the item
        if request.item_id in self.ratings and request.buyer_address in self.ratings[request.item_id]:
            return pb2.RateItemResponse(message="FAIL: You have already rated this item.")

        # Store the rating
        if request.item_id not in self.ratings:
            self.ratings[request.item_id] = {}
        self.ratings[request.item_id][request.buyer_address] = request.rating

        return pb2.RateItemResponse(message="SUCCESS")
        pass

    def AddToWishList(self, request, context):
        print(f"Wishlist request of item {request.item_id}, from {request.buyer_address}")
        
        
        if request.item_id not in self.items:
            return pb2.AddToWishListResponse(message="FAIL: Invalid item ID")
        
        
        if request.item_id not in self.wait_list:
            self.wait_list[request.item_id] = []
        self.wait_list[request.item_id].append(request.buyer_address)
        
        return pb2.AddToWishListResponse(message="SUCCESS")

    def RegisterSeller(self, request, context):
        
        print("Seller join request from", request.address, "uuid =", request.uuid)
        if request.address in self.sellers:
            return pb2.RegisterSellerResponse(message="FAIL: Address already registered")
        else:
            self.sellers[request.address] = request.uuid
            return pb2.RegisterSellerResponse(message="SUCCESS")
        pass

    def SellItem(self, request, context):
        
        print("Sell Item request from", request.seller_address)
        global items_number
        
        unique_item_id=items_number
        items_number+=1
        unique_item_id=str(unique_item_id)
        # also take care of buyer rating for this item --------------------------[PRIORITY]

      
        self.items[unique_item_id] = {
            'item_id':unique_item_id,
            'product_name': request.product_name,
            'category': request.category,
            'quantity': request.quantity,
            'description': request.description,
            'seller_address': request.seller_address,
            'price_per_unit': request.price_per_unit
        }
        return pb2.SellItemResponse(message="SUCCESS")
        pass

    def DeleteItem(self, request, context):
        
        print("Delete Item", request.item_id, "request from", request.seller_address)
        if request.seller_address not in self.sellers or self.sellers[request.seller_address] != request.seller_uuid:
            return pb2.DeleteItemResponse(message="FAIL: Invalid seller credentials")
        if request.item_id not in self.items:
            return pb2.DeleteItemResponse(message="FAIL: Item not found")
        del self.items[request.item_id]
        return pb2.DeleteItemResponse(message="SUCCESS")
        pass

    def DisplaySellerItems(self, request, context):
        print("Display Items request from", request.seller_address)
        if request.seller_address not in self.sellers or self.sellers[request.seller_address] != request.seller_uuid:
            return pb2.DisplaySellerItemsResponse(message="FAIL: Invalid seller credentials")
        response = pb2.DisplaySellerItemsResponse()

        

        for item_id, item_info in self.items.items():
            if item_info['seller_address'] == request.seller_address:
                item = response.items.add()
                #print("working")
                
                item.item_id = str(item_id)
                #print("working")
                item.product_name = item_info['product_name']
                item.category = item_info['category']
                item.quantity = item_info['quantity']
                item.description = item_info['description']
                item.price_per_unit = item_info['price_per_unit']
                item.seller=item_info['seller_address']

                #calculated avg rating
                total_ratings = 0
                num_ratings = 0
                for buyer_address, rating in self.ratings.get(item_id, {}).items():
                    total_ratings += rating
                    num_ratings += 1
                average_rating = total_ratings / num_ratings if num_ratings > 0 else 0
                item.average_rating = average_rating 
                
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()


    server.wait_for_termination()

class NotificationServicer(pb2_grpc.NotificationServicer):
    def NotifyClient(self, request, context):
        print("Notification received:", request.notification_message)
        return pb2.NotifyClientResponse(message="Notification received successfully.")

if __name__ == '__main__':
    serve()
