from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from Models.models import Order, OrderStatus, PizzaOption,CustomizationOption,SelectedCustomization, OrderItem
from Schemas.order import OrderCreate




async def createOrder(request:OrderCreate,db:Session):
    try:
        # create order if it already exists
        order = db.query(Order).filter(Order.customer_id == request.customer_id,Order.status==OrderStatus.PENDING).first()
        if order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order already exists"
            )

        new_order=Order(customer_id=request.customer_id,quantity=request.quantity,address=request.address,total_price=request.total_price,status=request.status,payment_status=request.payment_status)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # create order items in array
        for item in request.items:
            pizza_option=db.query(PizzaOption).filter(PizzaOption.id==item.pizza_option_id).first()
            if not pizza_option:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pizza Option not found"
                )
         # calculate customizationOptions
            customization_total_price=0.0
            selected_customization_options = []
            for customization_data in item.customizations:
                customization_option=db.query(CustomizationOption).filter(CustomizationOption.id==customization_data.customization_id).first()
                if not customization_option:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Customization Option not found"
                    )
                customization_total_price+=customization_option.price
                selected_customization_options.append(
                    SelectedCustomization(
                        customization_id=customization_option.id,
                        customization_price=customization_option.price,
                    )
                )

            base_price=pizza_option.base_price
            item_total_price=(base_price+customization_total_price)*item.quantity
            total_order_price=total_order_price+item_total_price

            # check if order already exists
            order_exits=db.query(OrderItem).filter(OrderItem.order_id==new_order.id,OrderItem.pizza_option_id==item.pizza_option_id).first()
            if order_exits:
                # update order item
                order_exits.quantity=order_exits.quantity+item.quantity
                order_exits.price=(base_price+customization_total_price)*order_exits.quantity
                order_exits.customizations.extend(selected_customization_options) # add selected customization options to order exits.

            else:
                # create order item
                new_order_item=OrderItem(pizza_option_id=item.pizza_option_id,quantity=item.quantity,customizations=selected_customization_options,price=item_total_price,order_id=new_order.id)
                db.add(new_order_item)


        new_order.total_price = total_order_price
        db.commit()

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