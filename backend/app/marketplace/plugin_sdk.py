"""
Plugin SDK for XReason Marketplace
Provides interfaces and utilities for third-party plugin development.
"""

import abc
import json
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class PluginType(str, Enum):
    """Types of plugins supported by XReason."""
    RULESET = "ruleset"
    ANALYTICS = "analytics"
    COMPLIANCE = "compliance"
    INTEGRATION = "integration"
    CUSTOM = "custom"


class PluginStatus(str, Enum):
    """Plugin status in the marketplace."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"


@dataclass
class PluginMetadata:
    """Metadata for a plugin."""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    requirements: Dict[str, str] = field(default_factory=dict)
    license: str = "MIT"
    homepage: Optional[str] = None
    repository: Optional[str] = None
    documentation: Optional[str] = None
    support_email: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PluginManifest:
    """Plugin manifest containing all plugin information."""
    metadata: PluginMetadata
    configuration_schema: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    hooks: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    ui_components: List[str] = field(default_factory=list)


class PluginInterface(abc.ABC):
    """Abstract base class for XReason plugins."""
    
    def __init__(self, manifest: PluginManifest):
        self.manifest = manifest
        self.logger = logging.getLogger(f"plugin.{manifest.metadata.name}")
    
    @abc.abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        pass
    
    @abc.abstractmethod
    def validate(self) -> bool:
        """Validate plugin configuration and dependencies."""
        pass
    
    @abc.abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the plugin's main functionality."""
        pass
    
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get plugin status and health information."""
        return {
            "name": self.manifest.metadata.name,
            "version": self.manifest.metadata.version,
            "status": "active",
            "last_execution": datetime.utcnow().isoformat()
        }


class PluginSDK:
    """SDK for developing XReason plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.logger = logging.getLogger("plugin_sdk")
    
    def register_plugin(self, plugin: PluginInterface) -> bool:
        """Register a plugin with the SDK."""
        try:
            plugin_name = plugin.manifest.metadata.name
            if plugin_name in self.plugins:
                self.logger.warning(f"Plugin {plugin_name} already registered")
                return False
            
            self.plugins[plugin_name] = plugin
            self.logger.info(f"Plugin {plugin_name} registered successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register plugin: {e}")
            return False
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin from the SDK."""
        try:
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                plugin.cleanup()
                del self.plugins[plugin_name]
                self.logger.info(f"Plugin {plugin_name} unregistered successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unregister plugin {plugin_name}: {e}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """Get a registered plugin by name."""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """List all registered plugin names."""
        return list(self.plugins.keys())
    
    def execute_plugin(self, plugin_name: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a plugin with the given context."""
        try:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                self.logger.error(f"Plugin {plugin_name} not found")
                return None
            
            return plugin.execute(context)
        except Exception as e:
            self.logger.error(f"Failed to execute plugin {plugin_name}: {e}")
            return None
    
    def validate_plugin(self, plugin_name: str) -> bool:
        """Validate a plugin's configuration and dependencies."""
        try:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                return False
            
            return plugin.validate()
        except Exception as e:
            self.logger.error(f"Failed to validate plugin {plugin_name}: {e}")
            return False
    
    def get_plugin_status(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get status information for a plugin."""
        try:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                return None
            
            return plugin.get_status()
        except Exception as e:
            self.logger.error(f"Failed to get status for plugin {plugin_name}: {e}")
            return None


class PluginValidator:
    """Validates plugin manifests and configurations."""
    
    @staticmethod
    def validate_manifest(manifest: PluginManifest) -> List[str]:
        """Validate a plugin manifest and return list of errors."""
        errors = []
        
        # Validate metadata
        if not manifest.metadata.name:
            errors.append("Plugin name is required")
        
        if not manifest.metadata.version:
            errors.append("Plugin version is required")
        
        if not manifest.metadata.description:
            errors.append("Plugin description is required")
        
        if not manifest.metadata.author:
            errors.append("Plugin author is required")
        
        # Validate version format (semantic versioning)
        if manifest.metadata.version and not PluginValidator._is_valid_version(manifest.metadata.version):
            errors.append("Invalid version format. Use semantic versioning (e.g., 1.0.0)")
        
        # Validate plugin type
        if manifest.metadata.plugin_type not in PluginType:
            errors.append(f"Invalid plugin type: {manifest.metadata.plugin_type}")
        
        return errors
    
    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """Check if version string follows semantic versioning."""
        import re
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
        return bool(re.match(pattern, version))
    
    @staticmethod
    def validate_configuration(config: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
        """Validate plugin configuration against schema."""
        errors = []
        
        # Basic schema validation
        for key, value in schema.items():
            if key not in config:
                if schema[key].get("required", False):
                    errors.append(f"Required configuration key missing: {key}")
            else:
                # Type validation
                expected_type = schema[key].get("type")
                if expected_type and not isinstance(config[key], expected_type):
                    errors.append(f"Invalid type for {key}: expected {expected_type}, got {type(config[key])}")
        
        return errors


class PluginManager:
    """Manages plugin lifecycle and marketplace operations."""
    
    def __init__(self):
        self.sdk = PluginSDK()
        self.validator = PluginValidator()
        self.logger = logging.getLogger("plugin_manager")
    
    def install_plugin(self, manifest_path: str, config: Dict[str, Any]) -> bool:
        """Install a plugin from manifest file."""
        try:
            # Load manifest
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
            
            # Create manifest object
            metadata = PluginMetadata(**manifest_data["metadata"])
            manifest = PluginManifest(
                metadata=metadata,
                configuration_schema=manifest_data.get("configuration_schema", {}),
                permissions=manifest_data.get("permissions", []),
                hooks=manifest_data.get("hooks", []),
                commands=manifest_data.get("commands", []),
                ui_components=manifest_data.get("ui_components", [])
            )
            
            # Validate manifest
            errors = self.validator.validate_manifest(manifest)
            if errors:
                self.logger.error(f"Manifest validation failed: {errors}")
                return False
            
            # Validate configuration
            config_errors = self.validator.validate_configuration(config, manifest.configuration_schema)
            if config_errors:
                self.logger.error(f"Configuration validation failed: {config_errors}")
                return False
            
            # TODO: Load plugin class and instantiate
            # For now, just register a placeholder
            self.logger.info(f"Plugin {metadata.name} installed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to install plugin: {e}")
            return False
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin."""
        return self.sdk.unregister_plugin(plugin_name)
    
    def list_installed_plugins(self) -> List[Dict[str, Any]]:
        """List all installed plugins with their status."""
        plugins = []
        for plugin_name in self.sdk.list_plugins():
            status = self.sdk.get_plugin_status(plugin_name)
            if status:
                plugins.append(status)
        return plugins
    
    def update_plugin(self, plugin_name: str, new_config: Dict[str, Any]) -> bool:
        """Update plugin configuration."""
        try:
            plugin = self.sdk.get_plugin(plugin_name)
            if not plugin:
                return False
            
            # Validate new configuration
            config_errors = self.validator.validate_configuration(
                new_config, 
                plugin.manifest.configuration_schema
            )
            if config_errors:
                self.logger.error(f"Configuration validation failed: {config_errors}")
                return False
            
            # Reinitialize plugin with new config
            return plugin.initialize(new_config)
            
        except Exception as e:
            self.logger.error(f"Failed to update plugin {plugin_name}: {e}")
            return False


# Global plugin manager instance
plugin_manager = PluginManager()
