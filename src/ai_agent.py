import numpy as np
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ACTIONS = ["KEEP_DIRECT", "SWITCH_TO_BACKUP", "KEEP_BACKUP", "RESTORE_DIRECT"]

@dataclass
class Observation:
    current_path_backup: int
    e2e_rtt_ms: float
    e2e_loss_pct: float
    throughput_mbps: float
    direct_probe_rtt_ms: float
    direct_probe_loss_pct: float
    direct_healthy_streak: int

    def as_array(self):
        return np.array([[self.current_path_backup, self.e2e_rtt_ms, self.e2e_loss_pct,
                          self.throughput_mbps, self.direct_probe_rtt_ms,
                          self.direct_probe_loss_pct, self.direct_healthy_streak]], dtype=float)

class LocalNetworkAIAgent:
    """Small local ML-based control agent.

    It is trained on synthetic examples that encode the desired control policy.
    At runtime, inference is done by the trained model, not by if/else rules.
    """
    def __init__(self, random_state=7):
        self.model = Pipeline([
            ("scale", StandardScaler()),
            ("rf", RandomForestClassifier(n_estimators=80, max_depth=6, random_state=random_state))
        ])
        self.is_trained = False

    def train_synthetic_policy(self, n=2500, random_state=7):
        rng = np.random.default_rng(random_state)
        X, y = [], []
        for _ in range(n):
            current_backup = int(rng.random() < 0.5)
            e2e_rtt = rng.uniform(1, 140)
            e2e_loss = rng.uniform(0, 15)
            throughput = rng.uniform(1, 100)
            direct_rtt = rng.uniform(1, 140)
            direct_loss = rng.uniform(0, 15)
            streak = rng.integers(0, 6)

            direct_bad = (direct_loss >= 2.0) or (direct_rtt >= 35.0)
            e2e_bad = (e2e_loss >= 2.0) or (e2e_rtt >= 35.0) or (throughput <= 40.0)
            direct_recovered = (direct_loss < 1.0) and (direct_rtt < 25.0) and (streak >= 3)

            if current_backup == 0:
                label = "SWITCH_TO_BACKUP" if (direct_bad or e2e_bad) else "KEEP_DIRECT"
            else:
                label = "RESTORE_DIRECT" if direct_recovered else "KEEP_BACKUP"

            X.append([current_backup, e2e_rtt, e2e_loss, throughput, direct_rtt, direct_loss, streak])
            y.append(label)

        self.model.fit(np.array(X, dtype=float), np.array(y))
        self.is_trained = True
        return self

    def predict(self, obs: Observation):
        if not self.is_trained:
            raise RuntimeError("Agent must be trained first.")
        action = self.model.predict(obs.as_array())[0]
        proba = {}
        if hasattr(self.model[-1], "classes_"):
            probs = self.model.predict_proba(obs.as_array())[0]
            proba = dict(zip(self.model[-1].classes_, probs))
        return action, proba
