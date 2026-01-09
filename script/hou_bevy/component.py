from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Int2:
    x: int = 0
    y: int = 0

    @classmethod
    def splat(cls, value: int) -> Int2:
        return cls(x=value, y=value)

    @classmethod
    def new(cls, x: int, y: int) -> Int2:
        return cls(x=x, y=y)

    def to_dict(self) -> List[int]:
        return [self.x, self.y]

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> Int2:
        return cls(x=data.get("x", 0), y=data.get("y", 0))

    @classmethod
    def to_list(cls, list: List[int]) -> List[Int2]:
        if len(list) % 2 != 0:
            raise ValueError(f"List length must be even, got {len(list)}")

        result = []
        for i in range(0, len(list), 3):
            result.append(cls(x=list[i], y=list[i + 1]))
        return result


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

    @classmethod
    def to_list(cls, list: List[float]) -> List[Vec3]:
        if len(list) % 2 != 0:
            raise ValueError(f"List length must be even, got {len(list)}")

        result = []
        for i in range(0, len(list), 3):
            result.append(cls(x=list[i], y=list[i + 1], z=list[i + 2]))
        return result


@dataclass
class Hou2dMesh:
    vertices: List[Vec2] = field(default_factory=lambda: [])
    normals: List[Vec3] = field(default_factory=lambda: [])
    indices: List[int] = field(default_factory=lambda: [])
    z: float = 0.0
    id: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vertices": [vert.to_dict() for vert in self.vertices],
            "indices": self.indices,
            "normals": [norm.to_dict() for norm in self.normals],
            "z": self.z,
            "id": self.id,
        }


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
    rect: Optional[List[HouRect]] = None
    mesh2d: Optional[List[Hou2dMesh]] = None

    @classmethod
    def new(cls) -> "HouLayer":
        return HouLayer()

    def append_data(self, data: Any):
        if isinstance(data, HouRect):
            self.append_rect(data)
        if isinstance(data, Hou2dMesh):
            if self.mesh2d is None:
                self.mesh2d = []
            self.mesh2d.append(data)

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.rect is not None:
            result["rect"] = [rect.to_dict() for rect in self.rect]
        if self.mesh2d is not None:
            result["mesh2d"] = [mesh2d.to_dict() for mesh2d in self.mesh2d]
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HouLayer:
        rect = None
        if "rect" in data and data["rect"] is not None:
            rect = [HouRect.from_dict(rect_data) for rect_data in data["rect"]]
        return cls(rect=rect)

    def append_rect(self, rect: HouRect) -> None:
        if self.rect is None:
            self.rect = []
        self.rect.append(rect)


@dataclass
class HouData:
    layer: Dict[str, HouLayer] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer": {
                layer_name: layer.to_dict() for layer_name, layer in self.layer.items()
            }
        }

    def create_layer(self, name: str):
        """
        Create HouLayer if not exists
        """
        if name not in self.layer.keys():
            layer = HouLayer.new()
            self.layer[name] = layer

    def get_layer(self, name: str) -> HouLayer | None:
        if name not in self.layer.keys():
            self.create_layer(name)

        return self.layer[name]

    def append_data(self, layer_name: str, data: Any):
        self.layer[layer_name].append_data(data)

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
