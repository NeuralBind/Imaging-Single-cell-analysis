from magicgui import magic_factory
from napari.layers import Image, Labels
import napari
import numpy as np
from scipy.ndimage import shift
from skimage import io

#translation widget for layer alignment
#keybindings are used, w:up,a:left,s:down,d:right. 
#to register and update napari coordinates press t.

@magic_factory(auto_call=True)
def translate(image: Labels, viewer: napari.Viewer): #change the image : to Labels or Image depending what data you have
    name=image.name
    prev_image=image
    @viewer.bind_key('w', overwrite=True)
    def up(viewer):
        y=image.translate[0]-5
        x=viewer.layers[name].translate[1]
        viewer.layers[name].translate=(y,x)

    @viewer.bind_key('a', overwrite=True)
    def left(viewer):
        y=viewer.layers[name].translate[0]
        x=viewer.layers[name].translate[1]-5
        viewer.layers[name].translate=(y,x)
        
    @viewer.bind_key('s', overwrite=True)
    def down(viewer):
        y=viewer.layers[name].translate[0]+5
        x=viewer.layers[name].translate[1]
        viewer.layers[name].translate=(y,x)

    @viewer.bind_key('d', overwrite=True)
    def right(viewer):
        y=viewer.layers[name].translate[0]
        x=viewer.layers[name].translate[1]+5
        viewer.layers[name].translate=(y,x)

    @viewer.bind_key('t', overwrite=True)
    def translate(viewer):
        x=viewer.layers[name].translate[0]
        y=viewer.layers[name].translate[1]
        img=viewer.layers[name].data.astype(np.uint16)
        viewer.layers.remove(name)
        img_shift=shift(img,[x,y])
        viewer.add_labels(img_shift,name=f'shifted_{name}',opacity=0.75)
        io.imsave("E:/Scripts/Quantification/notebooks/translated_segm/shifted_mask.tif",viewer.layers['shifted_mask'].data) 
