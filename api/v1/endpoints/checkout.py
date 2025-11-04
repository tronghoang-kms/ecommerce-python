from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from fastapi.responses import JSONResponse
from schemas.checkout import CheckoutSessionResponse
from models.user import User
from security.auth import get_current_user
from services.cart_service import CartService, get_cart_service
from services.payment_service import PaymentService, get_payment_service
from services.order_service import OrderService, get_order_service
from core.config import settings
import stripe

router = APIRouter()

@router.post("/create-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
    payment_service: PaymentService = Depends(get_payment_service)
):
    cart_detail = await cart_service.get_user_cart(current_user)
    if not cart_detail.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
        
    try:
        session_id = payment_service.create_checkout_session(cart_detail, current_user)
        return CheckoutSessionResponse(session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        payload = await request.body()
        webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
        if not webhook_secret:
            print("STRIPE_WEBHOOK_SECRET is not set in settings")
            raise HTTPException(status_code=500, detail="Webhook secret not configured")

        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=stripe_signature, secret=webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        if session.payment_status == "paid":
            try:
                await order_service.create_order_from_stripe_session(session)
            except Exception as e:
                print(f"Failed to fulfill order for session {session.id}: {e}")
                return JSONResponse(status_code=500, content={"detail": "Failed to process order"})

    return {"status": "success"}

