## Problem Description
Write a utility that takes as input the location of m commuters, n cabs and a destination location, and outputs optimised cab routes for picking up all commuters (on a shared basis) and dropping them off at the destination.

Optimisation should be on the basis of total distance travelled by the cabs i.e. the optimal set of cab routes will be the one in which the total of the distances travelled by all the cabs is the least.

Pickups will be on a shared basis i.e. commuters will need to be grouped into different routes based on their locations. It's okay to assume a common pick up point for all commuters sharing a cab. Thus, total distance travelled by a cab will be the distance from the location of the cab to the pick up point + distance from the pick up point to the destination.

Locations can be represented using cartesian co-ordinates i.e. (x, y) notation. Distance calculation can be simplified by using straight-line distance between the points. 

## Requirements
1. python >= 3.5.0
2. scipy
3. numpy
4. py.test

## Usage
`python solve.py`

## Test
`py.test`
