import grpc
import shopping_pb2 as pb2
import shopping_pb2_grpc as pb2_grpc
import uuid

def register_seller(stub):
    ip=input("Enter address (ip:port): ")
    response = stub.RegisterSeller(pb2.RegisterSellerRequest(address=ip, uuid=str(uuid.uuid1())))
    print(response.message)

def sell_item(stub):
    product_name=input("Product: ")
    category=input("Category: ")
    quantity=int(input("Quantity"))
    description=input("Description")
    seller_address=input("Seller Address: ")
    price_per_unit=float(input("Price per unit: "))
    seller_uuid=input("Seller UUID: ")

    response = stub.SellItem(pb2.SellItemRequest(product_name=product_name,category =category,quantity =quantity,description =description,seller_address =seller_address,seller_uuid =seller_uuid,price_per_unit =price_per_unit))

    print(response.message)
    #print("Item ID:", response.item_id)

def update_item(stub):
    # item id , price, quantity,sellers address,uuid
    item_id=input("Enter item id")
    price_per_unit=int(input("Enter new price"))
    quantity=int(input("Enter new quantity"))
    seller_address=input("Enter Seller's address")
    seller_uuid=input("Enter UUID")
    
    response=stub.UpdateItem(pb2.UpdateItemRequest(
        item_id=item_id,
        price_per_unit=price_per_unit,
        quantity=quantity,
        seller_address=seller_address,
        seller_uuid=seller_uuid))
    print(response.message)


def delete_item(stub):
    item_id=input("Enter item id")
    seller_address=input("Enter Seller's address")
    seller_uuid=input("Enter UUID")
    response=stub.DeleteItem(pb2.DeleteItemRequest(
        item_id=item_id,seller_address=seller_address,
        seller_uuid=seller_uuid))
    print(response.message)

def display_seller_items(stub):
    seller_address=input("Enter Seller's address")
    seller_uuid=input("Enter UUID")
    #response=stub.DisplaySellerItems(pb2.DisplaySellerItemsRequest(seller_address,seller_uuid))
    #response = stub.DisplaySellerItems(pb2.DisplaySellerItemsRequest(seller_address=seller_address, seller_uuid=seller_uuid))
    response = stub.DisplaySellerItems(pb2.DisplaySellerItemsRequest(seller_address=seller_address, seller_uuid=seller_uuid))

    # Assuming response is an instance of DisplaySellerItemsResponse
    for item in response.items:
        # Access item details, e.g., item.id, item.price, etc.
        print("Item ID: ", item.item_id)
        print("Price: ", item.price_per_unit)
        print("Name: ", item.product_name)
        print("Category: ", item.category)
        print("Description: ", item.description)
        print("Quantity: ", item.quantity)
        print("Seller: ", item.seller)
        print("Rating: ", item.average_rating)

        # Work on ratings...................

        #print("Rating:", item.price)
    

def recieve_notification(stub):
    # Method to handle notification from the server
    response = stub.NotifyClient(pb2.NotifyClientRequest(notification_message="Notification message"))
    print("Notification:", response.message)


def seller_menu():
    print("1.Register Seller\n2.Sell Item\n3.UpdateItem\n4.DeleteItem\n5DisplaySellerItems\n")

def main():
    with grpc.insecure_channel('34.131.131.188:50051') as channel:
        stub = pb2_grpc.MarketStub(channel)

        while True:
            seller_menu()
            menu_option=int(input("Choose the menu option number: "))
            if menu_option==1:
                register_seller(stub)
            elif menu_option==2:
                sell_item(stub)
            elif menu_option==3:
                update_item(stub)
            elif menu_option==4:
                delete_item(stub)
            elif menu_option==5:
                display_seller_items(stub)
            elif menu_option==6:
                break

        


if __name__ == '__main__':
    main()
