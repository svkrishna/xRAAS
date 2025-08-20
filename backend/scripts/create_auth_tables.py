#!/usr/bin/env python3
"""
Database migration script for authentication tables.
Creates all necessary tables for the authentication system.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.auth import Base, User, Tenant, TenantMembership, UserSession, APIKey, PasswordReset
from app.services.rbac_service import rbac_service
from app.schemas.auth import Role


def create_tables():
    """Create all authentication tables."""
    try:
        # Create database engine
        engine = create_engine(settings.database_url)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Authentication tables created successfully!")
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create default admin user if it doesn't exist
        create_default_admin(db)
        
        # Create default tenant if it doesn't exist
        create_default_tenant(db)
        
        db.close()
        print("✅ Default admin user and tenant created!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def create_default_admin(db):
    """Create a default admin user."""
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@xreason.com").first()
        if admin_user:
            print("ℹ️  Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@xreason.com",
            name="System Administrator",
            role=Role.OWNER,
            permissions=rbac_service.get_role_permissions(Role.OWNER),
            is_active=True,
            is_verified=True
        )
        admin_user.password = "admin123"  # Change this in production!
        
        db.add(admin_user)
        db.commit()
        print("✅ Default admin user created: admin@xreason.com / admin123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")


def create_default_tenant(db):
    """Create a default tenant."""
    try:
        # Check if default tenant already exists
        default_tenant = db.query(Tenant).filter(Tenant.slug == "xreason").first()
        if default_tenant:
            print("ℹ️  Default tenant already exists")
            return
        
        # Create default tenant
        default_tenant = Tenant(
            name="XReason",
            slug="xreason",
            domain="xreason.com",
            subscription_tier="enterprise",
            status="active"
        )
        
        db.add(default_tenant)
        db.commit()
        db.refresh(default_tenant)
        
        # Add admin user to default tenant
        admin_user = db.query(User).filter(User.email == "admin@xreason.com").first()
        if admin_user:
            membership = TenantMembership(
                user_id=admin_user.id,
                tenant_id=default_tenant.id,
                role=Role.OWNER,
                permissions=rbac_service.get_role_permissions(Role.OWNER)
            )
            db.add(membership)
            db.commit()
            print("✅ Default tenant created and admin user added")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating default tenant: {e}")


def drop_tables():
    """Drop all authentication tables (use with caution!)."""
    try:
        engine = create_engine(settings.database_url)
        Base.metadata.drop_all(bind=engine)
        print("✅ Authentication tables dropped successfully!")
        
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        print("⚠️  Dropping all authentication tables...")
        drop_tables()
    else:
        print("🚀 Creating authentication tables...")
        create_tables()
