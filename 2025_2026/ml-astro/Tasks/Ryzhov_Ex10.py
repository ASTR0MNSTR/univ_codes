from astroML.datasets import fetch_LINEAR_sample
import matplotlib.pyplot as plt
data = fetch_LINEAR_sample()

gr = data.targets['gr']
LP1 = data.targets['LP1'] 

rr_mask = (gr > 0.0) & (gr < 0.5) & (LP1 > -0.7) & (LP1 < 0.1)

fig, ax = plt.subplots(1, 1, figsize=(12, 6))

ax.scatter(gr, LP1, color='k', marker='.')
ax.scatter(gr[rr_mask], LP1[rr_mask], color='red', marker='.')

ax.set_xlabel('g-r')
ax.set_ylabel('log(P / days)')
ax.set_xlim(-0.5, 1.5)

plt.savefig('gr_LP1.pdf')
