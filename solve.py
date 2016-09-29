import math
import numpy as np

from scipy.cluster.vq import kmeans, vq

class Vector:
    """
    A Vector represents a point in a 2 dimensional Cartesian Coordinate system
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @staticmethod
    def zero() -> 'Vector':
        return Vector(0, 0)

    @staticmethod
    def from_string(val: str) -> 'Vector':
        """
        returns a vector from a string in the format 'x,y'
        """
        cord = val.split(',')
        return Vector(float(cord[0]), float(cord[1]))

    def distance(self, other: 'Vector') -> float:
        """
        returns the distance between this and other
        """
        x_d = other.x - self.x
        y_d = other.y - self.y
        return math.sqrt(x_d * x_d + y_d * y_d)

    def magnitude(self) -> float:
        """
        returns the magnitude of the vector
        """
        return self.x * self.x + self.y * self.y

    def __str__(self) -> str:
        return "{0},{1}".format(self.x, self.y)

    def __eq__(self, other: 'Vector') -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: 'Vector') -> bool:
        return self.x < other.x and self.y < other.y

    def __lte__(self, other: 'Vector') -> bool:
        return self.x <= other.x and self.y <= other.y


class TestVector:
    class Data:
        def __init__(self, a: Vector, b: Vector, result: int):
            self.a = a
            self.b = b
            self.result = result

    def test_distance(self):
        datapoints = [
            self.Data(Vector(0, 0), Vector(0, 1), 1),
            self.Data(Vector(0, 0), Vector(0, 2), 2),
            self.Data(Vector(1, 2), Vector(0, 2), 1),
        ]
        for d in datapoints:
            assert d.a.distance(d.b) == d.result

    def test_from_string(self):
        assert Vector.from_string('1,2') == Vector(1, 2)
        assert Vector.from_string('3,5') == Vector(3, 5)
        assert Vector.from_string('2,5') != Vector(3, 5)

class Commuter:
    """
    A Commuter represents a person who needs a to get to a place by an means
    """

    def __init__(self, loc: Vector):
        self.location = loc

    def __str__(self) -> str:
        return "Commuter: (%d, %d)" %(self.location.x, self.location.y)

    def __eq__(self, other: 'Commuter') -> bool:
        return self.location.x == other.location.x and self.location.y == other.location.y

    def __lt__(self, other: 'Commuter') -> bool:
        return self.location.x < other.location.x and self.location.y < other.location.y

    def __lte__(self, other: 'Commuter') -> bool:
        return self.location.x <= other.location.x and self.location.y <= other.location.y

class CommuterGroup:
    """
    A CommuterGroup represents a group of commuters travelling together to
    get to the same place
    """

    def __init__(self):
        self.commuters = []
        self.cab = None
        self.centroid = Vector.zero()

    def add_commuter(self, commuter: Commuter):
        self.commuters.append(commuter)

    def remove_commuter(self, commuter: Commuter):
        self.commuters.remove(commuter)

    def set_cab(self, cab: 'Cab'):
        self.cab = cab
        self.cab.pickup_point = self.centroid

    def __eq__(self, other: 'CommuterGroup') -> bool:
        return self.centroid.x == other.centroid.x and self.centroid.y == other.centroid.y

    def __lt__(self, other: 'CommuterGroup') -> bool:
        return self.centroid.x < other.centroid.x and self.centroid.y < other.centroid.y

    def __lte__(self, other: 'CommuterGroup') -> bool:
        return self.centroid.x <= other.centroid.x and self.centroid.y <= other.centroid.y

    def __str__(self) -> str:
        return 'CommuterGroup: (%d, %d)' %(self.centroid.x, self.centroid.y)

class Cab:
    """
    A Cab represents a mode of travel that will can get a commuter from src to dest
    """

    def __init__(self, loc: Vector):
        self.location = loc
        self.pickup_point = Vector.zero()
        self.destination = Vector.zero()

    def __str__(self) -> str:
        return 'Cab: (%d, %d)' %(self.location.x, self.location.y)

    def __eq__(self, other: 'Cab') -> bool:
        return self.location.x == other.location.x and self.location.y == other.location.y

    def __lt__(self, other: 'Cab') -> bool:
        return self.location.x < other.location.x and self.location.y < other.location.y

    def __lte__(self, other: 'Cab') -> bool:
        return self.location.x <= other.location.x and self.location.y <= other.location.y

def create_groups(commuters, no_of_cabs):
    """
    Takes a list of Commuter and the no of cabs available and partitions accordingly
    using kMeans clustering algorithm and returns a list of groups
    """
    data = np.array([[c.location.x, c.location.y] for c in commuters])
    centroids, _ = kmeans(data, no_of_cabs)
    idx, _ = vq(data, centroids)
    group_dict = {}
    for i, v in enumerate(idx):
        if v not in group_dict:
            group_dict[v] = CommuterGroup()
            group_dict[v].centroid = Vector(centroids[v][0], centroids[v][1])
        group_dict[v].add_commuter(commuters[i])
    return [v for v in group_dict.values()]

def assign_cab(groups, cabs):
    """
    Takes a list of groups and cabs and assigns the nearest cab to a group to
    that group
    """
    for cab in cabs:
        current_group = groups[0]
        previous_dist = cab.location.distance(current_group.centroid)
        for g in groups:
            if cab.location.distance(g.centroid) < previous_dist:
                current_group = g
        groups.remove(current_group)
        current_group.set_cab(cab)
        print(current_group)
        print(cab)

def read_vectors_from_file(name):
    vectors = []
    with open(name, "r") as input:
        lines = input.readlines()
        for line in lines:
            cord = line.rstrip('\n')
            vectors.append(Vector.from_string(cord))
    return vectors

def main():
    commuters = [Commuter(v) for v in read_vectors_from_file("commuters.txt")]
    cabs = [Cab(v) for v in read_vectors_from_file("cabs.txt")]
    groups = create_groups(commuters, len(cabs))
    assign_cab(groups, cabs)
    total_dist = 0.0
    for c in cabs:
        total_dist += c.location.distance(c.pickup_point)
    print("Total Distance Travelled: %d" %total_dist)

if __name__ == "__main__":
    main()

