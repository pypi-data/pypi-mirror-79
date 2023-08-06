# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from os.path import join
import numpy as np
import utool as ut
from six.moves import range, zip

print, rrr, profile = ut.inject2(__name__)


def load_mnist_images(gz_fpath):
    import gzip

    # Read the inputs in Yann LeCun's binary format.
    with gzip.open(gz_fpath, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    # The inputs are vectors now, we reshape them to monochrome 2D images,
    # use the cv2 convention for now (examples, rows, columns, channels)
    data = data.reshape(-1, 28, 28, 1)
    # The inputs come as bytes, we convert them to float32 in range [0,1].
    # (Actually to range [0, 255/256], for compatibility to the version
    # provided at http://deeplearning.net/data/mnist/mnist.pkl.gz.)
    return data / np.float32(256)


def load_mnist_labels(gz_fpath):
    import gzip

    # Read the labels in Yann LeCun's binary format.
    with gzip.open(gz_fpath, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=8)
    # The labels are vectors of integers now, that's exactly what we want.
    return data


def grab_mnist2():
    """ Follows lasange example """
    train_data_gz = ut.grab_file_url(
        'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
    )
    train_labels_gz = ut.grab_file_url(
        'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
    )
    test_data_gz = ut.grab_file_url(
        'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
    )
    test_labels_gz = ut.grab_file_url(
        'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
    )

    train_data = load_mnist_images(train_data_gz)
    test_data = load_mnist_images(test_data_gz)

    train_labels = load_mnist_labels(train_labels_gz)
    test_labels = load_mnist_labels(test_labels_gz)

    data = np.vstack((train_data, test_data))
    labels = np.append(train_labels, test_labels)
    metadata = {}
    metadata['splitset'] = ['train'] * len(train_data) + ['test'] * len(test_labels)
    return data, labels, metadata


def grab_mnist1():
    # This is the same mnist data used in the lasange script
    train_imgs_fpath = ut.grab_zipped_url(
        'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
    )
    train_lbls_fpath = ut.grab_zipped_url(
        'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
    )
    test_imgs_fpath = ut.grab_zipped_url(
        'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
    )
    test_lbls_fpath = ut.grab_zipped_url(
        'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
    )

    train_images, train_labels = open_mnist_files(train_imgs_fpath, train_lbls_fpath)
    test_images, test_labels = open_mnist_files(test_imgs_fpath, test_lbls_fpath)
    data = np.vstack((train_images, test_images))
    labels = np.append(train_labels, test_labels)
    metadata = None
    return data, labels, metadata


def open_mnist_files(data_fpath, labels_fpath):
    """
    For mnist1

    References:
        http://g.sweyla.com/blog/2012/mnist-numpy/
    """
    import struct

    # import os
    import numpy as np
    from array import array as pyarray

    with open(labels_fpath, 'rb') as flbl:
        magic_nr, size = struct.unpack('>II', flbl.read(8))
        lbl = pyarray('b', flbl.read())

    with open(data_fpath, 'rb') as fimg:
        magic_nr, size, rows, cols = struct.unpack('>IIII', fimg.read(16))
        img = pyarray('B', fimg.read())
    digits = np.arange(10)

    ind = [k for k in range(size) if lbl[k] in digits]
    N = len(ind)

    images = np.zeros((N, rows, cols), dtype=np.uint8)
    labels = np.zeros((N, 1), dtype=np.uint8)
    for i in range(len(ind)):
        images[i] = np.array(
            img[ind[i] * rows * cols : (ind[i] + 1) * rows * cols]
        ).reshape((rows, cols))
        labels[i] = lbl[ind[i]]
    return images, labels


def extract_liberty_style_patches(ds_path, pairs):
    """
    CommandLine:
        python -m wbia_cnn.ingest_data --test-grab_cached_liberty_data --show

    """
    from itertools import product
    import numpy as np
    from PIL import Image
    import subprocess

    patch_x = 64
    patch_y = 64
    rows = 16
    cols = 16

    def _available_patches(ds_path):
        """
        Number of patches in _dataset_ (a path).

        Only available through the line count
        in info.txt -- use unix 'wc'.

        _path_ is supposed to be a path to
        a directory with bmp patchsets.
        """
        fname = join(ds_path, 'info.txt')
        p = subprocess.Popen(
            ['wc', '-l', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])

    # def read_patch_ids():
    #    pass

    def matches(ds_path, pairs):
        """Return _pairs_ many match/non-match pairs for _dataset_.
        _dataset_ is one of "liberty", "yosemite", "notredame".
        Every dataset has a number of match-files, that
        have _pairs_ many matches and non-matches (always
        the same number).
        The naming of these files is confusing, e.g. if there are 500 matching
        pairs and 500 non-matching pairs the file name is
        'm50_1000_1000_0.txt' -- in total 1000 patch-ids are used for matches,
        and 1000 patch-ids for non-matches. These patch-ids need not be
        unique.

        Also returns the used patch ids in a list.

        Extract all matching and non matching pairs from _fname_.
        Every line in the matchfile looks like:
            patchID1 3DpointID1 unused1 patchID2 3DpointID2 unused2
        'matches' have the same 3DpointID.

        Every file has the same number of matches and non-matches.
        """
        # pairs = 500
        match_fname = ''.join(['m50_', str(2 * pairs), '_', str(2 * pairs), '_0.txt'])
        match_fpath = join(ds_path, match_fname)

        # print(pairs, "pairs each (matching/non_matching) from", match_fpath)

        with open(match_fpath) as match_file:
            # collect patches (id), and match/non-match pairs
            patch_ids, match, non_match = [], [], []

            for line in match_file:
                match_info = line.split()
                p1_id, p1_3d, p2_id, p2_3d = (
                    int(match_info[0]),
                    int(match_info[1]),
                    int(match_info[3]),
                    int(match_info[4]),
                )
                if p1_3d == p2_3d:
                    match.append((p1_id, p2_id))
                else:
                    non_match.append((p1_id, p2_id))
                patch_ids.append(p1_id)
                patch_ids.append(p2_id)

            patch_ids = list(set(patch_ids))
            patch_ids.sort()

            assert len(match) == len(
                non_match
            ), 'Different number of matches and non-matches.'

        return match, non_match, patch_ids

    def _crop_to_numpy(patchfile, requested_indicies):
        """
        Convert _patchfile_ to a numpy array with patches per row.
        A _patchfile_ is a .bmp file.
        """
        pil_img = Image.open(patchfile)
        ptch_iter = (
            pil_img.crop(
                (col * patch_x, row * patch_y, (col + 1) * patch_x, (row + 1) * patch_y)
            )
            for index, (row, col) in enumerate(product(range(rows), range(cols)))
            if index in requested_indicies
        )
        patches = [np.array(ptch) for ptch in ptch_iter]
        pil_img.close()
        return patches

    num_patch_per_bmp = rows * cols
    total_num_patches = _available_patches(ds_path)
    num_bmp_files, mod = divmod(total_num_patches, num_patch_per_bmp)

    patchfile_list = [
        join(ds_path, ''.join(['patches', str(i).zfill(4), '.bmp']))
        for i in range(num_bmp_files)
    ]

    # Build matching labels
    match_pairs, non_match_pairs, all_requested_patch_ids = matches(ds_path, pairs)
    all_requested_patch_ids = np.array(all_requested_patch_ids)
    print('len(match_pairs) = %r' % (len(match_pairs,)))
    print('len(non_match_pairs) = %r' % (len(non_match_pairs,)))
    print('len(all_requested_patch_ids) = %r' % (len(all_requested_patch_ids,)))

    assert len(list(set(ut.flatten(match_pairs) + ut.flatten(non_match_pairs)))) == len(
        all_requested_patch_ids
    )
    assert max(all_requested_patch_ids) <= total_num_patches

    # Read all patches out of the bmp file store
    all_patches = {}
    for pfx, patchfile in ut.ProgressIter(
        list(enumerate(patchfile_list)), lbl='Reading Patches', adjust=True
    ):
        patch_id_offset = pfx * num_patch_per_bmp
        # get local patch ids in this bmp file
        patch_ids_ = np.arange(num_patch_per_bmp) + patch_id_offset
        requested_patch_ids_ = np.intersect1d(patch_ids_, all_requested_patch_ids)
        requested_indicies = requested_patch_ids_ - patch_id_offset
        if len(requested_indicies) == 0:
            continue
        patches = _crop_to_numpy(patchfile, requested_indicies)
        for idx, patch in zip(requested_patch_ids_, patches):
            all_patches[idx] = patch

    # Read the last patches
    if mod > 0:
        pfx += 1
        patch_id_offset = pfx * num_patch_per_bmp
        patchfile = join(
            ds_path, ''.join(['patches', str(num_bmp_files).zfill(4), '.bmp'])
        )
        patch_ids_ = np.arange(mod) + patch_id_offset
        requested_patch_ids_ = np.intersect1d(patch_ids_, all_requested_patch_ids)
        requested_indicies = requested_patch_ids_ - patch_id_offset
        patches = _crop_to_numpy(patchfile, requested_indicies)
        for idx, patch in zip(requested_patch_ids_, patches):
            all_patches[idx] = patch

    print('read %d patches ' % (len(all_patches)))
    # patches_list += [patches]

    # all_patches = np.concatenate(patches_list, axis=0)

    matching_patches1 = [all_patches[idx1] for idx1, idx2 in match_pairs]
    matching_patches2 = [all_patches[idx2] for idx1, idx2 in match_pairs]
    nonmatching_patches1 = [all_patches[idx1] for idx1, idx2 in non_match_pairs]
    nonmatching_patches2 = [all_patches[idx2] for idx1, idx2 in non_match_pairs]

    labels = np.array(
        ([True] * len(matching_patches1)) + ([False] * len(nonmatching_patches1))
    )
    warped_patch1_list = matching_patches1 + nonmatching_patches1
    warped_patch2_list = matching_patches2 + nonmatching_patches2

    img_list = ut.flatten(list(zip(warped_patch1_list, warped_patch2_list)))
    data = np.array(img_list)
    del img_list
    # data_per_label = 2
    assert labels.shape[0] == data.shape[0] // 2
    return data, labels


def convert_category_to_siam_data(category_data, category_labels):
    # CONVERT CATEGORY LABELS TO PAIR LABELS
    # Make genuine imposter pairs
    import vtool as vt

    unique_labels, groupxs_list = vt.group_indices(category_labels)

    num_categories = len(unique_labels)

    num_geninue = 10000 * num_categories
    num_imposter = 10000 * num_categories

    num_gen_per_category = int(num_geninue / len(unique_labels))
    num_imp_per_category = int(num_imposter / len(unique_labels))

    np.random.seed(0)
    groupxs = groupxs_list[0]

    def find_fix_flags(pairxs):
        is_dup = vt.nonunique_row_flags(pairxs)
        is_eye = pairxs.T[0] == pairxs.T[1]
        needs_fix = np.logical_or(is_dup, is_eye)
        # print(pairxs[needs_fix])
        return needs_fix

    def swap_undirected(pairxs):
        """ ensure left indicies are lower """
        needs_swap = pairxs.T[0] > pairxs.T[1]
        arr = pairxs[needs_swap]
        tmp = arr.T[0].copy()
        arr.T[0, :] = arr.T[1]
        arr.T[1, :] = tmp
        pairxs[needs_swap] = arr
        return pairxs

    def sample_pairs(left_list, right_list, size):
        # Sample initial random left and right indices
        _index1 = np.random.choice(left_list, size=size, replace=True)
        _index2 = np.random.choice(right_list, size=size, replace=True)
        # stack
        _pairxs = np.vstack((_index1, _index2)).T
        # make undiractional
        _pairxs = swap_undirected(_pairxs)
        # iterate until feasible
        needs_fix = find_fix_flags(_pairxs)
        while np.any(needs_fix):
            num_fix = needs_fix.sum()
            print('fixing: %d' % num_fix)
            _pairxs.T[1][needs_fix] = np.random.choice(
                right_list, size=num_fix, replace=True
            )
            _pairxs = swap_undirected(_pairxs)
            needs_fix = find_fix_flags(_pairxs)
        return _pairxs

    print('sampling genuine pairs')
    genuine_pairx_list = []
    for groupxs in groupxs_list:
        left_list = groupxs
        right_list = groupxs
        size = num_gen_per_category
        _pairxs = sample_pairs(left_list, right_list, size)
        genuine_pairx_list.extend(_pairxs.tolist())

    print('sampling imposter pairs')
    imposter_pairx_list = []
    for index in range(len(groupxs_list)):
        # Pick random pairs of false matches
        groupxs = groupxs_list[index]
        bar_groupxs = np.hstack(groupxs_list[:index] + groupxs_list[index + 1 :])
        left_list = groupxs
        right_list = bar_groupxs
        size = num_imp_per_category
        _pairxs = sample_pairs(left_list, right_list, size)
        imposter_pairx_list.extend(_pairxs.tolist())

    # We might have added duplicate imposters, just remove them for now
    imposter_pairx_list = ut.take(
        imposter_pairx_list, vt.unique_row_indexes(np.array(imposter_pairx_list))
    )

    # structure data for output
    flat_data_pairxs = np.array(genuine_pairx_list + imposter_pairx_list)
    assert np.all(flat_data_pairxs.T[0] < flat_data_pairxs.T[1])
    assert find_fix_flags(flat_data_pairxs).sum() == 0
    # TODO: batch should use indicies into data
    flat_index_list = np.array(
        ut.flatten(list(zip(flat_data_pairxs.T[0], flat_data_pairxs.T[1])))
    )
    data = np.array(category_data.take(flat_index_list, axis=0))
    labels = np.array(
        [True] * len(genuine_pairx_list) + [False] * len(imposter_pairx_list)
    )
    return data, labels


if __name__ == '__main__':
    """
    CommandLine:
        python -m wbia_cnn.ingest_helpers
        python -m wbia_cnn.ingest_helpers --allexamples
        python -m wbia_cnn.ingest_helpers --allexamples --noface --nosrc
    """
    import multiprocessing

    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA

    ut.doctest_funcs()
