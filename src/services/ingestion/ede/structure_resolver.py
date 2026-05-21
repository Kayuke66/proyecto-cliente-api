from src.services.ingestion.ede.ede_types import EdeRow


class StructureResolver:
    def resolve(self, row: EdeRow):
        raw = row.objectName or row.keyname
        analysis = self._analyze(raw)
        parts = analysis["segments"]

        if len(parts) >= 5:
            hierarchy = {
                "buildingId": parts[0],
                "floorId": parts[1],
                "roomId": parts[2],
                "equipmentId": parts[-2] if len(parts) >= 4 else parts[-1],
            }
        elif len(parts) >= 3:
            hierarchy = {
                "buildingId": "default",
                "floorId": "default",
                "roomId": parts[0],
                "equipmentId": parts[1],
            }
        else:
            hierarchy = {
                "buildingId": "default",
                "floorId": "default",
                "roomId": "default",
                "equipmentId": parts[0] if parts else "unknown",
            }

        return {
            "source": "objectName" if row.objectName else "keyname",
            "hierarchy": hierarchy,
            "metric": parts[-1],
        }

    def _analyze(self, value: str):
        separators = ["'", ".", "/", "_"]

        best = {
            "segments": [value],
            "separator": "",
            "score": 0,
        }

        for separator in separators:
            parts = value.split(separator)

            if len(parts) <= 1:
                continue

            score = len(parts) * 2

            if value.startswith("OBJECT_"):
                score -= 10

            if ":" in value and len(parts) == 1:
                score -= 5

            if score > best["score"]:
                best = {
                    "segments": parts,
                    "separator": separator,
                    "score": score,
                }

        return best