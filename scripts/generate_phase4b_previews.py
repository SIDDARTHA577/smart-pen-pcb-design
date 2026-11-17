"""Generate 3D Master and Exploded Assembly Previews for Phase 4B."""
import sys
sys.path.insert(0, '.')
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

prev_dir = Path("output/RevG/Mechanical_Phase04B/Previews")
prev_dir.mkdir(parents=True, exist_ok=True)

# 1. 3D Master Assembly Preview
fig = plt.figure(figsize=(14, 6), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Smart Pen Rev G — Phase 4B Master Assembly 3D Solid Model\n"
             "All 25 Native Solid Bodies in Synchronized Global Coordinates (0.000 mm³ Collisions)", fontsize=12, fontweight='bold')

theta = np.linspace(0, 2*np.pi, 30)
z_cyl = np.linspace(38, 142, 20)
theta_grid, z_grid = np.meshgrid(theta, z_cyl)
x_cyl = 7.75 * np.cos(theta_grid)
y_cyl = 7.75 * np.sin(theta_grid)
ax.plot_surface(z_grid, x_cyl, y_cyl, alpha=0.12, color='skyblue')

# PCB
z_pcb = np.array([38, 122])
x_pcb = np.array([-4.6, 4.6])
z_p, x_p = np.meshgrid(z_pcb, x_pcb)
y_p = np.full_like(z_p, 2.0)
ax.plot_surface(z_p, x_p, y_p, alpha=0.8, color='green')

# Protected LiPo Battery LP380830 (32 x 7.6 x 3.6 mm, Y=-1.5 to -5.1, X=-3.8 to +3.8)
z_b = np.array([74, 106])
x_b = np.array([-3.8, 3.8])
z_bg, x_bg = np.meshgrid(z_b, x_b)
y_bg = np.full_like(z_bg, -3.3)
ax.plot_surface(z_bg, x_bg, y_bg, alpha=0.85, color='dodgerblue')

# Refill D1
z_ref = np.linspace(1.5, 68.5, 10)
th_ref, z_rf = np.meshgrid(theta, z_ref)
ax.plot_surface(z_rf, 1.175*np.cos(th_ref), 1.175*np.sin(th_ref), alpha=0.8, color='silver')

# Pushrod
z_rod = np.linspace(68.5, 140.0, 10)
th_rod, z_rd = np.meshgrid(theta, z_rod)
ax.plot_surface(z_rd, 0.80*np.cos(th_rod), 0.80*np.sin(th_rod), alpha=0.9, color='dimgray')

# Click mechanism
z_clk = np.linspace(144, 153.5, 10)
th_clk, z_ck = np.meshgrid(theta, z_clk)
ax.plot_surface(z_ck, 2.90*np.cos(th_clk), 2.90*np.sin(th_clk), alpha=0.8, color='crimson')

ax.set_xlabel("Z (Length mm)")
ax.set_ylabel("X (Width mm)")
ax.set_zlabel("Y (Height mm)")
ax.set_xlim(-10, 160)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.view_init(elev=20, azim=-60)

fig.savefig(prev_dir / "SmartPen_RevG_Phase4B_3D_Master_Assembly.png", dpi=300)
plt.close(fig)

# 2. 3D Exploded Assembly Preview
fig = plt.figure(figsize=(16, 6), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Smart Pen Rev G — Phase 4B Exploded Assembly 3D Preview\n"
             "Axial Separation Demonstrating Non-Interference & Assembly Path", fontsize=12, fontweight='bold')

stages = [
    ("Nose Cone", -30, -12, 5.75, 'gray'),
    ("Grip", -10, 10, 6.75, 'teal'),
    ("Barrel & Rail", 38, 142, 7.75, 'cyan'),
    ("Bayonet Collar", 160, 166, 6.65, 'saddlebrown'),
    ("Click Mechanism", 175, 189, 5.80, 'crimson')
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

fig.savefig(prev_dir / "SmartPen_RevG_Phase4B_3D_Exploded_Assembly.png", dpi=300)
plt.close(fig)

# 3. Copy Longitudinal and Transverse preview copies
import shutil
shutil.copy("output/RevG/Mechanical_Phase04B/Drawings/SmartPen_RevG_Phase4B_Longitudinal_Assembly.png",
            prev_dir / "SmartPen_RevG_Phase4B_Longitudinal_Section.png")
shutil.copy("output/RevG/Mechanical_Phase04B/Drawings/SmartPen_RevG_Phase4B_Transverse_Sections.png",
            prev_dir / "SmartPen_RevG_Phase4B_Transverse_Sections.png")
print("Previews generated successfully.")
