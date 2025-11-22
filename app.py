"""
ContentGenius - AI Content Generator SaaS
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from functools import wraps
import os
from datetime import datetime, timedelta
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import Database, User, Subscription, Generation
from auth import Auth
from stripe_handler import StripeHandler
from ai_generator import AIContentGenerator

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Initialize components
db = Database()
auth = Auth()
stripe_handler = StripeHandler()
ai_generator = AIContentGenerator()


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def subscription_required(f):
    """Decorator to require active subscription"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = db.get_user(session['user_id'])
        if not user or not user.has_active_subscription():
            return redirect(url_for('pricing'))

        return f(*args, **kwargs)
    return decorated_function


# ==================== Public Routes ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = auth.authenticate(email, password)
        if user:
            session['user_id'] = user.id
            session['email'] = user.email
            return jsonify({'success': True, 'redirect': '/dashboard'})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        # Check if user exists
        if db.get_user_by_email(email):
            return jsonify({'success': False, 'error': 'Email already registered'}), 400

        # Create user
        user = auth.create_user(email, password, name)

        # Create free tier subscription
        db.create_subscription(
            user_id=user.id,
            plan='free',
            status='active',
            generations_limit=5
        )

        session['user_id'] = user.id
        session['email'] = user.email

        return jsonify({'success': True, 'redirect': '/dashboard'})

    return render_template('signup.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))


# ==================== Protected Routes ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user = db.get_user(session['user_id'])
    subscription = db.get_user_subscription(user.id)
    generations = db.get_user_generations(user.id, limit=10)

    return render_template('dashboard.html',
                         user=user,
                         subscription=subscription,
                         generations=generations)


@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    """Content generation page"""
    if request.method == 'POST':
        data = request.json
        content_type = data.get('type')
        prompt = data.get('prompt')

        user = db.get_user(session['user_id'])
        subscription = db.get_user_subscription(user.id)

        # Check generation limit
        if not subscription.can_generate():
            return jsonify({
                'success': False,
                'error': 'Generation limit reached. Please upgrade your plan.'
            }), 403

        # Generate content
        try:
            content = ai_generator.generate(content_type, prompt, subscription.plan)

            # Save generation
            generation = db.create_generation(
                user_id=user.id,
                content_type=content_type,
                prompt=prompt,
                output=content
            )

            # Update usage
            subscription.increment_usage()

            return jsonify({
                'success': True,
                'content': content,
                'usage': {
                    'used': subscription.generations_used,
                    'limit': subscription.generations_limit
                }
            })

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    user = db.get_user(session['user_id'])
    subscription = db.get_user_subscription(user.id)

    return render_template('generate.html',
                         user=user,
                         subscription=subscription)


# ==================== Payment Routes ====================

@app.route('/subscribe/<plan>')
@login_required
def subscribe(plan):
    """Start subscription checkout"""
    user = db.get_user(session['user_id'])

    # Create Stripe checkout session
    checkout_url = stripe_handler.create_checkout_session(
        user_email=user.email,
        plan=plan,
        user_id=user.id
    )

    if checkout_url:
        return redirect(checkout_url)
    else:
        return "Error creating checkout session", 500


@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    event = stripe_handler.handle_webhook(payload, sig_header)

    if event:
        if event['type'] == 'checkout.session.completed':
            # Payment successful
            session_data = event['data']['object']
            user_id = session_data['client_reference_id']
            plan = session_data['metadata']['plan']

            # Update or create subscription
            db.update_subscription(
                user_id=user_id,
                plan=plan,
                status='active',
                stripe_customer_id=session_data['customer'],
                stripe_subscription_id=session_data['subscription']
            )

        elif event['type'] == 'customer.subscription.deleted':
            # Subscription cancelled
            subscription_id = event['data']['object']['id']
            db.cancel_subscription(stripe_subscription_id=subscription_id)

    return jsonify({'success': True})


@app.route('/success')
@login_required
def payment_success():
    """Payment success page"""
    return render_template('success.html')


@app.route('/cancel')
@login_required
def payment_cancel():
    """Payment cancelled page"""
    return redirect(url_for('pricing'))


# ==================== API Routes ====================

@app.route('/api/usage')
@login_required
def api_usage():
    """Get user usage stats"""
    user = db.get_user(session['user_id'])
    subscription = db.get_user_subscription(user.id)

    return jsonify({
        'plan': subscription.plan,
        'used': subscription.generations_used,
        'limit': subscription.generations_limit,
        'percentage': (subscription.generations_used / subscription.generations_limit * 100) if subscription.generations_limit > 0 else 0
    })


@app.route('/api/history')
@login_required
def api_history():
    """Get generation history"""
    user = db.get_user(session['user_id'])
    generations = db.get_user_generations(user.id, limit=50)

    return jsonify({
        'generations': [
            {
                'id': g.id,
                'type': g.content_type,
                'prompt': g.prompt,
                'output': g.output,
                'created_at': g.created_at.isoformat()
            }
            for g in generations
        ]
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Initialize database
    db.init_db()

    # Run app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
