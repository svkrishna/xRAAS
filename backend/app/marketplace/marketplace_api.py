"""
Marketplace API for XReason
Provides marketplace functionality for partners and plugins.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class MarketplaceItemType(str, Enum):
    """Types of marketplace items."""
    RULESET = "ruleset"
    PLUGIN = "plugin"
    INTEGRATION = "integration"
    TEMPLATE = "template"
    SERVICE = "service"


class MarketplaceItemStatus(str, Enum):
    """Status of marketplace items."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class PricingModel(str, Enum):
    """Pricing models for marketplace items."""
    FREE = "free"
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"
    USAGE_BASED = "usage_based"
    CUSTOM = "custom"


@dataclass
class MarketplaceItem:
    """A marketplace item (ruleset, plugin, etc.)."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    partner_id: str = ""
    name: str = ""
    description: str = ""
    item_type: MarketplaceItemType = MarketplaceItemType.RULESET
    status: MarketplaceItemStatus = MarketplaceItemStatus.DRAFT
    
    # Versioning
    version: str = "1.0.0"
    changelog: str = ""
    
    # Pricing
    pricing_model: PricingModel = PricingModel.FREE
    price: float = 0.0
    currency: str = "USD"
    pricing_details: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    compatibility: Dict[str, Any] = field(default_factory=dict)
    requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Files and assets
    download_url: Optional[str] = None
    documentation_url: Optional[str] = None
    demo_url: Optional[str] = None
    icon_url: Optional[str] = None
    
    # Statistics
    downloads: int = 0
    rating: float = 0.0
    review_count: int = 0
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "partner_id": self.partner_id,
            "name": self.name,
            "description": self.description,
            "item_type": self.item_type.value,
            "status": self.status.value,
            "version": self.version,
            "changelog": self.changelog,
            "pricing_model": self.pricing_model.value,
            "price": self.price,
            "currency": self.currency,
            "pricing_details": self.pricing_details,
            "tags": self.tags,
            "categories": self.categories,
            "compatibility": self.compatibility,
            "requirements": self.requirements,
            "download_url": self.download_url,
            "documentation_url": self.documentation_url,
            "demo_url": self.demo_url,
            "icon_url": self.icon_url,
            "downloads": self.downloads,
            "rating": self.rating,
            "review_count": self.review_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItem':
        """Create from dictionary."""
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            partner_id=data.get("partner_id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            item_type=MarketplaceItemType(data.get("item_type", "ruleset")),
            status=MarketplaceItemStatus(data.get("status", "draft")),
            version=data.get("version", "1.0.0"),
            changelog=data.get("changelog", ""),
            pricing_model=PricingModel(data.get("pricing_model", "free")),
            price=data.get("price", 0.0),
            currency=data.get("currency", "USD"),
            pricing_details=data.get("pricing_details", {}),
            tags=data.get("tags", []),
            categories=data.get("categories", []),
            compatibility=data.get("compatibility", {}),
            requirements=data.get("requirements", {}),
            download_url=data.get("download_url"),
            documentation_url=data.get("documentation_url"),
            demo_url=data.get("demo_url"),
            icon_url=data.get("icon_url"),
            downloads=data.get("downloads", 0),
            rating=data.get("rating", 0.0),
            review_count=data.get("review_count", 0),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )
        
        if data.get("published_at"):
            item.published_at = datetime.fromisoformat(data["published_at"])
        
        return item


@dataclass
class MarketplaceReview:
    """A review for a marketplace item."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str = ""
    user_id: str = ""
    user_name: str = ""
    rating: int = 0  # 1-5 stars
    title: str = ""
    comment: str = ""
    helpful_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "item_id": self.item_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "rating": self.rating,
            "title": self.title,
            "comment": self.comment,
            "helpful_count": self.helpful_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceReview':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            item_id=data.get("item_id", ""),
            user_id=data.get("user_id", ""),
            user_name=data.get("user_name", ""),
            rating=data.get("rating", 0),
            title=data.get("title", ""),
            comment=data.get("comment", ""),
            helpful_count=data.get("helpful_count", 0),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )


class MarketplaceAPI:
    """API for marketplace operations."""
    
    def __init__(self):
        self.items: Dict[str, MarketplaceItem] = {}
        self.reviews: Dict[str, List[MarketplaceReview]] = {}
        self.downloads: Dict[str, List[Dict[str, Any]]] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_item(self, partner_id: str, name: str, description: str,
                   item_type: MarketplaceItemType, **kwargs) -> MarketplaceItem:
        """Create a new marketplace item."""
        try:
            item = MarketplaceItem(
                partner_id=partner_id,
                name=name,
                description=description,
                item_type=item_type,
                **kwargs
            )
            
            self.items[item.id] = item
            
            self.logger.info(f"Created marketplace item: {item.name} ({item.id})")
            return item
            
        except Exception as e:
            self.logger.error(f"Error creating marketplace item: {e}")
            raise
    
    def get_item(self, item_id: str) -> Optional[MarketplaceItem]:
        """Get a marketplace item by ID."""
        return self.items.get(item_id)
    
    def get_items_by_partner(self, partner_id: str) -> List[MarketplaceItem]:
        """Get all items for a partner."""
        return [item for item in self.items.values() if item.partner_id == partner_id]
    
    def get_items_by_type(self, item_type: MarketplaceItemType) -> List[MarketplaceItem]:
        """Get all items of a specific type."""
        return [item for item in self.items.values() if item.item_type == item_type]
    
    def get_published_items(self, item_type: Optional[MarketplaceItemType] = None) -> List[MarketplaceItem]:
        """Get all published items."""
        items = [item for item in self.items.values() if item.status == MarketplaceItemStatus.PUBLISHED]
        
        if item_type:
            items = [item for item in items if item.item_type == item_type]
        
        return sorted(items, key=lambda x: x.downloads, reverse=True)
    
    def search_items(self, query: str, item_type: Optional[MarketplaceItemType] = None,
                    category: Optional[str] = None, tags: Optional[List[str]] = None) -> List[MarketplaceItem]:
        """Search marketplace items."""
        items = self.get_published_items(item_type)
        
        # Filter by query
        if query:
            query_lower = query.lower()
            items = [
                item for item in items
                if (query_lower in item.name.lower() or 
                    query_lower in item.description.lower() or
                    any(query_lower in tag.lower() for tag in item.tags))
            ]
        
        # Filter by category
        if category:
            items = [item for item in items if category in item.categories]
        
        # Filter by tags
        if tags:
            items = [item for item in items if any(tag in item.tags for tag in tags)]
        
        return items
    
    def update_item(self, item_id: str, **kwargs) -> bool:
        """Update a marketplace item."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            
            item.updated_at = datetime.utcnow()
            
            self.logger.info(f"Updated marketplace item: {item_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating marketplace item: {e}")
            return False
    
    def submit_for_review(self, item_id: str) -> bool:
        """Submit an item for review."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            if item.status != MarketplaceItemStatus.DRAFT:
                raise ValueError("Only draft items can be submitted for review")
            
            item.status = MarketplaceItemStatus.SUBMITTED
            item.updated_at = datetime.utcnow()
            
            self.logger.info(f"Submitted item for review: {item_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error submitting item for review: {e}")
            return False
    
    def approve_item(self, item_id: str) -> bool:
        """Approve a marketplace item."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            if item.status not in [MarketplaceItemStatus.SUBMITTED, MarketplaceItemStatus.UNDER_REVIEW]:
                raise ValueError("Item must be submitted or under review to be approved")
            
            item.status = MarketplaceItemStatus.APPROVED
            item.updated_at = datetime.utcnow()
            
            self.logger.info(f"Approved marketplace item: {item_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error approving item: {e}")
            return False
    
    def publish_item(self, item_id: str) -> bool:
        """Publish a marketplace item."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            if item.status != MarketplaceItemStatus.APPROVED:
                raise ValueError("Item must be approved to be published")
            
            item.status = MarketplaceItemStatus.PUBLISHED
            item.published_at = datetime.utcnow()
            item.updated_at = datetime.utcnow()
            
            self.logger.info(f"Published marketplace item: {item_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error publishing item: {e}")
            return False
    
    def reject_item(self, item_id: str, reason: str) -> bool:
        """Reject a marketplace item."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            if item.status not in [MarketplaceItemStatus.SUBMITTED, MarketplaceItemStatus.UNDER_REVIEW]:
                raise ValueError("Item must be submitted or under review to be rejected")
            
            item.status = MarketplaceItemStatus.REJECTED
            item.updated_at = datetime.utcnow()
            
            self.logger.info(f"Rejected marketplace item: {item_id} - {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error rejecting item: {e}")
            return False
    
    def add_review(self, item_id: str, user_id: str, user_name: str,
                  rating: int, title: str, comment: str) -> bool:
        """Add a review to a marketplace item."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
            
            review = MarketplaceReview(
                item_id=item_id,
                user_id=user_id,
                user_name=user_name,
                rating=rating,
                title=title,
                comment=comment
            )
            
            if item_id not in self.reviews:
                self.reviews[item_id] = []
            
            self.reviews[item_id].append(review)
            
            # Update item statistics
            self._update_item_statistics(item_id)
            
            self.logger.info(f"Added review to item: {item_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding review: {e}")
            return False
    
    def get_reviews(self, item_id: str) -> List[MarketplaceReview]:
        """Get reviews for a marketplace item."""
        return self.reviews.get(item_id, [])
    
    def record_download(self, item_id: str, user_id: str, tenant_id: str) -> bool:
        """Record a download of a marketplace item."""
        try:
            item = self.items.get(item_id)
            if not item:
                return False
            
            # Record download
            if item_id not in self.downloads:
                self.downloads[item_id] = []
            
            download_record = {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.downloads[item_id].append(download_record)
            
            # Update item download count
            item.downloads = len(self.downloads[item_id])
            item.updated_at = datetime.utcnow()
            
            self.logger.info(f"Recorded download for item: {item_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error recording download: {e}")
            return False
    
    def get_download_statistics(self, item_id: str) -> Dict[str, Any]:
        """Get download statistics for an item."""
        downloads = self.downloads.get(item_id, [])
        
        if not downloads:
            return {
                "total_downloads": 0,
                "unique_users": 0,
                "unique_tenants": 0,
                "downloads_by_date": {}
            }
        
        unique_users = len(set(d["user_id"] for d in downloads))
        unique_tenants = len(set(d["tenant_id"] for d in downloads))
        
        # Group by date
        downloads_by_date = {}
        for download in downloads:
            date = download["timestamp"][:10]  # YYYY-MM-DD
            downloads_by_date[date] = downloads_by_date.get(date, 0) + 1
        
        return {
            "total_downloads": len(downloads),
            "unique_users": unique_users,
            "unique_tenants": unique_tenants,
            "downloads_by_date": downloads_by_date
        }
    
    def _update_item_statistics(self, item_id: str) -> None:
        """Update item statistics based on reviews."""
        reviews = self.reviews.get(item_id, [])
        
        if not reviews:
            return
        
        item = self.items.get(item_id)
        if not item:
            return
        
        # Calculate average rating
        total_rating = sum(review.rating for review in reviews)
        item.rating = total_rating / len(reviews)
        item.review_count = len(reviews)
        item.updated_at = datetime.utcnow()
    
    def get_marketplace_statistics(self) -> Dict[str, Any]:
        """Get overall marketplace statistics."""
        total_items = len(self.items)
        published_items = len([item for item in self.items.values() 
                             if item.status == MarketplaceItemStatus.PUBLISHED])
        total_downloads = sum(item.downloads for item in self.items.values())
        total_reviews = sum(len(self.reviews.get(item.id, [])) for item in self.items.values())
        
        # Items by type
        items_by_type = {}
        for item_type in MarketplaceItemType:
            items_by_type[item_type.value] = len([item for item in self.items.values() 
                                                 if item.item_type == item_type])
        
        return {
            "total_items": total_items,
            "published_items": published_items,
            "total_downloads": total_downloads,
            "total_reviews": total_reviews,
            "items_by_type": items_by_type
        }


# Global marketplace API instance
marketplace_api = MarketplaceAPI()
