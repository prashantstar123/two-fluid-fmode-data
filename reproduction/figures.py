"""Data-only renderers for the core, self-coupling, and multipole figures."""
from pathlib import Path
import json
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.path import Path as PlotPath
from matplotlib.patches import PathPatch
from .data import open_data, ROOT
from .models import PLOT_ORDER, COLORS, FRACTIONS

META={'Creator':'Matplotlib','CreationDate':None,'ModDate':None}
BASE_STYLE={'font.family':'DejaVu Sans','mathtext.fontset':'dejavusans',
            'font.size':18,'axes.labelsize':22,'axes.linewidth':1.3,'pdf.fonttype':42}
DISPLAY_LIMITS=json.loads((ROOT/'reference/display_limits.json').read_text())

def display_limits(ax,name,panel=0):
    limits=DISPLAY_LIMITS[name][panel]
    ax.set_xlim(limits['x']);ax.set_ylim(limits['y'])

def save(fig,out,name):
    fig.savefig(out/f'{name}.pdf',metadata=META)
    plt.close(fig)

def style(ax):
    ax.minorticks_on()
    ax.tick_params(which='both',direction='in',top=True,right=True)
    ax.tick_params(which='major',length=6,width=1.1)
    ax.tick_params(which='minor',length=3,width=.8)
    ax.grid(True,alpha=.23,linewidth=.65)
    ax.set_axisbelow(True)

def label_fraction(ax,p):
    ax.text(.97,.045,rf'$F_{{\rm DM}}={p}\%$',transform=ax.transAxes,
            ha='right',va='bottom',fontsize=17,
            bbox=dict(boxstyle='round,pad=.2',facecolor='white',edgecolor='.5',alpha=.92))

def observation_regions(ax,labels=False):
    with open_data('observational_display.h5') as f:
        for g in f.values():
            path=PlotPath(g['radius_mass'][:],g['path_codes'][:])
            filled=bool(g.attrs['filled'])
            ax.add_patch(PathPatch(path,facecolor=g.attrs['rgb'] if filled else 'none',
                                  edgecolor='none' if filled else g.attrs['rgb'],
                                  alpha=float(g.attrs['alpha']),linewidth=float(g.attrs['linewidth']),
                                  zorder=0,clip_on=True))
    if labels:
        for x,y,text,color in ((9.6,.78,'HESS J1731-347','#e67e22'),
                (9.65,1.23,'PSR J0437-4715','#2980b9'),(9.02,1.64,'PSR J0614-3329','#27ae60'),
                (9.02,1.84,'PSR J1614-2230','#c2185b'),(14.8,1.57,'PSR J0030+0451','#8e44ad'),
                (14.25,2.35,'PSR J0740+6620','#c0392b')):
            ax.text(x,y,text,color=color,fontsize=11,weight='bold',zorder=4)

def ensemble_legend(fig):
    handles=[Line2D([0],[0],color=COLORS[e],lw=1.8,label=e) for e in PLOT_ORDER]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.985),
               ncol=7,fontsize=11,frameon=True,columnspacing=1.,handlelength=1.8)
    fig.subplots_adjust(left=.078,right=.98,bottom=.075,top=.87,hspace=.20,wspace=.20)

def render_core(out):
    with open_data('core_sequences.h5') as f, plt.rc_context(BASE_STYLE):
        for field,name in (('R','core_MR'),('f','core_freq'),('tau','core_tau')):
            fig,axes=plt.subplots(2,2,figsize=(14,13),sharex=field=='R',sharey=field=='R')
            for panel,(ax,p) in enumerate(zip(axes.flat,FRACTIONS)):
                if field=='R':observation_regions(ax,labels=panel==0)
                for eos in PLOT_ORDER:
                    g=f[eos];b=g['pure_nm'];h=g[f'F{p}'];color=COLORS[eos]
                    m=b['M'][:];selected=m>=.5
                    if field=='R':
                        ax.plot(b['R'][:][selected],m[selected],':',color=color,lw=1.5)
                        m=h['structure/M'][:];selected=m>=.5
                        ax.plot(h['structure/R'][:][selected],m[selected],'-',color=color,lw=1.6)
                    else:
                        ax.plot(m[selected],b[field][:][selected],':',color=color,lw=1.4)
                        for branch,ls in (('NM','-'),('DM','--')):
                            z=h[branch];m=z['M'][:];y=z[field][:]
                            selected=(m>=.5)&np.isfinite(y)&(y>0)
                            ax.plot(m[selected],y[selected],ls,color=color,lw=1.6)
                if field=='R':
                    ax.set(xlim=(9,17),ylim=(.5,2.9),xlabel=r'$R_{\rm NM}$ [km]')
                    if panel%2==0:ax.set_ylabel(r'$M$ [$M_\odot$]')
                else:
                    ax.set(xlim=(.4,2.86),xlabel=r'$M$ [$M_\odot$]')
                    ax.set_ylabel(r'$f$ [kHz]' if field=='f' else r'Damping time $\tau$ [s]')
                    if field=='f':ax.set_ylim({1:(1.,3.5),5:(1.,3.8),10:(1.4,4.3),20:(1.4,5.0)}[p])
                    else:ax.set_yscale('log')
                display_limits(ax,name,panel);style(ax);label_fraction(ax,p)
                if panel==0:
                    handles=[Line2D([0],[0],color='k',ls='-',label='2-fluid' if field=='R' else 'NM-led (2F)')]
                    if field!='R':handles.append(Line2D([0],[0],color='k',ls='--',label='DM-led (2F)'))
                    handles.append(Line2D([0],[0],color='k',ls=':',label='Single-fluid (pure NM)'))
                    ax.legend(handles=handles,loc='upper left',fontsize=12,framealpha=.94)
            ensemble_legend(fig);save(fig,out,name)

LAMBDA=(('0.5pi',.5,'black'),('pi',1,'blue'),('1.5pi',1.5,'green'),('2pi',2,'red'))

def coupling_handles():
    return [Line2D([0],[0],color=c,label=rf'$\lambda={v:g}\pi$') for _,v,c in LAMBDA]

def render_coupling(out):
    with open_data('self_coupling.h5') as f,plt.rc_context(BASE_STYLE):
        fig,ax=plt.subplots(figsize=(9,7))
        observation_regions(ax)
        for tag,value,color in LAMBDA:
            for p,ls in zip(FRACTIONS,('-','--','-.',':')):
                g=f[tag][f'F{p}']['branch']
                mass=g['M'][:];radius=g['R_NM'][:]
                # Shape-preserving plotting interpolation, through saved points.
                mplot=np.linspace(mass.min(),mass.max(),1000)
                ax.plot(PchipInterpolator(mass,radius)(mplot),mplot,ls,color=color,lw=2)
        ax.set(xlim=(10.5,14.5),ylim=(0,2.95),xlabel=r'$R_{\rm NM}$ [km]',ylabel=r'$M$ [$M_\odot$]')
        display_limits(ax,'MR_lam');style(ax)
        first=ax.legend(handles=coupling_handles(),loc='upper left',fontsize=15)
        ax.add_artist(first)
        ax.legend(handles=[Line2D([0],[0],color='k',ls=ls,label=rf'$F_{{\rm DM}}={p}\%$')
                           for p,ls in zip(FRACTIONS,('-','--','-.',':'))],loc='center left',fontsize=15)
        fig.tight_layout();save(fig,out,'MR_lam')
        for field,name in (('f','freq_mass_lam'),('tau','tau_mass_lam')):
            fig,axes=plt.subplots(2,2,figsize=(13,10))
            for panel,(ax,p) in enumerate(zip(axes.flat,FRACTIONS)):
                for tag,value,color in LAMBDA:
                    for branch,ls in (('NM','-'),('DM','--')):
                        g=f[tag][f'F{p}'][branch]
                        ax.plot(g['M'][:],g[field][:],ls,color=color,lw=1.8)
                ax.set(xlabel=r'$M$ [$M_\odot$]',ylabel=r'$f$ [kHz]' if field=='f' else r'$\tau$ [s]')
                ax.set_xlim({1:(.4,2.8),5:(.4,2.65),10:(.4,2.4),20:(.5,2.05)}[p])
                if field=='f':ax.set_ylim({1:(1.2,2.5),5:(1.2,2.85),10:(1.4,3.45),20:(1.4,4.2)}[p])
                else:ax.set_yscale('log')
                display_limits(ax,name,panel);style(ax);label_fraction(ax,p)
                if panel==0:
                    l=ax.legend(handles=coupling_handles(),loc='center left',fontsize=12);ax.add_artist(l)
                    ax.legend(handles=[Line2D([0],[0],color='k',ls=ls,label=label)
                                       for ls,label in (('-','NM-led'),('--','DM-led'))],loc='upper center',fontsize=12)
            fig.tight_layout();save(fig,out,name)

def render_multipoles(out):
    with open_data('core_sequences.h5') as low,open_data('higher_multipoles.h5') as high,plt.rc_context(BASE_STYLE):
        fig,ax=plt.subplots(figsize=(10,7))
        colors=plt.get_cmap('viridis')(np.linspace(.10,.90,4))
        for p,c in zip(FRACTIONS,colors):
            for ell,source,width in ((2,low['EOS1'],1.4),(3,high,2.5)):
                for branch,ls in (('NM','-'),('DM','--')):
                    g=source[f'F{p}'][branch]
                    ax.plot(g['M'][:],g['f'][:],ls,color=c,lw=width)
        a=ax.legend(handles=[Line2D([0],[0],color=c,label=rf'$F_{{\rm DM}}={p}\%$') for p,c in zip(FRACTIONS,colors)],
                    loc='upper left',fontsize=13);ax.add_artist(a)
        ax.legend(handles=[Line2D([0],[0],color='k',lw=1.4,label=r'$\ell=2$'),
                           Line2D([0],[0],color='k',lw=2.5,label=r'$\ell=3$'),
                           Line2D([0],[0],color='k',ls='-',label='NM-led'),
                           Line2D([0],[0],color='k',ls='--',label='DM-led')],loc='lower right',fontsize=13)
        ax.set(xlim=(.2,2.85),ylim=(.8,5.2),xlabel=r'$M$ [$M_\odot$]',ylabel=r'$f$ [kHz]')
        display_limits(ax,'higher_l_modes');style(ax);fig.tight_layout();save(fig,out,'higher_l_modes')
