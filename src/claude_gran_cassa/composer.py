import json
from anthropic import Anthropic
from .models import Composition
from .parser import ResponseParser


class Composer:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def _create_system_prompt(self) -> str:
        return """You are a techno music producer specializing in rhythm programming. Generate drum patterns in the following exact JSON format:

{
  "config": {
    "bpm": <integer 120-160>,
    "time_signature": [4, 4],
    "swing_amount": <float 0.0-1.0>
  },
  "patterns": [
    {
      "name": <string: "kick", "hihat", "snare", etc>,
      "hits": <list of 0/1 integers>,
      "divisions": <integer: typically 16 for 16th notes>,
      "triplet": <boolean>,
      "channel": <integer 1-16>,
      "note": <integer MIDI note 0-127>,
      "velocities": <list of integers 0-127, one per hit>,
      "panning": <list of integers -64 to 64, one per hit>,
      "bars": <integer: typically 1-4>
    }
  ]
}

Rules and Constraints:
1. Each "hits" list must be exactly "divisions" long
2. The number of values in "velocities" and "panning" must match the count of 1s in "hits"
3. Common MIDI notes: Kick=36, Snare=38, Closed HiHat=42, Open HiHat=46
4. Channel numbers must be unique per pattern
5. Pan values: 0=center, negative=left, positive=right
6. Always respond with ONLY the JSON pattern, no explanations or commentary

Example valid pattern:
{
  "config": {
    "bpm": 130,
    "time_signature": [4, 4],
    "swing_amount": 0.0
  },
  "patterns": [
    {
      "name": "kick",
      "hits": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
      "divisions": 16,
      "triplet": false,
      "channel": 1,
      "note": 36,
      "velocities": [127, 120, 127, 125],
      "panning": [0, 0, 0, 0],
      "bars": 1
    }
  ]
}"""

    def _validate_response(self, response: str) -> str:
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON object found in response")

            json_str = response[start:end]

            data = json.loads(json_str)
            required_top_level = {"config", "patterns"}
            if not all(k in data for k in required_top_level):
                raise ValueError(
                    f"Missing required keys: {required_top_level - set(data.keys())}"
                )

            return json_str

        except Exception as e:
            raise ValueError(f"Invalid response format: {str(e)}\nResponse: {response}")

    def _get_example_for_prompt(self, prompt: str) -> str:
        examples = {
            "minimal": {
                "config": {"bpm": 130, "time_signature": [4, 4], "swing_amount": 0.0},
                "patterns": [
                    {
                        "name": "kick",
                        "hits": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                        "divisions": 16,
                        "triplet": False,
                        "channel": 1,
                        "note": 36,
                        "velocities": [127, 120, 127, 125],
                        "panning": [0, 0, 0, 0],
                        "bars": 1,
                    }
                ],
            },
            "polyrhythm": {
                # TODO: Add example with triplets/polyrhythms
            },
            "breakbeat": {
                # TODO: Add example with complex kick patterns
            },
            # TODO: Add more examples for different styles
        }

        for key in examples:
            if key in prompt.lower():
                return f"\nHere's a relevant example:\n{json.dumps(examples[key], indent=2)}"
        return ""

    def generate_pattern(self, prompt: str) -> Composition:
        """Generate a new pattern based on the prompt"""
        system_prompt = self._create_system_prompt()
        example = self._get_example_for_prompt(prompt)

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}{example}\n\nRespond with ONLY the JSON pattern data.",
                }
            ],
        )

        validated_response = self._validate_response(response.content[0].text)
        return ResponseParser.parse(validated_response)

    def evolve_pattern(self, composition: Composition, prompt: str) -> Composition:
        """Evolve an existing pattern"""
        system_prompt = (
            self._create_system_prompt()
            + "\n\nWhen evolving patterns:\n1. Maintain the basic structure\n2. Preserve pattern length and divisions\n3. Only modify the elements mentioned in the prompt\n4. Keep all other elements unchanged"
        )

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Current pattern:\n{json.dumps(composition.to_dict(), indent=2)}\n\nModification request: {prompt}\n\nRespond with ONLY the modified JSON pattern data.",
                }
            ],
        )

        validated_response = self._validate_response(response.content[0].text)
        return ResponseParser.parse(validated_response)
