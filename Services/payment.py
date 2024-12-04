
from fastapi import HTTPException,status,Request
from pydantic import constr
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from Models.models import Payment,Order,OrderStatus,PaymentStatus
import razorpay

from Schemas.payment import WebhookEvent
from fastapi.responses import JSONResponse

client = razorpay.Client(auth=("rzp_test_EbeJ1sVuROEPXt", "1j8KhICswNhMfDMTHpWwto29"))


async def verifyPayment(request: Request, db: Session):
    try:
        # Define your webhook secret
        webhook_secret = "789secret729A@"

        # Retrieve Razorpay signature from headers
        razorpay_signature = request.headers.get("X-Razorpay-Signature")
        if not razorpay_signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing Razorpay signature"
            )

        # Read the raw body of the request
        body = await request.body()

        # Verify the webhook signature
        try:
            client.utility.verify_webhook_signature(
                body.decode("utf-8"), razorpay_signature, webhook_secret
            )
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )

        # Parse the JSON payload if signature verification succeeds
        webhook_payload = await request.json()
        event = webhook_payload.get("event")
        payload = webhook_payload.get("payload")
        print(event)

        print(payload)

        if not event or not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook payload"
            )

        # Handle payment.captured event
        if event == "payment.captured":
            payment_data = payload["payment"]["entity"]
            payment_id = payment_data.get("id")
            razorpay_order_id = payment_data.get("order_id")
            payment_status = payment_data.get("status")
            payment_amount = payment_data.get("amount", 0) / 100

            # Check order in database
            order = db.query(Order).filter(Order.payment_gateway_order_id == razorpay_order_id).first()
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )

            # Create and update payment
            payment = Payment(
                order_id=order.id,
                razorpay_payment_id=payment_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_signature=razorpay_signature,
                payment_status="completed",
                payment_amount=payment_amount
            )
            db.add(payment)

            # Update order status based on payment status
            if payment_status == "captured":
                order.status = OrderStatus.CONFIRMED
                order.payment_status = PaymentStatus.COMPLETED
            elif payment_status == "failed":
                order.status = OrderStatus.CANCELLED
                order.payment_status = PaymentStatus.FAILED
            elif payment_status == "authorized":
                order.status = OrderStatus.PENDING
                order.payment_status = PaymentStatus.PENDING

            db.commit()
            return {
                "message": "Payment verified successfully",
                "data": {
                    "event": webhook_payload["event"],
                    "payload": webhook_payload["payload"]
                }
            }

        # Handle payment.failed event
        elif event == "payment.failed":
            payment_data = payload["payment"]["entity"]
            razorpay_order_id = payment_data.get("order_id")

            order = db.query(Order).filter(Order.payment_gateway_order_id == razorpay_order_id).first()
            if order:
                order.status = OrderStatus.CANCELLED
                order.payment_status = PaymentStatus.FAILED
                db.commit()
            return {
                "message": "Payment failed",
                "data": {
                    "event": webhook_payload["event"],
                    "payload": webhook_payload["payload"]
                }
            }

        # Unhandled event types
        else:
            return {
                "message": f"Unhandled event: {event}"
            }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database integrity error occurred"
        )

    finally:
        db.close()