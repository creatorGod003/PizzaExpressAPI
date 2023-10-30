from fastapi import APIRouter, Depends,status
from fastapi_jwt_auth import AuthJWT
from schemas import OrderModel, OrderStatusModel
from fastapi.exceptions import HTTPException
from database import Session, engine
from models import User, Order
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session=Session(bind=engine)

# Route to manage placing the order
@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_order(order:OrderModel,Authorize:AuthJWT=Depends() ):

    """
        ## Place an Order
        This requires the following
        - quantity : integer
        - pizza_size : string
    """

    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    # Get the jwt subject's username
    current_user_name = Authorize.get_jwt_subject()
    
    # Fetching the first record of User where subject' username matches with username in User table
    user = session.query(User).filter(current_user_name == User.username).first()

    # Creating a new Order object
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    # setting up the reference of user to whom order is belong
    new_order.user=user

    # adding the order to database
    session.add(new_order)
    # committing the changes
    session.commit()

    # preparing the response dictionary
    response = {
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    # return the response in json format
    return jsonable_encoder(response)

# Route to see all the orders made in the application
@order_router.get("/orders")
async def get_placed_orders(Authorize:AuthJWT=Depends()):
    
    """
        ## List of orders
        This lists all order made. It can be accessed by superusers

    """

    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # Get the jwt subject's username
    current_user_name = Authorize.get_jwt_subject()

    # Fetching the first record of User where subject' username matches with username in User table
    user = session.query(User).filter(User.username == current_user_name).first()

    # Return all orders as a response upon finding that subject is staff . Raise 403 error if not staff.
    if(user.is_staff == True):
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    else:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a superuser"
        )
    
# Route to get list of orders placed by User
@order_router.get("/user/orders")
async def get_placed_orders(Authorize:AuthJWT=Depends()):

    """
        ## List of orders ordered by loggedIn User
        This gets an order by its ID and can only be accessed by logged-in user
        This requires the following : 
        - id : integer
    """

    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # Get the jwt subject'username
    current_user_name = Authorize.get_jwt_subject()

    # Fetching the first record of User where subject' username matches with username in User table
    current_user = session.query(User).filter(User.username == current_user_name).first()

    # returning the orders of users
    return jsonable_encoder(current_user.orders)

# Route to get specific order placed by User
@order_router.get("/user/order/{id}")
async def get_specific_order(id:int, Authorize:AuthJWT=Depends()):

    """
        ## Get an order by specifying its ID.
        This returs an order with specified ID.
        This can only be accessed by logged-in user
        This requires the following
        - id : Integer

    """
    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # Get the jwt subject'username
    current_user_name = Authorize.get_jwt_subject()

    # Fetching the first record of User where subject'username matches with username in User table
    current_user = session.query(User).filter(User.username == current_user_name).first()

    # checking if order id required matched subject's order. If so return Order in json format Else raise 404 error
    for order in current_user.orders:
        if(order.id == id):
            return jsonable_encoder(order)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# Route to update the order details
@order_router.put("/order/update/{id}")
async def update_order(id:int, order:OrderModel , Authorize:AuthJWT=Depends()):

    """
        ## Update an order by specifying its ID.
        This updates an order with specified ID.
        This can only be accessed by logged-in user
        This requires the following
        - id : Integer
        - order : OrderModel
        
    """

    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # Get the jwt subject'username
    current_user_name = Authorize.get_jwt_subject()

    # Fetching the first record of User where subject'username matches with username in User table
    current_user = session.query(User).filter(User.username == current_user_name).first()

    # checking if order id required matched subject's order. If so made changes and return updated order in json format Else raise 404 error
    for user_order in current_user.orders:
        if(user_order.id == id):
            current_order = session.query(Order).filter(Order.id == user_order.id).first()
            if(current_order.order_status != 'PENDING'):
                session.commit()
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Order details cannot be changed when order is in transit")
                
            current_order.quantity = order.quantity
            current_order.pizza_size = order.pizza_size
            session.commit()

            response={
                "id":current_order.id,
                "quantity":current_order.quantity,
                "pizza_size":current_order.pizza_size,
                "order_status":current_order.order_status,
            }

            return jsonable_encoder(current_order)
            
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order with such id is not found")

# Route to update the status of order
@order_router.patch("/order/update/{id}")
async def update_order_status(id:int, order:OrderStatusModel, Authorize: AuthJWT=Depends()):

    """
        ## Update an status of order by specifying its ID.
        This updates an order status with specified ID.
        This can only be accessed by super user
        This requires the following
        - id : Integer
        - order : OrderStatusModel
    """

    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    # Get the jwt subject'username
    current_user = Authorize.get_jwt_subject()

    # Fetching the first record of User where subject'username matches with username in User table
    current_user_obj = session.query(User).filter(current_user == User.username).first()

    # checking if subject is staff or not. If so change the order status else raise 403 error
    if(current_user_obj.is_staff):
        requested_order = session.query(Order).filter(Order.id == id).first()
        requested_order.order_status = order.order_status
        session.commit()
        response = {
                "id":requested_order.id,
                "pizza_quantity":requested_order.quantity,
                "pizza_size":requested_order.pizza_size,
                "order_status":requested_order.order_status
            }
        return jsonable_encoder(response)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not super user")

# Route to delete the order with specific id
@order_router.delete("/order/delete/{id}")
async def delete_order(id:int, Authorize:AuthJWT=Depends()):

    """
        ## Delete an order by specifying its ID.
        This delete an order with specified ID.
        This can only be accessed by logged-in user
        This requires the following
        - id : Integer
        
    """

    # Verify access token. Raise 401 exception on being found invalid.
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # Get the jwt subject'username
    current_username = Authorize.get_jwt_subject()

    # Fetching the first record of User where subject'username matches with username in User table
    current_user = session.query(User).filter(current_username == User.username).first()

    # checking if order id required matched subject's order. If so delete the record and return messsage Else raise 404 error
    for placed_order in current_user.orders:
        
        if(placed_order.id == id):
            if(placed_order.status!='PENDING'):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Order cannot be deleted")
            session.query(Order).filter(Order.id == id).delete(synchronize_session='fetch')
            session.commit()
            return {"message": "Order deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
