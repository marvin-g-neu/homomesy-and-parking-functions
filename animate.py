import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.transforms as transforms
from matplotlib.patches import Rectangle

def simulate_classical_parking(parking_func):
    """
    animation for classical PF_n; returns each frame of action taken
    """
    n = len(parking_func)
    frames = []
    assignment = [None]*n
    used_spots = set()
    
    # start with empty street
    frames.append(assignment[:])
    
    for i, preferred in enumerate(parking_func):
        spot = preferred
        while spot in used_spots and spot <= n:
            spot += 1
        
        # if no spot, car goes to end of street
        if spot > n:
            assignment[i] = None
            frames.append(assignment[:])
            break
        else:
            used_spots.add(spot)
            assignment[i] = spot
            frames.append(assignment[:])
    
    return frames

def simulate_k_naples_parking(parking_func, k):
    """
    animation for k-Naples PF_n
    """
    n = len(parking_func)
    frames = []
    assignment = [None]*n
    used_spots = set()
    
    frames.append(assignment[:])
    
    for i, preferred in enumerate(parking_func):
        spot = preferred
        
        if spot in used_spots:
            # try k steps back
            for back_spot in range(spot-1, max(0, spot-k-1), -1):
                if back_spot not in used_spots:
                    spot = back_spot
                    break
            
            # if no open spot, go to end of list
            if spot in used_spots:
                spot = preferred
                while spot in used_spots and spot <= n:
                    spot += 1
        
        # end of street
        if spot > n:
            assignment[i] = None
            frames.append(assignment[:])
            break
        else:
            used_spots.add(spot)
            assignment[i] = spot
            frames.append(assignment[:])
    
    return frames

def simulate_interval_parking(alpha, beta):
    """
    animation for l-interval PF_n
    """
    n = len(alpha)
    frames = []
    assignment = [None]*n
    used_spots = set()
    
    frames.append(assignment[:])
    
    for i in range(n):
        # try each spot in interval [a_i, b_i]
        parked = False
        for spot in range(alpha[i], beta[i] + 1):
            if spot not in used_spots:
                assignment[i] = spot
                used_spots.add(spot)
                parked = True
                break
        
        # end of street
        if not parked:
            assignment[i] = None
            frames.append(assignment[:])
        
        frames.append(assignment[:])
    
    return frames

def simulate_unit_interval_parking(alpha, beta):
    """
    animation for unit-interval PF_n
    """
    n = len(alpha)
    frames = []
    assignment = [None]*n
    used_spots = set()
    
    frames.append(assignment[:])
    
    for i in range(n):
        # we can only park at a_i or b_i
        parked = False
        
        # Try a_i first
        if alpha[i] not in used_spots:
            assignment[i] = alpha[i]
            used_spots.add(alpha[i])
            parked = True
        # Then try b_i
        elif beta[i] not in used_spots:
            assignment[i] = beta[i]
            used_spots.add(beta[i])
            parked = True
        
        # parking fails 
        if not parked:
            assignment[i] = None
            frames.append(assignment[:])
            break  # stop animation
        else:
            frames.append(assignment[:])
    
    return frames

def draw_car(ax, x_left, y_bottom, width, height,
             color='#63b6c8', label=None, label_size=10):
    """
    creates cars for the animation
    """
    Path = mpath.Path
    
    # wehhls
    wheel_radius = 0.12 * height
    car_body_height = height - 2*wheel_radius
    
    # based in box dimensions
    car_width = 0.8 * width
    x_offset = (width - car_width) / 2  # center
    
    # outline of car (polygon)
    vertices = [
        (0.0, wheel_radius),
        (car_width, wheel_radius),
        (car_width, wheel_radius + 0.7*car_body_height),
        (0.8*car_width, wheel_radius + car_body_height),
        (0.2*car_width, wheel_radius + car_body_height),
        (0.0, wheel_radius + 0.7*car_body_height),
        (0.0, wheel_radius)
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.CLOSEPOLY
    ]
    car_path = Path(vertices, codes)
    
    # translate
    t = transforms.Affine2D().translate(x_left + x_offset, y_bottom)
    car_path = t.transform_path(car_path)
    
    # draw body
    car_patch = mpatches.PathPatch(car_path, facecolor=color, edgecolor='black', linewidth=1)
    ax.add_patch(car_patch)
    
    # add wheels 
    front_wheel_center = (x_left + x_offset + 0.25*car_width, y_bottom + wheel_radius)
    back_wheel_center = (x_left + x_offset + 0.75*car_width, y_bottom + wheel_radius)
    ax.add_patch(mpatches.Circle(front_wheel_center, wheel_radius, facecolor='black'))
    ax.add_patch(mpatches.Circle(back_wheel_center, wheel_radius, facecolor='black'))
    
    # add label
    if label is not None:
        ax.text(
            x_left + x_offset + car_width/2,
            y_bottom + wheel_radius + 0.5*car_body_height,
            label,
            ha='center', va='center',
            fontsize=label_size,
            color='black',
            fontweight='bold'
        )

def plot_parking_state(parking_func, assignment, current_step):
    """
    plots a single frame of the parking state.
    """
    n = len(parking_func)
    
    fig, ax = plt.subplots(figsize=(max(12, n*1.5), 4))
    
    # axes
    left_bound, right_bound = -3, n + 2.5
    ax.set_xlim(left_bound, right_bound)
    ax.set_ylim(-0.2, 1.2)
    ax.axis('off')
    
    # center spots
    spot_spacing = 1.2
    axis_midpoint = (left_bound + right_bound) / 2
    total_spots_width = (n - 1) * spot_spacing
    spot_start = axis_midpoint - (total_spots_width / 2)
    
    # draw spots
    for spot_id in range(1, n + 1):
        x_pos = spot_start + (spot_id - 1) * spot_spacing
        ax.add_patch(
            Rectangle((x_pos - 0.4, 0.1), 0.8, 0.6,
                      edgecolor='black', facecolor='lightgray', alpha=0.3)
        )
        ax.text(
            x_pos, 0, f"Spot {spot_id}",
            ha='center', va='top', fontsize=8
        )
    
    # car
    car_width = 0.9
    car_height = 0.4
    
    if current_step < len(assignment) and assignment[current_step] is not None:
        x_left = -2.5
        y_bottom = 0.1
        draw_car(
            ax, x_left, y_bottom,
            car_width, car_height,
            color='lightblue',
            label=fr"$c_{{{current_step + 1}}}$"
        )

    for i in range(current_step):
        spot = assignment[i]
        if spot is not None:
            x_left = spot_start + (spot - 1)*spot_spacing - (car_width / 2)
            y_bottom = 0.1
            draw_car(
                ax, x_left, y_bottom,
                car_width, car_height,
                color='#5DADE2',
                label=fr"$c_{{{i + 1}}}$"
            )
        else:
            x_left = (n + 1.5) - (car_width / 2)
            y_bottom = 0.1
            draw_car(
                ax, x_left, y_bottom,
                car_width, car_height,
                color='#5DADE2',
                label=fr"$c_{{{i + 1}}}$"
            )
    
    return fig
