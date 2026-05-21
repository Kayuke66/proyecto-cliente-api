class HierarchyBuilder:
    def build_node(self, input_data: dict):
        return {
            "id": input_data["id"],
            "name": input_data.get("name", input_data["id"]),
            "description": input_data.get("description", input_data["id"]),
            "metadata": input_data.get("metadata"),
        }