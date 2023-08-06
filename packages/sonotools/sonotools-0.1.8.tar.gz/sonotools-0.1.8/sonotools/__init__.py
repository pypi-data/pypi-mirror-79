from sonotools.__version__ import __version__

import torch
import torchvision

import os, os.path
from pathlib import Path

import cv2  # pytype: disable=attribute-error
import matplotlib
import numpy as np

import wget

import PIL

def loadVideo(filename: str):
    """
    Loads a movie into a numpy array
    ----------
    filename : path or str
        location of video file
    Returns
    -------
    loadVideo : numpy array, uint8
        has shape (channels frames width height)
    Notes
    -----
    The shape of the output array is suited for pytorch
    """
    capture = cv2.VideoCapture(str(filename))

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    v = np.zeros((frame_count, frame_width, frame_height, 3), np.uint8)

    for count in range(frame_count):
        ret, frame = capture.read()
        if not ret:
            raise ValueError("Failed to load frame #{} of {}.".format(count, filename))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        v[count] = frame

    capture.release()
    v = v.transpose((3, 0, 1, 2)) # openCV to pytorch

    return v

def captureVideoProps(filename: str):
    """
    Returns frames per second, total frames, height, width of video
    ----------
    filename : path or str
        location of video file
    Returns
    -------
    props : tuple
        (fps, frame count, frame height, frame width)

    Notes
    -----
    Example fps,f,h,w = captureVideoProps(filepath)
    """
    capture = cv2.VideoCapture(str(filename))

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(capture.get(cv2.CAP_PROP_FPS))

    capture.release()
    return (frame_rate, frame_count, frame_height, frame_width)


def dice(im1, im2):
    """
    Computes the Dice coefficient, a measure of set similarity.
    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size. If not boolean, will be converted.
    Returns
    -------
    dice : float
        Dice coefficient as a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0

    Notes
    -----
    The order of inputs for `dice` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.
    """
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / (im1.sum() + im2.sum())


def cropSquare(img: PIL.Image):
    """
    Crop a PIL image into a square
    Parameters
    ----------
    img : PIL Image
        A pillow image
    Returns
    -------
    cropSquare : PIL Image
      Image cropped from it's center along it's short axis
    """
    w,h = img.size
    b = np.minimum(w,h)
    l = (w - b)/2
    t = (h - b)/2
    r = (w + b)/2
    bt = (h + b)/2
    return img.crop((l, t, r, bt))


def flushDotDS_Store(rootDir):
    """
    Deletes .DS_Store from a directory and it's children
    ----------
    rootDir : path or str
        directory to walk
    Notes
    -----
    Example
      flushDotDS_Store('./dataset')
    """
    for root, dirs, files in os.walk(rootDir):
        i = 0
        for file in files:
            if file.endswith('.DS_Store'):
                path = os.path.join(root, file)

                print("Deleting: %s" % path)

                if os.remove(path):
                    print("Unable to delete!")
                else:
                    print("Deleted...")
                    i = i+1

        print("Files Deleted: %d" % i)


def loadEchoNetSegmentation(DestinationForWeights: str):
    """
    Returns resnet 50 nn with weights loaded from echonet
    ----------
    DestinationForWeights : path or str
        directory to download / store weights file
    Returns
    -------
    model : DeepLabV3
        model for predicting LV from an apical four chamber view
    Notes
    -----
    Example
      model = loadEchoNetSegmentation('/content/weights')
    """
    if os.path.exists(DestinationForWeights):
        print("The weights are at", DestinationForWeights)
    else:
        print("Creating folder at ", DestinationForWeights, " to store weights")
        os.mkdir(DestinationForWeights)

    segmentationWeightsURL = 'https://github.com/douyang/EchoNetDynamic/releases/download/v1.0.0/deeplabv3_resnet50_random.pt'

    if not os.path.exists(os.path.join(DestinationForWeights, os.path.basename(segmentationWeightsURL))):
        print("Downloading Segmentation Weights, ", segmentationWeightsURL," to ",os.path.join(DestinationForWeights,os.path.basename(segmentationWeightsURL)))
        filename = wget.download(segmentationWeightsURL, out = DestinationForWeights)
    else:
        print("Segmentation Weights already present")

    weightsFile = Path(DestinationForWeights, 'deeplabv3_resnet50_random.pt')

    def collate_fn(x):
      x, f = zip(*x)
      i = list(map(lambda t: t.shape[1], x))
      x = torch.as_tensor(np.swapaxes(np.concatenate(x, 1), 0, 1))
      return x, f, i

    model = torchvision.models.segmentation.deeplabv3_resnet50(pretrained=False, aux_loss = False)
    model.classifier[-1] = torch.nn.Conv2d(model.classifier[-1].in_channels, 1, kernel_size=model.classifier[-1].kernel_size)

    if torch.cuda.is_available():
        print("cuda is available, original weights")
        device = torch.device("cuda")
        model = torch.nn.DataParallel(model)
        model.to(device)
        checkpoint = torch.load( str(weightsFile) )
        model.load_state_dict(checkpoint['state_dict'])
    else:
        print("cuda is not available, cpu weights")
        device = torch.device("cpu")
        checkpoint = torch.load(str(weightsFile), map_location=device)
        state_dict_cpu = {k[7:]: v for (k, v) in checkpoint['state_dict'].items()} # remove 'module' prefix from key
        model.load_state_dict(state_dict_cpu)

    model.eval()

    return model


def validateVideoForAutoCrop(filename: str):
    """
    Ensure video file has enough frames to be analyzed
    Default value of min_frames is 50
    """
    capture = cv2.VideoCapture(str(filename))

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(capture.get(cv2.CAP_PROP_FPS))

    capture.release()

    if frame_count < 50:
        raise ValueError(f'{str(filename)} has {frame_count} frames. At least 50 frames are required for analysis.')

    # If no errors raised then video passes validation
    return True

def countUniquePixels(a):
    return len(np.unique(a))

def countUniquePixelsAlongFrames(vid):
    f, height, width = vid.shape
    u = np.zeros((height, width), np.uint8)
    for i in range(height):
        u[i] = np.apply_along_axis(countUniquePixels, 0, vid[:,i,:])

    return u


def findEdges(x, thresh=0.1):
    # find the right
    right = len(x)
    a = x[int(len(x)/2):-1]
    b, = np.where( a <= thresh )
    if len(b)>0:
        right = int(len(x)/2)+b[0]

    # find the left
    left = 0
    a = np.flip(x[0:int(len(x)/2)])
    b, = np.where( a <= thresh )
    if len(b)>0:
        left = int(len(x)/2)-b[0]

    return (left,right)


def predictLV(model, filepath):

  def segmentPIL(inp, model):
    x = inp.transpose([2, 0, 1])  #  channels-first
    x = np.expand_dims(x, axis=0)  # adding a batch dimension

    mean = x.mean(axis=(0, 2, 3))
    std = x.std(axis=(0, 2, 3))
    x = x - mean.reshape(1, 3, 1, 1)
    x = x / std.reshape(1, 3, 1, 1)

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    with torch.no_grad():
        x = torch.from_numpy(x).type('torch.FloatTensor').to(device)
        output = model(x)

    y = output['out'].numpy()
    y = y.squeeze()

    out = y>0

    mask = np.zeros((inp.shape[0], inp.shape[1]), np.int8)
    mask[out] = 255

    return mask.astype(np.bool)

  img = PIL.Image.open(str(filepath))
  img = img.convert('RGB')
  img = cropSquare(img)
  img = img.resize((112,112))
  img = np.array(img)
  y = segmentPIL(img, model)

  return y


__all__ = ["__version__", "loadVideo", "captureVideoProps", "dice", "cropSquare", "findEdges", "countUniquePixels", "countUniquePixelsAlongFrames", "validateVideoForAutoCrop", "loadEchoNetSegmentation", "predictLV", "flushDotDS_Store"]
