import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure

def bytescale(data, high=255, low=0, cmin=None, cmax=None):
    if data.dtype == "uint8":
        return data

    if high > 255:
        raise ValueError("`high` should be less than or equal to 255.")
    if low < 0:
        raise ValueError("`low` should be greater than or equal to 0.")
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")

    if cmin is None or (cmin < data.min()):
        cmin = float(data.min())

    if (cmax is None) or (cmax > data.max()):
        cmax = float(data.max())

    # Calculate range of values
    crange = cmax - cmin
    if crange < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif crange == 0:
        raise ValueError(
            "`cmax` and `cmin` should not be the same value. Please specify "
            "`cmax` > `cmin`"
        )

    scale = float(high - low) / crange

    # If cmax is less than the data max, then this scale parameter will create
    # data > 1.0. clip the data to cmax first.
    data[data > cmax] = cmax
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype("uint8")

def _stretch_im(arr, str_clip,fillvalue, first_call, lowers, uppers, log_flag=0,cloud_mask=None):

    s_min = str_clip*1
    s_max = 100 - str_clip*2
    arr_rescaled = np.zeros_like(arr)

    if first_call==1: lowers=[];uppers=[]

    if log_flag==1:
        arr=arr.astype(float)

    for ii, band in enumerate(arr):

        if cloud_mask is None:
            good=np.where(band != fillvalue)
        else:
            good=np.where(np.logical_and(band!=fillvalue,cloud_mask==0))

        if len(good[0])==0: continue

        if log_flag==1:
            band[good]=np.log(band[good])

        if first_call==1:
            lower, upper = np.percentile(band[good], (s_min, s_max))
        else:
            lower=lowers[ii];upper=uppers[ii]

        arr_rescaled[ii] = exposure.rescale_intensity(band, in_range=(lower, upper))

        if first_call==1:
            lowers.append(lower); uppers.append(upper)

    return arr_rescaled.copy(), lowers, uppers


def plot_rgb(arr, rgb=[2,1,0], str_clip=2,fillvalue=0,first_call=1,lowers=[], uppers=[],outputname=None,figsize=(6,6),DPI=400,cloud_mask=None,log_flag=0):
        
        plt.figure(figsize=figsize)

        rgb_bands = arr[rgb, :, :]

        data, lowers, uppers = _stretch_im(rgb_bands, str_clip, fillvalue, \
                first_call, lowers, uppers, log_flag=log_flag,cloud_mask=cloud_mask)

        data=bytescale(data).transpose([1, 2, 0])

        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)

        plt.imshow(data)
        plt.axis('off')
        plt.tight_layout(pad=0)

        if outputname is not None:
            plt.savefig(outputname,bbox_inches='tight', pad_inches = 0, dpi=DPI,  transparent=True)
            plt.close('all')

        return lowers, uppers,data



