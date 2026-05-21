from src.core.errors.catalog import ERRORS
from src.core.errors.model import SantraError
from src.services.ingestion.ede.ede_types import EdeParsed, EdeMetadata, EdeRow


class EdeParser:
    def parse(self, content: str) -> EdeParsed:
        lines = content.split("\n")

        rows: list[EdeRow] = []
        project_name = "unknown"
        column_index: dict[str, int] = {}

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            if self._is_project_name_line(trimmed):
                project_name = self._extract_project_name(trimmed) or "default"
                continue

            if trimmed.startswith("#") and ";" in trimmed:
                header = trimmed.replace("#", "", 1).strip().split(";")
                column_index = self._build_column_index(header)
                continue

            if trimmed.startswith("#"):
                continue

            cols = trimmed.split(";")

            if len(cols) < 5:
                continue

            rows.append(
                EdeRow(
                    keyname=self._get_required(cols, column_index, "keyname"),
                    deviceId=self._get_required(cols, column_index, "deviceId"),
                    objectName=self._get_required(cols, column_index, "objectName"),
                    objectType=self._get_required(cols, column_index, "objectType"),
                    objectInstance=self._get_required(cols, column_index, "objectInstance"),
                    description=self._get(cols, column_index, "description"),
                    unit=self._get(cols, column_index, "unit"),
                    stateText=self._parse_state_text(self._get(cols, column_index, "stateText")),
                )
            )

        return EdeParsed(
            metadata=EdeMetadata(projectName=project_name),
            rows=rows,
        )

    def _build_column_index(self, header: list[str]) -> dict[str, int]:
        index: dict[str, int] = {}

        for i, col in enumerate(header):
            normalized = col.lower().replace(" ", "")

            if "keyname" in normalized:
                index["keyname"] = i
            if "device" in normalized:
                index["deviceId"] = i
            if "object-name" in normalized:
                index["objectName"] = i
            if "object-type" in normalized:
                index["objectType"] = i
            if "object-instance" in normalized:
                index["objectInstance"] = i
            if "description" in normalized:
                index["description"] = i
            if "unit" in normalized:
                index["unit"] = i
            if "state-text" in normalized:
                index["stateText"] = i

        return index

    def _get(self, cols: list[str], index: dict[str, int], key: str) -> str | None:
        i = index.get(key)
        if i is None:
            return None

        value = cols[i].strip() if i < len(cols) and cols[i] is not None else None
        return value if value != "" else None

    def _get_required(self, cols: list[str], index: dict[str, int], key: str) -> str:
        value = self._get(cols, index, key)

        if not value:
            err = ERRORS["IMPORT_EDE_VALIDATION_FAILED"]
            raise SantraError(
                code=err["code"],
                message=f'Missing required field "{key}" in EDE row',
                category=err["category"],
                module="ede.parser",
                meta={
                    "key": key,
                    "row": cols,
                },
                status_code=400,
            )

        return value

    def _parse_state_text(self, value: str | None):
        if not value:
            return None

        trimmed = value.strip()

        if trimmed.startswith("[") and trimmed.endswith("]"):
            return [v.strip() for v in trimmed[1:-1].split("|") if v.strip()]

        if ";" in trimmed:
            return [v.strip() for v in trimmed.split(";") if v.strip()]

        return [trimmed]

    def _is_project_name_line(self, line: str) -> bool:
        return line.startswith("PROJECT_NAME") or line.startswith("# PROJECT_NAME")

    def _extract_project_name(self, line: str) -> str:
        clean = line.removeprefix("# ").removeprefix("#")

        if ";" in clean:
            parts = clean.split(";")
            return parts[1].strip() if len(parts) > 1 and parts[1].strip() else "default"

        parts = clean.split()
        return " ".join(parts[1:]) if len(parts) > 1 else "default"