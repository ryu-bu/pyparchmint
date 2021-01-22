from __future__ import annotations
from parchmint.layer import Layer
from typing import List, Optional, Tuple
from parchmint.params import Params
from parchmint.target import Target


class Connection:
    def __init__(self, json=None, device_ref=None):

        self.name: Optional[str] = None
        self.ID: str = ""
        self.entity: Optional[str] = None
        self.params: Params = Params()
        self.source: Optional[Target] = None
        self.sinks: List[Target] = []
        self.layer: Layer = None

        if json:
            if device_ref is None:
                raise Exception(
                    "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
                )

            self.parse_from_json(json, device_ref)

    def parse_from_json(self, json, device_ref=None):
        if device_ref is None:
            raise Exception(
                "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
            )

        self.name = json["name"]
        self.ID = json["id"]
        self.layer = device_ref.get_layer(json["layer"])
        self.params = Params(json["params"])

        self.source = Target(json["source"])

        for target in json["sinks"]:
            self.sinks.append(Target(target))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def add_waypoints_path(
        self, source: Target, sink: Target, waypoints: List[Tuple[int, int]]
    ) -> None:
        path = Path(source, sink, waypoints)
        if self.params.exists("paths"):
            paths = self.params.get_param("paths")
            paths.append(path.to_parchmint_v1())
        else:
            self.params.set_param("paths", [path.to_parchmint_v1()])

    def to_parchmint_v1(self):
        return {
            "sinks": [s.to_parchmint_v1() for s in self.sinks],
            "name": self.name,
            "id": self.ID,
            "source": self.source.to_parchmint_v1(),
            "params": self.params.to_parchmint_v1(),
            "layer": self.layer.ID,
        }


class Path:
    def __init__(
        self, source: Target, sink: Target, waypoints: List[Tuple[int, int]] = []
    ) -> None:
        super().__init__()
        self.__source: Target = source
        self.__sink: Target = sink
        self.__waypoints: List[Tuple[int, int]] = waypoints

    def to_parchmint_v1(self):
        return {
            "source": None
            if self.__source is None
            else self.__source.to_parchmint_v1(),
            "sinks": None if self.__sink is None else self.__sink.to_parchmint_v1(),
            "wayPoints": [list(wp) for wp in self.__waypoints],
        }
