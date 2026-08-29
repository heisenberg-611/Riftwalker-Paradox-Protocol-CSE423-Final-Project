"""3D Mathematics, Vectors, Matrices, and Geometric Intersection Utilities."""
import math
from typing import Tuple, Optional


class Vector3:
    """3D Cartesian Vector with basic linear algebra operations."""
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> 'Vector3':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> 'Vector3':
        if scalar == 0.0:
            return Vector3(0.0, 0.0, 0.0)
        inv = 1.0 / scalar
        return Vector3(self.x * inv, self.y * inv, self.z * inv)

    def __neg__(self) -> 'Vector3':
        return Vector3(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return False
        return (math.isclose(self.x, other.x, abs_tol=1e-6) and
                math.isclose(self.y, other.y, abs_tol=1e-6) and
                math.isclose(self.z, other.z, abs_tol=1e-6))

    def __repr__(self) -> str:
        return f"Vector3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def normalized(self) -> 'Vector3':
        l = self.length()
        if l > 1e-8:
            return self / l
        return Vector3(0.0, 0.0, 0.0)

    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def distance_to(self, other: 'Vector3') -> float:
        return (self - other).length()

    def distance_squared_to(self, other: 'Vector3') -> float:
        return (self - other).length_squared()

    def lerp(self, target: 'Vector3', t: float) -> 'Vector3':
        return self + (target - self) * clamp(t, 0.0, 1.0)


class Matrix4:
    """4x4 Transformation Matrix (Column-Major for OpenGL compatibility)."""
    def __init__(self, data=None):
        if data is None:
            # Identity Matrix
            self.m = [
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
            ]
        else:
            self.m = list(data)

    @classmethod
    def translation(cls, x: float, y: float, z: float) -> 'Matrix4':
        mat = cls()
        mat.m[12] = x
        mat.m[13] = y
        mat.m[14] = z
        return mat

    @classmethod
    def scale(cls, sx: float, sy: float, sz: float) -> 'Matrix4':
        mat = cls()
        mat.m[0] = sx
        mat.m[5] = sy
        mat.m[10] = sz
        return mat


def clamp(val: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(val, max_val))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * clamp(t, 0.0, 1.0)


def ray_intersects_sphere(
    ray_origin: Vector3,
    ray_dir: Vector3,
    sphere_center: Vector3,
    radius: float
) -> Optional[float]:
    """
    Computes ray-sphere intersection distance.
    Returns distance along ray, or None if no hit.
    """
    oc = ray_origin - sphere_center
    a = ray_dir.dot(ray_dir)
    b = 2.0 * oc.dot(ray_dir)
    c = oc.dot(oc) - radius * radius
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0:
        return None
    sqrt_d = math.sqrt(discriminant)
    t0 = (-b - sqrt_d) / (2.0 * a)
    t1 = (-b + sqrt_d) / (2.0 * a)
    if t0 > 0.0:
        return t0
    if t1 > 0.0:
        return t1
    return None


def ray_intersects_aabb(
    ray_origin: Vector3,
    ray_dir: Vector3,
    box_min: Vector3,
    box_max: Vector3
) -> Optional[float]:
    """
    Slab method for Ray-AABB intersection.
    Returns distance along ray, or None if no hit.
    """
    tmin = -float('inf')
    tmax = float('inf')

    for i in ('x', 'y', 'z'):
        origin_val = getattr(ray_origin, i)
        dir_val = getattr(ray_dir, i)
        min_val = getattr(box_min, i)
        max_val = getattr(box_max, i)

        if abs(dir_val) < 1e-8:
            if origin_val < min_val or origin_val > max_val:
                return None
        else:
            t1 = (min_val - origin_val) / dir_val
            t2 = (max_val - origin_val) / dir_val
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmin > tmax:
                return None

    if tmax < 0:
        return None
    return tmin if tmin > 0 else tmax
