"""
Stripe payment integration
"""

import os
import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')


class StripeHandler:
    def __init__(self):
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

        # Price IDs for each plan (you'll get these from Stripe Dashboard)
        self.price_ids = {
            'pro': os.getenv('STRIPE_PRICE_ID_PRO'),
            'business': os.getenv('STRIPE_PRICE_ID_BUSINESS')
        }

    def create_checkout_session(self, user_email, plan, user_id):
        """Create Stripe checkout session"""
        try:
            # Get price ID for plan
            price_id = self.price_ids.get(plan)

            if not price_id:
                print(f"Warning: No price ID configured for plan '{plan}'")
                # Create a test price on the fly (for development)
                price_id = self._create_test_price(plan)

            success_url = os.getenv('APP_URL', 'http://localhost:5000') + '/success'
            cancel_url = os.getenv('APP_URL', 'http://localhost:5000') + '/cancel'

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=user_email,
                client_reference_id=str(user_id),
                metadata={'plan': plan}
            )

            return session.url

        except Exception as e:
            print(f"Error creating checkout session: {e}")
            return None

    def _create_test_price(self, plan):
        """Create test price for development"""
        prices = {
            'pro': 2900,  # $29.00
            'business': 7900  # $79.00
        }

        try:
            # Create product
            product = stripe.Product.create(
                name=f"ContentGenius {plan.title()} Plan"
            )

            # Create price
            price = stripe.Price.create(
                product=product.id,
                unit_amount=prices[plan],
                currency='usd',
                recurring={'interval': 'month'}
            )

            print(f"Created test price for {plan}: {price.id}")
            print(f"Add to .env: STRIPE_PRICE_ID_{plan.upper()}={price.id}")

            return price.id

        except Exception as e:
            print(f"Error creating test price: {e}")
            return None

    def create_payment_link(self, plan):
        """Create payment link for a plan"""
        try:
            price_id = self.price_ids.get(plan)

            if not price_id:
                price_id = self._create_test_price(plan)

            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    'price': price_id,
                    'quantity': 1
                }]
            )

            return payment_link.url

        except Exception as e:
            print(f"Error creating payment link: {e}")
            return None

    def handle_webhook(self, payload, sig_header):
        """Handle Stripe webhooks"""
        if not self.webhook_secret:
            # For development, skip signature verification
            import json
            return json.loads(payload)

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return event

        except ValueError:
            print("Invalid payload")
            return None
        except stripe.error.SignatureVerificationError:
            print("Invalid signature")
            return None

    def cancel_subscription(self, subscription_id):
        """Cancel a subscription"""
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            print(f"Error cancelling subscription: {e}")
            return False

    def get_customer_subscriptions(self, customer_id):
        """Get customer's subscriptions"""
        try:
            subscriptions = stripe.Subscription.list(customer=customer_id)
            return subscriptions.data
        except Exception as e:
            print(f"Error getting subscriptions: {e}")
            return []
