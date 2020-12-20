import flax
import numpy as np
import PIL
from vit_jax import checkpoint
from vit_jax import models


def inference(img):
    model = 'ViT-B_16'
    num_classes = 196
    VisionTransformer = models.KNOWN_MODELS[model].partial(num_classes=num_classes)
    # Load and convert pretrained checkpoint.
    params = checkpoint.load('ViT-B_16.npz')
    params['pre_logits'] = {}  # Need to restore empty leaf for Flax.
    # Get imagenet labels.
    imagenet_labels = dict(enumerate(open('cars196_label.txt')))

    img=img.resize((384,384))
    
    logits, = VisionTransformer.call(params, (np.array(img) / 128 - 1)[None, ...])
    preds = flax.nn.softmax(logits)
    return imagenet_labels[preds.argsort()[:-2:-1].item()]
