
import numpy as np
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u

# --------------------------------------------------
# PROJECT 5: 3D MAP OF NEARBY STARS
# Data source: Gaia Data Release 3
# --------------------------------------------------

# 1. Query stars with relatively precise parallaxes
query = """
SELECT TOP 3000
    source_id,
    ra,
    dec,
    parallax,
    parallax_error,
    parallax_over_error,
    phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE ra IS NOT NULL
  AND dec IS NOT NULL
  AND parallax > 5
  AND parallax_over_error >= 10
  AND phot_g_mean_mag IS NOT NULL
  AND random_index < 100000000
"""

print("Connecting to Gaia DR3...")

job = Gaia.launch_job_async(query, dump_to_file=False)
stars = job.get_results()

if len(stars) == 0:
    raise RuntimeError("No stars were returned by Gaia.")

print(f"Retrieved {len(stars)} stars.")

# 2. Extract parallax measurements
parallax_mas = np.asarray(stars["parallax"], dtype=float)

# 3. Estimate distances in parsecs
distance_pc = 1000.0 / parallax_mas

# 4. Convert equatorial coordinates into Galactic coordinates
coordinates = SkyCoord(
    ra=np.asarray(stars["ra"], dtype=float) * u.deg,
    dec=np.asarray(stars["dec"], dtype=float) * u.deg,
    distance=distance_pc * u.pc,
    frame="icrs"
)

galactic = coordinates.galactic

# 5. Extract 3D Cartesian positions in parsecs
x_pc = galactic.cartesian.x.to_value(u.pc)
y_pc = galactic.cartesian.y.to_value(u.pc)
z_pc = galactic.cartesian.z.to_value(u.pc)

# 6. Add calculated measurements to the table
stars["estimated_distance_pc"] = distance_pc
stars["galactic_x_pc"] = x_pc
stars["galactic_y_pc"] = y_pc
stars["galactic_z_pc"] = z_pc

# 7. Save the data
stars.write(
    "gaia_3d_stellar_map.csv",
    format="ascii.csv",
    overwrite=True
)

# 8. Create the 3D plot
fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection="3d")

scatter = ax.scatter(
    x_pc,
    y_pc,
    z_pc,
    c=distance_pc,
    cmap="viridis",
    s=5,
    alpha=0.7
)

ax.set_xlabel("Galactic X (pc)")
ax.set_ylabel("Galactic Y (pc)")
ax.set_zlabel("Galactic Z (pc)")

ax.set_title("Gaia DR3: 3D Map of Nearby Stars")

colorbar = plt.colorbar(scatter, ax=ax, pad=0.1)
colorbar.set_label("Estimated Distance (pc)")

plt.tight_layout()

# 9. Save and display the figure
plt.savefig("gaia_3d_stellar_map.png", dpi=200)

print("Saved gaia_3d_stellar_map.csv")
print("Saved gaia_3d_stellar_map.png")

plt.show()
