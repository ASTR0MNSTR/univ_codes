from astroquery.sdss import SDSS
from astropy.table import Table
import matplotlib.pyplot as plt

# Query SDSS for quasars (class = 'QSO') 
query = """
SELECT TOP 10000
    specObj.z AS redshift,
    photoObj.psfMag_r AS mag_r,
    photoObj.psfMag_i AS mag_i
FROM SpecObj AS specObj
JOIN PhotoObj AS photoObj
ON specObj.bestObjID = photoObj.objID
WHERE specObj.class = 'QSO'
AND specObj.z BETWEEN 0 AND 5
"""

# Run query
data = SDSS.query_sql(query)

# Convert to numpy arrays
z = data['redshift'].data
r = data['mag_r'].data
i = data['mag_i'].data

# Compute color index
ri = r - i

# Plot
plt.figure(figsize=(6,4))
plt.scatter(z, ri, s=1, alpha=0.5)
plt.xlabel('Redshift')
plt.ylabel('r - i Color Index')
plt.title('SDSS Quasar Colours r-i vs Redshift')
plt.grid(True)
plt.savefig('quasar.pdf')
