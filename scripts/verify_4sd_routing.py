import os, sys, math
os.environ["WXSUPPRESS_SIZER_FLAGS_CHECK"] = "1"
try:
    import wx; wx.DisableAsserts()
except: pass
import pcbnew

b = pcbnew.LoadBoard('scratch_test_restore_vsys.kicad_pcb')

# Let's inspect all coordinates and constraints
print("Board loaded successfully.")
print(f"Total tracks: {len(b.GetTracks())}")
