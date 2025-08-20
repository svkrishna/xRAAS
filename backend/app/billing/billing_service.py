"""
Billing Service for XReason
Handles invoices, payments, and billing operations.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class InvoiceStatus(str, Enum):
    """Invoice status enumeration."""
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    VOID = "void"


class PaymentMethodType(str, Enum):
    """Payment method types."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    WIRE_TRANSFER = "wire_transfer"


@dataclass
class PaymentMethod:
    """Payment method information."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    user_id: Optional[str] = None
    type: PaymentMethodType = PaymentMethodType.CREDIT_CARD
    name: str = ""
    last_four: str = ""
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    is_default: bool = False
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "type": self.type.value,
            "name": self.name,
            "last_four": self.last_four,
            "expiry_month": self.expiry_month,
            "expiry_year": self.expiry_year,
            "is_default": self.is_default,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaymentMethod':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            tenant_id=data.get("tenant_id", ""),
            user_id=data.get("user_id"),
            type=PaymentMethodType(data.get("type", "credit_card")),
            name=data.get("name", ""),
            last_four=data.get("last_four", ""),
            expiry_month=data.get("expiry_month"),
            expiry_year=data.get("expiry_year"),
            is_default=data.get("is_default", False),
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )


@dataclass
class InvoiceItem:
    """Individual item on an invoice."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    quantity: float = 1.0
    unit_price: float = 0.0
    amount: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate amount if not set."""
        if self.amount == 0.0:
            self.amount = self.quantity * self.unit_price
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "metadata": self.metadata
        }


@dataclass
class Invoice:
    """Invoice for billing."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    invoice_number: str = ""
    status: InvoiceStatus = InvoiceStatus.DRAFT
    issue_date: datetime = field(default_factory=datetime.utcnow)
    due_date: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=30))
    paid_date: Optional[datetime] = None
    
    # Billing information
    billing_name: str = ""
    billing_email: str = ""
    billing_address: Dict[str, str] = field(default_factory=dict)
    
    # Financial information
    subtotal: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    total_amount: float = 0.0
    currency: str = "USD"
    
    # Items
    items: List[InvoiceItem] = field(default_factory=list)
    
    # Metadata
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Calculate totals if not set."""
        if self.total_amount == 0.0:
            self.calculate_totals()
    
    def calculate_totals(self) -> None:
        """Calculate invoice totals."""
        self.subtotal = sum(item.amount for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def add_item(self, item: InvoiceItem) -> None:
        """Add an item to the invoice."""
        self.items.append(item)
        self.calculate_totals()
        self.updated_at = datetime.utcnow()
    
    def remove_item(self, item_id: str) -> None:
        """Remove an item from the invoice."""
        self.items = [item for item in self.items if item.id != item_id]
        self.calculate_totals()
        self.updated_at = datetime.utcnow()
    
    def mark_as_paid(self, paid_date: Optional[datetime] = None) -> None:
        """Mark invoice as paid."""
        self.status = InvoiceStatus.PAID
        self.paid_date = paid_date or datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "invoice_number": self.invoice_number,
            "status": self.status.value,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "paid_date": self.paid_date.isoformat() if self.paid_date else None,
            "billing_name": self.billing_name,
            "billing_email": self.billing_email,
            "billing_address": self.billing_address,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "items": [item.to_dict() for item in self.items],
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Invoice':
        """Create from dictionary."""
        invoice = cls(
            id=data.get("id", str(uuid.uuid4())),
            tenant_id=data.get("tenant_id", ""),
            invoice_number=data.get("invoice_number", ""),
            status=InvoiceStatus(data.get("status", "draft")),
            issue_date=datetime.fromisoformat(data.get("issue_date", datetime.utcnow().isoformat())),
            due_date=datetime.fromisoformat(data.get("due_date", (datetime.utcnow() + timedelta(days=30)).isoformat())),
            billing_name=data.get("billing_name", ""),
            billing_email=data.get("billing_email", ""),
            billing_address=data.get("billing_address", {}),
            subtotal=data.get("subtotal", 0.0),
            tax_amount=data.get("tax_amount", 0.0),
            discount_amount=data.get("discount_amount", 0.0),
            total_amount=data.get("total_amount", 0.0),
            currency=data.get("currency", "USD"),
            notes=data.get("notes", ""),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )
        
        # Set paid date if exists
        if data.get("paid_date"):
            invoice.paid_date = datetime.fromisoformat(data["paid_date"])
        
        # Add items
        for item_data in data.get("items", []):
            invoice.add_item(InvoiceItem(**item_data))
        
        return invoice


class BillingService:
    """Service for managing billing operations."""
    
    def __init__(self):
        self.invoices: Dict[str, Invoice] = {}
        self.payment_methods: Dict[str, List[PaymentMethod]] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_invoice(self, tenant_id: str, items: List[InvoiceItem], 
                      billing_info: Dict[str, Any]) -> Invoice:
        """Create a new invoice."""
        try:
            invoice = Invoice(
                tenant_id=tenant_id,
                invoice_number=self._generate_invoice_number(),
                billing_name=billing_info.get("name", ""),
                billing_email=billing_info.get("email", ""),
                billing_address=billing_info.get("address", {}),
                currency=billing_info.get("currency", "USD")
            )
            
            # Add items
            for item in items:
                invoice.add_item(item)
            
            # Store invoice
            self.invoices[invoice.id] = invoice
            
            self.logger.info(f"Created invoice {invoice.invoice_number} for tenant {tenant_id}")
            return invoice
            
        except Exception as e:
            self.logger.error(f"Error creating invoice: {e}")
            raise
    
    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """Get an invoice by ID."""
        return self.invoices.get(invoice_id)
    
    def get_tenant_invoices(self, tenant_id: str, 
                          status: Optional[InvoiceStatus] = None) -> List[Invoice]:
        """Get all invoices for a tenant."""
        invoices = [inv for inv in self.invoices.values() if inv.tenant_id == tenant_id]
        
        if status:
            invoices = [inv for inv in invoices if inv.status == status]
        
        return sorted(invoices, key=lambda x: x.created_at, reverse=True)
    
    def update_invoice_status(self, invoice_id: str, status: InvoiceStatus) -> bool:
        """Update invoice status."""
        try:
            invoice = self.invoices.get(invoice_id)
            if not invoice:
                return False
            
            invoice.status = status
            invoice.updated_at = datetime.utcnow()
            
            if status == InvoiceStatus.PAID:
                invoice.mark_as_paid()
            
            self.logger.info(f"Updated invoice {invoice_id} status to {status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating invoice status: {e}")
            return False
    
    def add_payment_method(self, tenant_id: str, payment_method: PaymentMethod) -> bool:
        """Add a payment method for a tenant."""
        try:
            if tenant_id not in self.payment_methods:
                self.payment_methods[tenant_id] = []
            
            # Set as default if it's the first one
            if not self.payment_methods[tenant_id]:
                payment_method.is_default = True
            
            self.payment_methods[tenant_id].append(payment_method)
            
            self.logger.info(f"Added payment method {payment_method.id} for tenant {tenant_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding payment method: {e}")
            return False
    
    def get_payment_methods(self, tenant_id: str) -> List[PaymentMethod]:
        """Get payment methods for a tenant."""
        return self.payment_methods.get(tenant_id, [])
    
    def get_default_payment_method(self, tenant_id: str) -> Optional[PaymentMethod]:
        """Get the default payment method for a tenant."""
        methods = self.get_payment_methods(tenant_id)
        for method in methods:
            if method.is_default:
                return method
        return methods[0] if methods else None
    
    def set_default_payment_method(self, tenant_id: str, method_id: str) -> bool:
        """Set a payment method as default."""
        try:
            methods = self.get_payment_methods(tenant_id)
            for method in methods:
                method.is_default = (method.id == method_id)
                method.updated_at = datetime.utcnow()
            
            self.logger.info(f"Set payment method {method_id} as default for tenant {tenant_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting default payment method: {e}")
            return False
    
    def process_payment(self, invoice_id: str, payment_method_id: str, 
                       amount: Optional[float] = None) -> bool:
        """Process a payment for an invoice."""
        try:
            invoice = self.get_invoice(invoice_id)
            if not invoice:
                return False
            
            # Find payment method
            payment_method = None
            for method in self.get_payment_methods(invoice.tenant_id):
                if method.id == payment_method_id:
                    payment_method = method
                    break
            
            if not payment_method:
                return False
            
            # Process payment (simplified - in real implementation, integrate with payment processor)
            payment_amount = amount or invoice.total_amount
            
            # Mark invoice as paid
            invoice.mark_as_paid()
            
            self.logger.info(f"Processed payment of {payment_amount} for invoice {invoice_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing payment: {e}")
            return False
    
    def generate_invoice_pdf(self, invoice_id: str) -> Optional[bytes]:
        """Generate PDF for an invoice."""
        try:
            invoice = self.get_invoice(invoice_id)
            if not invoice:
                return None
            
            # In a real implementation, generate PDF using a library like reportlab
            # For now, return None to indicate PDF generation is not implemented
            self.logger.info(f"PDF generation requested for invoice {invoice_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error generating invoice PDF: {e}")
            return None
    
    def send_invoice_email(self, invoice_id: str, email: str) -> bool:
        """Send invoice via email."""
        try:
            invoice = self.get_invoice(invoice_id)
            if not invoice:
                return False
            
            # In a real implementation, send email using a service like SendGrid
            # For now, just log the request
            self.logger.info(f"Email invoice {invoice_id} to {email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending invoice email: {e}")
            return False
    
    def _generate_invoice_number(self) -> str:
        """Generate a unique invoice number."""
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"INV-{timestamp}-{random_suffix}"


# Global billing service instance
billing_service = BillingService()
