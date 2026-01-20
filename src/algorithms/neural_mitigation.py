"""
SYNAPSE Neural Connection Layer - Automatic Mitigation Algorithms
=================================================================
Bu modül, SYNAPSE metodolojisinin "Nöral Bağlantı" katmanını uygular.
Proje bir biyolojik organizma olarak ele alınır ve otomatik savunma mekanizmaları devreye girer.

Algorithms:
1. IDI Brake (Integration Debt Index Freni)
2. Hardware-Software Balancing Algorithm
3. Neural Pruning (Otomatik Karantina)
4. Adaptive Throttling (Uyarlanabilir Kısıtlama)
5. Resource Rebalancing (Kaynak Yeniden Dengeleme)

Flavor Support:
- SYNAPSE/IoT, Cloud, Embedded, Infra, Data, Mobile
- Her flavor için özelleştirilmiş IDI hesaplama ve eşikler
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, TYPE_CHECKING
from enum import Enum
from datetime import datetime, timedelta
import math
import asyncio
from collections import deque

# Flavor desteği için import (circular import önlemek için lazy)
if TYPE_CHECKING:
    from synapse_flavors import SynapseFlavor, FlavorType


# =============================================================================
# ENUMS & DATA CLASSES
# =============================================================================

class SeverityLevel(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    QUARANTINE = "quarantine"


class ComponentType(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    FIRMWARE = "firmware"
    HYBRID = "hybrid"


class MitigationAction(Enum):
    NONE = "none"
    THROTTLE = "throttle"
    BRAKE = "brake"
    QUARANTINE = "quarantine"
    REBALANCE = "rebalance"
    ALERT = "alert"
    AUTO_INTEGRATE = "auto_integrate"


class FlavorType(Enum):
    """SYNAPSE Flavor tipleri - neural_mitigation modülünde kullanım için"""
    IOT = "iot"
    CLOUD = "cloud"
    EMBEDDED = "embedded"
    INFRA = "infra"
    DATA = "data"
    MOBILE = "mobile"


@dataclass
class TelemetryData:
    """Donanım ve yazılım telemetri verileri"""
    component_id: str
    timestamp: datetime
    cpu_usage: float  # 0-100
    memory_usage: float  # 0-100
    io_latency_ms: float
    network_latency_ms: float
    error_rate: float  # 0-1
    throughput: float  # requests/sec
    temperature: Optional[float] = None  # Hardware only (Celsius)
    power_consumption: Optional[float] = None  # Hardware only (Watts)


@dataclass
class ComponentState:
    """Bileşen durumu"""
    id: str
    name: str
    type: ComponentType
    idi_score: float
    days_since_integration: int
    loc_changed: int
    dependencies: int
    last_integration: datetime
    is_quarantined: bool = False
    throttle_level: float = 1.0  # 1.0 = full speed, 0.0 = stopped
    health_score: float = 100.0
    telemetry_history: deque = field(default_factory=lambda: deque(maxlen=100))
    # Flavor-specific fields
    flavor_type: FlavorType = FlavorType.IOT
    project_id: str = "default"
    # Cloud-specific
    pr_age_days: int = 0
    changed_files: int = 0
    dependent_services: int = 1
    # Embedded-specific
    modules: int = 1
    # Infra-specific (CDI)
    hours_since_apply: int = 0
    changed_resources: int = 0
    environments: int = 1
    # Data-specific (SDI)
    days_since_sync: int = 0
    breaking_changes: int = 0
    downstream_consumers: int = 1
    # Mobile-specific
    changed_screens: int = 0
    platform_factor: float = 1.0


@dataclass
class MitigationResult:
    """Mitigasyon sonucu"""
    action: MitigationAction
    component_id: str
    reason: str
    details: Dict
    timestamp: datetime = field(default_factory=datetime.now)


# =============================================================================
# THRESHOLDS & CONFIGURATION
# =============================================================================

class SynapseThresholds:
    """SYNAPSE eşik değerleri - organizmanın sinir sistemi"""

    # IDI Thresholds
    IDI_HEALTHY = 3.0
    IDI_WARNING = 5.0
    IDI_CRITICAL = 7.0
    IDI_QUARANTINE = 10.0

    # Hardware Constraints
    CPU_WARNING = 70.0
    CPU_CRITICAL = 85.0
    CPU_EMERGENCY = 95.0

    MEMORY_WARNING = 75.0
    MEMORY_CRITICAL = 90.0

    TEMPERATURE_WARNING = 70.0  # Celsius
    TEMPERATURE_CRITICAL = 85.0
    TEMPERATURE_SHUTDOWN = 95.0

    # Software Speed
    ERROR_RATE_WARNING = 0.01  # 1%
    ERROR_RATE_CRITICAL = 0.05  # 5%

    LATENCY_WARNING_MS = 100
    LATENCY_CRITICAL_MS = 500

    # Balancing
    HW_SW_IMBALANCE_THRESHOLD = 0.3  # 30% imbalance triggers rebalancing


# =============================================================================
# CORE ALGORITHMS
# =============================================================================

class IDICalculator:
    """
    Integration Debt Index (IDI) Calculator

    Formula: IDI = (Days Since Last Integration) × (LoC Changed / 1000) × (Dependencies / 10)

    Bu formül, bir bileşenin ne kadar "borçlu" olduğunu ölçer.
    Yüksek IDI = Entegrasyon riski yüksek
    """

    @staticmethod
    def calculate(days: int, loc_changed: int, dependencies: int) -> float:
        """IDI hesapla"""
        d = max(days, 0)
        l = max(loc_changed, 0) / 1000.0
        dep = max(dependencies, 1) / 10.0

        idi = d * l * dep
        return round(idi, 2)

    @staticmethod
    def get_severity(idi: float) -> SeverityLevel:
        """IDI'ye göre ciddiyet seviyesi"""
        if idi < SynapseThresholds.IDI_HEALTHY:
            return SeverityLevel.HEALTHY
        elif idi < SynapseThresholds.IDI_WARNING:
            return SeverityLevel.WARNING
        elif idi < SynapseThresholds.IDI_QUARANTINE:
            return SeverityLevel.CRITICAL
        else:
            return SeverityLevel.QUARANTINE

    @staticmethod
    def predict_idi(component: ComponentState, days_ahead: int) -> float:
        """Gelecekteki IDI tahminini hesapla"""
        # Günlük ortalama LoC değişimi tahmin et (son 7 günlük trend)
        daily_loc_rate = component.loc_changed / max(component.days_since_integration, 1)

        future_days = component.days_since_integration + days_ahead
        future_loc = component.loc_changed + (daily_loc_rate * days_ahead)

        return IDICalculator.calculate(
            future_days,
            int(future_loc),
            component.dependencies
        )


class FlavorAwareIDICalculator:
    """
    Flavor-Aware IDI Calculator

    Her SYNAPSE flavor'ı için özelleştirilmiş IDI/CDI/SDI hesaplama.

    Formüller:
    - IoT:      IDI = (Days × LoC/1000 × Dependencies/10) / 10
    - Cloud:    IDI = (PR_Age × Changed_Files × Dependent_Services) / 100
    - Embedded: IDI = (Days × LoC/500 × Modules) / 10
    - Infra:    CDI = (Hours × Changed_Resources × Environments) / 100
    - Data:     SDI = (Days × Breaking_Changes × Downstream_Consumers) / 50
    - Mobile:   IDI = (Days × Changed_Screens × Platform_Factor) / 100
    """

    # Flavor-specific thresholds
    THRESHOLDS = {
        FlavorType.IOT: {
            "healthy": 3.0, "warning": 5.0, "critical": 7.0, "quarantine": 10.0
        },
        FlavorType.CLOUD: {
            "healthy": 2.0, "warning": 4.0, "critical": 6.0, "quarantine": 8.0
        },
        FlavorType.EMBEDDED: {
            "healthy": 2.0, "warning": 3.5, "critical": 5.0, "quarantine": 7.0
        },
        FlavorType.INFRA: {
            "healthy": 5.0, "warning": 10.0, "critical": 20.0, "quarantine": 50.0
        },
        FlavorType.DATA: {
            "healthy": 3.0, "warning": 6.0, "critical": 10.0, "quarantine": 15.0
        },
        FlavorType.MOBILE: {
            "healthy": 3.0, "warning": 5.0, "critical": 8.0, "quarantine": 12.0
        }
    }

    METRIC_NAMES = {
        FlavorType.IOT: "IDI",
        FlavorType.CLOUD: "IDI",
        FlavorType.EMBEDDED: "IDI",
        FlavorType.INFRA: "CDI",
        FlavorType.DATA: "SDI",
        FlavorType.MOBILE: "IDI"
    }

    @classmethod
    def calculate_for_component(cls, component: ComponentState) -> float:
        """Bileşenin flavor'ına göre skor hesapla"""
        return cls.calculate(
            flavor=component.flavor_type,
            days=component.days_since_integration,
            loc_changed=component.loc_changed,
            dependencies=component.dependencies,
            pr_age_days=component.pr_age_days,
            changed_files=component.changed_files,
            dependent_services=component.dependent_services,
            modules=component.modules,
            hours_since_apply=component.hours_since_apply,
            changed_resources=component.changed_resources,
            environments=component.environments,
            days_since_sync=component.days_since_sync,
            breaking_changes=component.breaking_changes,
            downstream_consumers=component.downstream_consumers,
            changed_screens=component.changed_screens,
            platform_factor=component.platform_factor
        )

    @classmethod
    def calculate(cls, flavor: FlavorType, **kwargs) -> float:
        """Flavor'a göre skor hesapla"""

        if flavor == FlavorType.IOT:
            # IDI = (Days × LoC/1000 × Dependencies/10) / 10
            days = max(kwargs.get('days', 0), 0)
            loc = max(kwargs.get('loc_changed', 0), 0) / 1000.0
            deps = max(kwargs.get('dependencies', 1), 1) / 10.0
            return round((days * loc * deps) / 10.0, 2)

        elif flavor == FlavorType.CLOUD:
            # IDI = (PR_Age × Changed_Files × Dependent_Services) / 100
            pr_age = max(kwargs.get('pr_age_days', 0), 0)
            files = max(kwargs.get('changed_files', 0), 0)
            services = max(kwargs.get('dependent_services', 1), 1)
            return round((pr_age * files * services) / 100.0, 2)

        elif flavor == FlavorType.EMBEDDED:
            # IDI = (Days × LoC/500 × Modules) / 10 (daha hassas)
            days = max(kwargs.get('days', 0), 0)
            loc = max(kwargs.get('loc_changed', 0), 0) / 500.0
            modules = max(kwargs.get('modules', 1), 1)
            return round((days * loc * modules) / 10.0, 2)

        elif flavor == FlavorType.INFRA:
            # CDI = (Hours × Changed_Resources × Environments) / 100
            hours = max(kwargs.get('hours_since_apply', 0), 0)
            resources = max(kwargs.get('changed_resources', 0), 0)
            envs = max(kwargs.get('environments', 1), 1)
            return round((hours * resources * envs) / 100.0, 2)

        elif flavor == FlavorType.DATA:
            # SDI = (Days × Breaking_Changes × Downstream_Consumers) / 50
            days = max(kwargs.get('days_since_sync', 0), 0)
            changes = max(kwargs.get('breaking_changes', 0), 0)
            consumers = max(kwargs.get('downstream_consumers', 1), 1)
            return round((days * changes * consumers) / 50.0, 2)

        elif flavor == FlavorType.MOBILE:
            # IDI = (Days × Changed_Screens × Platform_Factor) / 100
            days = max(kwargs.get('days', 0), 0)
            screens = max(kwargs.get('changed_screens', 0), 0)
            pf = max(kwargs.get('platform_factor', 1.0), 1.0)
            return round((days * screens * pf) / 100.0, 2)

        # Default to IoT calculation
        return IDICalculator.calculate(
            kwargs.get('days', 0),
            kwargs.get('loc_changed', 0),
            kwargs.get('dependencies', 1)
        )

    @classmethod
    def get_thresholds(cls, flavor: FlavorType) -> Dict[str, float]:
        """Flavor için eşik değerlerini al"""
        return cls.THRESHOLDS.get(flavor, cls.THRESHOLDS[FlavorType.IOT])

    @classmethod
    def get_metric_name(cls, flavor: FlavorType) -> str:
        """Flavor için metrik adını al"""
        return cls.METRIC_NAMES.get(flavor, "IDI")

    @classmethod
    def get_severity(cls, score: float, flavor: FlavorType) -> SeverityLevel:
        """Flavor'a göre ciddiyet seviyesi"""
        thresholds = cls.get_thresholds(flavor)

        if score < thresholds["healthy"]:
            return SeverityLevel.HEALTHY
        elif score < thresholds["warning"]:
            return SeverityLevel.WARNING
        elif score < thresholds["quarantine"]:
            return SeverityLevel.CRITICAL
        else:
            return SeverityLevel.QUARANTINE

    @classmethod
    def predict(cls, component: ComponentState, days_ahead: int) -> float:
        """Gelecekteki skor tahminini hesapla"""
        # Flavor'a göre projeksiyon
        flavor = component.flavor_type

        if flavor == FlavorType.IOT:
            daily_loc_rate = component.loc_changed / max(component.days_since_integration, 1)
            future_days = component.days_since_integration + days_ahead
            future_loc = component.loc_changed + (daily_loc_rate * days_ahead)
            return cls.calculate(flavor, days=future_days, loc_changed=int(future_loc),
                               dependencies=component.dependencies)

        elif flavor == FlavorType.CLOUD:
            future_pr_age = component.pr_age_days + days_ahead
            return cls.calculate(flavor, pr_age_days=future_pr_age,
                               changed_files=component.changed_files,
                               dependent_services=component.dependent_services)

        elif flavor == FlavorType.EMBEDDED:
            future_days = component.days_since_integration + days_ahead
            daily_loc_rate = component.loc_changed / max(component.days_since_integration, 1)
            future_loc = component.loc_changed + (daily_loc_rate * days_ahead)
            return cls.calculate(flavor, days=future_days, loc_changed=int(future_loc),
                               modules=component.modules)

        elif flavor == FlavorType.INFRA:
            future_hours = component.hours_since_apply + (days_ahead * 24)
            return cls.calculate(flavor, hours_since_apply=future_hours,
                               changed_resources=component.changed_resources,
                               environments=component.environments)

        elif flavor == FlavorType.DATA:
            future_days = component.days_since_sync + days_ahead
            return cls.calculate(flavor, days_since_sync=future_days,
                               breaking_changes=component.breaking_changes,
                               downstream_consumers=component.downstream_consumers)

        elif flavor == FlavorType.MOBILE:
            future_days = component.days_since_integration + days_ahead
            return cls.calculate(flavor, days=future_days,
                               changed_screens=component.changed_screens,
                               platform_factor=component.platform_factor)

        return 0.0


class IDIBrake:
    """
    IDI Freni - Entegrasyon borcu yükseldiğinde otomatik yavaşlatma

    Biyolojik Analoji: Vücuttaki ağrı sinyali gibi, IDI yükseldiğinde
    sistem otomatik olarak yavaşlar ve dikkat çeker.

    Algoritma:
    1. IDI sürekli izlenir
    2. Eşikler aşıldığında throttle uygulanır
    3. Kritik seviyede yeni commit'ler engellenir
    4. Quarantine seviyesinde bileşen izole edilir
    """

    def __init__(self):
        self.brake_history: List[MitigationResult] = []

    def calculate_throttle_level(self, idi: float) -> float:
        """
        IDI'ye göre throttle seviyesi hesapla

        Returns: 0.0 (tam durdurma) - 1.0 (tam hız)
        """
        if idi < SynapseThresholds.IDI_HEALTHY:
            return 1.0  # Full speed

        elif idi < SynapseThresholds.IDI_WARNING:
            # Linear slowdown from 1.0 to 0.7
            ratio = (idi - SynapseThresholds.IDI_HEALTHY) / (SynapseThresholds.IDI_WARNING - SynapseThresholds.IDI_HEALTHY)
            return 1.0 - (ratio * 0.3)

        elif idi < SynapseThresholds.IDI_CRITICAL:
            # Aggressive slowdown from 0.7 to 0.3
            ratio = (idi - SynapseThresholds.IDI_WARNING) / (SynapseThresholds.IDI_CRITICAL - SynapseThresholds.IDI_WARNING)
            return 0.7 - (ratio * 0.4)

        elif idi < SynapseThresholds.IDI_QUARANTINE:
            # Near stop from 0.3 to 0.1
            ratio = (idi - SynapseThresholds.IDI_CRITICAL) / (SynapseThresholds.IDI_QUARANTINE - SynapseThresholds.IDI_CRITICAL)
            return 0.3 - (ratio * 0.2)

        else:
            return 0.0  # Full stop - quarantine

    def apply_brake(self, component: ComponentState) -> MitigationResult:
        """
        Bileşene fren uygula

        Bu fonksiyon her telemetri güncellemesinde çağrılır.
        """
        idi = component.idi_score
        severity = IDICalculator.get_severity(idi)
        throttle = self.calculate_throttle_level(idi)

        # Determine action
        if severity == SeverityLevel.QUARANTINE:
            action = MitigationAction.QUARANTINE
            reason = f"IDI ({idi}) exceeded quarantine threshold ({SynapseThresholds.IDI_QUARANTINE})"
            component.is_quarantined = True
            component.throttle_level = 0.0

        elif severity == SeverityLevel.CRITICAL:
            action = MitigationAction.BRAKE
            reason = f"IDI ({idi}) in critical zone - applying hard brake"
            component.throttle_level = throttle

        elif severity == SeverityLevel.WARNING:
            action = MitigationAction.THROTTLE
            reason = f"IDI ({idi}) in warning zone - applying soft throttle"
            component.throttle_level = throttle

        else:
            action = MitigationAction.NONE
            reason = "IDI healthy - no mitigation needed"
            component.throttle_level = 1.0

        result = MitigationResult(
            action=action,
            component_id=component.id,
            reason=reason,
            details={
                "idi_score": idi,
                "severity": severity.value,
                "throttle_level": throttle,
                "days_since_integration": component.days_since_integration,
                "loc_changed": component.loc_changed,
                "dependencies": component.dependencies,
                "prediction_7_days": IDICalculator.predict_idi(component, 7)
            }
        )

        self.brake_history.append(result)
        return result


class HardwareSoftwareBalancer:
    """
    Hardware-Software Balancing Algorithm

    Biyolojik Analoji: Vücuttaki homeostasis gibi, donanım kısıtları ile
    yazılım hızı arasında denge kurar.

    Problem:
    - Donanım yavaş ama güvenilir (tortoise)
    - Yazılım hızlı ama kaynak tüketir (hare)
    - İkisi arasında denge kurulmalı

    Algoritma:
    1. Donanım kapasitesini ölç (CPU, Memory, Temp, Power)
    2. Yazılım talebini ölç (Throughput, Latency, Error Rate)
    3. İmbalance skoru hesapla
    4. Gerekirse yazılımı yavaşlat veya donanımı uyar
    """

    def __init__(self):
        self.balance_history: List[Dict] = []
        self.moving_avg_window = 10

    def calculate_hardware_capacity(self, telemetry: TelemetryData) -> float:
        """
        Donanım kapasitesi skoru (0-100)

        Yüksek skor = Daha fazla kapasite mevcut
        """
        # CPU kapasitesi (ters orantılı)
        cpu_capacity = 100 - telemetry.cpu_usage

        # Memory kapasitesi (ters orantılı)
        memory_capacity = 100 - telemetry.memory_usage

        # Sıcaklık faktörü (eğer varsa)
        if telemetry.temperature:
            if telemetry.temperature > SynapseThresholds.TEMPERATURE_CRITICAL:
                temp_factor = 0.3
            elif telemetry.temperature > SynapseThresholds.TEMPERATURE_WARNING:
                temp_factor = 0.7
            else:
                temp_factor = 1.0
        else:
            temp_factor = 1.0

        # Ağırlıklı ortalama
        raw_capacity = (cpu_capacity * 0.4) + (memory_capacity * 0.4) + (100 * temp_factor * 0.2)

        return round(raw_capacity, 2)

    def calculate_software_demand(self, telemetry: TelemetryData, target_throughput: float = 1000) -> float:
        """
        Yazılım talep skoru (0-100)

        Yüksek skor = Daha fazla kaynak talebi
        """
        # Throughput bazlı talep
        throughput_demand = min((telemetry.throughput / target_throughput) * 100, 100)

        # Latency bazlı aciliyet (yüksek latency = daha fazla kaynak lazım)
        if telemetry.io_latency_ms > SynapseThresholds.LATENCY_CRITICAL_MS:
            latency_urgency = 100
        elif telemetry.io_latency_ms > SynapseThresholds.LATENCY_WARNING_MS:
            latency_urgency = 70
        else:
            latency_urgency = (telemetry.io_latency_ms / SynapseThresholds.LATENCY_WARNING_MS) * 50

        # Error rate bazlı stres
        error_stress = min(telemetry.error_rate * 1000, 100)  # 10% error = 100 stress

        # Ağırlıklı ortalama
        demand = (throughput_demand * 0.5) + (latency_urgency * 0.3) + (error_stress * 0.2)

        return round(demand, 2)

    def calculate_imbalance(self, hw_capacity: float, sw_demand: float) -> float:
        """
        İmbalance skoru hesapla (-1 ile +1 arası)

        Negatif = Donanım yetersiz (yazılım çok hızlı)
        Pozitif = Donanım atıl (yazılım çok yavaş)
        Sıfır = Denge
        """
        if hw_capacity + sw_demand == 0:
            return 0.0

        # Normalize edilmiş fark
        imbalance = (hw_capacity - sw_demand) / 100.0

        return round(imbalance, 3)

    def get_balancing_action(self, imbalance: float, component: ComponentState) -> MitigationResult:
        """
        İmbalance'a göre dengeleme aksiyonu belirle
        """
        threshold = SynapseThresholds.HW_SW_IMBALANCE_THRESHOLD

        if abs(imbalance) < threshold:
            # Dengede
            return MitigationResult(
                action=MitigationAction.NONE,
                component_id=component.id,
                reason="System is balanced",
                details={"imbalance": imbalance, "status": "balanced"}
            )

        elif imbalance < -threshold:
            # Donanım yetersiz - yazılımı yavaşlat
            throttle_amount = min(abs(imbalance), 0.5)  # Max 50% throttle
            new_throttle = max(component.throttle_level - throttle_amount, 0.2)

            return MitigationResult(
                action=MitigationAction.THROTTLE,
                component_id=component.id,
                reason=f"Hardware overloaded - throttling software by {throttle_amount*100:.0f}%",
                details={
                    "imbalance": imbalance,
                    "throttle_amount": throttle_amount,
                    "new_throttle_level": new_throttle,
                    "recommendation": "Consider scaling up hardware or optimizing software"
                }
            )

        else:
            # Donanım atıl - yazılımı hızlandırabilir
            boost_potential = min(imbalance, 0.3)  # Max 30% boost

            return MitigationResult(
                action=MitigationAction.ALERT,
                component_id=component.id,
                reason=f"Hardware underutilized - can boost software by {boost_potential*100:.0f}%",
                details={
                    "imbalance": imbalance,
                    "boost_potential": boost_potential,
                    "recommendation": "Consider increasing workload or scaling down hardware"
                }
            )

    def balance(self, component: ComponentState, telemetry: TelemetryData) -> MitigationResult:
        """
        Ana dengeleme fonksiyonu - her telemetri güncellemesinde çağrılır
        """
        hw_capacity = self.calculate_hardware_capacity(telemetry)
        sw_demand = self.calculate_software_demand(telemetry)
        imbalance = self.calculate_imbalance(hw_capacity, sw_demand)

        # Geçmişe kaydet
        self.balance_history.append({
            "timestamp": datetime.now(),
            "component_id": component.id,
            "hw_capacity": hw_capacity,
            "sw_demand": sw_demand,
            "imbalance": imbalance
        })

        # Son N kaydın ortalamasını al (smoothing)
        if len(self.balance_history) >= self.moving_avg_window:
            recent = self.balance_history[-self.moving_avg_window:]
            avg_imbalance = sum(r["imbalance"] for r in recent) / len(recent)
        else:
            avg_imbalance = imbalance

        return self.get_balancing_action(avg_imbalance, component)


class NeuralPruning:
    """
    Neural Pruning - Otomatik Karantina Mekanizması

    Biyolojik Analoji: Beyindeki sinaptik budama gibi, sorunlu
    bağlantıları (bileşenleri) otomatik olarak izole eder.

    Tetikleyiciler:
    1. IDI > Quarantine threshold
    2. Sürekli yüksek error rate
    3. Donanım arızası (sıcaklık, güç)
    4. Digital Twin fidelity düşüşü
    """

    def __init__(self):
        self.quarantine_list: Dict[str, Dict] = {}
        self.pruning_history: List[MitigationResult] = []

    def should_prune(self, component: ComponentState, telemetry: Optional[TelemetryData] = None) -> tuple[bool, str]:
        """
        Bileşenin budanıp budanmayacağını kontrol et

        Returns: (should_prune: bool, reason: str)
        """
        reasons = []

        # IDI kontrolü
        if component.idi_score >= SynapseThresholds.IDI_QUARANTINE:
            reasons.append(f"IDI ({component.idi_score}) >= {SynapseThresholds.IDI_QUARANTINE}")

        if telemetry:
            # Error rate kontrolü
            if telemetry.error_rate >= SynapseThresholds.ERROR_RATE_CRITICAL:
                reasons.append(f"Error rate ({telemetry.error_rate*100:.1f}%) >= {SynapseThresholds.ERROR_RATE_CRITICAL*100}%")

            # Sıcaklık kontrolü (donanım için)
            if telemetry.temperature and telemetry.temperature >= SynapseThresholds.TEMPERATURE_SHUTDOWN:
                reasons.append(f"Temperature ({telemetry.temperature}°C) >= {SynapseThresholds.TEMPERATURE_SHUTDOWN}°C")

            # Sistem kaynak tükenmesi
            if telemetry.cpu_usage >= SynapseThresholds.CPU_EMERGENCY and telemetry.memory_usage >= SynapseThresholds.MEMORY_CRITICAL:
                reasons.append("System resources critically exhausted")

        # Health score kontrolü
        if component.health_score < 20:
            reasons.append(f"Health score ({component.health_score}) critically low")

        if reasons:
            return True, "; ".join(reasons)

        return False, "Component is healthy"

    def prune(self, component: ComponentState, reason: str) -> MitigationResult:
        """
        Bileşeni budama (karantinaya al)
        """
        component.is_quarantined = True
        component.throttle_level = 0.0

        quarantine_entry = {
            "component_id": component.id,
            "component_name": component.name,
            "reason": reason,
            "quarantined_at": datetime.now(),
            "idi_at_quarantine": component.idi_score,
            "health_at_quarantine": component.health_score
        }

        self.quarantine_list[component.id] = quarantine_entry

        result = MitigationResult(
            action=MitigationAction.QUARANTINE,
            component_id=component.id,
            reason=f"NEURAL PRUNING: {reason}",
            details=quarantine_entry
        )

        self.pruning_history.append(result)
        return result

    def can_restore(self, component: ComponentState) -> tuple[bool, str]:
        """
        Bileşenin karantinadan çıkarılıp çıkarılamayacağını kontrol et
        """
        if component.id not in self.quarantine_list:
            return False, "Component not in quarantine"

        # IDI düşmeli
        if component.idi_score >= SynapseThresholds.IDI_WARNING:
            return False, f"IDI ({component.idi_score}) still too high"

        # Health score yükselmeli
        if component.health_score < 70:
            return False, f"Health score ({component.health_score}) still too low"

        # Minimum karantina süresi (1 saat)
        quarantine_entry = self.quarantine_list[component.id]
        time_in_quarantine = datetime.now() - quarantine_entry["quarantined_at"]
        if time_in_quarantine < timedelta(hours=1):
            return False, f"Minimum quarantine time not met ({time_in_quarantine})"

        return True, "Component can be restored"

    def restore(self, component: ComponentState) -> MitigationResult:
        """
        Bileşeni karantinadan çıkar
        """
        can_restore, reason = self.can_restore(component)

        if not can_restore:
            return MitigationResult(
                action=MitigationAction.NONE,
                component_id=component.id,
                reason=f"Cannot restore: {reason}",
                details={"status": "still_quarantined"}
            )

        component.is_quarantined = False
        component.throttle_level = 0.5  # Start at 50% - gradual ramp up

        del self.quarantine_list[component.id]

        return MitigationResult(
            action=MitigationAction.ALERT,
            component_id=component.id,
            reason="Component restored from quarantine - starting at 50% throttle",
            details={"new_throttle": 0.5, "status": "restored"}
        )


class AdaptiveThrottling:
    """
    Adaptive Throttling - Uyarlanabilir Kısıtlama

    Sistem yüküne göre dinamik olarak throttle seviyesini ayarlar.
    PID controller benzeri bir yaklaşım kullanır.
    """

    def __init__(self, kp: float = 0.5, ki: float = 0.1, kd: float = 0.05):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain

        self.integral = 0.0
        self.previous_error = 0.0
        self.target_utilization = 70.0  # Target CPU usage

    def calculate_throttle_adjustment(self, current_utilization: float) -> float:
        """
        PID controller ile throttle ayarlaması hesapla
        """
        error = self.target_utilization - current_utilization

        # Proportional
        p_term = self.kp * error

        # Integral (with anti-windup)
        self.integral = max(-50, min(50, self.integral + error))
        i_term = self.ki * self.integral

        # Derivative
        d_term = self.kd * (error - self.previous_error)
        self.previous_error = error

        # PID output
        adjustment = (p_term + i_term + d_term) / 100.0

        # Clamp to reasonable range
        return max(-0.3, min(0.3, adjustment))

    def adjust_throttle(self, component: ComponentState, telemetry: TelemetryData) -> float:
        """
        Bileşenin throttle seviyesini ayarla
        """
        adjustment = self.calculate_throttle_adjustment(telemetry.cpu_usage)

        new_throttle = component.throttle_level + adjustment
        new_throttle = max(0.1, min(1.0, new_throttle))  # Clamp between 0.1 and 1.0

        return round(new_throttle, 2)


# =============================================================================
# NEURAL ORCHESTRA - Ana Koordinatör
# =============================================================================

class NeuralOrchestra:
    """
    Neural Orchestra - Tüm mitigasyon algoritmalarını koordine eder

    Biyolojik Analoji: Merkezi sinir sistemi gibi, tüm alt sistemleri
    koordine eder ve kararlar alır.
    """

    def __init__(self):
        self.idi_brake = IDIBrake()
        self.balancer = HardwareSoftwareBalancer()
        self.pruner = NeuralPruning()
        self.throttler = AdaptiveThrottling()

        self.components: Dict[str, ComponentState] = {}
        self.event_handlers: List[Callable[[MitigationResult], None]] = []

    def register_component(self, component: ComponentState):
        """Bileşen kaydet"""
        self.components[component.id] = component

    def on_mitigation(self, handler: Callable[[MitigationResult], None]):
        """Mitigasyon event handler ekle"""
        self.event_handlers.append(handler)

    def _emit_event(self, result: MitigationResult):
        """Event'i tüm handler'lara gönder"""
        for handler in self.event_handlers:
            try:
                handler(result)
            except Exception as e:
                print(f"Event handler error: {e}")

    async def process_telemetry(self, component_id: str, telemetry: TelemetryData) -> List[MitigationResult]:
        """
        Ana işleme fonksiyonu - her telemetri geldiğinde çağrılır

        Bu fonksiyon WebSocket'ten gelen verileri işler ve
        gerekli mitigasyon aksiyonlarını tetikler.
        """
        results = []

        if component_id not in self.components:
            return results

        component = self.components[component_id]
        component.telemetry_history.append(telemetry)

        # 1. IDI Freni kontrolü
        idi_result = self.idi_brake.apply_brake(component)
        if idi_result.action != MitigationAction.NONE:
            results.append(idi_result)
            self._emit_event(idi_result)

        # 2. Neural Pruning kontrolü
        should_prune, prune_reason = self.pruner.should_prune(component, telemetry)
        if should_prune and not component.is_quarantined:
            prune_result = self.pruner.prune(component, prune_reason)
            results.append(prune_result)
            self._emit_event(prune_result)

        # 3. Eğer karantinada değilse, dengeleme yap
        if not component.is_quarantined:
            balance_result = self.balancer.balance(component, telemetry)
            if balance_result.action != MitigationAction.NONE:
                results.append(balance_result)
                self._emit_event(balance_result)

            # 4. Adaptive throttling
            new_throttle = self.throttler.adjust_throttle(component, telemetry)
            if abs(new_throttle - component.throttle_level) > 0.05:
                component.throttle_level = new_throttle

        # 5. Karantinadan çıkış kontrolü
        if component.is_quarantined:
            can_restore, _ = self.pruner.can_restore(component)
            if can_restore:
                restore_result = self.pruner.restore(component)
                results.append(restore_result)
                self._emit_event(restore_result)

        return results

    def get_system_health(self) -> Dict:
        """Sistem geneli sağlık durumu"""
        if not self.components:
            return {"status": "no_components", "health": 0}

        total_health = sum(c.health_score for c in self.components.values())
        avg_health = total_health / len(self.components)

        quarantined = [c.id for c in self.components.values() if c.is_quarantined]
        warning = [c.id for c in self.components.values()
                   if not c.is_quarantined and c.idi_score >= SynapseThresholds.IDI_WARNING]
        healthy = [c.id for c in self.components.values()
                   if not c.is_quarantined and c.idi_score < SynapseThresholds.IDI_WARNING]

        return {
            "status": "critical" if quarantined else ("warning" if warning else "healthy"),
            "average_health": round(avg_health, 1),
            "total_components": len(self.components),
            "healthy_count": len(healthy),
            "warning_count": len(warning),
            "quarantined_count": len(quarantined),
            "quarantined_components": quarantined
        }


# =============================================================================
# WEBSOCKET EVENT TYPES (for Frontend Integration)
# =============================================================================

class WebSocketEvents:
    """WebSocket event tipleri - Frontend ile iletişim için"""

    TELEMETRY_UPDATE = "telemetry:update"
    IDI_UPDATE = "idi:update"
    MITIGATION_TRIGGERED = "mitigation:triggered"
    COMPONENT_QUARANTINED = "component:quarantined"
    COMPONENT_RESTORED = "component:restored"
    SYSTEM_HEALTH_UPDATE = "system:health"
    BALANCE_UPDATE = "balance:update"


def create_websocket_payload(event_type: str, data: Dict) -> Dict:
    """WebSocket payload oluştur"""
    return {
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Demo
    orchestra = NeuralOrchestra()

    # Bileşen oluştur
    sensor_driver = ComponentState(
        id="comp-001",
        name="Sensor Driver",
        type=ComponentType.HARDWARE,
        idi_score=2.1,
        days_since_integration=3,
        loc_changed=1500,
        dependencies=4,
        last_integration=datetime.now() - timedelta(days=3)
    )

    ml_inference = ComponentState(
        id="comp-002",
        name="ML Inference",
        type=ComponentType.SOFTWARE,
        idi_score=6.5,
        days_since_integration=8,
        loc_changed=3200,
        dependencies=6,
        last_integration=datetime.now() - timedelta(days=8)
    )

    orchestra.register_component(sensor_driver)
    orchestra.register_component(ml_inference)

    # Event handler ekle
    def on_mitigation(result: MitigationResult):
        print(f"[MITIGATION] {result.action.value}: {result.reason}")

    orchestra.on_mitigation(on_mitigation)

    # Telemetri simüle et
    telemetry = TelemetryData(
        component_id="comp-002",
        timestamp=datetime.now(),
        cpu_usage=85.0,
        memory_usage=72.0,
        io_latency_ms=150,
        network_latency_ms=50,
        error_rate=0.02,
        throughput=800
    )

    # İşle
    import asyncio
    results = asyncio.run(orchestra.process_telemetry("comp-002", telemetry))

    print("\n=== System Health ===")
    print(orchestra.get_system_health())

    print("\n=== IDI Calculations ===")
    print(f"Sensor Driver IDI: {IDICalculator.calculate(3, 1500, 4)}")
    print(f"ML Inference IDI: {IDICalculator.calculate(8, 3200, 6)}")
