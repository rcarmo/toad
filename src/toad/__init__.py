from typing import Literal
import platform

type OS = Literal["linux", "macos", "windows", "unknown"]

_system = platform.system()
_OS_map: dict[str, OS] = {
    "Linux": "linux",
    "Darwin": "macos",
    "Windows": "windows",
}
os: OS = _OS_map.get(_system, "unknown")
