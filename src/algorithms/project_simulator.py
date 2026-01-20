"""
SYNAPSE Project Simulator
=========================

Proje simülasyonu için modül. Şunları simüle edebilir:
- Tarih bazlı simülasyonlar (deadline, due date)
- IDI bazlı simülasyonlar
- Takım genişliği değişiklikleri
- Kaynak tahsisi senaryoları
- Risk olasılıkları (Monte Carlo)

Kullanım:
    simulator = ProjectSimulator(project)
    result = simulator.simulate_timeline(
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=90),
        team_changes=[
            TeamChange(date=datetime(2024,3,1), delta=2),  # 2 kişi ekle
            TeamChange(date=datetime(2024,4,1), delta=-1)  # 1 kişi çıkar
        ]
    )
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable, Tuple
from enum import Enum
import random
import math
import json


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TeamMember:
    """Takım üyesi"""
    id: str
    name: str
    role: str
    velocity: float  # Story points per day
    skills: List[str] = field(default_factory=list)
    availability: float = 1.0  # 0-1 (1 = full time)


@dataclass
class TeamChange:
    """Takım değişikliği"""
    date: datetime
    delta: int  # Pozitif = ekleme, negatif = çıkarma
    role: Optional[str] = None
    reason: str = ""


@dataclass
class Component:
    """Proje bileşeni"""
    id: str
    name: str
    project_id: str
    component_type: str  # hardware, software, firmware
    estimated_effort: float  # Story points
    completed_effort: float = 0
    dependencies: List[str] = field(default_factory=list)
    idi_score: float = 0
    days_since_integration: int = 0
    loc_changed: int = 0


@dataclass
class Milestone:
    """Milestone"""
    id: str
    name: str
    target_date: datetime
    components: List[str]  # Component IDs
    completed: bool = False


@dataclass
class Project:
    """Proje"""
    id: str
    name: str
    start_date: datetime
    target_end_date: datetime
    components: List[Component] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    team: List[TeamMember] = field(default_factory=list)

    @property
    def total_effort(self) -> float:
        return sum(c.estimated_effort for c in self.components)

    @property
    def completed_effort(self) -> float:
        return sum(c.completed_effort for c in self.components)

    @property
    def progress(self) -> float:
        if self.total_effort == 0:
            return 0
        return (self.completed_effort / self.total_effort) * 100

    @property
    def team_velocity(self) -> float:
        """Günlük takım hızı"""
        return sum(m.velocity * m.availability for m in self.team)


@dataclass
class SimulationConfig:
    """Simülasyon konfigürasyonu"""
    num_iterations: int = 1000  # Monte Carlo iterasyon sayısı
    velocity_variance: float = 0.2  # Hız varyansı (±20%)
    risk_factor: float = 0.1  # Genel risk faktörü
    integration_overhead: float = 0.15  # Entegrasyon overhead'i
    idi_impact_factor: float = 0.05  # IDI'nin hıza etkisi


@dataclass
class DaySnapshot:
    """Bir günün snapshot'ı"""
    date: datetime
    remaining_effort: float
    team_size: int
    team_velocity: float
    progress: float
    idi_scores: Dict[str, float]
    risks: List[str]
    events: List[str]


@dataclass
class SimulationResult:
    """Simülasyon sonucu"""
    project_id: str
    simulation_date: datetime
    config: SimulationConfig

    # Timeline
    daily_snapshots: List[DaySnapshot] = field(default_factory=list)

    # Predictions
    predicted_end_date: datetime = None
    confidence_90: datetime = None  # %90 güvenle bitiş tarihi
    confidence_50: datetime = None  # %50 güvenle bitiş tarihi

    # Statistics
    on_time_probability: float = 0
    delay_days_avg: float = 0
    delay_days_p90: float = 0

    # IDI Predictions
    idi_breach_probability: Dict[str, float] = field(default_factory=dict)
    quarantine_risk_components: List[str] = field(default_factory=list)

    # Recommendations
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'project_id': self.project_id,
            'simulation_date': self.simulation_date.isoformat(),
            'predicted_end_date': self.predicted_end_date.isoformat() if self.predicted_end_date else None,
            'confidence_90': self.confidence_90.isoformat() if self.confidence_90 else None,
            'confidence_50': self.confidence_50.isoformat() if self.confidence_50 else None,
            'on_time_probability': self.on_time_probability,
            'delay_days_avg': self.delay_days_avg,
            'delay_days_p90': self.delay_days_p90,
            'idi_breach_probability': self.idi_breach_probability,
            'quarantine_risk_components': self.quarantine_risk_components,
            'recommendations': self.recommendations,
            'daily_snapshots': [
                {
                    'date': s.date.isoformat(),
                    'remaining_effort': s.remaining_effort,
                    'team_size': s.team_size,
                    'progress': s.progress
                }
                for s in self.daily_snapshots[:30]  # İlk 30 gün
            ]
        }


# =============================================================================
# IDI SIMULATOR
# =============================================================================

class IDISimulator:
    """IDI simülatörü"""

    IDI_THRESHOLD_WARNING = 5.0
    IDI_THRESHOLD_CRITICAL = 7.0
    IDI_THRESHOLD_QUARANTINE = 10.0

    @staticmethod
    def calculate_idi(days: int, loc: int, deps: int) -> float:
        """IDI hesapla"""
        d = max(days, 0)
        l = max(loc, 0) / 1000.0
        dep = max(deps, 1) / 10.0
        return d * l * dep

    @staticmethod
    def simulate_daily_loc(base_velocity: float, variance: float = 0.3) -> int:
        """Günlük LoC değişimini simüle et"""
        # Ortalama 100 LoC per story point
        base_loc = base_velocity * 100
        return int(base_loc * (1 + random.uniform(-variance, variance)))

    def simulate_idi_progression(self, component: Component, days: int,
                                  daily_velocity: float) -> List[Tuple[int, float]]:
        """Bileşenin IDI ilerlemesini simüle et"""
        results = []
        current_days = component.days_since_integration
        current_loc = component.loc_changed
        deps = len(component.dependencies) + 1

        for day in range(days):
            # Günlük LoC ekle
            daily_loc = self.simulate_daily_loc(daily_velocity)
            current_loc += daily_loc
            current_days += 1

            # Entegrasyon olasılığı (IDI yükseldikçe artar)
            idi = self.calculate_idi(current_days, current_loc, deps)

            # Entegrasyon tetiklendi mi?
            integration_prob = min(idi / 20.0, 0.5)  # Max %50
            if random.random() < integration_prob:
                current_days = 0
                current_loc = 0

            idi = self.calculate_idi(current_days, current_loc, deps)
            results.append((day, idi))

        return results


# =============================================================================
# PROJECT SIMULATOR
# =============================================================================

class ProjectSimulator:
    """Ana proje simülatörü"""

    def __init__(self, project: Project, config: Optional[SimulationConfig] = None):
        self.project = project
        self.config = config or SimulationConfig()
        self.idi_sim = IDISimulator()

    def _apply_team_changes(self, current_team: List[TeamMember],
                            changes: List[TeamChange], current_date: datetime) -> List[TeamMember]:
        """Takım değişikliklerini uygula"""
        team = current_team.copy()

        for change in changes:
            if change.date <= current_date:
                if change.delta > 0:
                    # Yeni üyeler ekle
                    for i in range(change.delta):
                        new_member = TeamMember(
                            id=f"new-{current_date.isoformat()}-{i}",
                            name=f"New Member {i+1}",
                            role=change.role or "Developer",
                            velocity=0.5,  # Yeni üyeler daha yavaş başlar
                            availability=0.8  # Ramp-up period
                        )
                        team.append(new_member)
                elif change.delta < 0:
                    # Üyeleri çıkar
                    for _ in range(abs(change.delta)):
                        if team:
                            team.pop()

        return team

    def _calculate_daily_velocity(self, team: List[TeamMember],
                                   idi_scores: Dict[str, float]) -> float:
        """Günlük hızı hesapla (IDI etkisi dahil)"""
        base_velocity = sum(m.velocity * m.availability for m in team)

        # IDI etkisi (yüksek IDI = düşük verimlilik)
        avg_idi = sum(idi_scores.values()) / max(len(idi_scores), 1)
        idi_penalty = 1 - (avg_idi * self.config.idi_impact_factor)
        idi_penalty = max(idi_penalty, 0.5)  # Min %50 verimlilik

        # Varyans ekle
        variance = random.uniform(-self.config.velocity_variance, self.config.velocity_variance)

        return base_velocity * idi_penalty * (1 + variance)

    def simulate_single_run(self, team_changes: List[TeamChange] = None) -> Tuple[datetime, List[DaySnapshot]]:
        """Tek bir simülasyon çalıştır"""
        team_changes = team_changes or []
        current_date = datetime.now()
        remaining_effort = self.project.total_effort - self.project.completed_effort
        team = self.project.team.copy()
        snapshots = []

        # Component IDI scores
        idi_scores = {c.id: c.idi_score for c in self.project.components}

        day = 0
        max_days = 365 * 2  # Max 2 yıl

        while remaining_effort > 0 and day < max_days:
            current_date += timedelta(days=1)
            day += 1

            # Hafta sonu kontrolü
            if current_date.weekday() >= 5:
                continue

            # Takım değişikliklerini uygula
            team = self._apply_team_changes(team, team_changes, current_date)

            # Günlük hız hesapla
            daily_velocity = self._calculate_daily_velocity(team, idi_scores)

            # İş tamamla
            completed_today = min(daily_velocity, remaining_effort)
            remaining_effort -= completed_today

            # IDI güncelle
            for comp_id in idi_scores:
                component = next((c for c in self.project.components if c.id == comp_id), None)
                if component:
                    loc_today = self.idi_sim.simulate_daily_loc(daily_velocity / len(idi_scores))
                    component.loc_changed += loc_today
                    component.days_since_integration += 1
                    idi_scores[comp_id] = self.idi_sim.calculate_idi(
                        component.days_since_integration,
                        component.loc_changed,
                        len(component.dependencies) + 1
                    )

            # Snapshot kaydet
            progress = ((self.project.total_effort - remaining_effort) / self.project.total_effort) * 100
            snapshot = DaySnapshot(
                date=current_date,
                remaining_effort=remaining_effort,
                team_size=len(team),
                team_velocity=daily_velocity,
                progress=progress,
                idi_scores=idi_scores.copy(),
                risks=[],
                events=[]
            )
            snapshots.append(snapshot)

        return current_date, snapshots

    def simulate_timeline(self, team_changes: List[TeamChange] = None,
                          num_iterations: Optional[int] = None) -> SimulationResult:
        """
        Monte Carlo simülasyonu ile timeline tahmin et

        Args:
            team_changes: Planlanan takım değişiklikleri
            num_iterations: Simülasyon sayısı

        Returns:
            SimulationResult
        """
        iterations = num_iterations or self.config.num_iterations
        end_dates = []
        all_idi_breaches = {c.id: 0 for c in self.project.components}

        for _ in range(iterations):
            end_date, snapshots = self.simulate_single_run(team_changes)
            end_dates.append(end_date)

            # IDI breach kontrolü
            for snapshot in snapshots:
                for comp_id, idi in snapshot.idi_scores.items():
                    if idi >= IDISimulator.IDI_THRESHOLD_CRITICAL:
                        all_idi_breaches[comp_id] += 1

        # Sonuçları hesapla
        end_dates.sort()

        result = SimulationResult(
            project_id=self.project.id,
            simulation_date=datetime.now(),
            config=self.config
        )

        # Tarih tahminleri
        result.predicted_end_date = end_dates[len(end_dates) // 2]  # Median
        result.confidence_50 = end_dates[int(len(end_dates) * 0.5)]
        result.confidence_90 = end_dates[int(len(end_dates) * 0.9)]

        # Gecikme hesapları
        target = self.project.target_end_date
        delays = [(d - target).days for d in end_dates]
        on_time = sum(1 for d in delays if d <= 0)
        result.on_time_probability = (on_time / iterations) * 100
        result.delay_days_avg = sum(max(0, d) for d in delays) / iterations
        result.delay_days_p90 = sorted(delays)[int(len(delays) * 0.9)]

        # IDI breach olasılıkları
        result.idi_breach_probability = {
            comp_id: (count / iterations) * 100
            for comp_id, count in all_idi_breaches.items()
        }
        result.quarantine_risk_components = [
            comp_id for comp_id, prob in result.idi_breach_probability.items()
            if prob > 50
        ]

        # Öneriler
        result.recommendations = self._generate_recommendations(result)

        # İlk run'ın snapshot'larını ekle
        _, snapshots = self.simulate_single_run(team_changes)
        result.daily_snapshots = snapshots

        return result

    def _generate_recommendations(self, result: SimulationResult) -> List[str]:
        """Öneriler oluştur"""
        recs = []

        if result.on_time_probability < 50:
            recs.append(f"⚠️ On-time probability is only {result.on_time_probability:.0f}%. Consider adding resources or reducing scope.")

        if result.delay_days_p90 > 30:
            recs.append(f"⚠️ 90% confidence shows {result.delay_days_p90:.0f} days delay. Review critical path.")

        for comp_id in result.quarantine_risk_components:
            recs.append(f"🔴 Component '{comp_id}' has high IDI breach risk. Schedule integration soon.")

        if len(self.project.team) < 3:
            recs.append("👥 Team size is small. Consider adding members to reduce risk.")

        return recs

    def simulate_team_change_impact(self, delta: int, from_date: datetime) -> Dict:
        """Takım değişikliğinin etkisini simüle et"""
        # Mevcut durum
        current_result = self.simulate_timeline()

        # Değişiklik sonrası
        change = TeamChange(date=from_date, delta=delta)
        new_result = self.simulate_timeline(team_changes=[change])

        return {
            'current_end_date': current_result.predicted_end_date.isoformat(),
            'new_end_date': new_result.predicted_end_date.isoformat(),
            'days_saved': (current_result.predicted_end_date - new_result.predicted_end_date).days,
            'current_on_time_prob': current_result.on_time_probability,
            'new_on_time_prob': new_result.on_time_probability,
            'recommendation': f"Adding {delta} team members would save approximately {(current_result.predicted_end_date - new_result.predicted_end_date).days} days"
        }

    def simulate_idi_scenario(self, component_id: str, days_without_integration: int) -> Dict:
        """IDI senaryosunu simüle et"""
        component = next((c for c in self.project.components if c.id == component_id), None)
        if not component:
            return {'error': 'Component not found'}

        # IDI ilerlemesini simüle et
        daily_velocity = self.project.team_velocity / len(self.project.components)
        progression = self.idi_sim.simulate_idi_progression(
            component, days_without_integration, daily_velocity
        )

        # Ne zaman eşikleri aşıyor?
        warning_day = None
        critical_day = None
        quarantine_day = None

        for day, idi in progression:
            if idi >= IDISimulator.IDI_THRESHOLD_WARNING and warning_day is None:
                warning_day = day
            if idi >= IDISimulator.IDI_THRESHOLD_CRITICAL and critical_day is None:
                critical_day = day
            if idi >= IDISimulator.IDI_THRESHOLD_QUARANTINE and quarantine_day is None:
                quarantine_day = day

        return {
            'component_id': component_id,
            'days_simulated': days_without_integration,
            'final_idi': progression[-1][1] if progression else 0,
            'warning_threshold_day': warning_day,
            'critical_threshold_day': critical_day,
            'quarantine_threshold_day': quarantine_day,
            'idi_progression': [(d, round(idi, 2)) for d, idi in progression[::7]],  # Haftalık
            'recommendation': (
                f"Component should be integrated within {critical_day or 'N/A'} days to avoid critical IDI"
                if critical_day else "Component IDI remains healthy"
            )
        }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Örnek proje oluştur
    project = Project(
        id="smart-iot-gateway",
        name="Smart IoT Gateway",
        start_date=datetime(2024, 1, 1),
        target_end_date=datetime(2024, 6, 30),
        components=[
            Component(
                id="sensor-driver",
                name="Sensor Driver",
                project_id="smart-iot-gateway",
                component_type="hardware",
                estimated_effort=100,
                completed_effort=68,
                dependencies=[]
            ),
            Component(
                id="ml-inference",
                name="ML Inference Engine",
                project_id="smart-iot-gateway",
                component_type="software",
                estimated_effort=150,
                completed_effort=67,
                dependencies=["sensor-driver"],
                days_since_integration=5,
                loc_changed=2400
            ),
            Component(
                id="cloud-gateway",
                name="Cloud Gateway",
                project_id="smart-iot-gateway",
                component_type="software",
                estimated_effort=80,
                completed_effort=45,
                dependencies=["sensor-driver", "ml-inference"]
            )
        ],
        team=[
            TeamMember(id="dev1", name="Alice", role="Senior Developer", velocity=2.0),
            TeamMember(id="dev2", name="Bob", role="Developer", velocity=1.5),
            TeamMember(id="dev3", name="Charlie", role="Junior Developer", velocity=1.0),
        ],
        milestones=[
            Milestone(
                id="alpha",
                name="Alpha Release",
                target_date=datetime(2024, 3, 1),
                components=["sensor-driver"]
            ),
            Milestone(
                id="beta",
                name="Beta Release",
                target_date=datetime(2024, 5, 1),
                components=["sensor-driver", "ml-inference"]
            )
        ]
    )

    # Simülatör oluştur
    simulator = ProjectSimulator(project)

    # Timeline simülasyonu
    print("=" * 60)
    print("TIMELINE SIMULATION")
    print("=" * 60)
    result = simulator.simulate_timeline(num_iterations=100)
    print(f"Target End Date: {project.target_end_date.strftime('%Y-%m-%d')}")
    print(f"Predicted End Date: {result.predicted_end_date.strftime('%Y-%m-%d')}")
    print(f"90% Confidence: {result.confidence_90.strftime('%Y-%m-%d')}")
    print(f"On-Time Probability: {result.on_time_probability:.1f}%")
    print(f"Average Delay: {result.delay_days_avg:.1f} days")

    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"  {rec}")

    # Takım değişikliği etkisi
    print("\n" + "=" * 60)
    print("TEAM CHANGE IMPACT")
    print("=" * 60)
    impact = simulator.simulate_team_change_impact(
        delta=2,
        from_date=datetime(2024, 3, 1)
    )
    print(json.dumps(impact, indent=2))

    # IDI senaryosu
    print("\n" + "=" * 60)
    print("IDI SCENARIO")
    print("=" * 60)
    idi_result = simulator.simulate_idi_scenario("ml-inference", 30)
    print(json.dumps(idi_result, indent=2))
