import stripe
from core.config import settings
from models.user import User
from schemas.cart import CartDetail
from typing import List, Dict

class PaymentService:

    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_checkout_session(self, cart_detail: CartDetail, user: User) -> str:
        line_items = []
        for item in cart_detail.items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100), # Stripe tính bằng cent
                },
                'quantity': item.quantity,
            })
            
        redirect_base = None
        if getattr(settings, 'FRONTEND_URL', None):
            redirect_base = settings.FRONTEND_URL
        else:
            redirect_base = getattr(settings, 'BACKEND_URL', None) or 'http://localhost:8000'

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                # Use backend endpoints for API-only usage when no frontend is configured
                success_url=f"{redirect_base}/api/v1/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{redirect_base}/api/v1/checkout/cancel",
                metadata={
                    "user_id": str(user.id),
                    "user_email": user.email
                },
                customer_email=user.email
            )
            return checkout_session.id
        except Exception as e:
            raise e

def get_payment_service() -> PaymentService:
    return PaymentService()
