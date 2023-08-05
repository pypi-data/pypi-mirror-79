# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to download samples from
    your datasets on the WhatToLabel platform.

"""

import os
import shutil

import boris.data as data
import hydra
from boris.api import get_samples_by_tag
from boris.cli._helpers import fix_input_path
from tqdm import tqdm


def _download_cli(cfg, is_cli_call=True):
    '''Download all samples in a given tag.
       If from_folder and to_folder are specified, a copy of all images
       in the tag will be stored in the to_folder directory.

    Args:
        cfg['from_folder']: (str, optional)
            Path to folder which holds all images from the dataset
        cfg['to_folder']: (str, optional)
            Path to folder where the copied images will be stored
        cfg['tag_name']: (str) Name of the requested tag
        cfg['dataset_id']: (str) Dataset identifier on the platform
        cfg['token']: (str) Token which grants access to the platform

    '''

    tag_name = cfg['tag_name']
    dataset_id = cfg['dataset_id']
    token = cfg['token']

    if not tag_name:
        print('Please specify a tag name')
        print('For help, try: boris-upload --help')
        return

    if not token or not dataset_id:
        print('Please specify your access token and dataset id')
        print('For help, try: boris-upload --help')
        return

    # get all samples in the queried tag
    samples = get_samples_by_tag(
        tag_name,
        dataset_id,
        token,
        mode='list',
        filenames=None
    )

    # store sample names in a .txt file
    with open(cfg['tag_name'] + '.txt', 'w') as f:
        for item in samples:
            f.write("%s\n" % item)

    if cfg['from_folder'] and cfg['to_folder']:
        # "name.jpg" -> "/name.jpg" to prevent bugs like this:
        # "path/to/1234.jpg" ends with both "234.jpg" and "1234.jpg"
        samples = [os.path.join(' ', s)[1:] for s in samples]

        # copy all images from one folder to the other
        from_folder = fix_input_path(cfg['from_folder'])
        to_folder = fix_input_path(cfg['to_folder'])

        dataset = data.BorisDataset(from_folder=from_folder)
        basenames = dataset.get_filenames()

        source_names = [os.path.join(from_folder, f) for f in basenames]
        target_names = [os.path.join(to_folder, f) for f in basenames]

        # only copy files which are in the tag
        indices = [i for i in range(len(source_names))
                   if any([source_names[i].endswith(s) for s in samples])]

        print(f'Copying files from {from_folder} to {to_folder}.')
        for i in tqdm(indices):
            dirname = os.path.dirname(target_names[i])
            os.makedirs(dirname, exist_ok=True)
            shutil.copy(source_names[i], target_names[i])


@hydra.main(config_path='config/config.yaml', strict=False)
def download_cli(cfg):
    '''Download all samples in a given tag.
       If from_folder and to_folder are specified, a copy of all images
       in the tag will be stored in the to_folder directory.

    Args:
        cfg['from_folder']: (str, optional)
            Path to folder which holds all images from the dataset
        cfg['to_folder']: (str, optional)
            Path to folder where the copied images will be stored
        cfg['tag_name']: (str) Name of the requested tag
        cfg['dataset_id']: (str) Dataset identifier on the platform
        cfg['token']: (str) Token which grants access to the platform

    '''
    _download_cli(cfg)


def entry():
    download_cli()
