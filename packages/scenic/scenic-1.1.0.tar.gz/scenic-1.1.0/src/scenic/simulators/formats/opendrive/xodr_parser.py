"""Parser for OpenDRIVE (.xodr) files."""

import math
import xml.etree.ElementTree as ET
import numpy as np
from scipy.integrate import quad
from scipy.integrate import odeint
from pynverse import inversefunc
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection, Point, MultiPoint
from shapely.ops import unary_union, snap
import abc

# Lane types on which cars can appear.
DRIVABLE = [
    'driving',
    'entry',
    'exit',
    'offRamp',
    'onRamp'
]

# Lane types representing sidewalks.
SIDEWALK = ['sidewalk']

def buffer_union(polygons, buf=0.1):
    return unary_union([p.buffer(buf) for p in polygons]).buffer(-buf)

class Poly3:
    '''Cubic polynomial.'''
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def eval_at(self, x):
        return self.a + self.b * x + self.c * x ** 2 + self.d * x ** 3

    def grad_at(self, x):
        return self.b + 2 * self.c * x + 3 * self.d * x ** 2


class Curve:
    ''' Geometric elements which compose road reference lines.
    See the OpenDRIVE Format Specification for coordinate system details.'''
    def __init__(self, x0, y0, hdg, length):
        self.x0 = x0
        self.y0 = y0
        self.hdg = hdg    # In radians counterclockwise, 0 at positive x-axis.
        self.length = length

    @abc.abstractmethod
    def to_points(self, num):
        '''Sample NUM evenly-spaced points from curve.
        Points are tuples of (x, y, s) with (x, y) absolute coordinates
        and s the arc length along the curve.'''
        return

    def rel_to_abs(self, points):
        '''Convert from relative coordinates of curve to absolute coordinates.
        I.e. rotate counterclockwise by self.hdg and translate by (x0, x1).'''
        def translate(p):
            return (p[0] + self.x0, p[1] + self.y0, p[2])

        def rotate(p):
            return (np.cos(self.hdg) * p[0] - np.sin(self.hdg) * p[1],
                    np.sin(self.hdg) * p[0] + np.cos(self.hdg) * p[1],
                    p[2])

        return [translate(rotate(p)) for p in points]


class Cubic(Curve):
    '''A curve defined by the cubic polynomial a + bu + cu^2 + du^3.
    The curve starts at (X0, Y0) in direction HDG, with length LENGTH.'''
    def __init__(self, x0, y0, hdg, length, a, b, c, d):
        super().__init__(x0, y0, hdg, length)
        self.poly = Poly3(a, b, c, d)

    def to_points(self, num):
        def arclength(s):
            d_arc = lambda x: np.sqrt(1 + self.poly.grad_at(x) ** 2)
            return quad(d_arc, 0, s)[0]

        s1 = inversefunc(arclength, self.length).tolist()
        points = [(s, self.poly.eval_at(s), arclength(s)) for s in np.linspace(0, s1, num=num)]
        return self.rel_to_abs(points)


class ParamCubic(Curve):
    ''' A curve defined by the parametric equations
    u = a_u + b_up + c_up^2 + d_up^3,
    v = a_v + b_vp + c_vp^2 + d_up^3,
    with p in [0, p_range].
    The curve starts at (X0, Y0) in direction HDG, with length LENGTH.'''
    def __init__(self, x0, y0, hdg, length,
                 au, bu, cu, du, av, bv, cv, dv, p_range=1):
        super().__init__(x0, y0, hdg, length)
        self.u_poly = Poly3(au, bu, cu, du)
        self.v_poly = Poly3(av, bv, cv, dv)
        self.p_range = p_range if p_range else 1

    def to_points(self, num):
        def eval_poly(s):
            return (self.u_poly.eval_at(s), self.v_poly.eval_at(s))

        def arclength(s):
            d_arc = lambda x: np.sqrt(self.u_poly.grad_at(s) ** 2
                                      + self.v_poly.grad_at(s))
            return quad(d_arc, 0, s)[0]

        points = [eval_poly(s) + (arclength(s),) for s in np.linspace(0, self.p_range, num=num)]
        return self.rel_to_abs(points)


class Clothoid(Curve):
    '''An Euler spiral with curvature varying linearly between CURV0 and CURV1.
    The spiral starts at (X0, Y0) in direction HDG, with length LENGTH.'''
    def __init__(self, x0, y0, hdg, length, curv0, curv1):
        super().__init__(x0, y0, hdg, length)
        # Initial and final curvature.
        self.curv0 = curv0
        self.curv1 = curv1

    def to_points(self, num):
        # Generate a origin-centered clothoid with zero curvature at origin,
        # then translate/rotate the relevant segment.
        # Arcs are just a degenerate clothiod:
        if self.curv0 == self.curv1:
            r = 1 / abs(self.curv0)
            theta = self.length / r
            th_space = np.linspace(0, theta, num=num)
            if self.curv0 == 0:
                points = [(x, 0, x) for x in np.linspace(0, self.length, num=num)]
            elif self.curv0 > 0:
                points = [(r * np.sin(th), r - r * np.cos(th), r * th) for th in th_space]
            else:
                points = [(r * np.sin(th), -r + r * np.cos(th), r * th) for th in th_space]
            return self.rel_to_abs(points)

        else:
            curve_rate = (self.curv1 - self.curv0) / self.length
            def clothoid_ode(state, s):
                x, y, theta = state[0], state[1], state[2]
                return np.array([np.cos(theta), np.sin(theta), self.curv0 + curve_rate * s])

            s_space = np.linspace(0, self.length, num)
            points = odeint(clothoid_ode, np.array([self.x0,self.y0,self.hdg]), s_space)
            return [(points[i,0], points[i,1], s_space[i]) for i in range(len(s_space))]


class Line(Curve):
    '''A line segment between (x0, y0) and (x1, y1).'''
    def __init__(self, x0, y0, hdg, length):
        super().__init__(x0, y0, hdg, length)
        # Endpoints of line.
        self.x1 = x0 + length * math.cos(hdg)
        self.y1 = y0 + length * math.sin(hdg)

    def to_points(self, num=10):
        x = np.linspace(self.x0, self.x1, num=num)
        y = np.linspace(self.y0, self.y1, num=num)
        s = [np.sqrt((x[i] - self.x0) **2 + (y[i] - self.y0) ** 2)
             for i in range(num)]
        return  list(zip(x, y, s))


class Lane():
    def __init__(self, id_, type_, pred=None, succ=None):
        self.id_ = id_
        self.width = []    # List of tuples (Poly3, int) for width and s-offset.
        self.type_ = type_
        self.pred = pred
        self.succ = succ

    def width_at(self, s):
        # S here is relative to start of LaneSection this lane is in.
        ind = 0
        while ind + 1 < len(self.width) and self.width[ind + 1][1] <= s:
            ind += 1
        assert self.width[ind][1] <= s, 'No matching width entry found.'
        w_poly, s_off = self.width[ind]
        assert(w_poly.eval_at(s - s_off) >= 0), 'Negative width!'
        return w_poly.eval_at(s - s_off)


class LaneSection():
    def __init__(self, s0, left_lanes={}, right_lanes={}):
        self.s0 = s0
        self.left_lanes = left_lanes
        self.right_lanes = right_lanes
        self.lanes = dict(list(left_lanes.items()) + list(right_lanes.items()))

    def get_lane(self, id_):
        if id_ in self.left_lanes:
            return self.left_lanes[id_]
        elif id_ in self.right_lanes:
            return self.right_lanes[id_]
        elif id_ == 0:
            return Lane(0, 'none')
        else:
            raise RuntimeError('Lane with id', id_, 'not found')

    def get_offsets(self, s):
        '''Returns dict of lane id and offset from
        reference line of lane boundary at coordinate S along line.
        By convention, left lanes have positive width offset and right lanes
        have negative.'''
        assert s >= self.s0, 'Input s is before lane start position.'
        offsets = {}
        left_lane_ids = sorted(self.left_lanes.keys())
        right_lane_ids = sorted(self.right_lanes.keys(), reverse=True)
        for lane_id in left_lane_ids:
            if lane_id - 1 in left_lane_ids:
                offsets[lane_id] = offsets[lane_id - 1] \
                    + self.left_lanes[lane_id].width_at(s - self.s0)
            else:
                offsets[lane_id] = self.left_lanes[lane_id].width_at(s - self.s0)
        for lane_id in right_lane_ids:
            if lane_id + 1 in right_lane_ids:
                offsets[lane_id] = offsets[lane_id + 1] \
                    - self.right_lanes[lane_id].width_at(s - self.s0)
            else:
                offsets[lane_id] = -self.right_lanes[lane_id].width_at(s - self.s0)
        return offsets


class RoadLink:
    '''Indicates Roads a and b, with ids id_a and id_b respectively, are connected.'''
    def __init__(self, id_a, id_b, contact_a, contact_b):
        self.id_a = id_a
        self.id_b = id_b
        # contact_a and contact_b should be of value "start" or "end"
        # and indicate which end of each road is connected to the other.
        self.contact_a = contact_a
        self.contact_b = contact_b


class Junction:
    class Connection:
        def __init__(self, incoming_id, connecting_id, connecting_contact):
            self.incoming_id = incoming_id
            # id of connecting road
            self.connecting_id = connecting_id
            # contact point ('start' or 'end') on connecting road
            self.connecting_contact = connecting_contact

    def __init__(self, id_):
        self.id_ = id_
        self.connections = []
        # Ids of roads that are paths within junction:
        self.paths = []

    def add_connection(self, incoming_id, connecting_id, connecting_contact):
        self.connections.append(Junction.Connection(incoming_id,
                                                    connecting_id,
                                                    connecting_contact))


class Road:
    def __init__(self, name, id_, length, drive_on_right=True):
        self.name = name
        self.id_ = id_
        self.length = length
        self.lane_secs = []    # List of LaneSection objects.
        self.ref_line = []    # List of Curve objects defining reference line.
        # NOTE: sec_points, sec_polys, sec_lane_polys should be ordered according to lane_secs.
        self.sec_points = []   # List of lists of points, one for each LaneSection.
        self.sec_polys = []   # List of Polygons, one for each LaneSections.
        self.sec_lane_polys = []    # List of dict of lane id to Polygon for each LaneSection.
        self.lane_polys = []    # List of lane polygons. Not a dict b/c lane id is not unique along road.
        # Each polygon in lane_polys is the union of connected lane section polygons.
        # lane_polys is currently not used.
        # Reference line offset:
        self.offset = []    # List of tuple (Poly3, s-coordinate).
        self.drive_on_right = drive_on_right
        # Used to fill in gaps between roads:
        self.start_bounds_left = {}
        self.start_bounds_right = {}
        self.end_bounds_left = {}
        self.end_bounds_right = {}

    def get_lane(self, id_, s):
        '''Returns Lane object with id_ at coordinate S along line.'''
        ind = 0
        while ind + 1 < len(self.lane_secs) and self.lane_secs[ind + 1].s0 <= s:
            ind += 1
        assert self.lane_secs[ind].s0 <= s, 'No matching lane section found.'
        return self.lane_secs[ind].get_lane(id_)

    def get_ref_line_offset(self, s):
        if not self.offset:
            return 0
        ind = 0
        while ind + 1 < len(self.offset) and self.offset[ind + 1][1] < s:
            ind += 1
        return self.offset[ind][0].eval_at(s)

    def get_ref_points(self, num):
        '''Returns list of list of points for each piece of ref_line.
        List of list structure necessary because each piece needs to be
        constructed into Polygon separately then unioned afterwards to avoid
        self-intersecting lines.'''
        ref_points = []
        for piece in self.ref_line:
            piece_points = piece.to_points(num)
            assert piece_points, 'Failed to get piece points'
            if ref_points:
                piece_points = [(p[0], p[1], p[2] + ref_points[-1][-1][2])
                                for p in piece_points]
            ref_points.append(piece_points)
        return ref_points

    def get_lane_offsets(self, s):
        '''Returns dict of lane id and offset from
        reference line of lane boundary at coordinate S along line.'''
        s = float(s)
        ind = 0
        while ind + 1 < len(self.lane_secs) and self.lane_secs[ind + 1].s0 <= s:
            ind += 1
        assert self.lane_secs[ind].s0 <= s, 'No matching lane section found.'
        offsets = self.lane_secs[ind].get_offsets(s)
        offsets[0] = 0    # Center lane has width 0 by convention.
        for id_ in offsets.keys():
            offsets[id_] += self.get_ref_line_offset(s)
        return offsets

    def heading_at(self, point):
        # Convert point to shapely Point.
        point = Point(point.x, point.y)
        for i in range(len(self.lane_secs)):
            ref_points = self.sec_points[i]
            poly = self.sec_polys[i]
            if point.within(poly.buffer(1)):
                lane_id = None
                for id_ in self.sec_lane_polys[i].keys():
                    if point.within(self.sec_lane_polys[i][id_].buffer(1)):
                        lane_id = id_
                        break
                assert lane_id is not None, 'Point not found in sec_lane_polys.'
                min_dist = float('inf')
                for i in range(len(ref_points)):
                    cur_point = Point(ref_points[i][0], ref_points[i][1])
                    if point.distance(cur_point) < min_dist:
                        closest_idx = i
                if closest_idx >= len(ref_points) - 1:
                   closest_idx = len(ref_points) - 2
                dy = ref_points[closest_idx + 1][1] - ref_points[closest_idx][1]
                dx = ref_points[closest_idx + 1][0] - ref_points[closest_idx][0]
                heading = math.atan2(dy, dx)
                # Right lanes have negative lane_id.
                # Flip heading if drive_on_right XOR right lane.
                if self.drive_on_right != (lane_id < 0):
                    heading += math.pi
                # Heading 0 is defined differently between OpenDrive and Scenic(?)
                heading -= math.pi / 2
                return (heading + math.pi) % (2 * math.pi) - math.pi

        raise RuntimeError('Point not found in piece_polys')

    def calc_geometry_for_type(self, lane_types, num, calc_gap=False):
        '''Given a list of lane types, returns a tuple of:
        - List of lists of points along the reference line, with same indexing as self.lane_secs
        - List of region polygons, with same indexing as self.lane_secs
        - List of dictionary of lane id to polygon, with same indexing as self.lane_secs
        - List of polygons for each lane (not necessarily by id, but respecting lane successor/predecessor)
        - Polygon for entire region.
        If calc_gap=True, fills in gaps between connected roads. This is fairly expensive.'''
        road_polygons = []
        ref_points = self.get_ref_points(num)
        cur_lane_polys = {}
        sec_points = []
        sec_polys = []
        sec_lane_polys = []
        lane_polys = []
        last_lefts = None
        last_rights = None

        for i in range(len(self.lane_secs)):
            cur_sec = self.lane_secs[i]
            cur_sec_points = []
            if i < len(self.lane_secs) - 1:
                next_sec = self.lane_secs[i + 1]
                s_stop = next_sec.s0
            else:
                s_stop = float('inf')
            left_bounds = {}
            right_bounds = {}
            cur_sec_lane_polys = {}
            cur_sec_polys = []
            # Last point in left/right lane boundary line for last road piece:
            start_of_sec = True
            end_of_sec = False

            while ref_points and not end_of_sec:
                if not ref_points[0] or ref_points[0][0][2] >= s_stop:
                    # Case 1: The current list of ref_points (corresponding to current piece)
                    # is empty, so we move onto the next list of points.
                    # Case 2: The s-coordinate has exceeded s_stop, so we should move
                    # onto the next LaneSection.
                    # Either way, we collect all the bound points so far into polygons.
                    if not ref_points[0]:
                        ref_points.pop(0)
                    else:
                       end_of_sec = True
                    cur_last_lefts = {}
                    cur_last_rights = {}
                    for id_ in left_bounds.keys():
                        # Polygon for piece of lane:
                        bounds = left_bounds[id_] + right_bounds[id_][::-1]
                        if len(bounds) < 3:
                            continue
                        poly = Polygon(bounds).buffer(0)
                        if poly.is_valid and not poly.is_empty:
                            if poly.geom_type == 'MultiPolygon':
                                poly = MultiPolygon([p for p in list(poly)
                                                     if not p.is_empty and p.exterior])
                                cur_sec_polys.extend(list(poly))
                            else:
                                cur_sec_polys.append(poly)
                            if id_ in cur_sec_lane_polys:
                                cur_sec_lane_polys[id_].append(poly)
                            else:
                                cur_sec_lane_polys[id_] = [poly]
                        if calc_gap:
                            # Polygon for gap between lanes:
                            if start_of_sec:
                                prev_id = cur_sec.lanes[id_].pred
                            else:
                                prev_id = id_
                            if last_lefts is not None and prev_id in last_lefts.keys():
                                gap_poly = MultiPoint([
                                    last_lefts[prev_id], last_rights[prev_id],
                                    left_bounds[id_][0], right_bounds[id_][0]]).convex_hull
                                assert gap_poly.is_valid, 'Gap polygon not valid.'
                                # Assume MultiPolygon cannot result from convex hull.
                                if gap_poly.geom_type == 'Polygon' and not gap_poly.is_empty:
                                    # plot_poly(gap_poly, 'b')
                                    gap_poly = gap_poly.buffer(0)
                                    cur_sec_polys.append(gap_poly)
                                    if id_ in cur_sec_lane_polys:
                                        cur_sec_lane_polys[id_].append(gap_poly)
                                    else:
                                        cur_sec_lane_polys[id_] = [gap_poly]
                        cur_last_lefts[id_] = left_bounds[id_][-1]
                        cur_last_rights[id_] = right_bounds[id_][-1]
                        if (start_of_sec and i == 0) or not self.start_bounds_left:
                            self.start_bounds_left[id_] = left_bounds[id_][0]
                            self.start_bounds_right[id_] = right_bounds[id_][0]

                    left_bounds = {}
                    right_bounds = {}
                    if cur_last_lefts and cur_last_rights:
                        last_lefts = cur_last_lefts
                        last_rights = cur_last_rights
                        start_of_sec = False
                else:
                    cur_p = ref_points[0].pop(0)
                    cur_sec_points.append(cur_p)
                    offsets = cur_sec.get_offsets(cur_p[2])
                    offsets[0] = 0
                    for id_ in offsets.keys():
                        offsets[id_] += self.get_ref_line_offset(cur_p[2])
                    if ref_points[0]:
                        next_p = ref_points[0][0]
                        tan_vec = (next_p[0] - cur_p[0],
                                   next_p[1] - cur_p[1])
                    else:
                        if len(cur_sec_points) >= 2:
                            prev_p = cur_sec_points[-2]
                        else:
                            assert len(sec_points) > 0
                            if sec_points[-1]:
                                prev_p = sec_points[-1][-1]
                            else:
                                prev_p = sec_points[-2][-1]

                        tan_vec = (cur_p[0] - prev_p[0],
                                   cur_p[1] - prev_p[1])
                    tan_norm = np.sqrt(tan_vec[0] ** 2 + tan_vec[1] ** 2)
                    # if tan_norm < 0.01:
                    #     continue
                    normal_vec = (-tan_vec[1] / tan_norm, tan_vec[0] / tan_norm)
                    for id_ in offsets.keys():
                        if cur_sec.get_lane(id_).type_ in lane_types:
                            if id_ > 0:
                                prev_id = id_ - 1
                            else:
                                prev_id = id_ + 1
                            left_bound = [cur_p[0] + normal_vec[0] * offsets[id_],
                                          cur_p[1] + normal_vec[1] * offsets[id_]]
                            right_bound = [cur_p[0] + normal_vec[0] * offsets[prev_id],
                                           cur_p[1] + normal_vec[1] * offsets[prev_id]]
                            if id_ not in left_bounds:
                                left_bounds[id_] = [left_bound]
                            else:
                                left_bounds[id_].append(left_bound)
                            if id_ not in right_bounds:
                                right_bounds[id_] = [right_bound]
                            else:
                                right_bounds[id_].append(right_bound)
            sec_points.append(cur_sec_points)
            sec_polys.append(buffer_union(cur_sec_polys))
            for id_ in cur_sec_lane_polys:
                cur_sec_lane_polys[id_] = buffer_union(cur_sec_lane_polys[id_])
            sec_lane_polys.append(cur_sec_lane_polys)
            next_lane_polys = {}
            for id_ in cur_sec_lane_polys:
                pred_id = cur_sec.get_lane(id_).pred
                if pred_id and pred_id in cur_lane_polys:
                    next_lane_polys[id_] = cur_lane_polys.pop(pred_id) \
                        + [cur_sec_lane_polys[id_]]
                else:
                    next_lane_polys[id_] = [cur_sec_lane_polys[id_]]
            for id_ in cur_lane_polys:
                lane_polys.append(buffer_union(cur_lane_polys[id_]))
            cur_lane_polys = next_lane_polys
        for id_ in cur_lane_polys:
            lane_polys.append(buffer_union(cur_lane_polys[id_]))
        union_poly = buffer_union(sec_polys)
        if last_lefts and last_rights:
            self.end_bounds_left.update(last_lefts)
            self.end_bounds_right.update(last_rights)
        return sec_points, sec_polys, sec_lane_polys, lane_polys, union_poly

    def calculate_geometry(self, num, calc_gap=False):
        # Note: this also calculates self.start_bounds_left, ,self.start_bounds_right,
        # self.end_bounds_left, self.end_bounds_right
        self.sec_points,\
            self.sec_polys,\
            self.sec_lane_polys,\
            self.lane_polys,\
            self.drivable_region =\
                self.calc_geometry_for_type(DRIVABLE, num, calc_gap=calc_gap)
        _, _, _, _, self.sidewalk_region = self.calc_geometry_for_type(SIDEWALK, num, calc_gap=calc_gap)

class RoadMap:
    def __init__(self):
        self.roads = {}
        self.road_links = []
        self.junctions = {}
        self.sec_lane_polys = []
        self.lane_polys = []
        self.intersection_region = None

    def calculate_geometry(self, num, calc_gap=False, calc_intersect=False):
        # If calc_gap=True, fills in gaps between connected roads.
        # If calc_intersect=True, calculates intersection regions.
        # These are fairly expensive.
        for road in self.roads.values():
            road.calculate_geometry(num, calc_gap=calc_gap)
        drivable_polys = {}
        sidewalk_polys = {}
        drivable_gap_polys = []
        sidewalk_gap_polys = []
        for road in self.roads.values():
            self.sec_lane_polys.extend(road.sec_lane_polys)
            self.lane_polys.extend(road.lane_polys)
            drivable_poly = road.drivable_region
            sidewalk_poly = road.sidewalk_region
            if not (drivable_poly is None or drivable_poly.is_empty):
                drivable_polys[road.id_] = drivable_poly.buffer(0.001)
            if not (sidewalk_poly is None or sidewalk_poly.is_empty):
                sidewalk_polys[road.id_] = sidewalk_poly.buffer(0.001)

        for link in self.road_links:
            road_a = self.roads[link.id_a]
            road_b = self.roads[link.id_b]
            assert link.contact_a in ['start', 'end'], 'Invalid link record.'
            assert link.contact_b in ['start', 'end'], 'Invalid link record.'
            if link.contact_a == 'start':
                a_sec = road_a.lane_secs[0]
                a_bounds_left = road_a.start_bounds_left
                a_bounds_right = road_a.start_bounds_right
            else:
                a_sec = road_a.lane_secs[-1]
                a_bounds_left = road_a.end_bounds_left
                a_bounds_right = road_a.end_bounds_right
            if link.contact_b == 'start':
                b_bounds_left = road_b.start_bounds_left
                b_bounds_right = road_b.start_bounds_right
            else:
                b_bounds_left = road_b.end_bounds_left
                b_bounds_right = road_b.end_bounds_right
            for id_, lane in a_sec.lanes.items():
                if link.contact_a == 'start':
                    other_id = lane.pred
                else:
                    other_id = lane.succ
                if other_id not in b_bounds_left or other_id not in b_bounds_right:
                    continue
                if id_ not in a_bounds_left or id_ not in a_bounds_right:
                    continue
                if calc_gap:
                    gap_poly = MultiPoint([
                        a_bounds_left[id_], a_bounds_right[id_],
                        b_bounds_left[other_id], b_bounds_right[other_id]
                    ]).convex_hull
                    if not gap_poly.is_valid:
                        continue
                    # assert gap_poly.is_valid, 'Gap polygon not valid.'
                    if gap_poly.geom_type == 'Polygon' and not gap_poly.is_empty:
                        if lane.type_ in DRIVABLE:
                            drivable_gap_polys.append(gap_poly)
                            # plot_poly(gap_poly, 'g')
                        elif lane.type_ in SIDEWALK:
                            sidewalk_gap_polys.append(gap_poly)
                            # plot_poly(gap_poly, 'k')

        self.drivable_region = buffer_union(list(drivable_polys.values()) + drivable_gap_polys)
        self.sidewalk_region = buffer_union(list(sidewalk_polys.values()) + sidewalk_gap_polys)
        self.calculate_intersections()

    def calculate_intersections(self):
        intersect_polys = []
        for junc in self.junctions.values():
            junc_roads = set()
            for conn in junc.connections:
               junc_roads.add(conn.incoming_id)
               junc_roads.add(conn.connecting_id)
            for road_i_idx in junc_roads:
                if road_i_idx in junc.paths:
                    road_i = self.roads[road_i_idx]
                    intersect_polys.append(road_i.drivable_region)
                    continue
                for road_j_idx in junc_roads:
                    if road_i_idx == road_j_idx:
                        continue
                    road_i = self.roads[road_i_idx]
                    road_j = self.roads[road_j_idx]
                    intersect_polys.append(
                        road_i.drivable_region.intersection(road_j.drivable_region))
        self.intersection_region = buffer_union(intersect_polys)

    def heading_at(self, point):
        '''Return the road heading at point.'''
        # Convert point to shapely Point.
        point = Point(point.x, point.y)
        for road in self.roads.values():
            if point.within(road.drivable_region.buffer(1)):
                return road.heading_at(point)
        #raise RuntimeError('Point not in RoadMap: ', point)
        return 0

    def plot_line(self, plt, num=500):
        '''Plot center line of road map for sanity check.'''
        for road in self.roads.values():
            for piece in road.ref_line:
                points = piece.to_points(num)
                x = [p[0] for p in points]
                y = [p[1] for p in points]
                plt.plot(x, y, 'b')
        plt.show()

    def plot_lanes(self, plt, num=500):
        '''Plot lane boundaries of road map for sanity check.'''
        bounds_x =[]
        bounds_y = []
        for road in self.roads.values():
            for piece in road.ref_line:
                ref_points = piece.to_points(num)
                for i in range(len(ref_points) - 1):
                    offsets = road.get_lane_offsets(ref_points[i][2])
                    tan_vec = (ref_points[i + 1][0] - ref_points[i][0],
                               ref_points[i + 1][1] - ref_points[i][1])
                    tan_norm = np.sqrt(tan_vec[0] ** 2 + tan_vec[1] ** 2)
                    normal_vec = (-tan_vec[1] / tan_norm, tan_vec[0] / tan_norm)
                    # ortho_line_x = []
                    # ortho_line_y = []
                    for id_ in offsets.keys():
                        if road.get_lane(id_, ref_points[i][2]).type_ == 'driving':
                            bounds_x.append(ref_points[i][0] + normal_vec[0] * offsets[id_])
                            bounds_y.append(ref_points[i][1] + normal_vec[1] * offsets[id_])
        plt.scatter(bounds_x, bounds_y, c='r', s=2)
        plt.show()

    def __parse_lanes(self, lanes_elem):
        '''Lanes_elem should be <left> or <right> element.
        Returns dict of lane ids and Lane objects.'''
        lanes = {}
        for l in lanes_elem.iter('lane'):
            id_ = int(l.get('id'))
            type_ = l.get('type')
            link = l.find('link')
            pred = None
            succ = None
            if link is not None:
                pred_elem = link.find('predecessor')
                succ_elem = link.find('successor')
                if pred_elem is not None:
                    pred = int(pred_elem.get('id'))
                if succ_elem is not None:
                    succ = int(succ_elem.get('id'))
            lane = Lane(id_, type_, pred, succ)
            for w in l.iter('width'):
                w_poly = Poly3(float(w.get('a')),
                               float(w.get('b')),
                               float(w.get('c')),
                               float(w.get('d')))
                lane.width.append((w_poly, float(w.get('sOffset'))))
            lanes[id_] = lane
        return lanes

    def __parse_link(self, link_elem, road_id, contact):
        if link_elem is None:
            return
        if link_elem.get('elementType') == 'road':
            self.road_links.append(RoadLink(road_id,
                                            int(link_elem.get('elementId')),
                                            contact,
                                            link_elem.get('contactPoint')))
        else:
            assert link_elem.get('elementType') == 'junction', 'Unknown link type'
            junction = int(link_elem.get('elementId'))
            connections = self.junctions[junction].connections
            for c in connections:
                if c.incoming_id == road_id:
                    self.road_links.append(RoadLink(road_id,
                                                    c.connecting_id,
                                                    contact,
                                                    c.connecting_contact))


    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        if root.tag != 'OpenDRIVE':
            raise RuntimeError(f'{path} does not appear to be an OpenDRIVE file')

        for j in root.iter('junction'):
            junction = Junction(int(j.get('id')))
            for c in j.iter('connection'):
                junction.add_connection(int(c.get('incomingRoad')),
                                        int(c.get('connectingRoad')),
                                        c.get('contactPoint'))
                junction.paths.append(int(c.get('connectingRoad')))
            self.junctions[junction.id_] = junction

        for r in root.iter('road'):
            link = r.find('link')
            if link is not None:
                pred_elem = link.find('predecessor')
                succ_elem = link.find('successor')
                self.__parse_link(pred_elem, int(r.get('id')), 'start')
                self.__parse_link(succ_elem, int(r.get('id')), 'end')
            road = Road(r.get('name'), int(r.get('id')), float(r.get('length')))

            # Parse planView:
            plan_view = r.find('planView')
            for geom in plan_view.iter('geometry'):
                x0 = float(geom.get('x'))
                y0 = float(geom.get('y'))
                s0 = float(geom.get('s'))
                hdg = float(geom.get('hdg'))
                length = float(geom.get('length'))
                curve_elem = geom[0]
                curve = None
                if curve_elem.tag == 'line':
                    curve = Line(x0, y0, hdg, length)
                elif curve_elem.tag == 'arc':
                    # Arc is clothoid of constant curvature.
                    curv = float(curve_elem.get('curvature'))
                    curve = Clothoid(x0, y0, hdg, length, curv, curv)
                elif curve_elem.tag == 'spiral':
                    curv0 = float(curve_elem.get('curvStart'))
                    curv1 = float(curve_elem.get('curvEnd'))
                    curve = Clothoid(x0, y0, hdg, length, curv0, curv1)
                elif curve_elem.tag == 'poly3':
                    a, b, c, d = cubic_elem.get('a'), \
                        float(curve_elem.get('b')), \
                        float(curve_elem.get('c')), \
                        float(curve_elem.get('d'))
                    curve = Cubic(x0, y0, hdg, length, a, b, c, d)
                elif curve_elem.tag == 'paramPoly3':
                    au, bu, cu, du, av, bv, cv, dv, p_range = \
                        float(curve_elem.get('aU')), \
                        float(curve_elem.get('bU')), \
                        float(curve_elem.get('cU')), \
                        float(curve_elem.get('dU')), \
                        float(curve_elem.get('aV')), \
                        float(curve_elem.get('bV')), \
                        float(curve_elem.get('cV')), \
                        float(curve_elem.get('dV')), \
                        float(curve_elem.get('pRange'))
                    curve = ParamCubic(x0, y0, hdg, length,
                                       au, bu, cu, du, av, bv,
                                       cv, dv, p_range)
                road.ref_line.append(curve)

            # Parse lanes:
            lanes = r.find('lanes')
            for offset in lanes.iter('laneOffset'):
                road.offset.append((Poly3(float(offset.get('a')),
                                         float(offset.get('b')),
                                         float(offset.get('c')),
                                         float(offset.get('d'))),
                                   float(offset.get('s'))))

            for ls_elem in lanes.iter('laneSection'):
                s = ls_elem.get('s')
                left = ls_elem.find('left')
                right = ls_elem.find('right')
                left_lanes = {}
                right_lanes = {}

                if left is not None:
                    left_lanes = self.__parse_lanes(left)

                if right is not None:
                    right_lanes = self.__parse_lanes(right)

                lane_sec = LaneSection(float(ls_elem.get('s')), left_lanes, right_lanes)
                road.lane_secs.append(lane_sec)
            self.roads[road.id_] = road
