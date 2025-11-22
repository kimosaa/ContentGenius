"""
Database models and operations
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List
import json


class User:
    def __init__(self, id, email, name, password_hash, created_at):
        self.id = id
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.created_at = created_at

    def has_active_subscription(self):
        """Check if user has active subscription"""
        db = Database()
        subscription = db.get_user_subscription(self.id)
        return subscription and subscription.status == 'active'


class Subscription:
    def __init__(self, id, user_id, plan, status, generations_limit, generations_used,
                 stripe_customer_id=None, stripe_subscription_id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.plan = plan
        self.status = status
        self.generations_limit = generations_limit
        self.generations_used = generations_used
        self.stripe_customer_id = stripe_customer_id
        self.stripe_subscription_id = stripe_subscription_id
        self.created_at = created_at

    def can_generate(self):
        """Check if user can generate content"""
        if self.plan == 'business':
            return True  # Unlimited
        return self.generations_used < self.generations_limit

    def increment_usage(self):
        """Increment generation usage"""
        db = Database()
        db.increment_generation_usage(self.id)
        self.generations_used += 1


class Generation:
    def __init__(self, id, user_id, content_type, prompt, output, created_at):
        self.id = id
        self.user_id = user_id
        self.content_type = content_type
        self.prompt = prompt
        self.output = output
        self.created_at = created_at


class Database:
    def __init__(self, db_path='contentgenius.db'):
        self.db_path = db_path

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                status TEXT NOT NULL,
                generations_limit INTEGER NOT NULL,
                generations_used INTEGER DEFAULT 0,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Generations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content_type TEXT NOT NULL,
                prompt TEXT NOT NULL,
                output TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    # ==================== User Operations ====================

    def create_user(self, email, password_hash, name):
        """Create new user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (email, password_hash, name)
            VALUES (?, ?, ?)
        ''', (email, password_hash, name))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return self.get_user(user_id)

    def get_user(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(**dict(row))
        return None

    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(**dict(row))
        return None

    # ==================== Subscription Operations ====================

    def create_subscription(self, user_id, plan, status, generations_limit,
                          stripe_customer_id=None, stripe_subscription_id=None):
        """Create new subscription"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO subscriptions
            (user_id, plan, status, generations_limit, stripe_customer_id, stripe_subscription_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, plan, status, generations_limit, stripe_customer_id, stripe_subscription_id))

        subscription_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return self.get_subscription(subscription_id)

    def get_subscription(self, subscription_id):
        """Get subscription by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM subscriptions WHERE id = ?', (subscription_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Subscription(**dict(row))
        return None

    def get_user_subscription(self, user_id):
        """Get user's active subscription"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM subscriptions
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC LIMIT 1
        ''', (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Subscription(**dict(row))
        return None

    def update_subscription(self, user_id, plan, status, stripe_customer_id=None, stripe_subscription_id=None):
        """Update or create subscription"""
        # Generation limits by plan
        limits = {
            'free': 5,
            'pro': 100,
            'business': 999999  # Unlimited
        }

        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if subscription exists
        cursor.execute('SELECT id FROM subscriptions WHERE user_id = ?', (user_id,))
        existing = cursor.fetchone()

        if existing:
            # Update existing
            cursor.execute('''
                UPDATE subscriptions
                SET plan = ?, status = ?, generations_limit = ?,
                    stripe_customer_id = ?, stripe_subscription_id = ?,
                    generations_used = 0
                WHERE user_id = ?
            ''', (plan, status, limits[plan], stripe_customer_id, stripe_subscription_id, user_id))
        else:
            # Create new
            cursor.execute('''
                INSERT INTO subscriptions
                (user_id, plan, status, generations_limit, stripe_customer_id, stripe_subscription_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, plan, status, limits[plan], stripe_customer_id, stripe_subscription_id))

        conn.commit()
        conn.close()

    def cancel_subscription(self, stripe_subscription_id):
        """Cancel subscription"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE subscriptions
            SET status = 'cancelled'
            WHERE stripe_subscription_id = ?
        ''', (stripe_subscription_id,))

        conn.commit()
        conn.close()

    def increment_generation_usage(self, subscription_id):
        """Increment generation usage count"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE subscriptions
            SET generations_used = generations_used + 1
            WHERE id = ?
        ''', (subscription_id,))

        conn.commit()
        conn.close()

    # ==================== Generation Operations ====================

    def create_generation(self, user_id, content_type, prompt, output):
        """Save generation"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO generations (user_id, content_type, prompt, output)
            VALUES (?, ?, ?, ?)
        ''', (user_id, content_type, prompt, output))

        generation_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return self.get_generation(generation_id)

    def get_generation(self, generation_id):
        """Get generation by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM generations WHERE id = ?', (generation_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            row_dict = dict(row)
            row_dict['created_at'] = datetime.fromisoformat(row_dict['created_at'])
            return Generation(**row_dict)
        return None

    def get_user_generations(self, user_id, limit=50):
        """Get user's generations"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM generations
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))

        rows = cursor.fetchall()
        conn.close()

        generations = []
        for row in rows:
            row_dict = dict(row)
            row_dict['created_at'] = datetime.fromisoformat(row_dict['created_at'])
            generations.append(Generation(**row_dict))

        return generations
