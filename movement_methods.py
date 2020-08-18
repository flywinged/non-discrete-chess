from math import cos, acos, sin, asin, tan, atan2, pi

def get_piece_type(data, piece):
   return data.player_piece_types[piece[0]][data.piece_type_hash[piece[0]][piece[1]]]

# Creates arcs
# Needs to consider collisions with the walls
# Consider if the piece can "jump" or is sliding
def create_arc(start, end, start_direction = None, end_direction = None):
   v = (end[0] - start[0], end[1] - start[1])
   v_mag = (v[0]**2 + v[1]**2)**(1/2)
   v = (v[0] / v_mag, v[1] / v_mag)
   
   try:
      v_angle = atan2(v[1], v[0]) % (2 * pi)
   except:
      if v[1] > 0:
         v_angle = pi / 2
      else:
         v_angle = 3 * pi / 2

   if start_direction != None and end_direction == None:
      d_mag = (start_direction[0]**2 + start_direction[1]**2)**(1/2)
      d_start = (start_direction[0] / d_mag, start_direction[1] / d_mag)
      d_angle = atan2(d_start[1], d_start[0]) % (2 * pi)
      angle_difference = (d_angle - v_angle) % (2 * pi)
      a_end = (v_angle - angle_difference) % (2 * pi)
      d_end = (cos(a_end), sin(a_end))
   elif end_direction != None and start_direction == None:
      d_mag = (end_direction[0]**2 + end_direction[1]**2)**(1/2)
      d_end = (end_direction[0] / d_mag, end_direction[1] / d_mag)
      d_angle = atan2(d_end[1], d_end[0]) % (2 * pi)
      angle_difference = (d_angle - v_angle) % (2 * pi)
      a_start = (v_angle - angle_difference) % (2 * pi)
      d_start = (cos(a_start), sin(a_start))
   else:
      assert(False)

   radius = (v_mag / 2) / abs(sin(angle_difference))
   epsilon = 1e-12
   
   r_direction = (d_start[1], -d_start[0])
   r = (start[0] + r_direction[0] * radius, start[1] + r_direction[1] * radius)
   v_to_start = (start[0] - r[0], start[1] - r[1])
   v_to_end   = (end[0]   - r[0], end[1]   - r[1])

   other = False
   clockwise = True
   for v in [v_to_start, v_to_end]:
      mag = (v[0]**2 + v[1]**2)**(1/2)
      if abs(mag - radius) > epsilon:
         other = True
         break

   if other:
      clockwise = False
      r_direction = (-d_start[1], d_start[0])
      r = (start[0] + r_direction[0] * radius, start[1] + r_direction[1] * radius)
      v_to_start = (start[0] - r[0], start[1] - r[1])
      v_to_end   = (end[0]   - r[0], end[1]   - r[1])

   theta_start = atan2(v_to_start[1], v_to_start[0]) % (2 * pi)
   theta_end   = atan2(v_to_end[1], v_to_end[0]) % (2 * pi)

   return [0, r, radius, theta_start, theta_end, clockwise]

# Consider if the piece collides with other pieces or walls in its movement
# and restricts its movement appropriately
def restrict_movement(data, piece):
   piece_type = get_piece_type(data, piece)
   if piece_type == None:
      return
   piece_width = data.piece_widths[piece_type]
   team = piece[0]
   if team == 1:
      enemy = 2
   else:
      enemy = 1
   position = (data.pieces[piece][0], data.pieces[piece][1])

   data.movement_availability[piece] = []
   data.capture_availability[piece] = []
   data.protection_availability[piece] = []

   piece_movement = data.piece_movement[piece_type][team]
   for t in range(len(piece_movement)):
      lines = piece_movement[t]
      new_type = []
      for i in range(len(lines)):
         l = lines[i]
         movement_type = data.piece_movement[piece_type][3][t][i]
         if movement_type == 1: # Can't be blocked
            if l[0] == 1: # Lines
               new_line = calculate_line_edge(l, data, piece)
               if new_line:
                  output = calculate_unblocked_line_intersection(new_line, data, piece)
                  new_lines = output[0]
                  for capture in output[1]:
                     data.capture_availability[piece].append(capture)
                  for protection in output[2]:
                     data.protection_availability[piece].append(protection)
               else:
                  continue
            elif l[0] == 0: # Arcs
               new_lines = []
               test_lines = calculate_arc_edge(l, data, piece)
               for new_line in test_lines:
                  new_test_lines = calculate_unblocked_circle_intersection(new_line, data, piece)
                  for capture in new_test_lines[1]:
                     data.capture_availability[piece].append(capture)
                  for protection in new_test_lines[2]:
                     data.protection_availability[piece].append(protection)
                  for r in new_test_lines[0]:
                     new_lines.append(r)
            for l in new_lines:
               new_type.append(l)

         else: # Can be blocked
            if l[0] == 1: # Lines
               new_line = calculate_line_edge(l, data, piece)
               if new_line:
                  output = calculate_blocked_line_intersection(new_line, data, piece)
                  new_line = output[0]
                  blocked = output[1]
                  if output[2] != None:
                     data.capture_availability[piece].append(output[2])
                  if output[3] != None:
                     data.protection_availability[piece].append(output[3])
               else:
                  continue
            elif l[0] == 0: # Arcs
               try:
                  new_line = calculate_arc_edge(l, data, piece)[0]
               except:
                  continue
               if new_line:
                  output = calculate_blocked_circle_intersection(new_line, data, piece)
                  new_line = output[0]
                  blocked = output[1]
                  if output[2] != None:
                     data.capture_availability[piece].append(output[2])
                  elif output[3] != None:
                     data.protection_availability[piece].append(output[3])
               else:
                  continue
            if type(new_line) == list:
               new_type.append(new_line)
            if blocked:
               break
      data.movement_availability[piece].append(new_type)


def is_angle_between(start, end, angle, clockwise):
   if end > start:
      if angle < end and angle > start:
         return not clockwise
      return clockwise
   else:
      if angle > end and angle < start:
         return clockwise
      return not clockwise

# Order angles around a circle starting at some angle going either clockwise or not
def order_angles(angles, start, clockwise):
   if len(angles) == 0:
      return angles
   sorted_angles = sorted(angles)
   cut = 0
   for i in range(len(sorted_angles)):
      angle = sorted_angles[i]
      if angle > start:
         cut = i
         break

   new = sorted_angles[cut:] + sorted_angles[:cut]
   if clockwise:
      return new[::-1]
   else:
      return new

# Determine if a point is touching any piece
def is_point_close_to_piece(data, point, close, omit):
   for p in data.pieces:
      if p in omit:
         continue
      p_type = get_piece_type(data, p)
      p_width = data.piece_widths[p_type]
      r = data.pieces[p]
      d = calculate_distance(r, point)
      if d < close + p_width:
         return True
   return False

# Helper function for restrict_movement()
def calculate_unblocked_circle_intersection(circle, data, piece):
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]
   position = (data.pieces[piece][0], data.pieces[piece][1])

   start_angle = circle[3]
   end_angle = circle[4]
   angles = []
   circle_center = add_vectors(circle[1], position)
   start = (cos(start_angle) * circle[2] + circle[1][0], sin(start_angle) * circle[2] + circle[1][1])
   start = add_vectors(start, position)
   inside = False

   captures = []
   protections = []

   for p in data.pieces:
      if p != piece:
         p_type = get_piece_type(data, p)
         p_width= data.piece_widths[p_type]
         px = data.pieces[p][0]
         py = data.pieces[p][1]
         p_position = (px, py)

      # Determine if the circle starts inside another piece
         if ((px - start[0])**2 + (py - start[1])**2) ** (1/2) < piece_width + p_width:
            inside = True

         collision = circle_collision(add_vectors(circle[1], position), (px, py), circle[2], piece_width + p_width)
         if collision == False:
            pass
         else:
            for c in collision:
               offset = add_vectors(c, scale_vector(circle_center, -1))
               angle = atan2(offset[1], offset[0]) % (2 * pi)
               if is_angle_between(start_angle, end_angle, angle, circle[5]) and not is_point_close_to_piece(data, c, piece_width, [piece, p]):
                  if p[0] == piece[0]:
                     protections.append(c)
                  else:
                     captures.append(c)
                  angles.append(angle)
      else:
         pass

   new_circles = []
   angles = [start_angle] + order_angles(angles, start_angle, circle[5]) + [end_angle]
   for a in range(len(angles)):
      angle = angles[a]
      if inside:
         inside = False
      else:
         inside = True
         if a + 1 < len(angles):
            end_angle = angles[a + 1]
            new_circle = [0, circle[1], circle[2], angle, end_angle, circle[5]]
            new_circles.append(new_circle)
     
   return [new_circles, captures, protections]

# Helper function for restrict_movement()
def calculate_blocked_circle_intersection(circle, data, piece):
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]
   position = (data.pieces[piece][0], data.pieces[piece][1])

   start_angle = circle[3]
   end_angle = circle[4]
   angles = []
   circle_center = add_vectors(circle[1], position)
   start = (cos(start_angle) * circle[2] + circle[1][0], sin(start_angle) * circle[2] + circle[1][1])
   start = add_vectors(start, position)
   blocked = False

   captures = []
   protections = []

   for p in data.pieces:
      if p != piece:
         p_type = get_piece_type(data, p)
         p_width= data.piece_widths[p_type]
         px = data.pieces[p][0]
         py = data.pieces[p][1]
         p_position = (px, py)

      # Determine if the circle starts inside another piece
         if ((px - start[0])**2 + (py - start[1])**2) ** (1/2) < piece_width + p_width - .000001:
            return [False, True, None, None]

         collision = circle_collision(add_vectors(circle[1], position), (px, py), circle[2], piece_width + p_width)
         if collision == False:
            pass
         else:
            blocked = True
            for c in collision:
               offset = add_vectors(c, scale_vector(circle_center, -1))
               angle = atan2(offset[1], offset[0]) % (2 * pi)
               if is_angle_between(start_angle, end_angle, angle, circle[5]):
                  if p[0] == piece[0]:
                     protections.append((c, angle))
                  else:
                     captures.append((c, angle))
                  angles.append(angle)
      else:
         pass

   angles = [start_angle] + order_angles(angles, start_angle, circle[5]) + [end_angle]
   angle = angles[0]
   end_angle = angles[1]
   new_circle = [0, circle[1], circle[2], angle, end_angle, circle[5]]
   
   protection = None
   for i in protections:
      if i[1] == end_angle:
         protection = i[0]

   capture = None
   for i in captures:
      if i[1] == end_angle:
         capture = i[0]

   return [new_circle, blocked, capture, protection] 

# Helper function for restrict_movement()
def circle_collision(c1, c2, r1, r2):
   d = calculate_distance(c1, c2)
   x = (d**2 - r2**2 + r1**2) / (2 * d)
   value = ((4 * d**2 * r1**2) - (d**2 - r2**2 + r1**2)**2) / (4 * d**2)
   if value <= 0:
      return False
   
   v = normalize_vector(add_vectors(c2, scale_vector(c1, -1)))
   add = scale_vector(v, x)
   center = add_vectors(c1, add)
   y = value ** (1/2)

   d1 = (v[1], -v[0])
   d2 = (-v[1], v[0])

   intersection_1 = add_vectors(center, scale_vector(d1, y))
   intersection_2 = add_vectors(center, scale_vector(d2, y))

   return [intersection_1, intersection_2]

def check_all_piece_movement(data):
   data.movement_availability = {}
   data.capture_availability = {}
   data.protection_availability = {}
   for piece in data.pieces:
      restrict_movement(data, piece)



def check_point_inside_board(p, width):
   epsilon = 10e-8
   if p[0] < 1 - width - epsilon and p[0] > width + epsilon and p[1] < 1 - width - epsilon and p[1] > width + epsilon:
      return True
   else:
      return False

def scale_vector(v, scale):
   return (v[0] * scale, v[1] * scale)

def add_vectors(v, o):
   return (v[0] + o[0], v[1] + o[1])

def normalize_vector(v):
   m = (v[0]**2 + v[1]**2)**(1/2)
   return scale_vector(v, 1 / m)

def cross_2d(v1, v2):
   return v1[0]*v2[1] - v1[1]*v2[0]

# Helper function for restrict_movement()
def line_collision(start_1, end_1, start_2, end_2):
   r = add_vectors(end_1, scale_vector(start_1, -1))
   s = add_vectors(end_2, scale_vector(start_2, -1))
   p = start_1
   q = start_2

   value_1 = cross_2d(r, s)
   value_2 = cross_2d(add_vectors(q, scale_vector(p, -1)), s)

   value_3 = cross_2d(add_vectors(q, scale_vector(p, -1)), r)

   if value_1 == 0:
      return False
   t = value_2 / value_1
   u = value_3 / value_1
   if t >= 0 and t <= 1 and u >= 0 and u <= 1:
      return add_vectors(p, scale_vector(r, t))

   return False

def calculate_arc_edge(arc, data, piece):
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]
   position = (data.pieces[piece][0], data.pieces[piece][1])
   epsilon = 10e-8

   start_angle = arc[3] % (2 * pi)
   end_angle = arc[4] % (2 * pi)


   start_x = cos(start_angle) * arc[2]
   start_y = sin(start_angle) * arc[2]
   
   center = add_vectors(arc[1], position)
   offset_start = add_vectors(arc[1], add_vectors(position, (start_x, start_y)))
   if offset_start[0] < 1 - piece_width and offset_start[0] > piece_width and offset_start[1] > piece_width and offset_start[1] < 1 - piece_width:
      inside = True
   else:
      inside = False
   angles = []

   for l in [[(piece_width, 1 - piece_width), (1 - piece_width, 1 - piece_width)],
             [(piece_width, piece_width), (1 - piece_width, piece_width)],
             [(1 - piece_width, piece_width), (1 - piece_width, 1 - piece_width)],
             [(piece_width, piece_width), (piece_width, 1 - piece_width)]]:
      intersections = line_intersect_circle([0, l[0], l[1]], center, arc[2])
      if intersections == False:
         pass
      elif type(intersections) == float:
         pass
      else:
         for i in intersections:
            if type(i) == tuple and type(i[0]) == float:
               offset = add_vectors(i, scale_vector(center, -1))
               angle = atan2(offset[1], offset[0]) % (2 * pi)
               if is_angle_between(start_angle, end_angle, angle, arc[5]):
                  angles.append(angle)

   new_circles = []
   angles = [start_angle] + order_angles(angles, start_angle, arc[5]) + [end_angle]
   for a in range(len(angles)):
      angle = angles[a]
      if not inside:
         inside = True
      else:
         inside = False
         if a + 1 < len(angles):
            end_angle = angles[a + 1]
            new_circle = [0, arc[1], arc[2], angle, end_angle, arc[5]]
            new_circles.append(new_circle)
     
   return new_circles

# Helper function for restrict_movement()
def calculate_line_edge(line, data, piece):
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]
   position = (data.pieces[piece][0], data.pieces[piece][1])

   start = add_vectors(line[1], position)
   end = add_vectors(line[2], position)

   start_inside = check_point_inside_board(start, piece_width)
   end_inside = check_point_inside_board(end, piece_width)
   if start_inside and end_inside:
      return line

   collisions = []
   for l in [[(piece_width, 1 - piece_width), (1 - piece_width, 1 - piece_width)],
             [(piece_width, piece_width), (1 - piece_width, piece_width)],
             [(1 - piece_width, piece_width), (1 - piece_width, 1 - piece_width)],
             [(piece_width, piece_width), (piece_width, 1 - piece_width)]]:
      edge_start = l[0]
      edge_end = l[1]
      collide = line_collision(start, end, edge_start, edge_end)
      if collide:
         collisions.append(add_vectors(collide, scale_vector(position, -1)))

   if len(collisions) == 0:
      if int(start_inside) + int(end_inside) == 0:
         return False
      else:
         return line
   elif len(collisions) == 1:
      if start_inside:
         return [1, line[1], collisions[0]]
      else:
         return [1, collisions[0], line[2]]
   else:
      if collisions[0] == collisions[1]:
         return [1, line[1], collisions[0]]
      else:
         return [1, collisions[0], collisions[1]]
   return line

# Helper function for restrict_movement()
def calculate_unblocked_line_intersection(line, data, piece):
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]
   position = (data.pieces[piece][0], data.pieces[piece][1])

   start = (line[1][0] + position[0], line[1][1] + position[1])
   end =   (line[2][0] + position[0], line[2][1] + position[1])
   distances = [(0, start), (calculate_distance(start, end), end)]
   inside = False

   captures = []
   protections = []

   for p in data.pieces:
      if p != piece:
         p_type = get_piece_type(data, p)
         p_width= data.piece_widths[p_type]
         px = data.pieces[p][0]
         py = data.pieces[p][1]
         p_position = (px, py)

      # Determine if the line starts inside another piece
         if ((px - start[0])**2 + (py - start[1])**2) ** (1/2) < piece_width + p_width:
            inside = True

         collision = line_intersect_circle([1, start, end], p_position, piece_width + p_width)
         if collision == False:
            pass
         elif type(collision) == float:
            pass
         else:
            for c in collision:
               if type(c) == float:
                  pass
               elif c[0] == False:
                  pass
               else:
                  new_distance = calculate_distance(c, start)
                  if new_distance < distances[-1][0] and not is_point_close_to_piece(data, c, piece_width, [piece, p]):
                     if p[0] == piece[0]:
                        protections.append(c)
                     else:
                        captures.append(c)
                     collided = True
                     distances.append((new_distance, c))
                     distances.sort()
      else:
         pass

   new_lines = []
   for p in range(len(distances)):
      point = distances[p][1]
      if inside:
         inside = False
      else:
         inside = True
         if p + 1 < len(distances):
            new_lines.append([1, point, distances[p + 1][1]])
         

   new_new_lines = []
   for l in new_lines:
      start = offset_vector(l[1], position, subtract = True)
      end = offset_vector(l[2], position, subtract = True)
      new_new_lines.append([1, start, end])
   return [new_new_lines, captures, protections]

# Helper function for restrict_movement()
def calculate_blocked_line_intersection(line, data, piece):
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]
   position = (data.pieces[piece][0], data.pieces[piece][1])

   start = (line[1][0] + position[0], line[1][1] + position[1])
   end =   (line[2][0] + position[0], line[2][1] + position[1])
   distance = calculate_distance(start, end)
   collided = False

   capture = None
   protection = None

   for p in data.pieces:
      if p != piece:
         p_type = get_piece_type(data, p)
         p_width= data.piece_widths[p_type]
         px = data.pieces[p][0]
         py = data.pieces[p][1]
         p_position = (px, py)

      # Return nothing if the start of the line is blocked by a piece
         if ((px - start[0])**2 + (py - start[1])**2) ** (1/2) < piece_width + p_width:
            return (None, True, None, None)

         collision = line_intersect_circle([1, start, end], p_position, piece_width + p_width)
         if collision == False:
            pass
         elif type(collision) == float:
            collided = True
            new_distance = calculate_distance(collision, start)
            if new_distance < distance:
               distance = new_distance
               end = collision
         else:
            for c in collision:
               if c == False:
                  pass
               elif type(c) == float:
                  pass
               else:
                  if c[0] == False:
                     pass
                  else:
                     collided = True
                     new_distance = calculate_distance(c, start)
                     if new_distance < distance:
                        if p[0] == piece[0]:
                           protection = c
                           capture = None
                        else:
                           protection = None
                           capture = c
                        distance = new_distance
                        end = c
      else:
         pass

   start = offset_vector(start, position, subtract = True)
   end = offset_vector(end, position, subtract = True)
   return ([1, start, end], collided, capture, protection)


def calculate_distance(p1, p2):
   return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)


def offset_vector(v, o, subtract = False):
   if subtract:
      return (v[0] - o[0], v[1] - o[1])
   else:
      return (v[0] + o[0], v[1] + o[1])


def line_intersect_circle(line, center, radius):
   (sx, sy) = line[1]
   (ex, ey) = line[2]
   (cx, cy) = center

   (dx, dy) = (ex - sx, ey - sy)
   (fx, fy) = (sx - cx, sy - cy)

   a = dx**2 + dy**2
   b = 2*(dx * fx + dy * fy)
   c = sx**2 + sy**2 + cx**2 + cy**2 - radius**2 - 2*(sx*cx + sy*cy)
   t = solve_quadratic(a, b, c)
   
   if t == False:
      return False
   elif type(t) == float:
      if t < 0:
         return False
      nx = (dx * t) + sx
      ny = (dy * t) + sy
      return (nx, ny)
   else:
      if t[0] >= 0 and t[0] <= 1:
         nx1 = (dx * t[0]) + sx
         ny1 = (dy * t[0]) + sy
      else:
         nx1, ny1 = False, False
      if t[1] >= 0 and t[1] <= 1:
         nx2 = (dx * t[1]) + sx
         ny2 = (dy * t[1]) + sy
      else:
         nx2, ny2 = False, False
      return [(nx1, ny1), (nx2, ny2)]


def closest_point_on_segment(line, point):
   start = line[1]
   end = line[2]

   r = add_vectors(end, scale_vector(start, -1))
   d = normalize_vector(r)
   s = (d[1], -d[0])

   p = start
   q = point

   value_1 = cross_2d(r, s)
   value_2 = cross_2d(add_vectors(q, scale_vector(p, -1)), s)

   value_3 = cross_2d(add_vectors(q, scale_vector(p, -1)), r)

   t = value_2 / value_1
   u = value_3 / value_1
   if t < 0:
      d = calculate_distance(start, point)
      return (d, start)
   elif t > 1:
      d = calculate_distance(end, point)
      return (d, end)
   else:
      v = add_vectors(p, scale_vector(r, t))
      d = calculate_distance(v, point)
      return (d, v)


def closest_point_on_arc(arc, point):
   start_angle = arc[3]
   end_angle = arc[4]
   clockwise = arc[5]

   d = calculate_distance(point, arc[1])
   r = add_vectors(point, scale_vector(arc[1], -1))
   angle = atan2(r[1], r[0]) % (2 * pi)
   if is_angle_between(start_angle, end_angle, angle, clockwise):
      offset = (cos(angle) * arc[2], sin(angle) * arc[2])
      return (abs(d - arc[2]), add_vectors(arc[1], offset))

   start_offset = (cos(start_angle) * arc[2], sin(start_angle) * arc[2])
   end_offset = (cos(end_angle) * arc[2], sin(end_angle) * arc[2])

   start = add_vectors(start_offset, arc[1])
   end = add_vectors(end_offset, arc[1])

   start_distance = calculate_distance(start, point)
   end_distance = calculate_distance(end, point)

   if start_distance > end_distance:
      return (end_distance, end)
   else:
      return (start_distance, start)

# Quadratic formula with different output types based on cases
def solve_quadratic(a, b, c):
   disc = b**2 - 4*a*c
   if a == 0:
      return False
   if disc < 0:
      return False
   elif disc == 0:
      return -b / (2*a)
   disc = disc**(1/2)
   solution_1 = (-b + disc) / (2*a)
   solution_2 = (-b - disc) / (2*a)
   return (solution_1, solution_2)

















