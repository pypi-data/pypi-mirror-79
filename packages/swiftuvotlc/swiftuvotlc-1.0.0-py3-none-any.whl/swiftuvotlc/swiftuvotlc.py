# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import gzip
import numpy as np
import matplotlib.pyplot as plt

class SwiftUVOTLC:
    """
    SwiftUVOTLC is a class to read a lightcurve file from Swift Archive.
    - file = path to file
    - isgz = True if file is gzip
    - filterobs_list = a list of filter names to be read, which is corresponding to extension names in the lightcurve file.
      - If a filter name in the list is missing from the extension names, the routine will except the filter name of the file.
      - 'default' will try to read all 6 filters of Swift UVOT except White.
    - column_list = a list of column names to be read.
      - 'default' will read AB_MAG, AB_MAG_ERR, AB_MAG_LIM, AB_FLUX_AA, AB_FLUX_AA_ERR, AB_FLUX_HZ, and AB_FLUX_HZ_ERR.
      - The routine will add time_since_trigger_sec and isupper automatically.
    Access the information, use self.table after instantiate.
    Use self.show() to plot data from self.table.
    For merging data from multiple files, use SwiftUVOTLC(file=None).merge(swiftuvotlc_list) where swiftuvotlc_list is a list of SwiftUVOTLC objects to be merged.
    """
    def __init__(self,file,isgz=True,filterobs_list='default',column_list='default'):
        self.file = file
        self.isgz = isgz
        self.filterobs_list = filterobs_list
        self.column_list = column_list
        if file is not None:
            self._fetch()
    def _fetch(self):
        filterobs_list = self._default(item='filterobs_list') if self.filterobs_list == 'default' else self.filterobs_list
        column_list = self._default(item='column_list') if self.column_list == 'default' else self.column_list
        t = fits.open(gzip.open(self.file)) if self.isgz else fits.open(self.file)
        table = {}
        for ii,i in enumerate(filterobs_list):
            try:
                tt = t[i].data
            except:
                continue
            table[i] = {}
            table[i]['time_since_trigger_sec'] = t[i].data['MET'] - t[i].header['TRIGTIME']
            table[i]['isupper'] = t[i].data['AB_MAG_LIM'] < t[i].data['AB_MAG']
            for jj,j in enumerate(column_list):
                table[i][j] = t[i].data[j]
        self.table = table
        print('Use self.table to access. Or, use self.show() to plot.')
    ##########
    ##########
    ##########
    def merge(self,swiftuvotlc_list,sort_by='default'):
        """
        To merge SwiftUVOTLC objects, use SwiftUVOTLC(file=None).merge(swiftuvotlc_list) where swiftuvotlc_list = a list of SwiftUVOTLC objects in the merge.
        - by default, sort_by
        """
        table = {}
        for ii,i in enumerate(swiftuvotlc_list):
            t = swiftuvotlc_list[ii].table
            for jj,j in enumerate(t.keys()):
                if j not in table.keys():
                    table[j] = {}
                for kk,k in enumerate(t[j].keys()):
                    if k not in table[j].keys():
                        table[j][k] = np.array([])
                    table[j][k] = np.concatenate([table[j][k],t[j][k]])
        table = self._merge_sort(table,sort_by)
        t = SwiftUVOTLC(None)
        t.table = table
        print('Use self.table to access. Or, use self.show() to plot.')
        return t
    def _merge_sort(self,table,sort_by):
        sort_by = 'time_since_trigger_sec' if sort_by=='default' else sort_by
        for ii,i in enumerate(table.keys()):
            ts = table[i][sort_by]
            m = np.argsort(ts)
            for jj,j in enumerate(table[i].keys()):
                table[i][j] = table[i][j][m]
        return table
    ##########
    ##########
    ##########
    def show(self,x='default',y='default',ey='default',
             inverty='default',
             title='default',xlabel='default',ylabel='default',
             include_lim=True,
             figsize=(5,5),fontsize_legend=10,fontsize_title=12,fontsize_xlabel=12,fontsize_ylabel=12,
             marker_point='s',markersize_point=8,
             marker_lim='v',markersize_lim=8,
             linestyle=':',
             xlim=None,ylim=None,
             xscale=None,yscale=None,
            ):
        """
        show() plots data in self.table by specifying a string of column name for x, y, ey.
        - inverty = bool. If default, True if y == 'default' and False otherwise.
        - by default: x = time_since_trigger_sec, y = AB_MAG, ey = AB_MAG_ERR, and therefore inverty = True.
        - by default: title = self.file, xlabel = Time since trigger (s), ylabel = AB mag
        - xlim, ylim, xscale, yscale can be specified using syntax from matplotlib.pyplot.
        """
        plt.figure(figsize=figsize)
        for i in self.table.keys():
            t = self.table[i]
            m = t['isupper'].astype(bool)
            tx = t['time_since_trigger_sec'] if x == 'default' else t[x]
            ty = t['AB_MAG'] if y == 'default' else t[y]
            tey = t['AB_MAG_ERR'] if ey == 'default' else t[ey]
            tt = plt.errorbar(tx[~m],ty[~m],tey[~m],marker=marker_point,markersize=markersize_point,ls=linestyle,label=i)
            tc = tt.lines[0].get_color()
            if include_lim:
                plt.plot(tx[m],ty[m],marker=marker_lim,markersize=markersize_lim,ls='',color=tc)
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        if xscale is not None:
            plt.xscale(xscale)
        if yscale is not None:
            plt.yscale(yscale)
        if inverty=='default':
            if y=='default':
                inverty = True
            else:
                inverty = False
        if inverty:
            plt.gca().invert_yaxis()
        plt.legend(loc=(1.01,0.),fontsize=fontsize_legend)
        string = self.file if title == 'default' else title
        plt.title(string,fontsize=fontsize_title)
        string = 'Time since trigger (s)' if xlabel == 'default' else xlabel
        plt.xlabel(string,fontsize=fontsize_xlabel)
        string = 'AB mag' if ylabel == 'default' else ylabel
        plt.ylabel(string,fontsize=fontsize_ylabel)
        plt.tight_layout()       
    ##########
    ##########
    ##########
    def _default(self,item):
        if item == 'filterobs_list':
            return ['UVW2','UVM2','UVW1','U','B','V']
        elif item == 'column_list':
            return ['AB_MAG','AB_MAG_ERR','AB_MAG_LIM',
                    'AB_FLUX_AA','AB_FLUX_AA_ERR',
                    'AB_FLUX_HZ','AB_FLUX_HZ_ERR']
        else:
            raise ValueError('item = {0} is not supported in self._default(item)'.format(item))
        