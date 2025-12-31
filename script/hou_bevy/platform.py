import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class HouRectMesh:
    size: List[float]
    translation: List[float]

    def __post_init__(self):
        """Validate data after initialization"""
        if len(self.size) != 2:
            raise ValueError(f"size must have 2 elements, got {len(self.size)}")
        if len(self.translation) != 3:
            raise ValueError(
                f"translation must have 3 elements, got {len(self.translation)}"
            )

    @classmethod
    def new(cls, size: List[float], translation: List[float]):
        return cls(size=size, translation=translation)


@dataclass
class HouPlatformData:
    rects: List[HouRectMesh] = field(default_factory=list)

    def __init__(self, rects: Optional[List[HouRectMesh]] = None):
        self.rects = rects if rects is not None else []

    def append_rect(self, rect: HouRectMesh):
        self.rects.append(rect)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "rects": [
                {"size": rect.size, "translation": rect.translation}
                for rect in self.rects
            ]
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)

    def export_to_file(self, filepath: Union[str, Path], indent: int = 2):
        """
        Export data to a JSON file

        Args:
            filepath: Path to save the JSON file
            indent: JSON indentation level
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=indent)

        print(f"✅ Successfully exported {len(self.rects)} rects to: {filepath}")


# Example usage function
def create_and_export_example():
    """Create example data and export to JSON"""
    # Create some test rectangles
    platform_data = HouPlatformData()

    platform_data.append_rect(
        HouRectMesh(size=[10.0, 5.0], translation=[0.0, 0.0, 0.0])
    )

    platform_data.append_rect(HouRectMesh(size=[8.0, 4.0], translation=[5.0, 2.0, 1.0]))

    platform_data.append_rect(
        HouRectMesh(size=[12.0, 3.0], translation=[-3.0, -1.0, 0.5])
    )

    # Display the data
    print(f"Created platform data with {len(platform_data.rects)} rectangles:")
    for i, rect in enumerate(platform_data.rects):
        print(f"  Rect {i}: size={rect.size}, translation={rect.translation}")

    # Export to JSON file
    platform_data.export_to_file("hou_platform_data.json")

    # Show JSON string
    print("\nJSON Output:")
    print(platform_data.to_json())

    return platform_data


# For direct execution
if __name__ == "__main__":
    data = create_and_export_example()
