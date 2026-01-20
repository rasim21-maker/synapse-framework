"""
SYNAPSE IDI-Lock Algorithm - CI/CD Pipeline Integration Lock
=============================================================

Bu script, IDI (Integration Debt Index) değeri eşik değerini aştığında
CI/CD pipeline'ını sadece bug-fix ve integration commit'lerine izin verecek
şekilde filtreler.

Kullanım:
    # Git hook olarak (pre-push)
    python idi_lock.py --mode=hook --component=sensor-driver

    # CI/CD pipeline'da
    python idi_lock.py --mode=ci --project=smart-iot-gateway

    # Manuel kontrol
    python idi_lock.py --mode=check --all

Exit Codes:
    0 = Commit izinli
    1 = Commit engellendi (IDI Lock aktif)
    2 = Konfigürasyon hatası
"""

import re
import sys
import json
import argparse
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
from pathlib import Path


# =============================================================================
# CONFIGURATION
# =============================================================================

class IDILockConfig:
    """IDI-Lock konfigürasyonu"""

    # IDI Eşik Değerleri
    IDI_SOFT_LOCK = 5.0      # Uyarı - sadece uyarı verir
    IDI_HARD_LOCK = 7.0      # Sert kilit - sadece belirli commit'lere izin
    IDI_TOTAL_LOCK = 10.0    # Tam kilit - hiçbir commit'e izin yok

    # İzin verilen commit türleri (IDI_HARD_LOCK durumunda)
    ALLOWED_COMMIT_TYPES = [
        'fix',          # Bug fix
        'bugfix',       # Bug fix alternatif
        'hotfix',       # Acil düzeltme
        'integration',  # Entegrasyon işlemi
        'merge',        # Merge commit
        'revert',       # Geri alma
        'ci',           # CI/CD değişiklikleri
    ]

    # Commit mesajı pattern'leri
    COMMIT_PATTERNS = {
        'conventional': r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|hotfix|bugfix|integration)(\(.+\))?!?:\s.+',
        'jira': r'^[A-Z]+-\d+\s+(fix|bugfix|integration|hotfix)',
        'simple': r'^(fix|bugfix|hotfix|integration|merge|revert)',
    }

    # Dosya uzantısı bazlı ağırlıklar (LoC hesaplama için)
    FILE_WEIGHTS = {
        '.py': 1.0,
        '.cpp': 1.2,
        '.hpp': 1.1,
        '.c': 1.2,
        '.h': 1.0,
        '.js': 0.9,
        '.ts': 1.0,
        '.tsx': 1.0,
        '.java': 1.1,
        '.go': 1.0,
        '.rs': 1.1,
        '.cs': 1.0,
        '.html': 0.5,
        '.css': 0.4,
        '.json': 0.3,
        '.yaml': 0.3,
        '.yml': 0.3,
        '.md': 0.1,
    }


class LockLevel(Enum):
    """Kilit seviyeleri"""
    NONE = "none"
    SOFT = "soft"       # Sadece uyarı
    HARD = "hard"       # Belirli commit'lere izin
    TOTAL = "total"     # Tam kilit


@dataclass
class ComponentState:
    """Bileşen durumu"""
    id: str
    name: str
    project_id: str
    idi_score: float
    days_since_integration: int
    loc_changed: int
    dependencies: int
    last_integration: datetime
    lock_level: LockLevel = LockLevel.NONE

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'idi_score': self.idi_score,
            'days_since_integration': self.days_since_integration,
            'loc_changed': self.loc_changed,
            'dependencies': self.dependencies,
            'last_integration': self.last_integration.isoformat(),
            'lock_level': self.lock_level.value
        }


@dataclass
class LockDecision:
    """Kilit kararı"""
    allowed: bool
    lock_level: LockLevel
    component_id: str
    idi_score: float
    reason: str
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'allowed': self.allowed,
            'lock_level': self.lock_level.value,
            'component_id': self.component_id,
            'idi_score': self.idi_score,
            'reason': self.reason,
            'suggestions': self.suggestions
        }


# =============================================================================
# IDI CALCULATOR
# =============================================================================

class IDICalculator:
    """IDI hesaplayıcı"""

    @staticmethod
    def calculate(days: int, loc_changed: int, dependencies: int) -> float:
        """
        IDI = (Days Since Last Integration) × (LoC Changed / 1000) × (Dependencies / 10)
        """
        d = max(days, 0)
        l = max(loc_changed, 0) / 1000.0
        dep = max(dependencies, 1) / 10.0

        return round(d * l * dep, 2)

    @staticmethod
    def get_lock_level(idi: float) -> LockLevel:
        """IDI'ye göre kilit seviyesi"""
        if idi >= IDILockConfig.IDI_TOTAL_LOCK:
            return LockLevel.TOTAL
        elif idi >= IDILockConfig.IDI_HARD_LOCK:
            return LockLevel.HARD
        elif idi >= IDILockConfig.IDI_SOFT_LOCK:
            return LockLevel.SOFT
        return LockLevel.NONE


# =============================================================================
# COMMIT ANALYZER
# =============================================================================

class CommitAnalyzer:
    """Commit mesajı analiz edici"""

    def __init__(self):
        self.patterns = IDILockConfig.COMMIT_PATTERNS
        self.allowed_types = IDILockConfig.ALLOWED_COMMIT_TYPES

    def get_commit_type(self, message: str) -> Optional[str]:
        """Commit mesajından tip çıkar"""
        message = message.strip().lower()

        # Conventional commits pattern
        match = re.match(r'^(\w+)(\(.+\))?!?:', message)
        if match:
            return match.group(1)

        # Simple pattern
        for commit_type in self.allowed_types:
            if message.startswith(commit_type):
                return commit_type

        # Merge commit
        if message.startswith('merge'):
            return 'merge'

        return None

    def is_allowed_commit(self, message: str) -> Tuple[bool, str]:
        """
        Commit'in izin verilip verilmediğini kontrol et

        Returns: (is_allowed, commit_type)
        """
        commit_type = self.get_commit_type(message)

        if commit_type is None:
            return False, "unknown"

        if commit_type in self.allowed_types:
            return True, commit_type

        return False, commit_type

    def analyze_commit(self, message: str, lock_level: LockLevel) -> LockDecision:
        """Commit'i analiz et ve karar ver"""

        if lock_level == LockLevel.NONE:
            return LockDecision(
                allowed=True,
                lock_level=lock_level,
                component_id="",
                idi_score=0,
                reason="No IDI lock active"
            )

        if lock_level == LockLevel.TOTAL:
            return LockDecision(
                allowed=False,
                lock_level=lock_level,
                component_id="",
                idi_score=0,
                reason="TOTAL LOCK: No commits allowed until integration is completed",
                suggestions=[
                    "Complete pending integration immediately",
                    "Contact team lead for emergency override",
                    "Run 'synapse integrate --force' if authorized"
                ]
            )

        is_allowed, commit_type = self.is_allowed_commit(message)

        if lock_level == LockLevel.HARD:
            if is_allowed:
                return LockDecision(
                    allowed=True,
                    lock_level=lock_level,
                    component_id="",
                    idi_score=0,
                    reason=f"HARD LOCK active but '{commit_type}' commits are allowed"
                )
            else:
                return LockDecision(
                    allowed=False,
                    lock_level=lock_level,
                    component_id="",
                    idi_score=0,
                    reason=f"HARD LOCK: Only fix/integration commits allowed. Got: '{commit_type}'",
                    suggestions=[
                        f"Change commit type to one of: {', '.join(self.allowed_types)}",
                        "Example: 'fix: resolve integration issue'",
                        "Example: 'integration: merge feature branch'"
                    ]
                )

        if lock_level == LockLevel.SOFT:
            return LockDecision(
                allowed=True,
                lock_level=lock_level,
                component_id="",
                idi_score=0,
                reason=f"SOFT LOCK: Warning - IDI is high. Commit type: '{commit_type}'",
                suggestions=[
                    "Consider completing integration soon",
                    "Avoid adding new features until integration"
                ]
            )

        return LockDecision(
            allowed=True,
            lock_level=lock_level,
            component_id="",
            idi_score=0,
            reason="Commit allowed"
        )


# =============================================================================
# GIT INTEGRATION
# =============================================================================

class GitIntegration:
    """Git entegrasyonu"""

    @staticmethod
    def get_current_branch() -> str:
        """Aktif branch'i al"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"

    @staticmethod
    def get_commit_message(commit_ref: str = "HEAD") -> str:
        """Commit mesajını al"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%B', commit_ref],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def get_changed_files(since_ref: Optional[str] = None) -> List[str]:
        """Değişen dosyaları al"""
        try:
            if since_ref:
                cmd = ['git', 'diff', '--name-only', since_ref, 'HEAD']
            else:
                cmd = ['git', 'diff', '--name-only', '--cached']

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return [f for f in result.stdout.strip().split('\n') if f]
        except subprocess.CalledProcessError:
            return []

    @staticmethod
    def get_loc_changed(since_ref: Optional[str] = None) -> int:
        """Değişen satır sayısını al"""
        try:
            if since_ref:
                cmd = ['git', 'diff', '--stat', since_ref, 'HEAD']
            else:
                cmd = ['git', 'diff', '--stat', '--cached']

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Son satırdan toplam değişiklik sayısını çıkar
            lines = result.stdout.strip().split('\n')
            if lines:
                last_line = lines[-1]
                # "X files changed, Y insertions(+), Z deletions(-)" formatından parse et
                match = re.search(r'(\d+) insertion', last_line)
                insertions = int(match.group(1)) if match else 0
                match = re.search(r'(\d+) deletion', last_line)
                deletions = int(match.group(1)) if match else 0
                return insertions + deletions
            return 0
        except subprocess.CalledProcessError:
            return 0

    @staticmethod
    def get_days_since_last_integration(branch: str = "main") -> int:
        """Son entegrasyondan bu yana geçen gün sayısı"""
        try:
            # Merge commit'leri bul
            result = subprocess.run(
                ['git', 'log', '--merges', '-1', '--format=%ct', branch],
                capture_output=True, text=True, check=True
            )
            if result.stdout.strip():
                timestamp = int(result.stdout.strip())
                last_merge = datetime.fromtimestamp(timestamp)
                days = (datetime.now() - last_merge).days
                return max(days, 0)
            return 0
        except subprocess.CalledProcessError:
            return 0


# =============================================================================
# IDI LOCK ENGINE
# =============================================================================

class IDILockEngine:
    """IDI-Lock ana motoru"""

    def __init__(self, config_path: Optional[str] = None):
        self.analyzer = CommitAnalyzer()
        self.git = GitIntegration()
        self.config_path = config_path or ".synapse/idi-lock.json"
        self.components: Dict[str, ComponentState] = {}
        self._load_config()

    def _load_config(self):
        """Konfigürasyon dosyasını yükle"""
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    for comp_data in data.get('components', []):
                        comp = ComponentState(
                            id=comp_data['id'],
                            name=comp_data['name'],
                            project_id=comp_data.get('project_id', 'default'),
                            idi_score=comp_data.get('idi_score', 0),
                            days_since_integration=comp_data.get('days_since_integration', 0),
                            loc_changed=comp_data.get('loc_changed', 0),
                            dependencies=comp_data.get('dependencies', 1),
                            last_integration=datetime.fromisoformat(comp_data.get('last_integration', datetime.now().isoformat())),
                            lock_level=LockLevel(comp_data.get('lock_level', 'none'))
                        )
                        self.components[comp.id] = comp
            except Exception as e:
                print(f"Warning: Could not load config: {e}", file=sys.stderr)

    def _save_config(self):
        """Konfigürasyonu kaydet"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'components': [comp.to_dict() for comp in self.components.values()],
            'last_updated': datetime.now().isoformat()
        }

        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)

    def update_component(self, component_id: str, project_id: str = "default",
                         dependencies: int = 1) -> ComponentState:
        """Bileşen IDI'sini güncelle"""
        days = self.git.get_days_since_last_integration()
        loc = self.git.get_loc_changed()

        idi = IDICalculator.calculate(days, loc, dependencies)
        lock_level = IDICalculator.get_lock_level(idi)

        comp = ComponentState(
            id=component_id,
            name=component_id,
            project_id=project_id,
            idi_score=idi,
            days_since_integration=days,
            loc_changed=loc,
            dependencies=dependencies,
            last_integration=datetime.now() - timedelta(days=days),
            lock_level=lock_level
        )

        self.components[component_id] = comp
        self._save_config()

        return comp

    def check_commit(self, component_id: str, commit_message: Optional[str] = None) -> LockDecision:
        """Commit'i kontrol et"""

        if component_id not in self.components:
            # Bileşen yoksa güncelle
            self.update_component(component_id)

        comp = self.components[component_id]

        if commit_message is None:
            commit_message = self.git.get_commit_message()

        decision = self.analyzer.analyze_commit(commit_message, comp.lock_level)
        decision.component_id = comp.id
        decision.idi_score = comp.idi_score

        return decision

    def get_status(self, project_id: Optional[str] = None) -> Dict:
        """Tüm bileşenlerin durumunu al"""
        components = self.components.values()

        if project_id:
            components = [c for c in components if c.project_id == project_id]

        return {
            'components': [c.to_dict() for c in components],
            'locked_count': sum(1 for c in components if c.lock_level != LockLevel.NONE),
            'hard_locked_count': sum(1 for c in components if c.lock_level in [LockLevel.HARD, LockLevel.TOTAL]),
            'average_idi': sum(c.idi_score for c in components) / max(len(list(components)), 1)
        }

    def force_unlock(self, component_id: str, reason: str) -> bool:
        """Acil durum kilidi kaldırma (admin only)"""
        if component_id in self.components:
            self.components[component_id].lock_level = LockLevel.NONE
            self._save_config()
            print(f"[IDI-LOCK] Force unlocked {component_id}. Reason: {reason}")
            return True
        return False


# =============================================================================
# CI/CD INTEGRATION
# =============================================================================

def ci_check(project_id: str, component_id: str) -> int:
    """
    CI/CD pipeline'da kullanılacak kontrol fonksiyonu

    Returns:
        0 = Continue pipeline
        1 = Block pipeline
    """
    engine = IDILockEngine()

    # Bileşeni güncelle
    comp = engine.update_component(component_id, project_id)

    # Commit'i kontrol et
    decision = engine.check_commit(component_id)

    # Çıktı
    print("=" * 60)
    print("SYNAPSE IDI-LOCK CI/CD CHECK")
    print("=" * 60)
    print(f"Project:    {project_id}")
    print(f"Component:  {component_id}")
    print(f"IDI Score:  {comp.idi_score}")
    print(f"Lock Level: {comp.lock_level.value.upper()}")
    print(f"Decision:   {'ALLOWED' if decision.allowed else 'BLOCKED'}")
    print(f"Reason:     {decision.reason}")

    if decision.suggestions:
        print("\nSuggestions:")
        for s in decision.suggestions:
            print(f"  - {s}")

    print("=" * 60)

    return 0 if decision.allowed else 1


def hook_check(component_id: str) -> int:
    """
    Git hook (pre-push) için kontrol fonksiyonu

    Returns:
        0 = Allow push
        1 = Block push
    """
    engine = IDILockEngine()
    decision = engine.check_commit(component_id)

    if not decision.allowed:
        print("\n" + "!" * 60)
        print("IDI-LOCK: Push blocked!")
        print("!" * 60)
        print(f"\nReason: {decision.reason}")
        print(f"IDI Score: {decision.idi_score}")
        print(f"Lock Level: {decision.lock_level.value.upper()}")

        if decision.suggestions:
            print("\nHow to fix:")
            for i, s in enumerate(decision.suggestions, 1):
                print(f"  {i}. {s}")

        print("\n" + "!" * 60)
        return 1

    if decision.lock_level == LockLevel.SOFT:
        print("\n" + "-" * 60)
        print("IDI-LOCK WARNING: IDI is getting high")
        print("-" * 60)
        print(f"IDI Score: {decision.idi_score}")
        print("Consider completing integration soon.")
        print("-" * 60 + "\n")

    return 0


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='SYNAPSE IDI-Lock - CI/CD Pipeline Integration Lock',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Git hook mode
  python idi_lock.py --mode=hook --component=sensor-driver

  # CI/CD mode
  python idi_lock.py --mode=ci --project=smart-iot --component=ml-inference

  # Check status
  python idi_lock.py --mode=status --project=smart-iot

  # Force unlock (emergency)
  python idi_lock.py --mode=unlock --component=sensor-driver --reason="Emergency hotfix"
        """
    )

    parser.add_argument('--mode', choices=['hook', 'ci', 'status', 'unlock', 'check'],
                        default='check', help='Operation mode')
    parser.add_argument('--project', default='default', help='Project ID')
    parser.add_argument('--component', help='Component ID')
    parser.add_argument('--message', help='Commit message (for testing)')
    parser.add_argument('--reason', help='Reason for unlock')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.mode == 'hook':
        if not args.component:
            print("Error: --component required for hook mode", file=sys.stderr)
            sys.exit(2)
        sys.exit(hook_check(args.component))

    elif args.mode == 'ci':
        if not args.component:
            print("Error: --component required for ci mode", file=sys.stderr)
            sys.exit(2)
        sys.exit(ci_check(args.project, args.component))

    elif args.mode == 'status':
        engine = IDILockEngine()
        status = engine.get_status(args.project if args.project != 'default' else None)

        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("\nSYNAPSE IDI-LOCK STATUS")
            print("=" * 50)
            print(f"Total Components:    {len(status['components'])}")
            print(f"Locked Components:   {status['locked_count']}")
            print(f"Hard Locked:         {status['hard_locked_count']}")
            print(f"Average IDI:         {status['average_idi']:.2f}")
            print("\nComponents:")
            for c in status['components']:
                lock_indicator = "🔴" if c['lock_level'] == 'total' else \
                                "🟠" if c['lock_level'] == 'hard' else \
                                "🟡" if c['lock_level'] == 'soft' else "🟢"
                print(f"  {lock_indicator} {c['name']}: IDI={c['idi_score']}, Lock={c['lock_level']}")

    elif args.mode == 'unlock':
        if not args.component or not args.reason:
            print("Error: --component and --reason required for unlock mode", file=sys.stderr)
            sys.exit(2)
        engine = IDILockEngine()
        if engine.force_unlock(args.component, args.reason):
            print(f"Component {args.component} unlocked successfully")
        else:
            print(f"Component {args.component} not found", file=sys.stderr)
            sys.exit(1)

    elif args.mode == 'check':
        if not args.component:
            print("Error: --component required for check mode", file=sys.stderr)
            sys.exit(2)

        engine = IDILockEngine()
        message = args.message or engine.git.get_commit_message()
        decision = engine.check_commit(args.component, message)

        if args.json:
            print(json.dumps(decision.to_dict(), indent=2))
        else:
            print(f"\nCommit: {message[:50]}...")
            print(f"Decision: {'✅ ALLOWED' if decision.allowed else '❌ BLOCKED'}")
            print(f"Reason: {decision.reason}")


if __name__ == "__main__":
    main()
