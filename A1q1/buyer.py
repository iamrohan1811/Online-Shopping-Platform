import grpc
import shopping_pb2 as pb2
import shopping_pb2_grpc as pb2_grpc

def search_item(stub):
    item_name=input("Item Name: ")
    category=input("Category: ")

    response = stub.SearchItem(pb2.SearchItemRequest(item_name=item_name, category=category))
    print("Search results:")
    for item in response.items:
        print(f"Item ID: {item.item_id},Price: {item.price_per_unit},Name: {item.product_name},Category: {item.category},Description: {item.description},Quantity Remaining: {item.quantity},Seller: {item.seller}")

def buy_item(stub):
    item_id = input("Enter item ID: ")
    quantity = int(input("Enter quantity: "))
    buyer_address = input("Enter buyer address (ip:port): ")

    response = stub.BuyItem(pb2.BuyItemRequest(
        item_id=item_id,
        quantity=quantity,
        buyer_address=buyer_address
    ))

    print(response.message)
    

def add_to_wishlist(stub):
    item_id = input("Enter item ID: ")
    buyer_address = input("Enter buyer address (ip:port): ")

    response = stub.AddToWishList(pb2.AddToWishListRequest(
        item_id=item_id,
        buyer_address=buyer_address
    ))

    print(response.message)

def rate_item(stub):
    item_id = input("Enter item ID: ")
    buyer_address = input("Enter buyer address (ip:port): ")
    rating=int(input("Enter rating: "))

    response=stub.RateItem(pb2.RateItemRequest(item_id=item_id,buyer_address=buyer_address,rating=rating))

    print(response.message)

def receive_notifications(stub):
    try:
        notification_iterator = stub.NotifyClient(pb2.NotifyClientRequest())
        for notification in notification_iterator:
            print("Notification:", notification.message)  # Print the notification message in the buyer's terminal
    except grpc.RpcError as rpc_error:
        print("Error occurred while receiving notifications:", rpc_error.details())

def buyer_menu():
    print("1.SearchItem\n2.BuyItem\n3.AddToWishList\n4.RateItem\n")

def main():
    with grpc.insecure_channel('34.131.131.188:50051') as channel:
        stub = pb2_grpc.MarketStub(channel)
        while True:
    
            buyer_menu()

            menu_option=int(input("Choose the menu option number: "))
            if menu_option==1:
                search_item(stub)
            elif menu_option==2:
                buy_item(stub)
            elif menu_option==3:
                add_to_wishlist(stub)
            elif menu_option==4:
                rate_item(stub)
            elif menu_option==5:
                break


if __name__ == '__main__':
    main()
