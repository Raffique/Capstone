import numpy as np
import pydicom as di
import os
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import figure_factory as FF
from plotly.graph_objs import *
import vtk


#      
# Loop over the image files and store everything into a list.
# 

class View3D:
    def __init__(self):
        self.image = None
        self.scan = None

    def load_scan(self, path):
        slices = [di.dcmread(path + '/' + s) for s in os.listdir(path)]
        slices.sort(key = lambda x: int(x.InstanceNumber))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
            
        for s in slices:
            s.SliceThickness = slice_thickness
            
        return slices

    def get_pixels_hu(self, scans):
        image = np.stack([s.pixel_array for s in scans])
        # Convert to int16 (from sometimes int16), 
        # should be possible as values should always be low enough (<32k)
        image = image.astype(np.int16)

        # Set outside-of-scan pixels to 1
        # The intercept is usually -1024, so air is approximately 0
        image[image == -2000] = 0
        
        # Convert to Hounsfield units (HU)
        intercept = scans[0].RescaleIntercept
        slope = scans[0].RescaleSlope
        
        if slope != 1:
            image = slope * image.astype(np.float64)
            image = image.astype(np.int16)
            
        image += np.int16(intercept)
        
        return np.array(image, dtype=np.int16)


    

    def save_3D_image(self, filename, image):
        np.save(filename, image)

    def load_3D_image(self, filename):
        self.image = np.load(filename)



    #resampling

    def resample(self, image, scan, new_spacing=[1,1,1]):
        # Determine current pixel spacing

        spacing = map(float, ([scan[0].SliceThickness] + list(scan[0].PixelSpacing)))
        spacing = np.array(list(spacing))

        resize_factor = spacing / new_spacing
        print(image.shape, resize_factor.shape)
        new_real_shape = image.shape * resize_factor
        new_shape = np.round(new_real_shape)
        real_resize_factor = new_shape / image.shape
        new_spacing = spacing / real_resize_factor
        
        image = scipy.ndimage.zoom(image, real_resize_factor, mode="nearest")
        
        return image, new_spacing

    



    #---------------------------------------------3D Plotting -----------------------------------
    def make_mesh(self, image, threshold=-300, step_size=1):

        print( "Transposing surface")
        p = image.transpose(2,1,0)
        
        print ("Calculating surface")
        verts, faces, norm, val = measure.marching_cubes(p, threshold, step_size=step_size, allow_degenerate=True) 
        return verts, faces

    def plotly_3d(self, verts, faces):
        x,y,z = zip(*verts) 
        
        print( "Drawing")
        
        # Make the colormap single color since the axes are positional not intensity. 
    #    colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
        colormap=['rgb(236, 236, 212)','rgb(236, 236, 212)']
        
        fig = FF.create_trisurf(
            x=x,
            y=y, 
            z=z, 
            plot_edges=False,
            colormap=colormap,
            simplices=faces,
            backgroundcolor='rgb(64, 64, 64)',
            title="Interactive Visualization"
        )
        #=============OPACITY===============#
        #this is to control the opacity 
        #fig['data'][0].update(opacity=0.5)
        iplot(fig)

    def plt_3d(self, verts, faces):
        print( "Drawing")
        x,y,z = zip(*verts) 
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Fancy indexing: `verts[faces]` to generate a collection of triangles
        mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=1)
        face_color = [1, 1, 0.9]
        mesh.set_facecolor(face_color)
        ax.add_collection3d(mesh)

        ax.set_xlim(0, max(x))
        ax.set_ylim(0, max(y))
        ax.set_zlim(0, max(z))
        ax.set_facecolor((0.7, 0.7, 0.7))
        plt.show()

    def plot_3d(self, image, threshold=-300):
    
        # Position the scan upright, 
        # so the head of the patient would be at the top facing the camera
        p = image.transpose(2,1,0)
        
        verts, faces, norm, val = measure.marching_cubes(p, threshold)

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Fancy indexing: `verts[faces]` to generate a collection of triangles
        mesh = Poly3DCollection(verts[faces], alpha=0.70)
        face_color = [0.45, 0.45, 0.75]
        mesh.set_facecolor(face_color)
        ax.add_collection3d(mesh)

        ax.set_xlim(0, p.shape[0])
        ax.set_ylim(0, p.shape[1])
        ax.set_zlim(0, p.shape[2])

        plt.show()

    
    def view_plt_3D(self, img, threshold=350):

        v, f = self.make_mesh(img, threshold)
        self.plt_3d(v, f)

    def view_plotly_3D(self, img, threshold=350, step=2):

        v, f = self.make_mesh(img, threshold, step)
        self.plotly_3d(v, f)

    def runner(self, filename):
        self.scan = self.load_scan(filename)
        self.image = self.get_pixels_hu(self.scan)
        #self.save_3D_image('patient0234.npy', self.image)
        self.image, spacing = self.resample(self.image, self.scan, [1,1,1])

        #self.view_plotly_3D(self.image)
        #self.plot_3d(self.image, 400)

        seglungs = self.segment_lung_mask(self.image, False)
        segfills = self.segment_lung_mask(self.image, True)

        #self.plot_3d(seglungs, 0)
        #self.plot_3d(segfills - seglungs, 0)

        self.view_plotly_3D(segfills-seglungs, None)



    #Standardize the pixel values
    def make_lungmask(self, img, display=False):
        row_size= img.shape[0]
        col_size = img.shape[1]
        
        mean = np.mean(img)
        std = np.std(img)
        img = img-mean
        img = img/std
        # Find the average pixel value near the lungs
        # to renormalize washed out images
        middle = img[int(col_size/5):int(col_size/5*4),int(row_size/5):int(row_size/5*4)] 
        mean = np.mean(middle)  
        max = np.max(img)
        min = np.min(img)
        # To improve threshold finding, I'm moving the 
        # underflow and overflow on the pixel spectrum
        img[img==max]=mean
        img[img==min]=mean
        #
        # Using Kmeans to separate foreground (soft tissue / bone) and background (lung/air)
        #
        kmeans = KMeans(n_clusters=2).fit(np.reshape(middle,[np.prod(middle.shape),1]))
        centers = sorted(kmeans.cluster_centers_.flatten())
        threshold = np.mean(centers)
        thresh_img = np.where(img<threshold,1.0,0.0)  # threshold the image

        # First erode away the finer elements, then dilate to include some of the pixels surrounding the lung.  
        # We don't want to accidentally clip the lung.

        eroded = morphology.erosion(thresh_img,np.ones([3,3]))
        dilation = morphology.dilation(eroded,np.ones([8,8]))

        labels = measure.label(dilation) # Different labels are displayed in different colors
        label_vals = np.unique(labels)
        regions = measure.regionprops(labels)
        good_labels = []
        for prop in regions:
            B = prop.bbox
            if B[2]-B[0]<row_size/10*9 and B[3]-B[1]<col_size/10*9 and B[0]>row_size/5 and B[2]<col_size/5*4:
                good_labels.append(prop.label)
        mask = np.ndarray([row_size,col_size],dtype=np.int8)
        mask[:] = 0

        #
        #  After just the lungs are left, we do another large dilation
        #  in order to fill in and out the lung mask 
        #
        for N in good_labels:
            mask = mask + np.where(labels==N,1,0)
        mask = morphology.dilation(mask,np.ones([10,10])) # one last dilation

        if (display):
            fig, ax = plt.subplots(3, 2, figsize=[12, 12])
            ax[0, 0].set_title("Original")
            ax[0, 0].imshow(img, cmap='gray')
            ax[0, 0].axis('off')
            ax[0, 1].set_title("Threshold")
            ax[0, 1].imshow(thresh_img, cmap='gray')
            ax[0, 1].axis('off')
            ax[1, 0].set_title("After Erosion and Dilation")
            ax[1, 0].imshow(dilation, cmap='gray')
            ax[1, 0].axis('off')
            ax[1, 1].set_title("Color Labels")
            ax[1, 1].imshow(labels)
            ax[1, 1].axis('off')
            ax[2, 0].set_title("Final Mask")
            ax[2, 0].imshow(mask, cmap='gray')
            ax[2, 0].axis('off')
            ax[2, 1].set_title("Apply Mask on Original")
            ax[2, 1].imshow(mask*img, cmap='gray')
            ax[2, 1].axis('off')
            
            plt.show()
        return mask*img

    def largest_label_volume(self, im, bg=-1):
        vals, counts = np.unique(im, return_counts=True)

        counts = counts[vals != bg]
        vals = vals[vals != bg]

        if len(counts) > 0:
            return vals[np.argmax(counts)]
        else:
            return None

    def segment_lung_mask(self, image, fill_lung_structures=True):
        
        # not actually binary, but 1 and 2. 
        # 0 is treated as background, which we do not want
        binary_image = np.array(image > -320, dtype=np.int8)+1
        labels = measure.label(binary_image)
        
        # Pick the pixel in the very corner to determine which label is air.
        #   Improvement: Pick multiple background labels from around the patient
        #   More resistant to "trays" on which the patient lays cutting the air 
        #   around the person in half
        background_label = labels[0,0,0]
        
        #Fill the air around the person
        binary_image[background_label == labels] = 2
        
        
        # Method of filling the lung structures (that is superior to something like 
        # morphological closing)
        if fill_lung_structures:
            # For every slice we determine the largest solid structure
            for i, axial_slice in enumerate(binary_image):
                axial_slice = axial_slice - 1
                labeling = measure.label(axial_slice)
                l_max = self.largest_label_volume(labeling, bg=0)
                
                if l_max is not None: #This slice contains some lung
                    binary_image[i][labeling != l_max] = 1

        
        binary_image -= 1 #Make the image actual binary
        binary_image = 1-binary_image # Invert it, lungs are now 1
        
        # Remove other air pockets insided body
        labels = measure.label(binary_image, background=0)
        l_max = self.largest_label_volume(labels, bg=0)
        if l_max is not None: # There are air pockets
            binary_image[labels != l_max] = 0
    
        return binary_image

if __name__ == "__main__":

    data_path = "/home/raffique/Desktop/train/6897fa9de148/2bfbb7fd2e8b"
    output_path = working_path = "/home/raffique/Documents/"
    g = glob(data_path + '/*')

    viewer = View3D()
    viewer.runner(data_path)