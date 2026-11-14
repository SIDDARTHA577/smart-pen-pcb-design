import os

# Check footprints in SmartPen.pretty
mod_dir = 'output/RevG/SmartPen.pretty'
mods = os.listdir(mod_dir)
print('Footprints in SmartPen.pretty:')
for m in sorted(mods):
    print(' ', m)

