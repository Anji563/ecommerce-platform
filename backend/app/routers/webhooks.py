import hmac
import hashlib
import os
import json
import stripe
from fastapi import APIRouter, Request, HTTPException, Header, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderStatus, ProcessedWebhook
from app.tasks import generate_pdf_invoice, send_transactional_email

router = APIRouter(prefix="/api/v1/webhooks", tags=["Webhooks"])

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")

@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    db: Session = Depends(get_db)
):
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing signature header")

    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook verification failed: {str(e)}")

    event_id = event["id"]
    
    # Idempotency Check
    if db.query(ProcessedWebhook).filter_by(event_id=event_id).first():
        return {"status": "already_processed"}

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        order_id = payment_intent.get("metadata", {}).get("order_id")
        user_email = payment_intent.get("metadata", {}).get("user_email")

        if order_id:
            order = db.query(Order).filter(Order.id == int(order_id)).first()
            if order:
                order.status = OrderStatus.PAID
                db.add(ProcessedWebhook(event_id=event_id, provider="stripe"))
                db.commit()

                # Queue Celery tasks asynchronously
                chain = generate_pdf_invoice.s(order.id) | send_transactional_email.s(user_email=user_email, order_id=order.id)
                chain.apply_async()

    return {"status": "success"}

@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None, alias="x-razorpay-signature"),
    db: Session = Depends(get_db)
):
    if not x_razorpay_signature:
        raise HTTPException(status_code=400, detail="Missing signature header")

    payload = await request.body()
    generated_sig = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(generated_sig, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    data = json.loads(payload.decode("utf-8"))
    event_id = data.get("event_id")

    if db.query(ProcessedWebhook).filter_by(event_id=event_id).first():
        return {"status": "already_processed"}

    if data.get("event") == "payment.captured":
        entity = data["payload"]["payment"]["entity"]
        order_id = entity.get("notes", {}).get("order_id")
        user_email = entity.get("email")

        if order_id:
            order = db.query(Order).filter(Order.id == int(order_id)).first()
            if order:
                order.status = OrderStatus.PAID
                db.add(ProcessedWebhook(event_id=event_id, provider="razorpay"))
                db.commit()

                chain = generate_pdf_invoice.s(order.id) | send_transactional_email.s(user_email=user_email, order_id=order.id)
                chain.apply_async()

    return {"status": "success"}
