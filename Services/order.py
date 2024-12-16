from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Models.models import Order, OrderStatus, PizzaOption,CustomizationOption,SelectedCustomization, OrderItem,OrderStatusByAdmin,User,Restaurant
from Schemas.order import OrderCreate
from config.O2Auth import get_current_user
from typing import Annotated
import razorpay


from config.eta import get_eta

from config.envFile import GOOGLE_MAPS_API_KEY

razorpay_client = razorpay.Client(auth=("rzp_test_EbeJ1sVuROEPXt", "1j8KhICswNhMfDMTHpWwto29"))
async def createOrder(request: OrderCreate, db: Session, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        print(current_user)
        # Check if an order already exists for the customer with a PENDING status
        order = db.query(Order).filter(
            Order.customer_id == current_user.id, Order.status == OrderStatus.PENDING
        ).first()
        if order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order already exists"
            )
        # Calculate ETA using Google Maps
        restaurant=db.query(Restaurant).filter(Restaurant.id==request.restaurant_id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )


        delivery_address = request.address
        estimated_delivery_time = await get_eta(GOOGLE_MAPS_API_KEY,restaurant.address,delivery_address)



        # Create a new order
        new_order = Order(
            restaurant_id=request.restaurant_id,
            customer_id=current_user.id,
            quantity=request.quantity,
            address=request.address,
            total_price=request.total_price,
            status=request.status,
            payment_status=request.payment_status,
            estimated_delivery_time=estimated_delivery_time

        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Initialize total order price
        total_order_price = 0.0

        # Create order items and calculate total price
        for item in request.items:
            # Fetch pizza option from database
            pizza_option = db.query(PizzaOption).filter(PizzaOption.id == item.pizza_option_id).first()
            if not pizza_option:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pizza Option not found"
                )

            # Calculate order item price
            item_total_price = pizza_option.base_price * item.quantity

            # Create an order item
            order_item = OrderItem(
                order_id=new_order.id,
                pizza_option_id=item.pizza_option_id,
                quantity=item.quantity,
                price=item_total_price
            )
            db.add(order_item)
            db.commit()
            db.refresh(order_item)

            # Initialize customization total price
            customization_total_price = 0.0

            # Handle customizations for the item
            for customization_data in item.customizations:
                customization_option = db.query(CustomizationOption).filter(
                    CustomizationOption.id == customization_data.customization_id
                ).first()
                if not customization_option:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Customization Option not found"
                    )

                # Calculate customization price
                customization_total_price += customization_option.price

                # Create a customization record
                db_customization = SelectedCustomization(
                    order_item_id=order_item.id,
                    customization_id=customization_option.id,
                    customization_price=customization_option.price
                )
                db.add(db_customization)

            # Update item price with customization total
            order_item.price += customization_total_price
            total_order_price += order_item.price
            db.commit()

        # Update total order price
        new_order.total_price = total_order_price
        db.commit()
        db.refresh(new_order)

        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create(data={
            "amount": int(total_order_price * 100),  # Convert to paise
            "currency": "INR",
            "receipt": f"order_{new_order.id}"
        })

        # Link Razorpay order ID to the order
        new_order.payment_gateway_order_id = razorpay_order.get("id")
        db.commit()
         # notify restaurant for new order
        return {
            "message": "Order created successfully",
            "data": new_order
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )
    # except razorpay.exceptions.Error as e:
    #     db.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Razorpay Error: {str(e)}"
    #     )

async def getOrders(db:Session):
    try:
        orders= db.query(Order).all()
        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found"
            )
        return {
            "message": "Orders fetched successfully",
            "data": orders
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


async def getOrderById(db:Session, id:int):
    try:
        order= db.query(Order).filter(Order.id == id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return {
            "message": "Order fetched successfully",
            "data": order
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

async def updateOrderStatusById(id:int,db:Session,request:OrderStatusByAdmin):
    try:
        order= db.query(Order).filter(Order.id == id, Order.status=="confirmed").first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        print(request)
        order.status=request
        db.commit()
        return {
            "message": "Order updated successfully",
            "data": order
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )