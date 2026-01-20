"""
SYNAPSE Quality Gates - Comprehensive Quality Gate System
=========================================================

Bu modül, SYNAPSE metodolojisindeki Quality Gate'lerin tam implementasyonunu sağlar.
Her flavor için özelleştirilmiş gate'ler, threshold'lar ve enforcement kuralları içerir.

Supported Flavors:
- IoT: Hardware constraints, firmware limits, latency requirements
- Cloud: API performance, DORA metrics, cost management
- Embedded: Safety-critical, MISRA compliance, MC/DC coverage
- Infra: IaC validation, policy compliance, drift detection
- Data: Schema validation, data quality, freshness SLAs
- Mobile: App size, performance, crash-free rates
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from enum import Enum
from datetime import datetime
import json


# =============================================================================
# ENUMS
# =============================================================================

class GateCategory(Enum):
    """Quality Gate kategorileri"""
    HARDWARE = "hardware"
    FIRMWARE = "firmware"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    SECURITY = "security"
    SAFETY = "safety"
    MEMORY = "memory"
    TIMING = "timing"
    RELIABILITY = "reliability"
    RESOURCES = "resources"
    DORA = "dora"
    COST = "cost"
    COMPLIANCE = "compliance"
    SCHEMA = "schema"
    TIMELINESS = "timeliness"
    PRIVACY = "privacy"
    SIZE = "size"
    STABILITY = "stability"
    ACCESSIBILITY = "accessibility"
    VALIDATION = "validation"
    ML = "ml"


class GateSeverity(Enum):
    """Gate ciddiyet seviyeleri"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GateOperator(Enum):
    """Karşılaştırma operatörleri"""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"


class EnforcementPoint(Enum):
    """Gate uygulama noktaları"""
    PRE_COMMIT = "pre_commit"
    BUILD_PIPELINE = "build_pipeline"
    PRE_MERGE = "pre_merge"
    PRE_DEPLOY = "pre_deploy"
    HIL_TESTING = "hil_testing"
    STATIC_ANALYSIS = "static_analysis"
    FORMAL_VERIFICATION = "formal_verification"
    CANARY = "canary"
    PRODUCTION = "production"
    PLAN = "plan"
    PRE_APPLY = "pre_apply"
    SCHEDULED_DAILY = "scheduled_daily"
    SCHEDULED_WEEKLY = "scheduled_weekly"
    PIPELINE_START = "pipeline_start"
    PIPELINE_END = "pipeline_end"
    PRE_PRODUCTION = "pre_production"
    CONTINUOUS = "continuous"
    DEVICE_FARM = "device_farm"
    BETA = "beta"
    METRIC_ONLY = "metric_only"


class FlavorType(Enum):
    """SYNAPSE Flavor tipleri"""
    IOT = "iot"
    CLOUD = "cloud"
    EMBEDDED = "embedded"
    INFRA = "infra"
    DATA = "data"
    MOBILE = "mobile"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class QualityGate:
    """Quality Gate tanımı"""
    id: str
    name: str
    description: str
    category: GateCategory
    metric: str
    operator: GateOperator
    threshold: Any  # float, int, bool, or str
    severity: GateSeverity
    enforcement: List[EnforcementPoint]
    unit: Optional[str] = None
    components: Optional[List[str]] = None
    platform: Optional[str] = None
    scope: Optional[str] = None
    exceptions: Optional[List[str]] = None

    def evaluate(self, value: Any) -> bool:
        """Gate'i değerle karşılaştır"""
        if self.operator == GateOperator.EQUALS:
            return value == self.threshold
        elif self.operator == GateOperator.NOT_EQUALS:
            return value != self.threshold
        elif self.operator == GateOperator.LESS_THAN:
            return value < self.threshold
        elif self.operator == GateOperator.LESS_THAN_OR_EQUAL:
            return value <= self.threshold
        elif self.operator == GateOperator.GREATER_THAN:
            return value > self.threshold
        elif self.operator == GateOperator.GREATER_THAN_OR_EQUAL:
            return value >= self.threshold
        elif self.operator == GateOperator.CONTAINS:
            return self.threshold in value
        elif self.operator == GateOperator.NOT_CONTAINS:
            return self.threshold not in value
        return False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "metric": self.metric,
            "operator": self.operator.value,
            "threshold": self.threshold,
            "severity": self.severity.value,
            "enforcement": [e.value for e in self.enforcement],
            "unit": self.unit,
            "components": self.components,
            "platform": self.platform,
            "scope": self.scope
        }


@dataclass
class GateResult:
    """Gate değerlendirme sonucu"""
    gate_id: str
    passed: bool
    actual_value: Any
    threshold: Any
    message: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class NeuralPruningTrigger:
    """Neural Pruning tetikleyici kuralı"""
    condition: str
    action: str
    description: Optional[str] = None


@dataclass
class IDIConfig:
    """IDI konfigürasyonu"""
    formula: str
    thresholds: Dict[str, float]
    metric_name: str = "IDI"


@dataclass
class FlavorGateConfig:
    """Flavor için tam Quality Gate konfigürasyonu"""
    flavor: FlavorType
    version: str
    description: str
    gates: List[QualityGate]
    idi_config: IDIConfig
    neural_pruning_triggers: List[NeuralPruningTrigger]
    global_enforcement: Dict[str, bool] = field(default_factory=dict)


# =============================================================================
# QUALITY GATE TEMPLATES
# =============================================================================

class QualityGateTemplates:
    """Her flavor için Quality Gate template'leri"""

    @staticmethod
    def get_iot_gates() -> FlavorGateConfig:
        """SYNAPSE/IoT Quality Gates"""
        gates = [
            # Hardware Constraints
            QualityGate(
                id="power_budget",
                name="Power Budget",
                description="Maximum power consumption in watts",
                category=GateCategory.HARDWARE,
                metric="power_watts",
                operator=GateOperator.LESS_THAN,
                threshold=5.0,
                unit="W",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT, EnforcementPoint.BUILD_PIPELINE],
                components=["hardware", "firmware"]
            ),
            QualityGate(
                id="thermal_limit",
                name="Thermal Limit",
                description="Maximum operating temperature",
                category=GateCategory.HARDWARE,
                metric="temperature_celsius",
                operator=GateOperator.LESS_THAN,
                threshold=85,
                unit="°C",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.HIL_TESTING],
                components=["hardware"]
            ),
            QualityGate(
                id="memory_footprint",
                name="Firmware Memory Footprint",
                description="Maximum firmware size in flash",
                category=GateCategory.FIRMWARE,
                metric="firmware_size_kb",
                operator=GateOperator.LESS_THAN,
                threshold=512,
                unit="KB",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.BUILD_PIPELINE],
                components=["firmware"]
            ),
            QualityGate(
                id="ram_usage",
                name="RAM Usage",
                description="Maximum runtime RAM usage",
                category=GateCategory.FIRMWARE,
                metric="ram_usage_kb",
                operator=GateOperator.LESS_THAN,
                threshold=128,
                unit="KB",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.BUILD_PIPELINE],
                components=["firmware"]
            ),
            # Latency & Performance
            QualityGate(
                id="latency_threshold",
                name="End-to-End Latency",
                description="Maximum sensor-to-cloud latency",
                category=GateCategory.PERFORMANCE,
                metric="latency_ms",
                operator=GateOperator.LESS_THAN,
                threshold=100,
                unit="ms",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.BUILD_PIPELINE, EnforcementPoint.PRE_DEPLOY],
                components=["firmware", "backend"]
            ),
            QualityGate(
                id="boot_time",
                name="Device Boot Time",
                description="Time from power-on to operational",
                category=GateCategory.PERFORMANCE,
                metric="boot_time_seconds",
                operator=GateOperator.LESS_THAN,
                threshold=10,
                unit="s",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.BUILD_PIPELINE]
            ),
            # Code Quality
            QualityGate(
                id="test_coverage",
                name="Test Coverage",
                description="Minimum code coverage percentage",
                category=GateCategory.QUALITY,
                metric="coverage_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=80,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE],
                components=["firmware", "backend", "frontend"]
            ),
            QualityGate(
                id="static_analysis",
                name="Static Analysis",
                description="No critical static analysis findings",
                category=GateCategory.QUALITY,
                metric="critical_findings",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT, EnforcementPoint.BUILD_PIPELINE]
            ),
            # Security
            QualityGate(
                id="security_vulnerabilities",
                name="Security Vulnerabilities",
                description="No critical/high security vulnerabilities",
                category=GateCategory.SECURITY,
                metric="critical_high_vulns",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE, EnforcementPoint.PRE_DEPLOY]
            ),
            QualityGate(
                id="firmware_signing",
                name="Firmware Signing",
                description="All firmware must be cryptographically signed",
                category=GateCategory.SECURITY,
                metric="is_signed",
                operator=GateOperator.EQUALS,
                threshold=True,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_DEPLOY]
            ),
        ]

        return FlavorGateConfig(
            flavor=FlavorType.IOT,
            version="1.0",
            description="Quality gates for IoT projects with hardware, firmware, and cloud components",
            gates=gates,
            idi_config=IDIConfig(
                formula="(days * loc_changed / 1000 * dependencies / 10) / 10",
                thresholds={"healthy": 3.0, "warning": 5.0, "critical": 7.0, "quarantine": 10.0},
                metric_name="IDI"
            ),
            neural_pruning_triggers=[
                NeuralPruningTrigger("idi > 7.0", "quarantine"),
                NeuralPruningTrigger("power_budget.exceeded_by > 20%", "quarantine"),
                NeuralPruningTrigger("integration_failures >= 3", "quarantine"),
                NeuralPruningTrigger("security_vulnerability.severity == critical", "immediate_quarantine")
            ],
            global_enforcement={
                "pre_commit": True,
                "build_pipeline": True,
                "pre_merge": True,
                "pre_deploy": True
            }
        )

    @staticmethod
    def get_cloud_gates() -> FlavorGateConfig:
        """SYNAPSE/Cloud Quality Gates"""
        gates = [
            # API Performance
            QualityGate(
                id="api_response_time",
                name="API Response Time",
                description="99th percentile API response time",
                category=GateCategory.PERFORMANCE,
                metric="api_p99_ms",
                operator=GateOperator.LESS_THAN,
                threshold=200,
                unit="ms",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.CANARY, EnforcementPoint.PRODUCTION],
                components=["backend", "api_gateway"]
            ),
            QualityGate(
                id="api_error_rate",
                name="API Error Rate",
                description="Maximum 5xx error rate",
                category=GateCategory.RELIABILITY,
                metric="error_rate_percent",
                operator=GateOperator.LESS_THAN,
                threshold=0.1,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.CANARY, EnforcementPoint.PRODUCTION]
            ),
            QualityGate(
                id="api_availability",
                name="API Availability",
                description="Minimum uptime percentage",
                category=GateCategory.RELIABILITY,
                metric="availability_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=99.9,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRODUCTION]
            ),
            # Frontend Performance
            QualityGate(
                id="bundle_size",
                name="Frontend Bundle Size",
                description="Maximum gzipped bundle size",
                category=GateCategory.PERFORMANCE,
                metric="bundle_size_kb",
                operator=GateOperator.LESS_THAN,
                threshold=500,
                unit="KB",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.BUILD_PIPELINE],
                components=["frontend"]
            ),
            QualityGate(
                id="lighthouse_score",
                name="Lighthouse Performance Score",
                description="Minimum Lighthouse performance score",
                category=GateCategory.PERFORMANCE,
                metric="lighthouse_performance",
                operator=GateOperator.GREATER_THAN,
                threshold=80,
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.PRE_MERGE],
                components=["frontend"]
            ),
            # Container Resources
            QualityGate(
                id="container_memory",
                name="Container Memory Limit",
                description="Maximum container memory usage",
                category=GateCategory.RESOURCES,
                metric="memory_mb",
                operator=GateOperator.LESS_THAN,
                threshold=512,
                unit="MB",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_DEPLOY]
            ),
            QualityGate(
                id="container_cpu",
                name="Container CPU Limit",
                description="Maximum container CPU usage",
                category=GateCategory.RESOURCES,
                metric="cpu_millicores",
                operator=GateOperator.LESS_THAN,
                threshold=500,
                unit="m",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_DEPLOY]
            ),
            # Code Quality
            QualityGate(
                id="test_coverage",
                name="Test Coverage",
                description="Minimum code coverage",
                category=GateCategory.QUALITY,
                metric="coverage_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=80,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            QualityGate(
                id="code_complexity",
                name="Cyclomatic Complexity",
                description="Maximum cyclomatic complexity per function",
                category=GateCategory.QUALITY,
                metric="max_complexity",
                operator=GateOperator.LESS_THAN,
                threshold=20,
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.PRE_COMMIT]
            ),
            # DORA Metrics
            QualityGate(
                id="deployment_frequency",
                name="Deployment Frequency",
                description="Target deployments per day",
                category=GateCategory.DORA,
                metric="deploys_per_day",
                operator=GateOperator.GREATER_THAN,
                threshold=1,
                severity=GateSeverity.INFO,
                enforcement=[EnforcementPoint.METRIC_ONLY]
            ),
            QualityGate(
                id="change_failure_rate",
                name="Change Failure Rate",
                description="Percentage of deployments causing failures",
                category=GateCategory.DORA,
                metric="failure_rate_percent",
                operator=GateOperator.LESS_THAN,
                threshold=5,
                unit="%",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.METRIC_ONLY]
            ),
            QualityGate(
                id="mttr",
                name="Mean Time to Recovery",
                description="Average time to recover from failures",
                category=GateCategory.DORA,
                metric="mttr_minutes",
                operator=GateOperator.LESS_THAN,
                threshold=60,
                unit="min",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.METRIC_ONLY]
            ),
            # Cost
            QualityGate(
                id="cost_delta",
                name="Cloud Cost Delta",
                description="Maximum cost increase per deployment",
                category=GateCategory.COST,
                metric="cost_increase_percent",
                operator=GateOperator.LESS_THAN,
                threshold=10,
                unit="%",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.PRE_DEPLOY]
            ),
            # Security
            QualityGate(
                id="security_scan",
                name="Security Scan",
                description="No critical/high vulnerabilities",
                category=GateCategory.SECURITY,
                metric="critical_high_vulns",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE, EnforcementPoint.PRE_DEPLOY]
            ),
            QualityGate(
                id="owasp_compliance",
                name="OWASP Top 10 Compliance",
                description="No OWASP Top 10 violations",
                category=GateCategory.SECURITY,
                metric="owasp_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
        ]

        return FlavorGateConfig(
            flavor=FlavorType.CLOUD,
            version="1.0",
            description="Quality gates for cloud-native SaaS and microservices projects",
            gates=gates,
            idi_config=IDIConfig(
                formula="(pr_age_days * changed_files * dependent_services) / 100",
                thresholds={"healthy": 2.0, "warning": 4.0, "critical": 6.0, "quarantine": 8.0},
                metric_name="IDI"
            ),
            neural_pruning_triggers=[
                NeuralPruningTrigger("idi > 6.0", "quarantine"),
                NeuralPruningTrigger("error_rate > 1% for 5 minutes", "quarantine"),
                NeuralPruningTrigger("deployment_failures >= 2", "quarantine"),
                NeuralPruningTrigger("security_vulnerability.severity == critical", "immediate_quarantine"),
                NeuralPruningTrigger("cost_anomaly > 50%", "alert_and_review")
            ],
            global_enforcement={
                "pre_commit": True,
                "build_pipeline": True,
                "pre_merge": True,
                "canary": True,
                "production": True
            }
        )

    @staticmethod
    def get_embedded_gates() -> FlavorGateConfig:
        """SYNAPSE/Embedded Quality Gates - Safety-Critical"""
        gates = [
            # Memory Constraints
            QualityGate(
                id="stack_usage",
                name="Stack Usage",
                description="Maximum stack usage percentage",
                category=GateCategory.MEMORY,
                metric="stack_usage_percent",
                operator=GateOperator.LESS_THAN,
                threshold=80,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.BUILD_PIPELINE, EnforcementPoint.STATIC_ANALYSIS]
            ),
            QualityGate(
                id="rom_usage",
                name="ROM/Flash Usage",
                description="Maximum flash memory usage",
                category=GateCategory.MEMORY,
                metric="rom_usage_percent",
                operator=GateOperator.LESS_THAN,
                threshold=90,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.BUILD_PIPELINE]
            ),
            QualityGate(
                id="ram_usage",
                name="RAM Usage",
                description="Maximum RAM usage",
                category=GateCategory.MEMORY,
                metric="ram_usage_percent",
                operator=GateOperator.LESS_THAN,
                threshold=85,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.BUILD_PIPELINE]
            ),
            QualityGate(
                id="heap_fragmentation",
                name="Heap Fragmentation",
                description="Maximum heap fragmentation",
                category=GateCategory.MEMORY,
                metric="fragmentation_percent",
                operator=GateOperator.LESS_THAN,
                threshold=10,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.STATIC_ANALYSIS]
            ),
            # Timing Constraints
            QualityGate(
                id="wcet",
                name="Worst Case Execution Time",
                description="WCET must be less than deadline",
                category=GateCategory.TIMING,
                metric="wcet_margin_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=20,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.STATIC_ANALYSIS, EnforcementPoint.FORMAL_VERIFICATION]
            ),
            QualityGate(
                id="interrupt_latency",
                name="Interrupt Latency",
                description="Maximum interrupt response time",
                category=GateCategory.TIMING,
                metric="interrupt_latency_us",
                operator=GateOperator.LESS_THAN,
                threshold=10,
                unit="μs",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.BUILD_PIPELINE]
            ),
            # Code Quality & Safety
            QualityGate(
                id="misra_compliance",
                name="MISRA C Compliance",
                description="No MISRA rule violations",
                category=GateCategory.SAFETY,
                metric="misra_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT, EnforcementPoint.BUILD_PIPELINE]
            ),
            QualityGate(
                id="cyclomatic_complexity",
                name="Cyclomatic Complexity",
                description="Maximum complexity per function",
                category=GateCategory.QUALITY,
                metric="max_complexity",
                operator=GateOperator.LESS_THAN,
                threshold=15,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_COMMIT]
            ),
            QualityGate(
                id="mcdc_coverage",
                name="MC/DC Coverage",
                description="Modified Condition/Decision Coverage for critical paths",
                category=GateCategory.SAFETY,
                metric="mcdc_coverage_percent",
                operator=GateOperator.EQUALS,
                threshold=100,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE],
                scope="safety_critical_modules"
            ),
            QualityGate(
                id="statement_coverage",
                name="Statement Coverage",
                description="Minimum statement coverage",
                category=GateCategory.QUALITY,
                metric="statement_coverage_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=95,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            # Static Analysis
            QualityGate(
                id="static_analysis_critical",
                name="Static Analysis (Critical)",
                description="No critical static analysis findings",
                category=GateCategory.SAFETY,
                metric="critical_findings",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT, EnforcementPoint.BUILD_PIPELINE]
            ),
            QualityGate(
                id="undefined_behavior",
                name="Undefined Behavior",
                description="No undefined behavior detected",
                category=GateCategory.SAFETY,
                metric="undefined_behavior_count",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.STATIC_ANALYSIS]
            ),
            # Security
            QualityGate(
                id="secure_coding",
                name="Secure Coding Standards",
                description="CERT C compliance",
                category=GateCategory.SECURITY,
                metric="cert_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT]
            ),
        ]

        return FlavorGateConfig(
            flavor=FlavorType.EMBEDDED,
            version="1.0",
            description="Quality gates for safety-critical firmware and RTOS projects",
            gates=gates,
            idi_config=IDIConfig(
                formula="(days * loc_changed / 500 * modules) / 10",
                thresholds={"healthy": 2.0, "warning": 3.0, "critical": 4.0, "quarantine": 5.0},
                metric_name="IDI"
            ),
            neural_pruning_triggers=[
                NeuralPruningTrigger("any safety_critical test failure", "immediate_quarantine"),
                NeuralPruningTrigger("misra_violation.mandatory == true", "immediate_quarantine"),
                NeuralPruningTrigger("stack_overflow_detected", "immediate_quarantine"),
                NeuralPruningTrigger("wcet_deadline_miss", "immediate_quarantine"),
                NeuralPruningTrigger("idi > 4.0", "quarantine")
            ],
            global_enforcement={
                "pre_commit": True,
                "build_pipeline": True,
                "pre_merge": True,
                "static_analysis": True,
                "formal_verification": True
            }
        )

    @staticmethod
    def get_infra_gates() -> FlavorGateConfig:
        """SYNAPSE/Infra Quality Gates"""
        gates = [
            # IaC Validation
            QualityGate(
                id="terraform_validate",
                name="Terraform Validate",
                description="Terraform configuration must be valid",
                category=GateCategory.VALIDATION,
                metric="validate_errors",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT, EnforcementPoint.PLAN]
            ),
            QualityGate(
                id="terraform_fmt",
                name="Terraform Format",
                description="Code must be properly formatted",
                category=GateCategory.QUALITY,
                metric="format_errors",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.PRE_COMMIT]
            ),
            # Policy Compliance
            QualityGate(
                id="opa_policy",
                name="OPA Policy Compliance",
                description="All OPA/Sentinel policies must pass",
                category=GateCategory.COMPLIANCE,
                metric="policy_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE, EnforcementPoint.PRE_APPLY]
            ),
            QualityGate(
                id="security_checkov",
                name="Checkov Security Scan",
                description="No high/critical security findings",
                category=GateCategory.SECURITY,
                metric="checkov_critical_high",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            QualityGate(
                id="tfsec_scan",
                name="tfsec Security Scan",
                description="No critical security issues",
                category=GateCategory.SECURITY,
                metric="tfsec_critical",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            # Blast Radius Control
            QualityGate(
                id="blast_radius",
                name="Blast Radius",
                description="Maximum resources affected per change",
                category=GateCategory.SAFETY,
                metric="resources_affected",
                operator=GateOperator.LESS_THAN,
                threshold=50,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_APPLY],
                exceptions=["initial_deployment", "approved_large_change"]
            ),
            QualityGate(
                id="destructive_changes",
                name="Destructive Changes",
                description="Require approval for destroy/recreate",
                category=GateCategory.SAFETY,
                metric="destructive_resources",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_APPLY],
                exceptions=["manual_approval"]
            ),
            # Cost Management
            QualityGate(
                id="cost_estimate",
                name="Cost Estimate Delta",
                description="Maximum monthly cost increase",
                category=GateCategory.COST,
                metric="cost_increase_percent",
                operator=GateOperator.LESS_THAN,
                threshold=20,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE, EnforcementPoint.PRE_APPLY]
            ),
            QualityGate(
                id="cost_anomaly",
                name="Cost Anomaly Detection",
                description="Alert on unusual cost patterns",
                category=GateCategory.COST,
                metric="cost_anomaly_score",
                operator=GateOperator.LESS_THAN,
                threshold=2.0,
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.PRODUCTION]
            ),
            # Drift Detection
            QualityGate(
                id="drift_detection",
                name="Configuration Drift",
                description="Maximum acceptable drift percentage",
                category=GateCategory.COMPLIANCE,
                metric="drift_percent",
                operator=GateOperator.LESS_THAN,
                threshold=5,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.SCHEDULED_DAILY]
            ),
            # RBAC & Access
            QualityGate(
                id="rbac_audit",
                name="RBAC Audit",
                description="No overprivileged roles",
                category=GateCategory.SECURITY,
                metric="overprivileged_roles",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.SCHEDULED_WEEKLY]
            ),
            QualityGate(
                id="secrets_scan",
                name="Secrets Scan",
                description="No hardcoded secrets",
                category=GateCategory.SECURITY,
                metric="exposed_secrets",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_COMMIT]
            ),
        ]

        return FlavorGateConfig(
            flavor=FlavorType.INFRA,
            version="1.0",
            description="Quality gates for IaC, DevOps, and platform engineering projects",
            gates=gates,
            idi_config=IDIConfig(
                formula="(hours_since_apply * changed_resources * environments) / 100",
                thresholds={"healthy": 2.0, "warning": 4.0, "critical": 6.0, "quarantine": 8.0},
                metric_name="CDI"
            ),
            neural_pruning_triggers=[
                NeuralPruningTrigger("drift > 20%", "quarantine"),
                NeuralPruningTrigger("cost_anomaly > 100%", "alert_and_review"),
                NeuralPruningTrigger("security_policy_violation", "quarantine"),
                NeuralPruningTrigger("failed_apply_production", "quarantine"),
                NeuralPruningTrigger("cdi > 6.0", "quarantine")
            ],
            global_enforcement={
                "pre_commit": True,
                "plan": True,
                "pre_merge": True,
                "pre_apply": True
            }
        )

    @staticmethod
    def get_data_gates() -> FlavorGateConfig:
        """SYNAPSE/Data Quality Gates"""
        gates = [
            # Schema Validation
            QualityGate(
                id="schema_validation",
                name="Schema Validation",
                description="Data must match defined schema",
                category=GateCategory.SCHEMA,
                metric="schema_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PIPELINE_START]
            ),
            QualityGate(
                id="schema_evolution",
                name="Schema Evolution Check",
                description="No breaking schema changes without migration",
                category=GateCategory.SCHEMA,
                metric="breaking_changes",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_PRODUCTION]
            ),
            # Data Freshness
            QualityGate(
                id="data_freshness",
                name="Data Freshness",
                description="Data must be within SLA",
                category=GateCategory.TIMELINESS,
                metric="data_age_minutes",
                operator=GateOperator.LESS_THAN,
                threshold=60,
                unit="min",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.CONTINUOUS]
            ),
            QualityGate(
                id="pipeline_sla",
                name="Pipeline SLA",
                description="Pipeline must complete within SLA",
                category=GateCategory.TIMELINESS,
                metric="pipeline_duration_minutes",
                operator=GateOperator.LESS_THAN,
                threshold=120,
                unit="min",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PIPELINE_END]
            ),
            # Data Quality
            QualityGate(
                id="null_rate",
                name="Null Rate",
                description="Maximum null percentage per column",
                category=GateCategory.QUALITY,
                metric="max_null_rate_percent",
                operator=GateOperator.LESS_THAN,
                threshold=5,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PIPELINE_END]
            ),
            QualityGate(
                id="uniqueness",
                name="Primary Key Uniqueness",
                description="PK columns must be 100% unique",
                category=GateCategory.QUALITY,
                metric="pk_uniqueness_percent",
                operator=GateOperator.EQUALS,
                threshold=100,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PIPELINE_END]
            ),
            QualityGate(
                id="completeness",
                name="Data Completeness",
                description="Minimum completeness score",
                category=GateCategory.QUALITY,
                metric="completeness_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=99,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PIPELINE_END]
            ),
            QualityGate(
                id="row_count_delta",
                name="Row Count Delta",
                description="Row count change within expected range",
                category=GateCategory.QUALITY,
                metric="row_count_change_percent",
                operator=GateOperator.LESS_THAN,
                threshold=20,
                unit="%",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.PIPELINE_END]
            ),
            QualityGate(
                id="data_type_match",
                name="Data Type Match",
                description="All columns match expected types",
                category=GateCategory.SCHEMA,
                metric="type_mismatches",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PIPELINE_START]
            ),
            # Privacy & Security
            QualityGate(
                id="pii_detection",
                name="PII Detection",
                description="No unmasked PII in production data",
                category=GateCategory.PRIVACY,
                metric="unmasked_pii_columns",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_PRODUCTION]
            ),
            QualityGate(
                id="data_encryption",
                name="Data Encryption",
                description="Sensitive data must be encrypted",
                category=GateCategory.SECURITY,
                metric="unencrypted_sensitive",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_PRODUCTION]
            ),
            # ML Specific
            QualityGate(
                id="model_accuracy",
                name="Model Accuracy",
                description="Minimum model accuracy threshold",
                category=GateCategory.ML,
                metric="accuracy_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=90,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_PRODUCTION],
                scope="ml_models"
            ),
            QualityGate(
                id="model_drift",
                name="Model Drift",
                description="Model performance drift detection",
                category=GateCategory.ML,
                metric="drift_score",
                operator=GateOperator.LESS_THAN,
                threshold=0.1,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.CONTINUOUS],
                scope="ml_models"
            ),
        ]

        return FlavorGateConfig(
            flavor=FlavorType.DATA,
            version="1.0",
            description="Quality gates for data pipelines, ETL, and ML training",
            gates=gates,
            idi_config=IDIConfig(
                formula="(days_since_schema_sync * breaking_changes * downstream_consumers) / 50",
                thresholds={"healthy": 2.0, "warning": 4.0, "critical": 6.0, "quarantine": 8.0},
                metric_name="SDI"
            ),
            neural_pruning_triggers=[
                NeuralPruningTrigger("schema_breaking_change without migration", "quarantine"),
                NeuralPruningTrigger("data_freshness_sla_breach > 2 hours", "quarantine"),
                NeuralPruningTrigger("data_quality_score < 90%", "alert_and_review"),
                NeuralPruningTrigger("pipeline_failure >= 3 consecutive", "quarantine"),
                NeuralPruningTrigger("sdi > 6.0", "quarantine"),
                NeuralPruningTrigger("pii_leak_detected", "immediate_quarantine")
            ],
            global_enforcement={
                "pipeline_start": True,
                "pipeline_end": True,
                "pre_production": True,
                "continuous": True
            }
        )

    @staticmethod
    def get_mobile_gates() -> FlavorGateConfig:
        """SYNAPSE/Mobile Quality Gates"""
        gates = [
            # App Size
            QualityGate(
                id="ios_bundle_size",
                name="iOS Bundle Size",
                description="Maximum iOS app size",
                category=GateCategory.SIZE,
                metric="ios_size_mb",
                operator=GateOperator.LESS_THAN,
                threshold=100,
                unit="MB",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.BUILD_PIPELINE],
                platform="ios"
            ),
            QualityGate(
                id="android_apk_size",
                name="Android APK Size",
                description="Maximum Android APK size",
                category=GateCategory.SIZE,
                metric="apk_size_mb",
                operator=GateOperator.LESS_THAN,
                threshold=50,
                unit="MB",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.BUILD_PIPELINE],
                platform="android"
            ),
            # Performance
            QualityGate(
                id="cold_start_time",
                name="Cold Start Time",
                description="Maximum app launch time",
                category=GateCategory.PERFORMANCE,
                metric="cold_start_seconds",
                operator=GateOperator.LESS_THAN,
                threshold=2,
                unit="s",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.DEVICE_FARM]
            ),
            QualityGate(
                id="memory_usage",
                name="Memory Usage",
                description="Maximum runtime memory",
                category=GateCategory.PERFORMANCE,
                metric="memory_mb",
                operator=GateOperator.LESS_THAN,
                threshold=200,
                unit="MB",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.DEVICE_FARM]
            ),
            QualityGate(
                id="battery_impact",
                name="Battery Impact",
                description="Maximum battery drain per hour active",
                category=GateCategory.PERFORMANCE,
                metric="battery_percent_per_hour",
                operator=GateOperator.LESS_THAN,
                threshold=5,
                unit="%",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.DEVICE_FARM]
            ),
            QualityGate(
                id="frame_rate",
                name="Frame Rate",
                description="Minimum smooth frame rate",
                category=GateCategory.PERFORMANCE,
                metric="fps_p90",
                operator=GateOperator.GREATER_THAN,
                threshold=55,
                unit="fps",
                severity=GateSeverity.MEDIUM,
                enforcement=[EnforcementPoint.DEVICE_FARM]
            ),
            # Stability
            QualityGate(
                id="crash_free_rate",
                name="Crash-Free Rate",
                description="Minimum crash-free user sessions",
                category=GateCategory.STABILITY,
                metric="crash_free_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=99.5,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRODUCTION]
            ),
            QualityGate(
                id="anr_rate",
                name="ANR Rate (Android)",
                description="Maximum Application Not Responding rate",
                category=GateCategory.STABILITY,
                metric="anr_rate_percent",
                operator=GateOperator.LESS_THAN,
                threshold=0.1,
                unit="%",
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRODUCTION],
                platform="android"
            ),
            # Code Quality
            QualityGate(
                id="test_coverage",
                name="Test Coverage",
                description="Minimum code coverage",
                category=GateCategory.QUALITY,
                metric="coverage_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=70,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            QualityGate(
                id="ui_test_coverage",
                name="UI Test Coverage",
                description="Critical user flows tested",
                category=GateCategory.QUALITY,
                metric="ui_coverage_percent",
                operator=GateOperator.GREATER_THAN,
                threshold=70,
                unit="%",
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            # Accessibility
            QualityGate(
                id="accessibility_score",
                name="Accessibility Score",
                description="Minimum accessibility compliance",
                category=GateCategory.ACCESSIBILITY,
                metric="a11y_score",
                operator=GateOperator.GREATER_THAN,
                threshold=90,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.BUILD_PIPELINE]
            ),
            QualityGate(
                id="accessibility_violations",
                name="Accessibility Violations",
                description="No critical accessibility issues",
                category=GateCategory.ACCESSIBILITY,
                metric="critical_a11y_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.HIGH,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
            # Security
            QualityGate(
                id="security_scan",
                name="Mobile Security Scan",
                description="No critical security vulnerabilities",
                category=GateCategory.SECURITY,
                metric="critical_vulns",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE, EnforcementPoint.BETA]
            ),
            QualityGate(
                id="certificate_pinning",
                name="Certificate Pinning",
                description="SSL pinning must be enabled",
                category=GateCategory.SECURITY,
                metric="ssl_pinning_enabled",
                operator=GateOperator.EQUALS,
                threshold=True,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.BUILD_PIPELINE]
            ),
            # Store Compliance
            QualityGate(
                id="store_guidelines",
                name="Store Guidelines Compliance",
                description="No store guideline violations detected",
                category=GateCategory.COMPLIANCE,
                metric="guideline_violations",
                operator=GateOperator.EQUALS,
                threshold=0,
                severity=GateSeverity.CRITICAL,
                enforcement=[EnforcementPoint.PRE_MERGE]
            ),
        ]

        return FlavorGateConfig(
            flavor=FlavorType.MOBILE,
            version="1.0",
            description="Quality gates for native and cross-platform mobile apps",
            gates=gates,
            idi_config=IDIConfig(
                formula="(days * changed_screens * platform_factor) / 100",
                thresholds={"healthy": 2.0, "warning": 4.0, "critical": 6.0, "quarantine": 8.0},
                metric_name="IDI"
            ),
            neural_pruning_triggers=[
                NeuralPruningTrigger("crash_free_rate < 99%", "quarantine"),
                NeuralPruningTrigger("app_store_rejection", "quarantine"),
                NeuralPruningTrigger("security_vulnerability.critical", "immediate_quarantine"),
                NeuralPruningTrigger("idi > 6.0", "quarantine"),
                NeuralPruningTrigger("bundle_size_increase > 20%", "alert_and_review")
            ],
            global_enforcement={
                "pre_commit": True,
                "build_pipeline": True,
                "pre_merge": True,
                "device_farm": True,
                "beta": True,
                "production": True
            }
        )


# =============================================================================
# QUALITY GATE REGISTRY
# =============================================================================

class QualityGateRegistry:
    """Quality Gate kayıt ve yönetim sistemi"""

    _configs: Dict[FlavorType, FlavorGateConfig] = {}

    @classmethod
    def get_config(cls, flavor: FlavorType) -> FlavorGateConfig:
        """Flavor için gate konfigürasyonunu al"""
        if flavor not in cls._configs:
            configs = {
                FlavorType.IOT: QualityGateTemplates.get_iot_gates,
                FlavorType.CLOUD: QualityGateTemplates.get_cloud_gates,
                FlavorType.EMBEDDED: QualityGateTemplates.get_embedded_gates,
                FlavorType.INFRA: QualityGateTemplates.get_infra_gates,
                FlavorType.DATA: QualityGateTemplates.get_data_gates,
                FlavorType.MOBILE: QualityGateTemplates.get_mobile_gates,
            }
            cls._configs[flavor] = configs[flavor]()
        return cls._configs[flavor]

    @classmethod
    def get_gates(cls, flavor: FlavorType) -> List[QualityGate]:
        """Flavor için tüm gate'leri al"""
        return cls.get_config(flavor).gates

    @classmethod
    def get_gate_by_id(cls, flavor: FlavorType, gate_id: str) -> Optional[QualityGate]:
        """ID ile gate bul"""
        for gate in cls.get_gates(flavor):
            if gate.id == gate_id:
                return gate
        return None

    @classmethod
    def get_gates_by_category(cls, flavor: FlavorType, category: GateCategory) -> List[QualityGate]:
        """Kategoriye göre gate'leri filtrele"""
        return [g for g in cls.get_gates(flavor) if g.category == category]

    @classmethod
    def get_gates_by_severity(cls, flavor: FlavorType, severity: GateSeverity) -> List[QualityGate]:
        """Ciddiyete göre gate'leri filtrele"""
        return [g for g in cls.get_gates(flavor) if g.severity == severity]

    @classmethod
    def get_gates_for_enforcement(cls, flavor: FlavorType, point: EnforcementPoint) -> List[QualityGate]:
        """Enforcement point'e göre gate'leri filtrele"""
        return [g for g in cls.get_gates(flavor) if point in g.enforcement]

    @classmethod
    def evaluate_gates(cls, flavor: FlavorType, metrics: Dict[str, Any],
                       enforcement_point: Optional[EnforcementPoint] = None) -> List[GateResult]:
        """Tüm gate'leri değerlendir"""
        gates = cls.get_gates(flavor)
        if enforcement_point:
            gates = [g for g in gates if enforcement_point in g.enforcement]

        results = []
        for gate in gates:
            if gate.metric in metrics:
                value = metrics[gate.metric]
                passed = gate.evaluate(value)
                results.append(GateResult(
                    gate_id=gate.id,
                    passed=passed,
                    actual_value=value,
                    threshold=gate.threshold,
                    message=f"{gate.name}: {'PASSED' if passed else 'FAILED'} - {value} {gate.operator.value} {gate.threshold}"
                ))

        return results

    @classmethod
    def get_summary(cls, flavor: FlavorType) -> Dict:
        """Gate özeti"""
        config = cls.get_config(flavor)
        gates = config.gates

        by_category = {}
        by_severity = {}

        for gate in gates:
            cat = gate.category.value
            sev = gate.severity.value
            by_category[cat] = by_category.get(cat, 0) + 1
            by_severity[sev] = by_severity.get(sev, 0) + 1

        return {
            "flavor": flavor.value,
            "total_gates": len(gates),
            "by_category": by_category,
            "by_severity": by_severity,
            "idi_metric": config.idi_config.metric_name,
            "neural_pruning_triggers": len(config.neural_pruning_triggers)
        }

    @classmethod
    def export_to_yaml(cls, flavor: FlavorType) -> str:
        """YAML formatında export et"""
        config = cls.get_config(flavor)

        yaml_str = f"""# synapse-gates-{flavor.value}.yaml
# Quality Gates for SYNAPSE/{flavor.value.upper()} Projects

version: "{config.version}"
flavor: {flavor.value}
description: "{config.description}"

global:
  enforcement:
"""
        for key, value in config.global_enforcement.items():
            yaml_str += f"    {key}: {str(value).lower()}\n"

        yaml_str += "\ngates:\n"

        for gate in config.gates:
            yaml_str += f"""  - id: {gate.id}
    name: "{gate.name}"
    description: "{gate.description}"
    category: {gate.category.value}
    metric: {gate.metric}
    operator: {gate.operator.value}
    threshold: {gate.threshold}
"""
            if gate.unit:
                yaml_str += f"    unit: \"{gate.unit}\"\n"
            yaml_str += f"    severity: {gate.severity.value}\n"
            yaml_str += "    enforcement:\n"
            for ep in gate.enforcement:
                yaml_str += f"      - {ep.value}\n"
            if gate.components:
                yaml_str += "    components:\n"
                for comp in gate.components:
                    yaml_str += f"      - {comp}\n"
            if gate.platform:
                yaml_str += f"    platform: {gate.platform}\n"
            yaml_str += "\n"

        yaml_str += f"""# IDI Configuration
idi:
  formula: "{config.idi_config.formula}"
  thresholds:
    healthy: {config.idi_config.thresholds['healthy']}
    warning: {config.idi_config.thresholds['warning']}
    critical: {config.idi_config.thresholds['critical']}
    quarantine: {config.idi_config.thresholds['quarantine']}

# Neural Pruning Triggers
neural_pruning:
  triggers:
"""
        for trigger in config.neural_pruning_triggers:
            yaml_str += f'    - condition: "{trigger.condition}"\n'
            yaml_str += f'      action: {trigger.action}\n'

        return yaml_str


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SYNAPSE Quality Gates System")
    print("=" * 70)

    # Her flavor için özet
    for flavor in FlavorType:
        summary = QualityGateRegistry.get_summary(flavor)
        print(f"\n--- SYNAPSE/{flavor.value.upper()} ---")
        print(f"  Total Gates: {summary['total_gates']}")
        print(f"  Metric: {summary['idi_metric']}")
        print(f"  Categories: {summary['by_category']}")
        print(f"  Severities: {summary['by_severity']}")

    # IoT örnek değerlendirme
    print("\n" + "=" * 70)
    print("Example: Evaluating IoT Gates")
    print("=" * 70)

    sample_metrics = {
        "power_watts": 4.2,
        "temperature_celsius": 72,
        "firmware_size_kb": 450,
        "ram_usage_kb": 100,
        "latency_ms": 85,
        "coverage_percent": 82,
        "critical_findings": 0,
        "critical_high_vulns": 1,  # This will FAIL
    }

    results = QualityGateRegistry.evaluate_gates(FlavorType.IOT, sample_metrics)

    for result in results:
        status = "✓" if result.passed else "✗"
        print(f"  {status} {result.message}")

    # YAML export örneği
    print("\n" + "=" * 70)
    print("YAML Export Sample (first 50 lines)")
    print("=" * 70)
    yaml_output = QualityGateRegistry.export_to_yaml(FlavorType.CLOUD)
    print("\n".join(yaml_output.split("\n")[:50]))
