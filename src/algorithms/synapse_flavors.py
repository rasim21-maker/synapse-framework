"""
SYNAPSE Flavors - Project Type Tailoring System
================================================

Chapter 12: Tailoring SYNAPSE to Project Types

SYNAPSE metodolojisi farklı proje tiplerine uyarlanabilir.
Her "lezzet" (flavor), projenin doğasına göre özelleştirilmiş:
- IDI formülü
- Quality Gate'ler
- Digital Twin implementasyonu
- Neural Pruning tetikleyicileri

6 Farklı Flavor:
1. SYNAPSE/IoT - IoT ve gömülü sistemler (kanonik)
2. SYNAPSE/Cloud - Bulut-native ve mikroservisler
3. SYNAPSE/Embedded - Kritik gömülü sistemler (otomotiv, medikal)
4. SYNAPSE/Infra - Altyapı ve DevOps (Terraform, K8s)
5. SYNAPSE/Data - Veri platformları ve ML pipeline'ları
6. SYNAPSE/Mobile - Mobil uygulama geliştirme
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import math


# =============================================================================
# FLAVOR ENUMS
# =============================================================================

class FlavorType(Enum):
    """SYNAPSE Flavor tipleri"""
    IOT = "iot"                    # IoT ve gömülü sistemler
    CLOUD = "cloud"               # Bulut-native, mikroservisler
    EMBEDDED = "embedded"         # Kritik gömülü (otomotiv, medikal)
    INFRA = "infra"               # Altyapı, IaC, DevOps
    DATA = "data"                 # Veri platformları, ML
    MOBILE = "mobile"             # Mobil uygulamalar


class QualityGateType(Enum):
    """Quality Gate tipleri"""
    DESIGN = "design"
    DEVELOPMENT = "development"
    INTEGRATION = "integration"
    TESTING = "testing"
    RELEASE = "release"
    DEPLOYMENT = "deployment"


class DigitalTwinType(Enum):
    """Digital Twin tipleri"""
    HARDWARE_SIMULATOR = "hardware_simulator"       # Donanım simülasyonu
    SERVICE_MESH = "service_mesh"                   # Servis mesh simülasyonu
    HIL_SIMULATOR = "hil_simulator"                 # Hardware-in-the-loop
    ENVIRONMENT_CLONE = "environment_clone"         # Ortam klonu (Terraform)
    DATA_LINEAGE = "data_lineage"                   # Veri soyağacı
    DEVICE_FARM = "device_farm"                     # Cihaz çiftliği


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class QualityGate:
    """Quality Gate tanımı"""
    name: str
    type: QualityGateType
    description: str
    criteria: List[str]
    blocking: bool = True
    auto_close: bool = False


@dataclass
class NeuralPruningTrigger:
    """Neural Pruning tetikleyici kuralı"""
    name: str
    condition: str
    threshold: float
    action: str
    description: str


@dataclass
class FlavorMetrics:
    """Flavor-specific metrikler"""
    primary_metric: str           # Ana metrik adı
    primary_threshold_warning: float
    primary_threshold_critical: float
    primary_threshold_quarantine: float
    secondary_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class DigitalTwinConfig:
    """Digital Twin konfigürasyonu"""
    type: DigitalTwinType
    description: str
    fidelity_target: float        # Hedef doğruluk (0-1)
    update_frequency_seconds: int
    components: List[str]


# =============================================================================
# IDI CALCULATORS - FLAVOR SPECIFIC
# =============================================================================

class BaseIDICalculator(ABC):
    """Tüm IDI hesaplayıcılarının temel sınıfı"""

    @abstractmethod
    def calculate(self, **kwargs) -> float:
        """IDI hesapla"""
        pass

    @abstractmethod
    def get_severity(self, score: float) -> str:
        """Skor'a göre ciddiyet seviyesi"""
        pass

    @abstractmethod
    def get_metric_name(self) -> str:
        """Metrik adını döndür"""
        pass


class IoTIDICalculator(BaseIDICalculator):
    """
    SYNAPSE/IoT IDI Hesaplayıcı (Kanonik)

    Formula: IDI = (Days × LoC/1000 × Dependencies/10) / 10

    Parameters:
    - days: Son entegrasyondan bu yana geçen gün
    - loc_changed: Değişen kod satır sayısı
    - dependencies: Bağımlılık sayısı
    """

    # Thresholds
    HEALTHY = 3.0
    WARNING = 5.0
    CRITICAL = 7.0
    QUARANTINE = 10.0

    def calculate(self, days: int = 0, loc_changed: int = 0,
                  dependencies: int = 1, **kwargs) -> float:
        d = max(days, 0)
        l = max(loc_changed, 0) / 1000.0
        dep = max(dependencies, 1) / 10.0

        idi = (d * l * dep) / 10.0
        return round(idi, 2)

    def get_severity(self, score: float) -> str:
        if score < self.HEALTHY:
            return "healthy"
        elif score < self.WARNING:
            return "warning"
        elif score < self.QUARANTINE:
            return "critical"
        return "quarantine"

    def get_metric_name(self) -> str:
        return "IDI"


class CloudIDICalculator(BaseIDICalculator):
    """
    SYNAPSE/Cloud IDI Hesaplayıcı

    Formula: IDI = (PR_Age_Days × Changed_Files × Dependent_Services) / 100

    Parameters:
    - pr_age_days: PR'ın açık kaldığı gün sayısı
    - changed_files: Değişen dosya sayısı
    - dependent_services: Etkilenen bağımlı servis sayısı
    """

    HEALTHY = 2.0
    WARNING = 4.0
    CRITICAL = 6.0
    QUARANTINE = 8.0

    def calculate(self, pr_age_days: int = 0, changed_files: int = 0,
                  dependent_services: int = 1, **kwargs) -> float:
        pr_age = max(pr_age_days, 0)
        files = max(changed_files, 0)
        services = max(dependent_services, 1)

        idi = (pr_age * files * services) / 100.0
        return round(idi, 2)

    def get_severity(self, score: float) -> str:
        if score < self.HEALTHY:
            return "healthy"
        elif score < self.WARNING:
            return "warning"
        elif score < self.QUARANTINE:
            return "critical"
        return "quarantine"

    def get_metric_name(self) -> str:
        return "IDI"


class EmbeddedIDICalculator(BaseIDICalculator):
    """
    SYNAPSE/Embedded IDI Hesaplayıcı

    Formula: IDI = (Days × LoC/500 × Modules) / 10

    Daha sıkı hesaplama - kritik sistemler için.
    LoC böleni 500 (1000 yerine) - daha hassas.

    Parameters:
    - days: Son entegrasyondan bu yana geçen gün
    - loc_changed: Değişen kod satır sayısı
    - modules: Etkilenen modül sayısı
    """

    HEALTHY = 2.0       # Daha düşük eşikler
    WARNING = 3.5
    CRITICAL = 5.0
    QUARANTINE = 7.0

    def calculate(self, days: int = 0, loc_changed: int = 0,
                  modules: int = 1, **kwargs) -> float:
        d = max(days, 0)
        l = max(loc_changed, 0) / 500.0  # Daha hassas
        m = max(modules, 1)

        idi = (d * l * m) / 10.0
        return round(idi, 2)

    def get_severity(self, score: float) -> str:
        if score < self.HEALTHY:
            return "healthy"
        elif score < self.WARNING:
            return "warning"
        elif score < self.QUARANTINE:
            return "critical"
        return "quarantine"

    def get_metric_name(self) -> str:
        return "IDI"


class InfraCDICalculator(BaseIDICalculator):
    """
    SYNAPSE/Infra CDI Hesaplayıcı (Configuration Debt Index)

    Formula: CDI = (Hours_Since_Last_Apply × Changed_Resources × Environments) / 100

    Altyapı değişiklikleri için özelleştirilmiş.
    Saat bazında hesaplama (gün yerine).

    Parameters:
    - hours_since_apply: Son terraform apply'dan bu yana saat
    - changed_resources: Değişen kaynak sayısı
    - environments: Etkilenen ortam sayısı (dev, staging, prod)
    """

    HEALTHY = 5.0
    WARNING = 10.0
    CRITICAL = 20.0
    QUARANTINE = 50.0

    def calculate(self, hours_since_apply: int = 0, changed_resources: int = 0,
                  environments: int = 1, **kwargs) -> float:
        hours = max(hours_since_apply, 0)
        resources = max(changed_resources, 0)
        envs = max(environments, 1)

        cdi = (hours * resources * envs) / 100.0
        return round(cdi, 2)

    def get_severity(self, score: float) -> str:
        if score < self.HEALTHY:
            return "healthy"
        elif score < self.WARNING:
            return "warning"
        elif score < self.QUARANTINE:
            return "critical"
        return "quarantine"

    def get_metric_name(self) -> str:
        return "CDI"  # Configuration Debt Index


class DataSDICalculator(BaseIDICalculator):
    """
    SYNAPSE/Data SDI Hesaplayıcı (Schema Debt Index)

    Formula: SDI = (Days_Since_Schema_Sync × Breaking_Changes × Downstream_Consumers) / 50

    Veri platformları için şema uyumsuzluk riski.

    Parameters:
    - days_since_sync: Son şema senkronizasyonundan bu yana gün
    - breaking_changes: Breaking change sayısı
    - downstream_consumers: Etkilenen downstream consumer sayısı
    """

    HEALTHY = 3.0
    WARNING = 6.0
    CRITICAL = 10.0
    QUARANTINE = 15.0

    def calculate(self, days_since_sync: int = 0, breaking_changes: int = 0,
                  downstream_consumers: int = 1, **kwargs) -> float:
        days = max(days_since_sync, 0)
        changes = max(breaking_changes, 0)
        consumers = max(downstream_consumers, 1)

        sdi = (days * changes * consumers) / 50.0
        return round(sdi, 2)

    def get_severity(self, score: float) -> str:
        if score < self.HEALTHY:
            return "healthy"
        elif score < self.WARNING:
            return "warning"
        elif score < self.QUARANTINE:
            return "critical"
        return "quarantine"

    def get_metric_name(self) -> str:
        return "SDI"  # Schema Debt Index


class MobileIDICalculator(BaseIDICalculator):
    """
    SYNAPSE/Mobile IDI Hesaplayıcı

    Formula: IDI = (Days × Changed_Screens × Platform_Factor) / 100

    Platform faktörü:
    - iOS only: 1.0
    - Android only: 1.0
    - Cross-platform: 1.5 (daha riskli)
    - Web + Mobile: 2.0

    Parameters:
    - days: Son release'den bu yana gün
    - changed_screens: Değişen ekran/view sayısı
    - platform_factor: Platform çarpanı
    """

    HEALTHY = 3.0
    WARNING = 5.0
    CRITICAL = 8.0
    QUARANTINE = 12.0

    PLATFORM_FACTORS = {
        "ios": 1.0,
        "android": 1.0,
        "cross_platform": 1.5,
        "web_mobile": 2.0
    }

    def calculate(self, days: int = 0, changed_screens: int = 0,
                  platform_factor: float = 1.0, platform: str = None, **kwargs) -> float:
        d = max(days, 0)
        screens = max(changed_screens, 0)

        # Platform string verilmişse faktörü al
        if platform and platform in self.PLATFORM_FACTORS:
            pf = self.PLATFORM_FACTORS[platform]
        else:
            pf = max(platform_factor, 1.0)

        idi = (d * screens * pf) / 100.0
        return round(idi, 2)

    def get_severity(self, score: float) -> str:
        if score < self.HEALTHY:
            return "healthy"
        elif score < self.WARNING:
            return "warning"
        elif score < self.QUARANTINE:
            return "critical"
        return "quarantine"

    def get_metric_name(self) -> str:
        return "IDI"


# =============================================================================
# FLAVOR DEFINITIONS
# =============================================================================

class SynapseFlavor:
    """SYNAPSE Flavor tanımı"""

    def __init__(self, flavor_type: FlavorType):
        self.flavor_type = flavor_type
        self.calculator = self._get_calculator()
        self.quality_gates = self._get_quality_gates()
        self.neural_pruning_triggers = self._get_pruning_triggers()
        self.digital_twin_config = self._get_digital_twin_config()
        self.metrics = self._get_metrics()

    def _get_calculator(self) -> BaseIDICalculator:
        """Flavor'a göre IDI calculator döndür"""
        calculators = {
            FlavorType.IOT: IoTIDICalculator(),
            FlavorType.CLOUD: CloudIDICalculator(),
            FlavorType.EMBEDDED: EmbeddedIDICalculator(),
            FlavorType.INFRA: InfraCDICalculator(),
            FlavorType.DATA: DataSDICalculator(),
            FlavorType.MOBILE: MobileIDICalculator(),
        }
        return calculators.get(self.flavor_type, IoTIDICalculator())

    def _get_quality_gates(self) -> List[QualityGate]:
        """Flavor'a göre Quality Gate'leri döndür"""
        gates = {
            FlavorType.IOT: [
                QualityGate(
                    name="Hardware Spec Review",
                    type=QualityGateType.DESIGN,
                    description="Donanım spesifikasyonlarının incelenmesi",
                    criteria=[
                        "Güç tüketimi hedefleri tanımlanmış",
                        "Termal limitler belirlenmiş",
                        "I/O pinout doğrulanmış",
                        "Bellek haritası onaylanmış"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Firmware Integration Test",
                    type=QualityGateType.INTEGRATION,
                    description="Firmware entegrasyon testleri",
                    criteria=[
                        "HAL layer testleri geçti",
                        "Interrupt handling doğrulandı",
                        "DMA transferleri test edildi",
                        "Watchdog timeout testleri geçti"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Digital Twin Fidelity Check",
                    type=QualityGateType.TESTING,
                    description="Digital Twin doğruluk kontrolü",
                    criteria=[
                        "Fidelity score >= 85%",
                        "Timing accuracy < 5ms",
                        "Sensor data correlation > 95%"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Field Deployment Approval",
                    type=QualityGateType.RELEASE,
                    description="Saha deployment onayı",
                    criteria=[
                        "OTA update mechanism tested",
                        "Rollback procedure verified",
                        "Battery life validated",
                        "Connectivity stress tested"
                    ],
                    blocking=True
                )
            ],
            FlavorType.CLOUD: [
                QualityGate(
                    name="API Contract Review",
                    type=QualityGateType.DESIGN,
                    description="API kontratlarının incelenmesi",
                    criteria=[
                        "OpenAPI spec tanımlanmış",
                        "Breaking changes documented",
                        "Backward compatibility checked",
                        "Rate limiting defined"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Service Mesh Validation",
                    type=QualityGateType.INTEGRATION,
                    description="Servis mesh doğrulaması",
                    criteria=[
                        "Service discovery works",
                        "Circuit breakers configured",
                        "Retry policies defined",
                        "Timeout configurations set"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Load Testing",
                    type=QualityGateType.TESTING,
                    description="Yük testi",
                    criteria=[
                        "P99 latency < 200ms",
                        "Error rate < 0.1%",
                        "Auto-scaling tested",
                        "Resource utilization optimal"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Canary Deployment",
                    type=QualityGateType.DEPLOYMENT,
                    description="Canary deployment",
                    criteria=[
                        "5% traffic canary passed",
                        "No error rate increase",
                        "Latency within SLO",
                        "Rollback tested"
                    ],
                    blocking=True,
                    auto_close=True
                )
            ],
            FlavorType.EMBEDDED: [
                QualityGate(
                    name="Safety Requirements Review",
                    type=QualityGateType.DESIGN,
                    description="Güvenlik gereksinimleri incelemesi",
                    criteria=[
                        "ASIL level determined",
                        "Fault tree analysis complete",
                        "FMEA documented",
                        "Safety goals defined"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Static Analysis",
                    type=QualityGateType.DEVELOPMENT,
                    description="Statik kod analizi",
                    criteria=[
                        "MISRA-C compliance",
                        "Polyspace verification",
                        "Coverity zero critical",
                        "Memory leak free"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="HIL Testing",
                    type=QualityGateType.TESTING,
                    description="Hardware-in-the-loop testleri",
                    criteria=[
                        "All test vectors passed",
                        "Timing requirements met",
                        "Fault injection tested",
                        "Boundary conditions verified"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Certification Readiness",
                    type=QualityGateType.RELEASE,
                    description="Sertifikasyon hazırlığı",
                    criteria=[
                        "Traceability matrix complete",
                        "Test coverage > 100% MC/DC",
                        "Safety case documented",
                        "Independent review done"
                    ],
                    blocking=True
                )
            ],
            FlavorType.INFRA: [
                QualityGate(
                    name="Terraform Plan Review",
                    type=QualityGateType.DESIGN,
                    description="Terraform plan incelemesi",
                    criteria=[
                        "No destructive changes",
                        "Cost estimate acceptable",
                        "Security groups reviewed",
                        "Tagging standards met"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Policy Compliance",
                    type=QualityGateType.DEVELOPMENT,
                    description="Policy uyumluluk kontrolü",
                    criteria=[
                        "OPA policies passed",
                        "Sentinel checks passed",
                        "Compliance scan clean",
                        "No hardcoded secrets"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Environment Parity",
                    type=QualityGateType.INTEGRATION,
                    description="Ortam paritesi kontrolü",
                    criteria=[
                        "Dev-Prod parity verified",
                        "State file consistency",
                        "Module versions locked",
                        "Provider versions pinned"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Production Apply",
                    type=QualityGateType.DEPLOYMENT,
                    description="Production apply onayı",
                    criteria=[
                        "Change window approved",
                        "Rollback plan documented",
                        "Monitoring alerts set",
                        "On-call notified"
                    ],
                    blocking=True
                )
            ],
            FlavorType.DATA: [
                QualityGate(
                    name="Schema Design Review",
                    type=QualityGateType.DESIGN,
                    description="Şema tasarım incelemesi",
                    criteria=[
                        "Schema versioning strategy defined",
                        "Backward compatibility ensured",
                        "Data types validated",
                        "Partitioning strategy reviewed"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Data Quality Check",
                    type=QualityGateType.DEVELOPMENT,
                    description="Veri kalitesi kontrolü",
                    criteria=[
                        "Schema validation passed",
                        "Null checks implemented",
                        "Data profiling complete",
                        "Anomaly detection set up"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Pipeline Testing",
                    type=QualityGateType.TESTING,
                    description="Pipeline testleri",
                    criteria=[
                        "Unit tests passed",
                        "Integration tests passed",
                        "Data lineage tracked",
                        "SLA compliance verified"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Production Deployment",
                    type=QualityGateType.DEPLOYMENT,
                    description="Production deployment",
                    criteria=[
                        "Shadow mode testing complete",
                        "Consumer notification sent",
                        "Rollback procedure tested",
                        "Monitoring dashboards ready"
                    ],
                    blocking=True
                )
            ],
            FlavorType.MOBILE: [
                QualityGate(
                    name="UX Review",
                    type=QualityGateType.DESIGN,
                    description="Kullanıcı deneyimi incelemesi",
                    criteria=[
                        "Figma designs approved",
                        "Accessibility reviewed",
                        "Platform guidelines followed",
                        "Localization planned"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Code Quality",
                    type=QualityGateType.DEVELOPMENT,
                    description="Kod kalitesi kontrolü",
                    criteria=[
                        "Lint rules passed",
                        "Unit test coverage > 80%",
                        "No memory leaks",
                        "Battery usage optimized"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Device Testing",
                    type=QualityGateType.TESTING,
                    description="Cihaz testleri",
                    criteria=[
                        "Top 10 devices tested",
                        "Different OS versions tested",
                        "Network conditions tested",
                        "Crash rate < 0.1%"
                    ],
                    blocking=True
                ),
                QualityGate(
                    name="Store Submission",
                    type=QualityGateType.RELEASE,
                    description="Store gönderim onayı",
                    criteria=[
                        "App store guidelines met",
                        "Screenshots updated",
                        "Release notes written",
                        "Staged rollout planned"
                    ],
                    blocking=True
                )
            ]
        }
        return gates.get(self.flavor_type, gates[FlavorType.IOT])

    def _get_pruning_triggers(self) -> List[NeuralPruningTrigger]:
        """Flavor'a göre Neural Pruning tetikleyicileri"""
        triggers = {
            FlavorType.IOT: [
                NeuralPruningTrigger(
                    name="IDI Quarantine",
                    condition="idi_score >= threshold",
                    threshold=10.0,
                    action="quarantine",
                    description="IDI eşiği aşıldığında bileşeni karantinaya al"
                ),
                NeuralPruningTrigger(
                    name="Digital Twin Drift",
                    condition="fidelity_score < threshold",
                    threshold=0.7,
                    action="alert",
                    description="Digital Twin doğruluğu düştüğünde uyar"
                ),
                NeuralPruningTrigger(
                    name="Hardware Overload",
                    condition="cpu_usage > threshold AND memory_usage > threshold",
                    threshold=90.0,
                    action="throttle",
                    description="Donanım aşırı yüklendiğinde yazılımı yavaşlat"
                )
            ],
            FlavorType.CLOUD: [
                NeuralPruningTrigger(
                    name="PR Aging",
                    condition="pr_age_days > threshold",
                    threshold=7,
                    action="alert",
                    description="PR çok uzun süredir açık"
                ),
                NeuralPruningTrigger(
                    name="Service Cascade",
                    condition="dependent_services > threshold",
                    threshold=5,
                    action="review_required",
                    description="Çok fazla servis etkileniyor"
                ),
                NeuralPruningTrigger(
                    name="Error Spike",
                    condition="error_rate > threshold",
                    threshold=0.05,
                    action="rollback",
                    description="Hata oranı spike'ı tespit edildi"
                )
            ],
            FlavorType.EMBEDDED: [
                NeuralPruningTrigger(
                    name="Safety Violation",
                    condition="safety_check_failed",
                    threshold=1,
                    action="halt",
                    description="Güvenlik kontrolü başarısız - tam durdurma"
                ),
                NeuralPruningTrigger(
                    name="MISRA Violation",
                    condition="misra_violations > threshold",
                    threshold=0,
                    action="block",
                    description="MISRA-C ihlali tespit edildi"
                ),
                NeuralPruningTrigger(
                    name="Timing Violation",
                    condition="worst_case_execution_time > deadline",
                    threshold=1.0,
                    action="quarantine",
                    description="Zamanlama ihlali - bileşen karantinaya alındı"
                )
            ],
            FlavorType.INFRA: [
                NeuralPruningTrigger(
                    name="Drift Detection",
                    condition="drift_count > threshold",
                    threshold=0,
                    action="reconcile",
                    description="Konfigürasyon kayması tespit edildi"
                ),
                NeuralPruningTrigger(
                    name="Cost Spike",
                    condition="cost_increase_percent > threshold",
                    threshold=20,
                    action="alert",
                    description="Maliyet artışı tespit edildi"
                ),
                NeuralPruningTrigger(
                    name="Security Finding",
                    condition="critical_security_findings > threshold",
                    threshold=0,
                    action="block",
                    description="Kritik güvenlik bulgusu"
                )
            ],
            FlavorType.DATA: [
                NeuralPruningTrigger(
                    name="Schema Breaking Change",
                    condition="breaking_changes > threshold",
                    threshold=0,
                    action="review_required",
                    description="Breaking schema değişikliği tespit edildi"
                ),
                NeuralPruningTrigger(
                    name="Data Quality Drop",
                    condition="quality_score < threshold",
                    threshold=0.95,
                    action="alert",
                    description="Veri kalitesi düştü"
                ),
                NeuralPruningTrigger(
                    name="Pipeline SLA Breach",
                    condition="latency > sla_threshold",
                    threshold=1.0,
                    action="escalate",
                    description="Pipeline SLA ihlali"
                )
            ],
            FlavorType.MOBILE: [
                NeuralPruningTrigger(
                    name="Crash Rate Spike",
                    condition="crash_rate > threshold",
                    threshold=0.01,
                    action="rollback",
                    description="Crash oranı spike'ı - rollback gerekli"
                ),
                NeuralPruningTrigger(
                    name="ANR Rate High",
                    condition="anr_rate > threshold",
                    threshold=0.005,
                    action="alert",
                    description="ANR (Application Not Responding) oranı yüksek"
                ),
                NeuralPruningTrigger(
                    name="Battery Drain",
                    condition="battery_drain_score > threshold",
                    threshold=50,
                    action="review_required",
                    description="Aşırı pil tüketimi tespit edildi"
                )
            ]
        }
        return triggers.get(self.flavor_type, triggers[FlavorType.IOT])

    def _get_digital_twin_config(self) -> DigitalTwinConfig:
        """Flavor'a göre Digital Twin konfigürasyonu"""
        configs = {
            FlavorType.IOT: DigitalTwinConfig(
                type=DigitalTwinType.HARDWARE_SIMULATOR,
                description="Donanım simülasyonu - sensörler, aktüatörler, MCU",
                fidelity_target=0.85,
                update_frequency_seconds=100,  # 100ms
                components=["sensors", "actuators", "mcu", "communication"]
            ),
            FlavorType.CLOUD: DigitalTwinConfig(
                type=DigitalTwinType.SERVICE_MESH,
                description="Servis mesh simülasyonu - mikroservisler arası iletişim",
                fidelity_target=0.90,
                update_frequency_seconds=1000,  # 1s
                components=["api_gateway", "services", "databases", "message_queues"]
            ),
            FlavorType.EMBEDDED: DigitalTwinConfig(
                type=DigitalTwinType.HIL_SIMULATOR,
                description="Hardware-in-the-loop simülasyonu - gerçek zamanlı test",
                fidelity_target=0.95,  # Daha yüksek doğruluk gerekli
                update_frequency_seconds=10,  # 10ms - gerçek zamanlı
                components=["ecu", "can_bus", "sensors", "actuators", "plant_model"]
            ),
            FlavorType.INFRA: DigitalTwinConfig(
                type=DigitalTwinType.ENVIRONMENT_CLONE,
                description="Ortam klonu - Terraform state, K8s cluster",
                fidelity_target=0.99,  # Neredeyse birebir
                update_frequency_seconds=60000,  # 1 dakika
                components=["vpc", "compute", "storage", "networking", "iam"]
            ),
            FlavorType.DATA: DigitalTwinConfig(
                type=DigitalTwinType.DATA_LINEAGE,
                description="Veri soyağacı - şema versiyonlama, pipeline tracking",
                fidelity_target=0.95,
                update_frequency_seconds=300000,  # 5 dakika
                components=["sources", "transformations", "sinks", "schemas", "quality_rules"]
            ),
            FlavorType.MOBILE: DigitalTwinConfig(
                type=DigitalTwinType.DEVICE_FARM,
                description="Cihaz çiftliği - farklı cihaz ve OS versiyonları",
                fidelity_target=0.80,
                update_frequency_seconds=5000,  # 5s
                components=["ios_devices", "android_devices", "emulators", "network_profiles"]
            )
        }
        return configs.get(self.flavor_type, configs[FlavorType.IOT])

    def _get_metrics(self) -> FlavorMetrics:
        """Flavor'a göre metrikler"""
        calc = self.calculator
        return FlavorMetrics(
            primary_metric=calc.get_metric_name(),
            primary_threshold_warning=calc.WARNING,
            primary_threshold_critical=calc.CRITICAL,
            primary_threshold_quarantine=calc.QUARANTINE
        )

    def calculate_score(self, **kwargs) -> float:
        """Flavor'a uygun skor hesapla"""
        return self.calculator.calculate(**kwargs)

    def get_severity(self, score: float) -> str:
        """Skor'a göre ciddiyet seviyesi"""
        return self.calculator.get_severity(score)

    def to_dict(self) -> Dict:
        """Flavor'ı dictionary olarak döndür"""
        return {
            "type": self.flavor_type.value,
            "metric_name": self.calculator.get_metric_name(),
            "thresholds": {
                "healthy": self.calculator.HEALTHY,
                "warning": self.calculator.WARNING,
                "critical": self.calculator.CRITICAL,
                "quarantine": self.calculator.QUARANTINE
            },
            "quality_gates": [
                {
                    "name": g.name,
                    "type": g.type.value,
                    "description": g.description,
                    "criteria": g.criteria,
                    "blocking": g.blocking
                }
                for g in self.quality_gates
            ],
            "neural_pruning_triggers": [
                {
                    "name": t.name,
                    "condition": t.condition,
                    "threshold": t.threshold,
                    "action": t.action,
                    "description": t.description
                }
                for t in self.neural_pruning_triggers
            ],
            "digital_twin": {
                "type": self.digital_twin_config.type.value,
                "description": self.digital_twin_config.description,
                "fidelity_target": self.digital_twin_config.fidelity_target,
                "update_frequency_seconds": self.digital_twin_config.update_frequency_seconds,
                "components": self.digital_twin_config.components
            }
        }


# =============================================================================
# FLAVOR REGISTRY
# =============================================================================

class FlavorRegistry:
    """Flavor kayıt ve yönetim sistemi"""

    _flavors: Dict[FlavorType, SynapseFlavor] = {}

    @classmethod
    def get_flavor(cls, flavor_type: FlavorType) -> SynapseFlavor:
        """Flavor'ı al (lazy initialization)"""
        if flavor_type not in cls._flavors:
            cls._flavors[flavor_type] = SynapseFlavor(flavor_type)
        return cls._flavors[flavor_type]

    @classmethod
    def get_all_flavors(cls) -> List[SynapseFlavor]:
        """Tüm flavor'ları al"""
        return [cls.get_flavor(ft) for ft in FlavorType]

    @classmethod
    def get_flavor_by_name(cls, name: str) -> Optional[SynapseFlavor]:
        """İsme göre flavor al"""
        try:
            flavor_type = FlavorType(name.lower())
            return cls.get_flavor(flavor_type)
        except ValueError:
            return None

    @classmethod
    def get_flavor_summary(cls) -> Dict:
        """Tüm flavor'ların özeti"""
        return {
            "flavors": [
                {
                    "type": ft.value,
                    "name": f"SYNAPSE/{ft.value.upper()}",
                    "metric": cls.get_flavor(ft).calculator.get_metric_name(),
                    "description": cls._get_flavor_description(ft)
                }
                for ft in FlavorType
            ],
            "total_flavors": len(FlavorType)
        }

    @staticmethod
    def _get_flavor_description(flavor_type: FlavorType) -> str:
        """Flavor açıklaması"""
        descriptions = {
            FlavorType.IOT: "IoT ve gömülü sistemler için kanonik SYNAPSE implementasyonu",
            FlavorType.CLOUD: "Bulut-native ve mikroservis mimarileri için optimize edilmiş",
            FlavorType.EMBEDDED: "Kritik gömülü sistemler (otomotiv, medikal) için güvenlik odaklı",
            FlavorType.INFRA: "Infrastructure as Code ve DevOps için özelleştirilmiş (Terraform, K8s)",
            FlavorType.DATA: "Veri platformları ve ML pipeline'ları için şema yönetimi odaklı",
            FlavorType.MOBILE: "Mobil uygulama geliştirme için platform-aware"
        }
        return descriptions.get(flavor_type, "")


# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

@dataclass
class ProjectFlavorConfig:
    """Proje bazlı flavor konfigürasyonu"""
    project_id: str
    project_name: str
    flavor_type: FlavorType
    custom_thresholds: Optional[Dict[str, float]] = None
    custom_quality_gates: Optional[List[QualityGate]] = None
    created_at: datetime = field(default_factory=datetime.now)

    def get_flavor(self) -> SynapseFlavor:
        """Proje için konfigüre edilmiş flavor'ı al"""
        flavor = FlavorRegistry.get_flavor(self.flavor_type)

        # Custom thresholds varsa uygula
        if self.custom_thresholds:
            calc = flavor.calculator
            if "healthy" in self.custom_thresholds:
                calc.HEALTHY = self.custom_thresholds["healthy"]
            if "warning" in self.custom_thresholds:
                calc.WARNING = self.custom_thresholds["warning"]
            if "critical" in self.custom_thresholds:
                calc.CRITICAL = self.custom_thresholds["critical"]
            if "quarantine" in self.custom_thresholds:
                calc.QUARANTINE = self.custom_thresholds["quarantine"]

        return flavor

    def to_dict(self) -> Dict:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "flavor_type": self.flavor_type.value,
            "custom_thresholds": self.custom_thresholds,
            "created_at": self.created_at.isoformat()
        }


# =============================================================================
# EXAMPLE USAGE & DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SYNAPSE Flavors - Project Type Tailoring System")
    print("=" * 70)

    # Tüm flavor'ları listele
    print("\n--- Available Flavors ---")
    summary = FlavorRegistry.get_flavor_summary()
    for f in summary["flavors"]:
        print(f"  {f['name']}: {f['description']}")

    # Her flavor için örnek IDI hesaplaması
    print("\n--- Sample IDI Calculations ---")

    # IoT
    iot = FlavorRegistry.get_flavor(FlavorType.IOT)
    iot_score = iot.calculate_score(days=5, loc_changed=2000, dependencies=8)
    print(f"\n[SYNAPSE/IoT]")
    print(f"  Formula: IDI = (Days × LoC/1000 × Dependencies/10) / 10")
    print(f"  Input: days=5, loc_changed=2000, dependencies=8")
    print(f"  IDI Score: {iot_score} ({iot.get_severity(iot_score)})")

    # Cloud
    cloud = FlavorRegistry.get_flavor(FlavorType.CLOUD)
    cloud_score = cloud.calculate_score(pr_age_days=3, changed_files=15, dependent_services=4)
    print(f"\n[SYNAPSE/Cloud]")
    print(f"  Formula: IDI = (PR_Age_Days × Changed_Files × Dependent_Services) / 100")
    print(f"  Input: pr_age_days=3, changed_files=15, dependent_services=4")
    print(f"  IDI Score: {cloud_score} ({cloud.get_severity(cloud_score)})")

    # Embedded
    embedded = FlavorRegistry.get_flavor(FlavorType.EMBEDDED)
    emb_score = embedded.calculate_score(days=2, loc_changed=500, modules=3)
    print(f"\n[SYNAPSE/Embedded]")
    print(f"  Formula: IDI = (Days × LoC/500 × Modules) / 10")
    print(f"  Input: days=2, loc_changed=500, modules=3")
    print(f"  IDI Score: {emb_score} ({embedded.get_severity(emb_score)})")

    # Infra
    infra = FlavorRegistry.get_flavor(FlavorType.INFRA)
    cdi_score = infra.calculate_score(hours_since_apply=48, changed_resources=10, environments=3)
    print(f"\n[SYNAPSE/Infra]")
    print(f"  Formula: CDI = (Hours_Since_Apply × Changed_Resources × Environments) / 100")
    print(f"  Input: hours_since_apply=48, changed_resources=10, environments=3")
    print(f"  CDI Score: {cdi_score} ({infra.get_severity(cdi_score)})")

    # Data
    data = FlavorRegistry.get_flavor(FlavorType.DATA)
    sdi_score = data.calculate_score(days_since_sync=5, breaking_changes=2, downstream_consumers=8)
    print(f"\n[SYNAPSE/Data]")
    print(f"  Formula: SDI = (Days_Since_Sync × Breaking_Changes × Downstream_Consumers) / 50")
    print(f"  Input: days_since_sync=5, breaking_changes=2, downstream_consumers=8")
    print(f"  SDI Score: {sdi_score} ({data.get_severity(sdi_score)})")

    # Mobile
    mobile = FlavorRegistry.get_flavor(FlavorType.MOBILE)
    mobile_score = mobile.calculate_score(days=7, changed_screens=20, platform="cross_platform")
    print(f"\n[SYNAPSE/Mobile]")
    print(f"  Formula: IDI = (Days × Changed_Screens × Platform_Factor) / 100")
    print(f"  Input: days=7, changed_screens=20, platform=cross_platform (factor=1.5)")
    print(f"  IDI Score: {mobile_score} ({mobile.get_severity(mobile_score)})")

    # Quality Gates örneği
    print("\n--- Quality Gates Example (SYNAPSE/Embedded) ---")
    for gate in embedded.quality_gates:
        print(f"\n  [{gate.type.value.upper()}] {gate.name}")
        print(f"    {gate.description}")
        print(f"    Blocking: {gate.blocking}")
        for criterion in gate.criteria[:2]:  # İlk 2 kriter
            print(f"      - {criterion}")

    # Neural Pruning Triggers örneği
    print("\n--- Neural Pruning Triggers Example (SYNAPSE/Cloud) ---")
    for trigger in cloud.neural_pruning_triggers:
        print(f"\n  {trigger.name}")
        print(f"    Condition: {trigger.condition}")
        print(f"    Threshold: {trigger.threshold}")
        print(f"    Action: {trigger.action}")

    # Digital Twin Config örneği
    print("\n--- Digital Twin Configurations ---")
    for ft in FlavorType:
        flavor = FlavorRegistry.get_flavor(ft)
        dt = flavor.digital_twin_config
        print(f"\n  SYNAPSE/{ft.value.upper()}: {dt.type.value}")
        print(f"    Fidelity Target: {dt.fidelity_target*100}%")
        print(f"    Update Frequency: {dt.update_frequency_seconds}ms")

    print("\n" + "=" * 70)
