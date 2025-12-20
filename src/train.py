import os
import random
from functools import partial
from pathlib import Path

import click
import numpy as np
import torch
from fastai.data.all import Normalize, get_files
from fastai.metrics import DiceMulti
from fastai.vision.all import (
    Resize,
    SegmentationDataLoaders,
    imagenet_stats,
    models,
    unet_learner,
)

RANDOM_SEED = 42
VALID_PCT = 0.1
ARCH = "shufflenet_v2_x2_0"
IMG_SIZE = 256
BATCH_SIZE = 8
EPOCHS = 8
BASE_LR = 0.01


DATA_DIR = Path("data").resolve()
TRAIN_DATA_DIR = DATA_DIR / "train_data"
TEST_DATA_DIR = DATA_DIR / "test_data"
MODEL_DIR = Path("models").resolve()


def get_mask_path(x, train_data_dir):
    return Path(train_data_dir) / f"{Path(x).stem}.png"


@click.command()
@click.option("--train_data_dir", default=TRAIN_DATA_DIR, type=Path)
@click.option("--random_seed", default=RANDOM_SEED, type=int, show_default=True)
@click.option("--valid_pct", default=VALID_PCT, type=float, show_default=True)
@click.option("--arch", default=ARCH, show_default=True)
@click.option("--img_size", default=IMG_SIZE, type=int, show_default=True)
@click.option("--batch_size", default=BATCH_SIZE, type=int, show_default=True)
@click.option("--epochs", default=EPOCHS, type=int, show_default=True)
@click.option("--base_lr", default=BASE_LR, type=float, show_default=True)
def train(
    train_data_dir, random_seed, valid_pct, arch, img_size, batch_size, epochs, base_lr
) -> None:
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)
    random.seed(random_seed)

    data_loader = SegmentationDataLoaders.from_label_func(
        path=train_data_dir,
        fnames=get_files(train_data_dir, extensions=".jpg"),
        label_func=partial(get_mask_path, train_data_dir=train_data_dir),
        codes=["not-pool", "pool"],
        bs=batch_size,
        valid_pct=valid_pct,
        item_tfms=Resize(img_size),
        batch_tfms=[
            Normalize.from_stats(*imagenet_stats),
        ],
    )

    model_names = [
        name
        for name in dir(models)
        if not name.startswith("_")
        and name.islower()
        and name not in ("all", "tvm", "unet", "xresnet")
    ]
    if ARCH not in model_names:
        raise ValueError(f"Unsupported model, must be one of:\n{model_names}")

    learn = unet_learner(data_loader, arch=getattr(models, ARCH), metrics=DiceMulti)

    learn.fine_tune(
        epochs=epochs,
        base_lr=base_lr,
    )

    MODEL_DIR.mkdir(exist_ok=True)
    learn.export(fname=(MODEL_DIR / "model.pkl"))
    torch.save(learn.model, (MODEL_DIR / "model.pth"))


if __name__ == "__main__":
    train()
