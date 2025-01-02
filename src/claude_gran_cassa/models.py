from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SongConfig:
    bpm: int = 130
    time_signature: tuple[int, int] = (4, 4)
    swing_amount: float = 0.0


@dataclass
class Pattern:
    # Core rhythm properties
    hits: List[int]  # 1 for hit, 0 for rest
    divisions: int = 16
    triplet: bool = False

    # Sound properties
    channel: int = 1
    note: int = 36

    # Expression properties
    velocities: Optional[List[int]] = None  # 0-127 for each hit
    panning: Optional[List[int]] = None  # 0-127 for each hit (64 = center)

    # Metadata
    name: str = ""
    bars: int = 1

    def __post_init__(self):
        hit_count = sum(self.hits)
        if self.velocities is None:
            self.velocities = [100] * hit_count
        if self.panning is None:
            self.panning = [64] * hit_count

    def to_dict(self) -> dict:
        return {
            "hits": self.hits,
            "divisions": self.divisions,
            "triplet": self.triplet,
            "channel": self.channel,
            "note": self.note,
            "velocities": self.velocities,
            "panning": self.panning,
            "name": self.name,
            "bars": self.bars,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pattern":
        return cls(
            hits=data["hits"],
            divisions=data["divisions"],
            triplet=data.get("triplet", False),
            channel=data["channel"],
            note=data["note"],
            velocities=data.get("velocities"),
            panning=data.get("panning"),
            name=data.get("name", ""),
            bars=data.get("bars", 1),
        )


@dataclass
class Composition:
    config: SongConfig
    patterns: List[Pattern]

    def to_dict(self) -> dict:
        return {
            "config": {
                "bpm": self.config.bpm,
                "time_signature": list(self.config.time_signature),
                "swing_amount": self.config.swing_amount,
            },
            "patterns": [pattern.to_dict() for pattern in self.patterns],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Composition":
        config = SongConfig(
            bpm=data["config"]["bpm"],
            time_signature=tuple(data["config"]["time_signature"]),
            swing_amount=data["config"].get("swing_amount", 0.0),
        )
        patterns = [Pattern.from_dict(p) for p in data["patterns"]]
        return cls(config=config, patterns=patterns)
