
import numpy as np
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia

# Query a sample of stars from Gaia Data Release 3
query = """
SELECT TOP 500
    source_id,
    ra,
    dec,
    parallax,
    parallax_error,
    parallax_over_error,
    phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE parallax IS NOT NULL
  AND parallax > 0
  AND parallax_over_error >= 10
  AND phot_g_mean_mag IS NOT NULL
ORDER BY random_index
"""

print("Connecting to the Gaia Archive...")
job = Gaia.launch_job_async(query, dump_to_file=False)
stars = job.get_results()

if len(stars) == 0:
    raise RuntimeError("The Gaia query returned no stars.")

# Approximate distance: parsecs = 1000 / parallax in milliarcseconds
parallax_mas = np.asarray(stars["parallax"], dtype=float)
distance_pc = 1000.0 / parallax_mas

stars["estimated_distance_pc"] = distance_pc

# Save the catalogue sample locally
stars.write(
    "gaia_stars_sample.csv",
    format="ascii.csv",
    overwrite=True
)

# Plot apparent brightness against estimated distance
magnitude = np.asarray(stars["phot_g_mean_mag"], dtype=float)

plt.figure(figsize=(9, 6))
plt.scatter(distance_pc, magnitude, s=16, alpha=0.65)
plt.gca().invert_yaxis()
plt.xlabel("Estimated distance (parsecs)")
plt.ylabel("Gaia G-band apparent magnitude")
plt.title("Gaia DR3: Stellar Brightness vs Distance")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("gaia_stellar_distances.png", dpi=150)
print(f"Retrieved {len(stars)} stars.")
print("Saved gaia_stars_sample.csv")
print("Saved gaia_stellar_distances.png")

plt.show()
