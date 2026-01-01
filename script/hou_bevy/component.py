from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0

    @classmethod
    def splat(cls, value: float) -> Vec2:
        return cls(x=value, y=value)

    @classmethod
    def new(cls, x: float, y: float) -> Vec2:
        return cls(x=x, y=y)

    def to_dict(self) -> List[float]:
        return [self.x, self.y]

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> Vec2:
        return cls(x=data.get("x", 0.0), y=data.get("y", 0.0))

    @classmethod
    def to_list(cls, list: List[float]) -> List[Vec2]:
        if len(list) % 2 != 0:
            raise ValueError(f"List length must be even, got {len(list)}")

        result = []
        for i in range(0, len(list), 3):
            result.append(cls(x=list[i], y=list[i + 1]))
        return result


@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def splat(cls, value: float) -> Vec3:
        return cls(x=value, y=value, z=value)

    @classmethod
    def new(cls, x: float, y: float, z: float) -> Vec3:
        return cls(x=x, y=y, z=z)

    def to_dict(self) -> List[float]:
        return [self.x, self.y, self.z]

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> Vec3:
        return cls(x=data.get("x", 0.0), y=data.get("y", 0.0), z=data.get("z", 0.0))


@dataclass
class HouRect:
    size: Vec2 = field(default_factory=lambda: Vec2.splat(0.5))
    translation: Vec3 = field(default_factory=lambda: Vec3.splat(0.0))
    uv: List[Vec2] = field(default_factory=list)

    @classmethod
    def new(cls, size: Vec2, translation: Vec3, uv: List[Vec2]) -> HouRect:
        return cls(size=size, translation=translation, uv=uv)

    def __post_init__(self):
        if len(self.uv) != 4:
            raise ValueError(f"uv must have 4 elements, got {len(self.uv)}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "size": self.size.to_dict(),
            "translation": self.translation.to_dict(),
            "uv": [uv.to_dict() for uv in self.uv],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HouRect:
        size = Vec2.from_dict(data.get("size", {"x": 0.5, "y": 0.5}))
        translation = Vec3.from_dict(
            data.get("translation", {"x": 0.0, "y": 0.0, "z": 0.0})
        )
        uv = [Vec2.from_dict(uv_data) for uv_data in data.get("uv", [])]
        return cls(size=size, translation=translation, uv=uv)


@dataclass
class HouLayer:
    mesh2d: Optional[List[HouRect]] = None

    @classmethod
    def new(cls) -> "HouLayer":
        return HouLayer()

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.mesh2d is not None:
            result["mesh2d"] = [rect.to_dict() for rect in self.mesh2d]
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HouLayer:
        mesh2d = None
        if "mesh2d" in data and data["mesh2d"] is not None:
            mesh2d = [HouRect.from_dict(rect_data) for rect_data in data["mesh2d"]]
        return cls(mesh2d=mesh2d)

    def append_hou_rect(self, rect: HouRect) -> None:
        if self.mesh2d is None:
            self.mesh2d = []
        self.mesh2d.append(rect)


@dataclass
class HouData:
    layer: Dict[str, HouLayer] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer": {
                layer_name: layer.to_dict() for layer_name, layer in self.layer.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HouData:
        layers = {}
        for layer_name, layer_data in data.get("layer", {}).items():
            layers[layer_name] = HouLayer.from_dict(layer_data)
        return cls(layer=layers)

    @classmethod
    def from_json(cls, json_str: str) -> HouData:
        data = json.loads(json_str)
        return cls.from_dict(data)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def export_as_json(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def import_from_json(cls, file_path: str) -> HouData:
        with open(file_path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)
