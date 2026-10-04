"""Draw the two representative eigenfunction figures from saved profiles."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from .data import open_data
from .figures import META

STYLE={'font.family':'serif','font.serif':['cmr10','STIXGeneral','DejaVu Serif'],
       'mathtext.fontset':'cm','axes.formatter.use_mathtext':True,'font.size':11,
       'axes.labelsize':15,'xtick.labelsize':12,'ytick.labelsize':12,
       'legend.fontsize':11,'axes.linewidth':1.1,'xtick.major.size':5,'ytick.major.size':5}

def render_radial(out):
    with open_data('eigenfunctions_0501.h5') as f,plt.rc_context(STYLE):
        r=f['radius_km'][:];rd=float(f['R_DM_km'][()]);rn=float(f['R_NM_km'][()])
        nd=int(np.searchsorted(r,rd,side='right'));nn=int(np.searchsorted(r,rn,side='right'))
        fig,axes=plt.subplots(1,2,figsize=(7.2,3.55),sharey=True)
        for panel,ax,key in zip(('(a)','(b)'),axes,('nm_led','dm_led')):
            wd=f[f'W_DM_{key}'][:];wn=f[f'W_NM_{key}'][:]
            ax.plot(r[:nd],wd[:nd],color='#D55E00',lw=2.1,label=r'$W_{\rm DM}$')
            ax.plot(r[:nn],wn[:nn],color='#0072B2',lw=2.1,label=r'$W_{\rm NM}$')
            ax.axvline(rd,color='.45',ls='--',lw=1.25);ax.axvline(rn,color='.45',ls=':',lw=1.25)
            ax.axhline(0,color='.15',lw=.65)
            transform=blended_transform_factory(ax.transData,ax.transAxes)
            for x,label in ((rd,r'$R_{\rm DM}$'),(rn,r'$R_{\rm NM}$')):
                ax.text(x,.34,label,transform=transform,rotation=90,fontsize=10,va='center',ha='right',color='.3',
                        bbox=dict(boxstyle='round,pad=.12',fc='white',ec='none',alpha=.85))
            ax.set(xlim=(0,rn*1.02),ylim=(-.25,1.18),xlabel=r'$r$ [km]')
            ax.minorticks_on();ax.tick_params(which='both',direction='in',top=True,right=True);ax.grid(alpha=.22,lw=.6)
            ax.text(.035,.94,panel,transform=ax.transAxes,fontsize=13,va='top')
            ax.legend(loc='upper center',ncol=2,handlelength=1.7,columnspacing=1.1,borderpad=.4,fontsize=11)
            values=wd[:nd] if key=='nm_led' else wn[:nn]
            low,high=values.min(),values.max();pad=.35*(high-low)+.004
            small=inset_axes(ax,width='40%',height='31%',loc='lower right' if key=='nm_led' else 'center right',borderpad=1.25)
            small.plot(r[:nd],wd[:nd],color='#D55E00',lw=1.35)
            small.plot(r[:nn],wn[:nn],color='#0072B2',lw=1.35)
            small.axvline(rd,color='.45',ls='--',lw=.9);small.axhline(0,color='.15',lw=.5)
            small.set(xlim=(0,rn*1.02),ylim=(low-pad,high+pad))
            small.minorticks_on();small.tick_params(which='both',direction='in',top=True,right=True,labelsize=9,length=3)
            label=r'zoom: $W_{\rm DM}$' if key=='nm_led' else r'zoom: $W_{\rm NM}$'
            small.text(.05,.93,label,transform=small.transAxes,fontsize=9,va='top',
                       bbox=dict(boxstyle='round,pad=.18',fc='white',ec='.6',lw=.5,alpha=.85))
        axes[0].set_ylabel(r'$W_X/\max|W_X|$')
        fig.subplots_adjust(left=.09,right=.99,bottom=.17,top=.985,wspace=.08)
        fig.savefig(out/'fig01_core_eigenfunctions.pdf',bbox_inches='tight',metadata=META);plt.close(fig)

def render_metric(out):
    with open_data('eigenfunctions_1400.h5') as f,plt.rc_context(STYLE|{'font.size':13,'axes.labelsize':17,
             'axes.titlesize':17,'xtick.labelsize':14,'ytick.labelsize':14,'legend.fontsize':14}):
        rn=f['r_NM_km'][:];rd=f['r_DM_km'][:]
        fig,axes=plt.subplots(2,3,figsize=(18,10))
        for j,branch in enumerate(('NM','DM')):
            g=f[branch]
            for k,(inner,outer,letter) in enumerate((('WI','WO','W'),('VI','VO','V'))):
                axes[j,k].plot(rd,g[inner][:],color='#D55E00',lw=2.4,label=rf'${letter}_{{\rm DM}}$ (inner)')
                axes[j,k].plot(rn,g[outer][:],color='#0072B2',lw=2.4,label=rf'${letter}_{{\rm NM}}$ (outer)')
            for key,label,color,ls in (('H0',r'$H_0$','#009E73','-'),('H1',r'$H_1$','#CC79A7','-'),('K',r'$K$','#7030A0','--')):
                axes[j,2].plot(rn,g[key][:],color=color,lw=2.4,ls=ls,label=label)
            label=r'$f^O$ (NM-led)' if j==0 else r'$f^I$ (DM-led)'
            axes[j,0].set_ylabel(label+'\n\nnormalized')
            for k,ax in enumerate(axes[j]):
                ax.axvline(f.attrs['R_DM_km'],ls=':',color='.45',lw=1.4);ax.axhline(0,color='.1',lw=.6)
                ax.set_xlim(0,f.attrs['R_NM_km']*1.02);ax.minorticks_on()
                ax.tick_params(which='both',direction='in',top=True,right=True);ax.grid(alpha=.25,lw=.6)
                ax.legend(loc='best',handlelength=1.8,framealpha=.9)
                if j==1:ax.set_xlabel(r'$r$ [km]')
                if j==0:ax.set_title((r'Radial displacement $W(r)$',r'Transverse displacement $V(r)$',r'Shared metric $H_0,\,H_1,\,K$')[k],pad=8)
            axes[j,0].text(.05,.08,rf'$f={g.attrs["frequency_kHz"]:.3f}$ kHz'+'\n'+rf'$\tau={g.attrs["tau_s"]:.3g}$ s',
                           transform=axes[j,0].transAxes,fontsize=13,va='bottom',
                           bbox=dict(boxstyle='round,pad=.3',fc='white',ec='.6',alpha=.9))
        fig.tight_layout();fig.savefig(out/'fig02_core_edge.pdf',bbox_inches='tight',metadata=META);plt.close(fig)
