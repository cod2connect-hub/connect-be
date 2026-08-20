"""Stripe adapter."""

import stripe

from ...core.config import settings

stripe.api_key = settings.stripe_secret_key


class StripePaymentProvider:
    async def create_charge(self, tenant_id, amount_cents, currency, metadata) -> str:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            metadata={"tenant_id": str(tenant_id), **metadata},
        )
        return intent.id

    async def create_subscription(self, tenant_id, price_ids) -> str:
        sub = stripe.Subscription.create(
            customer=str(tenant_id),
            items=[{"price": p} for p in price_ids],
        )
        return sub.id
