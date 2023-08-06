from pyimgaug3d.augmentation.src.base_augmentation import BaseAugmentation

class Identity(BaseAugmentation):
    def __init__(self):
        super().__init__()

    def __call__(self, imgs):
        return imgs