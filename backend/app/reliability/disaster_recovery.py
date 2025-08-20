"""
Disaster Recovery Management
Backup strategies, recovery procedures, and business continuity planning.
"""

import uuid
import json
import shutil
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)


class BackupType(str, Enum):
    """Types of backup strategies."""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"
    CONTINUOUS = "continuous"


class BackupStatus(str, Enum):
    """Backup status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VERIFIED = "verified"
    EXPIRED = "expired"


class RecoveryTier(str, Enum):
    """Recovery time objectives (RTO) tiers."""
    CRITICAL = "critical"  # RTO < 1 hour
    HIGH = "high"          # RTO < 4 hours
    MEDIUM = "medium"      # RTO < 24 hours
    LOW = "low"            # RTO < 72 hours


@dataclass
class BackupLocation:
    """Backup storage location configuration."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: str = "local"  # local, s3, gcs, azure
    path: str = ""
    credentials: Dict[str, Any] = field(default_factory=dict)
    retention_days: int = 30
    encryption_enabled: bool = True
    compression_enabled: bool = True
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "path": self.path,
            "credentials": self.credentials,
            "retention_days": self.retention_days,
            "encryption_enabled": self.encryption_enabled,
            "compression_enabled": self.compression_enabled,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupLocation':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            type=data.get("type", "local"),
            path=data.get("path", ""),
            credentials=data.get("credentials", {}),
            retention_days=data.get("retention_days", 30),
            encryption_enabled=data.get("encryption_enabled", True),
            compression_enabled=data.get("compression_enabled", True),
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )


@dataclass
class BackupStrategy:
    """Backup strategy configuration."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    backup_type: BackupType = BackupType.FULL
    schedule: str = "0 2 * * *"  # Cron expression
    locations: List[BackupLocation] = field(default_factory=list)
    retention_policy: Dict[str, Any] = field(default_factory=dict)
    encryption_key: Optional[str] = None
    compression_level: int = 6
    parallel_backups: int = 1
    verification_enabled: bool = True
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "backup_type": self.backup_type.value,
            "schedule": self.schedule,
            "locations": [loc.to_dict() for loc in self.locations],
            "retention_policy": self.retention_policy,
            "encryption_key": self.encryption_key,
            "compression_level": self.compression_level,
            "parallel_backups": self.parallel_backups,
            "verification_enabled": self.verification_enabled,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupStrategy':
        """Create from dictionary."""
        strategy = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            backup_type=BackupType(data.get("backup_type", "full")),
            schedule=data.get("schedule", "0 2 * * *"),
            retention_policy=data.get("retention_policy", {}),
            encryption_key=data.get("encryption_key"),
            compression_level=data.get("compression_level", 6),
            parallel_backups=data.get("parallel_backups", 1),
            verification_enabled=data.get("verification_enabled", True),
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )
        
        # Add locations
        for loc_data in data.get("locations", []):
            strategy.locations.append(BackupLocation.from_dict(loc_data))
        
        return strategy


@dataclass
class BackupJob:
    """A backup job instance."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    strategy_id: str = ""
    status: BackupStatus = BackupStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    size_bytes: int = 0
    location_paths: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    verification_result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "strategy_id": self.strategy_id,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "size_bytes": self.size_bytes,
            "location_paths": self.location_paths,
            "error_message": self.error_message,
            "verification_result": self.verification_result,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupJob':
        """Create from dictionary."""
        job = cls(
            id=data.get("id", str(uuid.uuid4())),
            strategy_id=data.get("strategy_id", ""),
            status=BackupStatus(data.get("status", "pending")),
            size_bytes=data.get("size_bytes", 0),
            location_paths=data.get("location_paths", []),
            error_message=data.get("error_message"),
            verification_result=data.get("verification_result"),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )
        
        # Set timestamps if provided
        if data.get("start_time"):
            job.start_time = datetime.fromisoformat(data["start_time"])
        if data.get("end_time"):
            job.end_time = datetime.fromisoformat(data["end_time"])
        
        return job


@dataclass
class RecoveryPlan:
    """Disaster recovery plan."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    recovery_tier: RecoveryTier = RecoveryTier.MEDIUM
    rto_hours: int = 24  # Recovery Time Objective
    rpo_hours: int = 4   # Recovery Point Objective
    backup_strategies: List[str] = field(default_factory=list)  # Strategy IDs
    recovery_steps: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    contact_info: Dict[str, str] = field(default_factory=dict)
    is_active: bool = True
    last_tested: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "recovery_tier": self.recovery_tier.value,
            "rto_hours": self.rto_hours,
            "rpo_hours": self.rpo_hours,
            "backup_strategies": self.backup_strategies,
            "recovery_steps": self.recovery_steps,
            "dependencies": self.dependencies,
            "contact_info": self.contact_info,
            "is_active": self.is_active,
            "last_tested": self.last_tested.isoformat() if self.last_tested else None,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecoveryPlan':
        """Create from dictionary."""
        plan = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            recovery_tier=RecoveryTier(data.get("recovery_tier", "medium")),
            rto_hours=data.get("rto_hours", 24),
            rpo_hours=data.get("rpo_hours", 4),
            backup_strategies=data.get("backup_strategies", []),
            recovery_steps=data.get("recovery_steps", []),
            dependencies=data.get("dependencies", []),
            contact_info=data.get("contact_info", {}),
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )
        
        if data.get("last_tested"):
            plan.last_tested = datetime.fromisoformat(data["last_tested"])
        
        return plan


class DisasterRecoveryManager:
    """Manages disaster recovery operations and backup strategies."""
    
    def __init__(self):
        self.backup_strategies: Dict[str, BackupStrategy] = {}
        self.backup_jobs: Dict[str, BackupJob] = {}
        self.recovery_plans: Dict[str, RecoveryPlan] = {}
        self.backup_locations: Dict[str, BackupLocation] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize default configurations
        self._initialize_default_configurations()
    
    def create_backup_strategy(self, name: str, backup_type: BackupType,
                              schedule: str, locations: List[BackupLocation],
                              **kwargs) -> BackupStrategy:
        """Create a new backup strategy."""
        try:
            strategy = BackupStrategy(
                name=name,
                backup_type=backup_type,
                schedule=schedule,
                locations=locations,
                **kwargs
            )
            
            self.backup_strategies[strategy.id] = strategy
            
            # Store locations
            for location in locations:
                self.backup_locations[location.id] = location
            
            self.logger.info(f"Created backup strategy: {name} ({strategy.id})")
            return strategy
            
        except Exception as e:
            self.logger.error(f"Error creating backup strategy: {e}")
            raise
    
    def get_backup_strategy(self, strategy_id: str) -> Optional[BackupStrategy]:
        """Get a backup strategy by ID."""
        return self.backup_strategies.get(strategy_id)
    
    def list_backup_strategies(self) -> List[BackupStrategy]:
        """List all backup strategies."""
        return list(self.backup_strategies.values())
    
    def update_backup_strategy(self, strategy_id: str, **kwargs) -> bool:
        """Update a backup strategy."""
        try:
            strategy = self.backup_strategies.get(strategy_id)
            if not strategy:
                return False
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(strategy, key):
                    setattr(strategy, key, value)
            
            self.logger.info(f"Updated backup strategy: {strategy_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating backup strategy: {e}")
            return False
    
    def delete_backup_strategy(self, strategy_id: str) -> bool:
        """Delete a backup strategy."""
        try:
            if strategy_id not in self.backup_strategies:
                return False
            
            del self.backup_strategies[strategy_id]
            self.logger.info(f"Deleted backup strategy: {strategy_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting backup strategy: {e}")
            return False
    
    async def execute_backup(self, strategy_id: str) -> BackupJob:
        """Execute a backup job."""
        try:
            strategy = self.backup_strategies.get(strategy_id)
            if not strategy:
                raise ValueError(f"Backup strategy {strategy_id} not found")
            
            # Create backup job
            job = BackupJob(
                strategy_id=strategy_id,
                status=BackupStatus.IN_PROGRESS,
                start_time=datetime.utcnow()
            )
            
            self.backup_jobs[job.id] = job
            
            # Execute backup (simplified implementation)
            await self._perform_backup(job, strategy)
            
            return job
            
        except Exception as e:
            self.logger.error(f"Error executing backup: {e}")
            raise
    
    async def _perform_backup(self, job: BackupJob, strategy: BackupStrategy):
        """Perform the actual backup operation."""
        try:
            # Simulate backup process
            await asyncio.sleep(2)  # Simulate backup time
            
            # Update job status
            job.status = BackupStatus.COMPLETED
            job.end_time = datetime.utcnow()
            job.size_bytes = 1024 * 1024 * 100  # Simulate 100MB backup
            
            # Add backup locations
            for location in strategy.locations:
                backup_path = f"{location.path}/backup_{job.id}.tar.gz"
                job.location_paths.append(backup_path)
            
            # Verify backup if enabled
            if strategy.verification_enabled:
                job.verification_result = await self._verify_backup(job)
                if job.verification_result.get("success"):
                    job.status = BackupStatus.VERIFIED
            
            self.logger.info(f"Backup completed: {job.id}")
            
        except Exception as e:
            job.status = BackupStatus.FAILED
            job.error_message = str(e)
            job.end_time = datetime.utcnow()
            self.logger.error(f"Backup failed: {e}")
    
    async def _verify_backup(self, job: BackupJob) -> Dict[str, Any]:
        """Verify backup integrity."""
        try:
            # Simulate verification
            await asyncio.sleep(1)
            
            return {
                "success": True,
                "checksum": "abc123",
                "verification_time": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "verification_time": datetime.utcnow().isoformat()
            }
    
    def create_recovery_plan(self, name: str, recovery_tier: RecoveryTier,
                            rto_hours: int, rpo_hours: int,
                            backup_strategies: List[str], **kwargs) -> RecoveryPlan:
        """Create a disaster recovery plan."""
        try:
            plan = RecoveryPlan(
                name=name,
                recovery_tier=recovery_tier,
                rto_hours=rto_hours,
                rpo_hours=rpo_hours,
                backup_strategies=backup_strategies,
                **kwargs
            )
            
            self.recovery_plans[plan.id] = plan
            
            self.logger.info(f"Created recovery plan: {name} ({plan.id})")
            return plan
            
        except Exception as e:
            self.logger.error(f"Error creating recovery plan: {e}")
            raise
    
    def get_recovery_plan(self, plan_id: str) -> Optional[RecoveryPlan]:
        """Get a recovery plan by ID."""
        return self.recovery_plans.get(plan_id)
    
    def list_recovery_plans(self) -> List[RecoveryPlan]:
        """List all recovery plans."""
        return list(self.recovery_plans.values())
    
    async def execute_recovery(self, plan_id: str, target_environment: str) -> Dict[str, Any]:
        """Execute disaster recovery plan."""
        try:
            plan = self.recovery_plans.get(plan_id)
            if not plan:
                raise ValueError(f"Recovery plan {plan_id} not found")
            
            # Simulate recovery process
            recovery_result = {
                "plan_id": plan_id,
                "status": "in_progress",
                "start_time": datetime.utcnow().isoformat(),
                "target_environment": target_environment,
                "steps_completed": [],
                "current_step": "initializing"
            }
            
            # Execute recovery steps
            for i, step in enumerate(plan.recovery_steps):
                recovery_result["current_step"] = step.get("name", f"step_{i}")
                await asyncio.sleep(1)  # Simulate step execution
                recovery_result["steps_completed"].append(step.get("name", f"step_{i}"))
            
            recovery_result["status"] = "completed"
            recovery_result["end_time"] = datetime.utcnow().isoformat()
            
            self.logger.info(f"Recovery completed: {plan_id}")
            return recovery_result
            
        except Exception as e:
            self.logger.error(f"Error executing recovery: {e}")
            raise
    
    def get_backup_status(self, strategy_id: Optional[str] = None) -> Dict[str, Any]:
        """Get backup status and statistics."""
        try:
            if strategy_id:
                jobs = [job for job in self.backup_jobs.values() if job.strategy_id == strategy_id]
            else:
                jobs = list(self.backup_jobs.values())
            
            total_jobs = len(jobs)
            completed_jobs = len([j for j in jobs if j.status == BackupStatus.COMPLETED])
            failed_jobs = len([j for j in jobs if j.status == BackupStatus.FAILED])
            
            total_size = sum(job.size_bytes for job in jobs if job.status == BackupStatus.COMPLETED)
            
            return {
                "total_jobs": total_jobs,
                "completed_jobs": completed_jobs,
                "failed_jobs": failed_jobs,
                "success_rate": (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
                "total_size_bytes": total_size,
                "total_size_gb": total_size / (1024 * 1024 * 1024),
                "last_backup": max([job.end_time for job in jobs if job.end_time], default=None)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting backup status: {e}")
            return {}
    
    def cleanup_expired_backups(self) -> int:
        """Clean up expired backups based on retention policies."""
        try:
            cleaned_count = 0
            
            for job in list(self.backup_jobs.values()):
                # Check if job is expired (simplified logic)
                if job.created_at < datetime.utcnow() - timedelta(days=30):
                    del self.backup_jobs[job.id]
                    cleaned_count += 1
            
            self.logger.info(f"Cleaned up {cleaned_count} expired backups")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up expired backups: {e}")
            return 0
    
    def _initialize_default_configurations(self):
        """Initialize default backup and recovery configurations."""
        
        # Default backup location
        default_location = BackupLocation(
            name="Local Backup",
            type="local",
            path="./backups",
            retention_days=30
        )
        self.backup_locations[default_location.id] = default_location
        
        # Default backup strategy
        default_strategy = BackupStrategy(
            name="Daily Full Backup",
            description="Daily full backup of all data",
            backup_type=BackupType.FULL,
            schedule="0 2 * * *",  # Daily at 2 AM
            locations=[default_location],
            retention_policy={
                "daily": 7,
                "weekly": 4,
                "monthly": 12
            }
        )
        self.backup_strategies[default_strategy.id] = default_strategy
        
        # Default recovery plan
        default_plan = RecoveryPlan(
            name="Standard Recovery Plan",
            description="Standard disaster recovery plan",
            recovery_tier=RecoveryTier.MEDIUM,
            rto_hours=24,
            rpo_hours=4,
            backup_strategies=[default_strategy.id],
            recovery_steps=[
                {"name": "Validate backup integrity", "duration_minutes": 30},
                {"name": "Restore database", "duration_minutes": 60},
                {"name": "Restore application data", "duration_minutes": 45},
                {"name": "Verify system functionality", "duration_minutes": 30}
            ],
            contact_info={
                "primary": "admin@xreason.com",
                "secondary": "support@xreason.com"
            }
        )
        self.recovery_plans[default_plan.id] = default_plan
        
        self.logger.info("Initialized default disaster recovery configurations")


# Global disaster recovery manager instance
disaster_recovery_manager = DisasterRecoveryManager()
