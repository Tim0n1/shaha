"""Script to generate the YAML configuration files for each of the candidate piece classification model architectures.
The candidates are defined in the :mod:`~intellichess.piece_classifier.models` module.

.. code-block:: console

    $ python -m intellichess.piece_classifier.create_configs --help
    usage: create_configs.py [-h]
    
    Generate the YAML configuration for the piece
    classifiers.
    
    optional arguments:
      -h, --help  show this help message and exit
"""

from intellichess.core.training import create_configs
import argparse

if __name__ == "__main__":
    argparse.ArgumentParser(
        description="Generate the YAML configuration for the piece classifiers.").parse_args()
    create_configs("piece_classifier")
