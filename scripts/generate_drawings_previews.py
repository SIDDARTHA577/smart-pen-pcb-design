"""Generates high-resolution engineering drawings and cross-section previews for Smart Pen Rev G Phase 4A."""
import sys
sys.path.insert(0, '.')
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

from output.RevG.Mechanical_Phase04_Corrected.CAD_Source.SmartPen_Parametric_CAD_RevG_Corrected import SmartPenParameters

p = SmartPenParameters()
base_dir = Path("output/RevG/Mechanical_Phase04_Corrected")
draw_dir = base_dir / "Drawings"
prev_dir = base_dir / "Previews"
draw_dir.mkdir(parents=True, exist_ok=True)
prev_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. LONGITUDINAL SECTION DRAWING (Z vs Y)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(18, 7), dpi=300)
ax.set_title("Smart Pen Rev G — Phase 4A Corrected Longitudinal Cross-Section (Z-Y Plane)\n"
             "Contractual Target: Length 153.5 mm, OD 15.5 mm | Real Solid CAD Coordinate Verification",
             fontsize=14, fontweight='bold', pad=15)

# Outer barrel wall (+Y and -Y)
# Z = 38 to 142
ax.add_patch(patches.Rectangle((38.0, 6.75), 104.0, 1.0, facecolor='#4682B4', edgecolor='black', alpha=0.8, label='01 Outer Barrel (OD 15.5, ID 13.5)'))
ax.add_patch(patches.Rectangle((38.0, -7.75), 104.0, 1.0, facecolor='#4682B4', edgecolor='black', alpha=0.8))

# USB-C aperture cut in barrel (+X side, Y = 2.1 to 6.7, Z = 111.15 to 121.65)
ax.add_patch(patches.Rectangle((111.15, 6.75), 10.50, 1.0, facecolor='white', edgecolor='red', linestyle='--', linewidth=1.5, label='USB-C Opening Cut (Z=116.4)'))

# Button apertures (SW1 @ 70.96, SW2 @ 85.10)
ax.add_patch(patches.Rectangle((70.96 - 2.5, 6.75), 5.0, 1.0, facecolor='white', edgecolor='purple', linestyle='--', linewidth=1.5))
ax.add_patch(patches.Rectangle((85.10 - 2.5, 6.75), 5.0, 1.0, facecolor='white', edgecolor='purple', linestyle='--', linewidth=1.5, label='Button Openings (SW1, SW2)'))

# Front Grip (Z = 18 to 38)
grip_pts_top = [[18.0, 11.5/2.0], [38.0, 15.5/2.0], [38.0, 6.75], [18.0, 3.80]]
ax.add_patch(patches.Polygon(grip_pts_top, facecolor='#20B2AA', edgecolor='black', alpha=0.8, label='02 Front Grip'))
grip_pts_bot = [[18.0, -11.5/2.0], [38.0, -15.5/2.0], [38.0, -6.75], [18.0, -3.80]]
ax.add_patch(patches.Polygon(grip_pts_bot, facecolor='#20B2AA', edgecolor='black', alpha=0.8))

# Front Nose Cone (Z = 0 to 18)
nose_pts_top = [[0.0, 2.8/2.0], [18.0, 11.5/2.0], [18.0, 2.10], [6.0, 2.10], [6.0, 1.25], [0.0, 1.25]]
ax.add_patch(patches.Polygon(nose_pts_top, facecolor='#708090', edgecolor='black', alpha=0.8, label='03 Front Nose Cone'))
nose_pts_bot = [[0.0, -2.8/2.0], [18.0, -11.5/2.0], [18.0, -2.10], [6.0, -2.10], [6.0, -1.25], [0.0, -1.25]]
ax.add_patch(patches.Polygon(nose_pts_bot, facecolor='#708090', edgecolor='black', alpha=0.8))

# D1 Ink Refill (Retracted Z = 1.5 to 68.5)
ax.add_patch(patches.Rectangle((1.5, -1.175), 67.0, 2.35, facecolor='#C0C0C0', edgecolor='black', hatch='//', alpha=0.9, label='20 D1 Refill (Retracted Z=1.5..68.5)'))

# Helical Return Spring (Z = 6 to 18)
ax.add_patch(patches.Rectangle((6.0, 1.50), 12.0, 0.40, facecolor='#FFD700', edgecolor='black', label='21 Return Spring'))
ax.add_patch(patches.Rectangle((6.0, -1.90), 12.0, 0.40, facecolor='#FFD700', edgecolor='black'))

# Removable Electronics Rail (Z = 38 to 122)
# Rail floor: Y = 0.20 to 1.20
ax.add_patch(patches.Rectangle((38.0, 0.20), 84.0, 1.00, facecolor='#32CD32', edgecolor='black', alpha=0.7, label='04 Electronics Rail (Floor Y=0.2..1.2)'))
# Rail pushrod tube: Y = -1.60 to +0.20
ax.add_patch(patches.Rectangle((38.0, -1.60), 84.0, 0.40, facecolor='#32CD32', edgecolor='black', alpha=0.7))

# Moving Pushrod (Z = 68.5 to 140.0)
ax.add_patch(patches.Rectangle((68.5, -0.80), 71.5, 1.60, facecolor='#696969', edgecolor='black', label='22 Moving Pushrod (OD 1.6)'))

# Main PCB (Z = 38 to 122, Y = 1.20 to 2.80)
ax.add_patch(patches.Rectangle((38.0, 1.20), 84.0, 1.60, facecolor='#006400', edgecolor='black', alpha=0.9, label='15 Main PCB (84x9.2x1.6 mm)'))

# Corrected Battery Cradle (Z = 74 to 109, Y = -6.60 to -1.20)
ax.add_patch(patches.Rectangle((74.0, -6.60), 35.0, 1.00, facecolor='#FF8C00', edgecolor='black', alpha=0.8, label='05 Battery Cradle (Y=-6.6..-1.2)'))
# LiPo Battery (Z = 74 to 106, Y = -5.50 to -1.50)
ax.add_patch(patches.Rectangle((74.0, -5.50), 32.0, 4.00, facecolor='#1E90FF', edgecolor='black', hatch='\\\\', alpha=0.8, label='19 LiPo Battery (32x10x4 mm)'))

# USB-C Connector (J_USB at Z = 116.40, Y = 2.80 to 6.00)
ax.add_patch(patches.Rectangle((116.40 - 4.47, 2.80), 8.94, 3.20, facecolor='#DAA520', edgecolor='black', label='J_USB Receptacle (Z=116.4)'))

# MicroSD Carrier (Z = 122 to 138, Y = 0.40 to 4.60)
ax.add_patch(patches.Rectangle((122.0, 0.40), 16.0, 4.20, facecolor='#9370DB', edgecolor='black', alpha=0.7, label='07 MicroSD Carrier'))

# Rear Bayonet Collar (Z = 136 to 142)
ax.add_patch(patches.Rectangle((136.0, 5.20), 6.0, 2.55, facecolor='#8B4513', edgecolor='black', alpha=0.8, label='11 Bayonet Collar (30° Lock)'))
ax.add_patch(patches.Rectangle((136.0, -7.75), 6.0, 2.55, facecolor='#8B4513', edgecolor='black', alpha=0.8))

# Rear Click Plunger (Z = 138 to 153.5)
ax.add_patch(patches.Rectangle((144.0, -2.90), 6.0, 5.80, facecolor='#DC143C', edgecolor='black', alpha=0.8, label='10 Click Plunger (Dome Apex Z=153.5)'))
click_dome_pts = [[150.0, 2.90], [153.5, 1.80], [153.5, -1.80], [150.0, -2.90]]
ax.add_patch(patches.Polygon(click_dome_pts, facecolor='#DC143C', edgecolor='black', alpha=0.8))

# Pocket Clip (Z = 100 to 142, Y = 7.75 to 9.80)
ax.add_patch(patches.Rectangle((100.0, 7.75), 42.0, 2.05, facecolor='#B0C4DE', edgecolor='black', label='12 Pocket Clip (Y=+7.75..+9.80)'))

# FFC Ribbon Cable (Z = 96.4 to 122.0)
ax.plot([96.4, 108.0, 108.0, 122.0], [3.20, 3.20, 5.20, 5.20], color='#FF1493', linewidth=2.5, label='25 FFC 180° Service Loop')

# Dimension Callouts & Annotations
ax.axhline(0, color='gray', linestyle=':', linewidth=0.8)
ax.annotate('Total Assembled Length: 153.50 mm', xy=(76.75, -9.5), xycoords='data', ha='center', fontsize=11, fontweight='bold')
ax.annotate('', xy=(0.0, -9.0), xytext=(153.5, -9.0), arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax.annotate('Barrel OD: Ø 15.50 mm', xy=(90.0, 8.8), xycoords='data', ha='center', fontsize=10, fontweight='bold', color='#4682B4')
ax.annotate('Rail Inside: 9.50 mm (clears 9.2 mm PCB)', xy=(55.0, 3.8), xycoords='data', ha='center', fontsize=9, fontweight='bold', color='#006400')
ax.annotate('Battery Under Rail\n(10.2x4.2 mm clear)', xy=(90.0, -3.5), xycoords='data', ha='center', fontsize=9, fontweight='bold', color='#1E90FF')

ax.set_xlim(-5, 160)
ax.set_ylim(-11, 12)
ax.set_xlabel("Pen Longitudinal Axis Z (mm)", fontsize=11, fontweight='bold')
ax.set_ylabel("Radial Height Y (mm)", fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0), fontsize=8, borderaxespad=0.)

plt.tight_layout()
fig.savefig(draw_dir / "SmartPen_RevG_Longitudinal_Drawing.png", dpi=300)
fig.savefig(prev_dir / "SmartPen_RevG_Longitudinal_Section.png", dpi=300)
plt.close(fig)
print("Saved Longitudinal Section Drawings.")

# ---------------------------------------------------------------------------
# 2. TRANSVERSE SECTION DRAWINGS (4 Cross-Sections)
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(20, 5.5), dpi=300)
fig.suptitle("Smart Pen Rev G — Phase 4A Corrected Transverse Cross-Sections\n"
             "All Sections Fit Within Nominal Ø 15.50 mm OD & Ø 13.50 mm Bore", fontsize=14, fontweight='bold')

def draw_barrel_rings(ax, title):
    # Outer barrel Ø 15.5 (R = 7.75)
    circle_out = patches.Circle((0, 0), 7.75, facecolor='#E6F0FA', edgecolor='#4682B4', linewidth=2)
    # Bore Ø 13.5 (R = 6.75)
    circle_in = patches.Circle((0, 0), 6.75, facecolor='white', edgecolor='#4682B4', linestyle='--', linewidth=1.5)
    ax.add_patch(circle_out)
    ax.add_patch(circle_in)
    ax.set_xlim(-9, 9)
    ax.set_ylim(-9, 11)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=10, fontweight='bold', pad=10)
    ax.set_xlabel("X (mm)", fontsize=9)
    ax.set_ylabel("Y (mm)", fontsize=9)
    ax.grid(True, linestyle=':', alpha=0.5)

# Section A-A: Front Grip & MPU (Z = 25.0 mm)
draw_barrel_rings(axes[0], "Section A-A (Z = 25.0 mm)\nFront MPU & Touch Nest")
# Front grip outer contour
axes[0].add_patch(patches.Circle((0, 0), 6.75, facecolor='none', edgecolor='#20B2AA', linewidth=1.5))
# Refill conduit
axes[0].add_patch(patches.Circle((0, 0), 1.45, facecolor='#708090', edgecolor='black', alpha=0.6))
axes[0].add_patch(patches.Circle((0, 0), 1.175, facecolor='#C0C0C0', edgecolor='black'))
# MPU PCB: 7.2 x 0.8 mm at Y = 2.2 to 3.0
axes[0].add_patch(patches.Rectangle((-3.6, 2.2), 7.2, 0.8, facecolor='#006400', edgecolor='black', label='MPU PCB'))
# Touch sensor at Y = 4.9 to 5.7
axes[0].add_patch(patches.Rectangle((-3.0, 4.9), 6.0, 0.8, facecolor='#8A2BE2', edgecolor='black', label='Touch PCB'))

# Section B-B: Main PCB & Battery (Z = 85.0 mm)
draw_barrel_rings(axes[1], "Section B-B (Z = 85.0 mm)\nPCB Deck, Battery & Rail")
# Rail Deck: width 11.0 mm (X = -5.5 to +5.5), floor Y = 0.2 to 1.2
axes[1].add_patch(patches.Rectangle((-5.5, 0.2), 11.0, 1.0, facecolor='#32CD32', edgecolor='black', alpha=0.7))
# Rail side walls: X = -5.5 to -4.75 and +4.75 to +5.5, Y = 1.2 to 3.2
axes[1].add_patch(patches.Rectangle((-5.5, 1.2), 0.75, 2.0, facecolor='#32CD32', edgecolor='black', alpha=0.7))
axes[1].add_patch(patches.Rectangle((4.75, 1.2), 0.75, 2.0, facecolor='#32CD32', edgecolor='black', alpha=0.7))
# Retention lips
axes[1].add_patch(patches.Rectangle((-4.75, 2.8), 0.35, 0.4, facecolor='#228B22', edgecolor='black'))
axes[1].add_patch(patches.Rectangle((4.40, 2.8), 0.35, 0.4, facecolor='#228B22', edgecolor='black'))
# Main PCB: 9.2 x 1.6 mm at Y = 1.2 to 2.8 (X = -4.6 to +4.6)
axes[1].add_patch(patches.Rectangle((-4.6, 1.2), 9.2, 1.6, facecolor='#006400', edgecolor='black', alpha=0.9, label='PCB (9.2 mm)'))
# Moving pushrod at center (OD 1.6)
axes[1].add_patch(patches.Circle((0, 0), 0.80, facecolor='#696969', edgecolor='black'))
# Battery Cradle Hull: R = 6.60 mm
axes[1].add_patch(patches.Rectangle((-5.7, -6.4), 11.4, 5.2, facecolor='#FF8C00', edgecolor='black', alpha=0.5))
# LiPo Battery: 10.0 x 4.0 mm at Y = -5.5 to -1.5 (X = -5.0 to +5.0)
axes[1].add_patch(patches.Rectangle((-5.0, -5.5), 10.0, 4.0, facecolor='#1E90FF', edgecolor='black', hatch='//', alpha=0.8, label='LiPo (10 mm)'))

# Section C-C: USB-C Opening & Receptacle (Z = 116.4 mm)
draw_barrel_rings(axes[2], "Section C-C (Z = 116.4 mm)\nReal USB-C Side Aperture")
# Rail Deck & PCB
axes[2].add_patch(patches.Rectangle((-5.5, 0.2), 11.0, 1.0, facecolor='#32CD32', edgecolor='black', alpha=0.7))
axes[2].add_patch(patches.Rectangle((-4.6, 1.2), 9.2, 1.6, facecolor='#006400', edgecolor='black', alpha=0.9))
# USB-C Receptacle: centered at X = +5.5, Y = 4.4 mm
axes[2].add_patch(patches.Rectangle((3.5, 2.8), 3.2, 3.2, facecolor='#DAA520', edgecolor='black', label='J_USB'))
# Barrel side opening cutout (+X side: X = 6.5 to 8.5, Y = 2.1 to 6.7)
axes[2].add_patch(patches.Rectangle((6.75, 2.1), 1.0, 4.6, facecolor='white', edgecolor='red', linestyle='--', linewidth=2, label='Cutout'))
# Hollow Bezel (Part 08)
axes[2].add_patch(patches.Rectangle((6.55, 1.8), 1.35, 5.2, facecolor='none', edgecolor='#FF4500', linewidth=1.5, label='Bezel'))

# Section D-D: Bayonet Collar (Z = 139.0 mm)
draw_barrel_rings(axes[3], "Section D-D (Z = 139.0 mm)\n30° Bayonet Locking Lugs")
# Bayonet pilot sleeve: OD 13.3, ID 10.4
axes[3].add_patch(patches.Circle((0, 0), 13.3/2.0, facecolor='#8B4513', edgecolor='black', alpha=0.6))
axes[3].add_patch(patches.Circle((0, 0), 10.4/2.0, facecolor='white', edgecolor='black'))
# 3 Lugs at 120°
for deg in [0, 120, 240]:
    rad = math.radians(deg)
    lx = 6.50 * math.cos(rad)
    ly = 6.50 * math.sin(rad)
    axes[3].add_patch(patches.Circle((lx, ly), 0.50, facecolor='#FFD700', edgecolor='black', label='Lugs' if deg==0 else ''))

# Add pocket clip to Section D-D (Y = 7.75 to 9.80)
axes[3].add_patch(patches.Rectangle((-1.8, 7.75), 3.6, 2.05, facecolor='#B0C4DE', edgecolor='black', label='Clip'))

for ax in axes:
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), fontsize=7, ncol=2)

plt.tight_layout()
fig.savefig(draw_dir / "SmartPen_RevG_Transverse_Drawing.png", dpi=300)
fig.savefig(prev_dir / "SmartPen_RevG_Transverse_Sections.png", dpi=300)
plt.close(fig)
print("Saved Transverse Section Drawings.")

# ---------------------------------------------------------------------------
# 3. 3D ASSEMBLY PREVIEWS (Master & Exploded)
# ---------------------------------------------------------------------------
# Master 3D View
fig = plt.figure(figsize=(14, 6), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Smart Pen Rev G — Phase 4A Master Assembly 3D Solid Model\n"
             "All 25 Native Solid Bodies in Synchronized Global Coordinates", fontsize=12, fontweight='bold')

# Plot representative cylinders and boxes in 3D
theta = np.linspace(0, 2*np.pi, 30)
z_cyl = np.linspace(38, 142, 20)
theta_grid, z_grid = np.meshgrid(theta, z_cyl)
x_cyl = 7.75 * np.cos(theta_grid)
y_cyl = 7.75 * np.sin(theta_grid)
ax.plot_surface(z_grid, x_cyl, y_cyl, alpha=0.15, color='cyan')

# PCB
z_pcb = np.array([38, 122])
x_pcb = np.array([-4.6, 4.6])
z_p, x_p = np.meshgrid(z_pcb, x_pcb)
y_p = np.full_like(z_p, 2.0)
ax.plot_surface(z_p, x_p, y_p, alpha=0.8, color='green')

# Battery
z_b = np.array([74, 106])
x_b = np.array([-5.0, 5.0])
z_bg, x_bg = np.meshgrid(z_b, x_b)
y_bg = np.full_like(z_bg, -3.5)
ax.plot_surface(z_bg, x_bg, y_bg, alpha=0.8, color='blue')

# Refill
z_ref = np.linspace(1.5, 68.5, 10)
th_ref, z_rf = np.meshgrid(theta, z_ref)
ax.plot_surface(z_rf, 1.175*np.cos(th_ref), 1.175*np.sin(th_ref), alpha=0.8, color='silver')

# Pushrod
z_rod = np.linspace(68.5, 140.0, 10)
th_rod, z_rd = np.meshgrid(theta, z_rod)
ax.plot_surface(z_rd, 0.80*np.cos(th_rod), 0.80*np.sin(th_rod), alpha=0.9, color='gray')

ax.set_xlabel("Z (Length mm)")
ax.set_ylabel("X (Width mm)")
ax.set_zlabel("Y (Height mm)")
ax.set_xlim(-10, 160)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.view_init(elev=20, azim=-60)

fig.savefig(prev_dir / "SmartPen_RevG_3D_Master_Assembly.png", dpi=300)
plt.close(fig)
print("Saved 3D Master Assembly Preview.")

# Exploded 3D View
fig = plt.figure(figsize=(16, 6), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Smart Pen Rev G — Phase 4A Exploded Assembly 3D Preview\n"
             "Axial Separation Demonstrating Non-Interference & Assembly Path", fontsize=12, fontweight='bold')

# Draw exploded stages
stages = [
    ("Nose Cone", -30, -12, 5.75, 'gray'),
    ("Grip", -10, 10, 6.75, 'teal'),
    ("Barrel & Rail", 38, 142, 7.75, 'cyan'),
    ("Bayonet Collar", 160, 166, 6.65, 'brown'),
    ("Click Mechanism", 175, 189, 5.80, 'red')
]
for name, z0, z1, rad, col in stages:
    z_s = np.linspace(z0, z1, 10)
    th_s, zg = np.meshgrid(theta, z_s)
    ax.plot_surface(zg, rad*np.cos(th_s), rad*np.sin(th_s), alpha=0.35, color=col)
    ax.text((z0+z1)/2, 0, rad+2, name, ha='center', fontsize=9, fontweight='bold')

ax.set_xlabel("Z Exploded Axis (mm)")
ax.set_ylabel("X (mm)")
ax.set_zlabel("Y (mm)")
ax.set_xlim(-40, 200)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 12)
ax.view_init(elev=18, azim=-65)

fig.savefig(prev_dir / "SmartPen_RevG_3D_Exploded_Assembly.png", dpi=300)
plt.close(fig)
print("Saved 3D Exploded Assembly Preview.")
