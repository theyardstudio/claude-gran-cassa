import json
from .models import Composition, Pattern, SongConfig


class ResponseParser:
    @staticmethod
    def normalize_pan(pan_value: int) -> int:
        """Convert pan values from -64~64 or -100~100 to 0~127"""
        if -64 <= pan_value <= 64:
            return int((pan_value + 64) * (127 / 128))
        elif -100 <= pan_value <= 100:
            return int((pan_value + 100) * (127 / 200))
        raise ValueError(f"Unexpected pan value: {pan_value}")

    @classmethod
    def parse(cls, response: str) -> Composition:
        """Parse Claude's response into a Composition"""
        try:
            data = json.loads(response.strip())

            config = SongConfig(
                bpm=data["config"]["bpm"],
                time_signature=tuple(data["config"]["time_signature"]),
                swing_amount=data["config"].get("swing_amount", 0.0),
            )

            patterns = [
                Pattern(
                    hits=p["hits"],
                    divisions=p["divisions"],
                    triplet=p.get("triplet", False),
                    channel=p["channel"],
                    note=p["note"],
                    velocities=p["velocities"],
                    panning=[cls.normalize_pan(pan) for pan in p["panning"]],
                    name=p["name"],
                    bars=p.get("bars", 1),
                )
                for p in data["patterns"]
            ]

            return Composition(config=config, patterns=patterns)

        except Exception as e:
            raise ValueError(
                f"Failed to parse Claude's response: {str(e)}\nResponse: {response}"
            )
