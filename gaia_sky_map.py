
import numpy as np
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u

# 1. Retrieve a sample of stars from Gaia DR3
query = """
SELECT TOP 20000
    source_id,
    ra,
    dec,
    phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE ra IS NOT NULL
  AND dec IS NOT NULL
  AND phot_g_mean_mag < 17
ORDER BY random_index
"""

print("Connecting to Gaia DR3...")
job = Gaia.launch_job_async(query, dump_to_file=False)
stars = job.get_results()

if len(stars) == 0:
    raise RuntimeError("No stars were returned by Gaia.")

print(f"Retrieved {len(stars)} stars.")

# 2. Extract equatorial coordinates
ra_deg = np.asarray(stars["ra"], dtype=float)
dec_deg = np.asarray(stars["dec"], dtype=float)

# 3. Convert equatorial coordinates to Galactic coordinates
coordinates = SkyCoord(
    ra=ra_deg * u.deg,
    dec=dec_deg * u.deg,
    frame="icrs"
)

galactic = coordinates.galactic

# Put Galactic longitude in the range -180 to +180 degrees
longitude = galactic.l.wrap_at(180 * u.deg).degree
latitude = galactic.b.degree

# 4. Add Galactic coordinates to the table
stars["galactic_longitude_deg"] = longitude
stars["galactic_latitude_deg"] = latitude

# 5. Save the data
stars.write(
    "gaia_sky_map.csv",
    format="ascii.csv",
    overwrite=True
)

# 6. Plot the distribution of stars
plt.figure(figsize=(12, 6))

plt.scatter(
    longitude,
    latitude,
    s=1,
    alpha=0.45
)

# Centre Galactic longitude at zero
plt.xlim(180, -180)
plt.ylim(-90, 90)

plt.xlabel("Galactic longitude (degrees)")
plt.ylabel("Galactic latitude (degrees)")
plt.title("Gaia DR3: Distribution of Sampled Stars")
plt.grid(True, alpha=0.25)
plt.tight_layout()

# 7. Save the map
plt.savefig("gaia_sky_map.png", dpi=200)

print("Saved gaia_sky_map.csv")
print("Saved gaia_sky_map.png")

plt.show()
