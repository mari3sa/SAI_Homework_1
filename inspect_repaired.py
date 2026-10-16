from pathlib import Path
import sys,struct
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/pythonlibs'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def points(path):
    xyz=[]; rgb=[]
    with path.open('rb') as f:
        n=struct.unpack('<Q',f.read(8))[0]
        for _ in range(n):
            v=struct.unpack('<QdddBBBd',f.read(43)); xyz.append(v[1:4]); rgb.append(v[4:7])
            track=struct.unpack('<Q',f.read(8))[0]; f.seek(8*track,1)
    return np.array(xyz),np.array(rgb)/255
fig,axs=plt.subplots(1,3,figsize=(14,5),squeeze=False)
for row,n in enumerate((9,)):
    p,c=points(ROOT/'experiments/repaired/workspace/sparse/0/points3D.bin')
    center=np.median(p,axis=0)
    # Robust central region for readable projections; does not modify models.
    lo,hi=np.percentile(p,[2,98],axis=0)
    keep=((p>=lo)&(p<=hi)).all(axis=1)
    _,_,vt=np.linalg.svd(p[keep]-center,full_matrices=False)
    q=(p-center)@vt.T
    for col,(a,b) in enumerate(((0,1),(0,2),(1,2))):
        ax=axs[row,col]; ax.set_facecolor('#333333')
        ax.scatter(q[:,a],q[:,b],c=c,s=2)
        lim=np.percentile(q,[2,98],axis=0)
        ax.set_xlim(lim[0,a],lim[1,a]);ax.set_ylim(lim[0,b],lim[1,b]);ax.set_aspect('equal')
        ax.set_title(f'{n} foto input - {len(p)} punti / proiezione {a+1}-{b+1}')
        ax.set_xlabel('Scala arbitraria');ax.set_ylabel('Scala arbitraria')
fig.suptitle('Riparazione: 6 foto iniziali + 3 nuove viste\nAssi PCA indipendenti; vista limitata ai percentili 2-98 per leggibilita',fontsize=14)
fig.tight_layout(rect=(0,0,1,.94))
fig.savefig(ROOT/'report/repaired_clouds.png',dpi=150,bbox_inches='tight')
print(ROOT/'report/repaired_clouds.png')
