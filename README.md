


combines traditional computer vision techniques with deep learning to recognise chess positions from photos.



## Background

A casual over-the-board game between two friends will often reach an interesting position. After the game, the players will want to analyse that position on a computer, so they take a photo of the position. On the computer, they need to drag and drop pieces onto a virtual chessboard until the position matches the one they had on the photograph, and then they must double-check that they did not miss any pieces.

The goal of this project is to develop a system that is able to map a photo of a chess position to a structured format that can be understood by chess engines, such as the widely-used Forsyth–Edwards Notation (FEN).

## Overview

The chess recognition system is trained using a dataset of ~5,000 synthetically generated images of chess positions (3D renderings of different chess positions at various camera angles and lighting conditions).
The dataset is available [here](https://doi.org/10.17605/OSF.IO/XF3KA).
At a high level, the recognition system itself consists of the following pipeline:

1. board localisation (square and corner detection)
2. occupancy classification
3. piece classification
4. post-processing to generate the FEN string

## Installing

1. **Using poetry (recommended).**
   Ensure you have [poetry](https://python-poetry.org) installed, then clone this repository, and install intellichess:
   ```bash
   git clone 
   cd intellichess
   poetry install
   ```

### Downloading the dataset and models

To download and split the dataset, run:

```bash
python -m intellichess.data_synthesis.download_dataset
python -m intellichess.data_synthesis.split_dataset
```

Finally, ensure that you download the trained models:

```bash
python -m intellichess.occupancy_classifier.download_model
python -m intellichess.piece_classifier.download_model
```

## Acknowledgments

This project is heavily inspired by the work of [@username](https://github.com/georg-wolflein). Their insights, guidance, and previous work have played a crucial role in shaping this repository. I highly recommend checking out their work [here](https://github.com/georg-wolflein/chesscog).

