import logging
import shutil
from pathlib import Path

import click
import numpy as np
from fastai.vision.all import get_files

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_REGION = "REGION_1"
DATA_DIR = Path("data")
RANDOM_SEED = 42


@click.command()
@click.option("--data_dir", default=DATA_DIR, type=Path)
@click.option("--test_region", default=TEST_REGION)
@click.option("--random_seed", default=RANDOM_SEED)
def data_split(data_dir, test_region, random_seed):
    np.random.seed(random_seed)
    img_fpaths = get_files(data_dir / "pool_data" / "images", extensions=".jpg")

    train_data_dir = data_dir / "train_data"
    train_data_dir.mkdir(exist_ok=True)
    test_data_dir = data_dir / "test_data"
    test_data_dir.mkdir(exist_ok=True)
    for img_path in img_fpaths:
        msk_path = data_dir / "pool_data" / "masks" / f"{img_path.stem}.png"
        if test_region in str(img_path):
            logger.debug(f"Copying {img_path} to {test_data_dir}")
            shutil.copy(img_path, test_data_dir)
            shutil.copy(msk_path, test_data_dir)
        else:
            logger.debug(f"Copying {img_path} to {train_data_dir}")
            shutil.copy(img_path, train_data_dir)
            shutil.copy(msk_path, train_data_dir)

    logger.info(f"Train data size: {len(list(train_data_dir.glob('*')))}")
    logger.info(f"Test data size: {len(list(test_data_dir.glob('*')))}")


if __name__ == "__main__":
    data_split()
