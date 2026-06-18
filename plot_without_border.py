import matplotlib.pyplot as plt
import numpy as np

def plot_without_border(data, figsize=(7,7),title='',inter_method='none', outputname=None, vmin=None, vmax=None, colorbar=1,tick_labels=None):

        if vmin is None:
            vmin=data.min()
        if vmax is None:
            vmax=data.max()

        plt.figure(figsize=figsize)
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
        im=plt.imshow(data, interpolation=inter_method, vmin=vmin, vmax=vmax)
        plt.axis('off')
        plt.tight_layout(pad=0)

        if colorbar==1:
            if tick_labels is not None:
                cbar = plt.colorbar(im, ticks=np.arange(len(tick_labels)))
                cbar.ax.set_yticklabels(unique_vals)
            else:
                plt.colorbar()

        if outputname is not None:
            plt.savefig(outputname,bbox_inches='tight', dpi=720,pad_inches = 0)
            plt.close('all')



def plot_image_with_overlay_colorbar(data, figsize=(7, 7), inter_method='nearest', vmin=None, vmax=None, colorbar=False,cmap='viridis',outputname=None):
    fig, ax = plt.subplots(figsize=figsize)

    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)


    # Hide axes completely
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    img = ax.imshow(data, interpolation=inter_method, vmin=vmin, vmax=vmax,cmap=cmap)

    # Overlay colorbar
    if colorbar:
        # Create an inset_axes that overlays the image
        cax = ax.inset_axes([0.92, 0.1, 0.02, 0.5])  # [x-position, y-position, width, height] in fraction of figure
        cb = fig.colorbar(img, cax=cax)
        cb.outline.set_visible(False)  # Hide the colorbar frame


    if outputname is not None:
        plt.savefig(outputname,bbox_inches='tight', dpi=720,pad_inches = 0)
        plt.close('all')




if __name__=="__main__":
    delta = 0.025
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2

    plot_image_with_overlay_colorbar(Z, colorbar=1)
    plt.show(block=False)
