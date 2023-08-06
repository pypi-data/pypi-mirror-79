#!/usr/bin/env python
#

""" Library containing field information """
import os
import numpy as np
from pandas import read_csv
from astropy import units
import matplotlib.pyplot as mpl
from matplotlib.patches import Polygon

_FIELD_SOURCE = os.path.dirname(os.path.realpath(__file__))+"/data/ztf_fields.txt"
FIELD_DATAFRAME = read_csv(_FIELD_SOURCE)

_CCD_COORDS  = read_csv(os.path.dirname(os.path.realpath(__file__))+"/data/ztf_ccd_layout.tbl") # corner of each CCDS
_ccd_xmin, _ccd_xmax = np.percentile(_CCD_COORDS["EW"], [0,100])
_ccd_ymin, _ccd_ymax = np.percentile(_CCD_COORDS["NS"], [0,100])
CCD_EDGES_DEG = np.asarray([[ _ccd_xmin, _ccd_ymin], [ _ccd_xmin, _ccd_ymax],
                            [_ccd_xmax, _ccd_ymax], [_ccd_xmax, _ccd_ymin]])


FIELD_COLOR = {1: "C2", 2: "C3", 3:"C1"}
FIELDNAME_COLOR = {"zg": "C2", "zr":"C3", "zi":"C1"}


##############################
#                            #
#  Fields and References     #
#                            #
##############################

def has_field_reference(fieldid, ccdid=1, qid=1, **kwargs):
    """ get the following dictionary {zg:bool, zr:bool, zi:bool}
    where bool is True if the field has a reference image and false otherwise
    
    **kwargs goes to load_metadata(), for instance auth=[username, password]
    Returns
    -------
    {zg:bool, zr:bool, zi:bool}
    """
    from .query import ZTFQuery
    zquery_ = ZTFQuery()
    zquery_.load_metadata(kind="ref", sql_query="field=%s and ccdid=%s and qid=%s"%(fieldid,ccdid,qid), **kwargs)
    return {k: k in zquery_.metatable["filtercode"].values for k in ["zg", "zr","zi"]}

def get_fields_with_band_reference(filter_, ccdid=1, qid=1, **kwargs):
    """ returns the list of fieldid that have a reference image in the `filter_` band.
    filter_ is a filtercode entry [zg, zr or zg]
    
    **kwargs goes to load_metadata(), for instance auth=[username, password]
    Returns
    -------
    list of fieldid
    """
    from .query import ZTFQuery
    zquery_ = ZTFQuery()
    zquery_.load_metadata(kind="ref",
            sql_query="filtercode='%s' and ccdid=%s and qid=%s"%(filter_,ccdid,qid), **kwargs)
    return zquery_.metatable["field"].values

def show_reference_map(band, **kwargs):
    """ Display the 'field plot' in which field with image reference in the given band are colored. """
    title   = "Fields with reference in the %s-band"%band[1]
    field_i = get_fields_with_band_reference(band)
    return show_fields(field_i, facecolor=FIELDNAME_COLOR[band], alpha=0.3, title=title, **kwargs)
    
##############################
#                            #
#  Generic Tools             #
#                            #
##############################
def fields_in_main(field):
    """ """
    return np.asarray(np.atleast_1d(field), dtype="int")<880

def field_to_coords(fieldid, system="radec"):
    """ Returns the central coordinate [RA,Dec] or  of the given field 

    Parameters
    ----------
    fieldid: [int]
        single field ID

    system: [string] -optional-
        which coordinate system ?
        radec / galactic / ecliptic (default radec)

    Returns
    -------
    [[x_i, y_i],[]]... (depending on your coordinate system)
    Remark if only 1 fieldid given, you have [[x,y]] (not [x,y])
    """
    if system in ["radec", "RADec","RA,Dec", "ra,dec"]:
        syst = ["RA", "Dec"]
    elif system.lower() in ["gal","galactic"]:
        syst = ["Gal Long","Gal Lat"]
    elif system.lower() in ["ecl","ecliptic"]:
        syst = ["Ecl Long","Ecl Lat"]
    else:
        raise ValueError("unknown coordinate system %s select among: [radec / galactic / ecliptic]"%system)
    fieldid = np.atleast_1d(fieldid)
    radec = np.asarray(FIELD_DATAFRAME[np.in1d(FIELD_DATAFRAME['ID'], fieldid)][syst].values)
    
    return radec


def get_camera_corner(ra_field, dec_field, steps=5,
                inrad=True, origin=0, east_left=False):
        """ """
        from .utils.tools import rot_xz_sph, _DEG2RA
        # Top (left to right)
        dec1 = np.ones(steps) * _ccd_ymax
        ra1 = np.linspace(_ccd_xmin, _ccd_xmax, steps) / np.cos(_ccd_ymax*_DEG2RA)
        
        # Right (top to bottom)
        dec2 = np.linspace(_ccd_ymax, _ccd_ymin, steps)
        ra2 = _ccd_ymax/np.cos(dec2*_DEG2RA)

        # Bottom (right to left)
        dec3 = np.ones(steps) * (_ccd_ymin)
        ra3 = np.linspace(_ccd_xmax,_ccd_xmin, steps) / np.cos(_ccd_ymax*_DEG2RA)
        
        # Left (bottom to top)
        dec4 = np.linspace(_ccd_ymin,_ccd_ymax, steps)
        ra4 = _ccd_ymin/np.cos(dec4*_DEG2RA)
        #
        # 
        ra_bd = np.concatenate((ra1, ra2, ra3, ra4  ))  
        dec_bd = np.concatenate((dec1, dec2, dec3,dec4 )) 

        ra, dec = rot_xz_sph(ra_bd, dec_bd, dec_field)
        ra += ra_field

        
        ra -= origin # assumes center = 180

        if inrad:
            ra *= _DEG2RA
            dec *= _DEG2RA
        
        if east_left:
            ra = -ra
            
        return np.asarray([ra,dec]).T

# ===================== #
#                       #
#    SHOW FIELD         #
#                       #
# ===================== #
def show_fields(field_val,ax=None, savefile=None,
                show_ztf_fields=True, title=None,
                colorbar=True, cax=None, clabel=" ", 
                cmap="viridis",origin=180,
                facecolor=None, 
                vmin=None, vmax=None,  **kwargs):
    """ 
    Parameters
    ----------
    colored_by: 
    """
    import warnings
    import matplotlib.pyplot as mpl
    
    if origin != 180:
        warnings.warn("Only the origin 180 has been implemented. boundaries issue arises otherwise. origin set to 180")
        origin = 180
            
    tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
    tick_labels = np.remainder(tick_labels+360+origin,360)

    # - Axes definition
    if ax is None:
        fig = mpl.figure(figsize=(8,5))
        ax = fig.add_subplot(111, projection="hammer")
    else:
        fig = ax.figure

    ax.set_xticklabels(tick_labels)     # we add the scale on the x axis
    # - Plotting
    if show_ztf_fields:
        show_ZTF_fields(ax)

    # Removing the NaNs
    if type(field_val)==dict:
        
        field_val = {f:v for f,v in field_val.items() if not np.isnan(v)}
        values = list(field_val.values())
        if len(values)==0 or not np.any(values):
            if cax is not None:
                cax.set_visible(False)
            return
        
        if vmin is None: vmin = "0"
        if type(vmin) == str: vmin=np.percentile(values, float(vmin))
        if vmax is None: vmax = "100"
        if type(vmax) == str: vmax=np.percentile(values, float(vmax))
        if type(cmap) == str: cmap = mpl.get_cmap(cmap)
        for f,v in field_val.items():
            display_field(ax, f,
                    facecolor=cmap((v-vmin)/(vmax-vmin)) if vmax-vmin !=0 else cmap(0),origin=origin, 
                    **kwargs)

        if colorbar:
            if vmax-vmin !=0:
                from .utils.tools import insert_ax, colorbar
                if cax is None: cax = insert_ax(ax, "bottom",
                                            shrunk=0.93, space=-0.0, axspace=0.02)
                colorbar(cax, cmap, vmin=vmin, vmax=vmax, label=clabel)
            elif cax is not None:
                cax.set_visible(False)
    else:
        field_val = np.atleast_1d(field_val)
        for f in field_val:
            display_field(ax, f,
                        facecolor=facecolor,origin=origin, 
                    **kwargs)

    if title is not None:
        fig.text(0.5,0.9, title,
                     va="top", ha="center", fontsize="large")
    # Output
    if savefile is not None:
        fig.savefig(savefile, dpi=150)
        
    return {"ax":ax,"fig":fig}
                
    
def show_ZTF_fields(ax, maingrid=True, lower_dec=-30, alpha=0.1, facecolor="0.8", edgecolor="0.8", **kwargs):
    """ """
    if maingrid:
        allfields = FIELD_DATAFRAME[FIELD_DATAFRAME["ID"]<880]['ID'].values
    else:
        allfields = FIELD_DATAFRAME[FIELD_DATAFRAME["ID"]>999]['ID'].values
        
    return display_field(ax, allfields, lower_dec=lower_dec, alpha=alpha,
                      facecolor=facecolor, edgecolor=edgecolor, **kwargs)
    
def display_field(ax, fieldid, origin=180, facecolor="0.8", lower_dec=None, edgecolor=None, **kwargs):
    """ """
    p = {}
#    for ra,dec in field_to_coords( np.asarray(np.atleast_1d(fieldid), dtype="int")   ):
    for i,f_ in enumerate(fieldid):
        ra, dec = np.asarray(field_to_coords(f_), dtype="int")[0]
        if lower_dec is not None and dec<lower_dec:
            continue
        p_ = ax.add_patch(Polygon( get_camera_corner(ra,dec, inrad=True, origin=origin, east_left=True),
                                facecolor=facecolor,edgecolor=edgecolor, **kwargs))
        p[f_] = p_
        
    return p

def get_field_vertices(fieldid, origin=180, indeg=True):
    """ """
    coef = 1 if not indeg else 180/np.pi
    return np.asarray([ get_camera_corner(ra,dec, inrad=True, origin=origin, east_left=True)
                        for ra,dec in field_to_coords( np.asarray(np.atleast_1d(fieldid), dtype="int")   )])*coef

def get_fields_containing_target(ra,dec, origin=180):
    """ return the list of fields into which the position ra, dec is. 
    Remark that this is based on predefined field positions. Hence, small attrition could affect this.

    Parameters
    ----------
    ra,dec: [float,float]
       coordinates in degree. 

    origin: [float] -optional-
       If ra is defined between 0 and 360, use origin=360. [default]
       If ra is defined between -180 and 180 use origin=180
       
    Returns
    -------
    list (all the field ID that contain the given ra,dec coordinates)
    """
    try:
        from shapely import geometry
    except ImportError:
        raise ImportError("You need shapely to use this function. pip install shapely")

    coordpoint = geometry.Point(ra,dec)
    return [f for f in FIELD_DATAFRAME["ID"].values
            if geometry.Polygon( get_field_vertices(f, origin=origin)[0]).contains(coordpoint)]
        
##############################
#                            #
#  Individual Field Class    #
#                            #
##############################


##############################
#                            #
#  Individual Field Class    #
#                            #
##############################
class Field():
    """ """
    def __init__(self, fieldid=None, ra=None, dec=None):
        """ """
        self.id = "Unkown" if fieldid is None else fieldid
        # Coordinates
        if ra is not None and dec is not None:
            self.set_radec(ra, dec)
            
        elif id is not None:
            datafield = load_fields_data()
            self.set_radec(*field_to_radec(fieldid))
        

    
    # ================== #
    #    Methods         #
    # ================== #
    # --------- #
    #  SETTER   #
    # --------- #
    
    

    # --------- #
    #  SETTER   #
    # --------- #
    def set_radec(self, ra, dec):
        """ Set the field coordinates """
        self.ra, self.dec  = ra, dec


    def display(self, ax):
        """ """

        
    # ================== #
    #   Properties       #
    # ================== #
    

##############################
#                            #
#    ZTF Fields Class        #
#                            #
##############################
def load_fields_data():
    """ Pandas DataFrame containing field information
    (See http://noir.caltech.edu/twiki_ptf/bin/view/ZTF/ZTFFieldGrid)
    """
    return read_csv(_FIELD_SOURCE)

class ZTFFields():
    """ """
    def __init__(self):
        """ """
        self._fieldsdata = load_fields_data()

    # ================== #
    #   Properties       #
    # ================== #
    @property
    def fieldsdata(self):
        """ Pandas DataFrame containing ztf field information.
        Primary Grid patern have ID<1000 ; Secondary are field >1000
        """
        return self._fieldsdata





class FieldAnimation():
    
    def __init__(self, fields, dates=None, facecolors=None, alphas=None, edgecolors=None):
        """ """
        self.set_fields(fields)
        self.set_dates(dates)
        self.set_properties(facecolors=facecolors, alphas=alphas, edgecolors=edgecolors)
        self.load_ax()
    # ================= #
    #   Methods         #
    # ================= #
    
    # ---------- #
    #  SETUP     #
    # ---------- #
    def load_ax(self, dpi=100, iref=0):
        """ """
        self.fig = mpl.figure(figsize=(8,5))
        self.ax = self.fig.add_axes([0.1,0.1,0.9,0.9], projection="hammer")
        self.fig.set_dpi(dpi)

        # Build the first
        self.poly_ = Polygon(self.field_vertices[self.fields[0]],
                        facecolor=self.display_prop["facecolor"][0],
                        edgecolor=self.display_prop["edgecolor"][0],
                        alpha=self.display_prop["alpha"][0])
        if self._dates is not None:
            self.text_ = self.fig.text(0.01,0.99, self._dates[0],
                                           va="top", ha="left", weight="bold")
            
        p_ = self.ax.add_patch(self.poly_)
        
    def set_dates(self, dates):
        """ """
        self._dates = np.atleast_1d(dates) if dates is not None else None

    def set_fields(self, fields):
        """ """
        self._fields = fields
        self._unique_fields = np.unique(self._fields)
        self._field_vertices = fv = {k:v for k,v in zip(np.unique(self._unique_fields),
                                                        get_field_vertices(self._unique_fields, indeg=False))}
        
    def set_properties(self, facecolors=None, edgecolors=None, alphas=None):
        """ """
        self._display_prop = {}
        self._set_prop_("facecolor", facecolors, "0.7")
        self._set_prop_("edgecolor", edgecolors, "None")
        self._set_prop_("alpha", alphas, 1)

    def _set_prop_(self, key, value, default=None):
        """ """
        if not hasattr(self,"_display_prop"):
            self._display_prop = {}
            
        if value is None:
            value = default
            
        if len(np.atleast_1d(value)) == 1:
            self.display_prop[key] = np.atleast_1d(value)
            self.display_prop[f"unique_{key}"] = True
        else:
            self.display_prop[key] = value
            self.display_prop[f"unique_{key}"] = False
        

    # ---------- #
    #  Animate   #
    # ---------- #
    def init(self):
        """ """
        return self.poly_
    
    def update_field_to(self, i):
        """ """
        try:
            self.poly_.set_xy(self.field_vertices[ self.fields[i] ])
            if self.dates is not None and len(self.dates)>1:
                self.text_.set_text(self.dates[i])
        except:
            print(f"FAILES for i={i}")
            
        for key in ["facecolor","edgecolor","alpha"]:
            if not self.display_prop[f"unique_{key}"]:
                getattr(self.poly_,f"set_{key}")(self.display_prop[key][i])
        return self.poly_

    def launch(self, interval=5, repeat=False, blit=True, savefile=None):
        """ """
        from matplotlib import animation
        self.anim = animation.FuncAnimation(self.fig, self.update_field_to,
                                                init_func=self.init,
                               frames=self.nfields, interval=interval, repeat=repeat, blit=blit)
        
    # ================= #
    #   Properties      #
    # ================= #
    @property
    def fields(self):
        """ Fields that should be shown """
        return self._fields

    @property
    def dates(self):
        """ Observation dates if any """
        return self._dates
    @property
    def nfields(self):
        """ size of self.fields """
        return len(self.fields)

    @property
    def field_vertices(self):
        """ vertices of the fields """
        return self._field_vertices

    @property
    def display_prop(self):
        """ """
        return self._display_prop
