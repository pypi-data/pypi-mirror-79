# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from wbia_cnn import utils
from wbia_cnn import ingest_helpers
from wbia_cnn import ingest_wbia
from wbia_cnn.dataset import DataSet
from os.path import join, basename, splitext
import utool as ut

print, rrr, profile = ut.inject2(__name__)


NOCACHE_DATASET = ut.get_argflag(('--nocache-cnn', '--nocache-dataset'))


def testdata_dataset():
    dataset = get_wbia_patch_siam_dataset(max_examples=5)
    return dataset


def testdata_patchmatch():
    """
    >>> from wbia_cnn.ingest_data import *  # NOQA
    """
    dataset = get_wbia_patch_siam_dataset(max_examples=5)
    data_fpath = dataset.data_fpath
    labels_fpath = dataset.labels_fpath
    data_cv2, labels = utils.load(data_fpath, labels_fpath)
    data = utils.convert_cv2_images_to_theano_images(data_cv2)
    return data, labels


def testdata_patchmatch2():
    """
    >>> from wbia_cnn.ingest_data import *  # NOQA
    """
    dataset = get_wbia_patch_siam_dataset(max_examples=5)
    data_fpath = dataset.data_fpath
    labels_fpath = dataset.labels_fpath
    data, labels = utils.load(data_fpath, labels_fpath)
    return data, labels


def get_extern_training_dpath(alias_key):
    return DataSet.from_alias_key(alias_key).training_dpath


def view_training_directories():
    r"""
    CommandLine:
        python -m wbia_cnn.ingest_data --test-view_training_directories

    Example:
        >>> # UTILITY_SCRIPT
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> result = view_training_directories()
        >>> print(result)
    """
    ut.vd(ingest_wbia.get_juction_dpath())


def merge_datasets(dataset_list):
    """
    Merges a list of dataset objects into a single combined dataset.
    """

    def consensus_check_factory():
        """
        Returns a temporary function used to check that all incoming values
        with the same key are consistent
        """
        from collections import defaultdict

        past_values = defaultdict(lambda: None)

        def consensus_check(value, key):
            assert (
                past_values[key] is None or past_values[key] == value
            ), 'key=%r with value=%r does not agree with past_value=%r' % (
                key,
                value,
                past_values[key],
            )
            past_values[key] = value
            return value

        return consensus_check

    total_num_labels = 0
    total_num_data = 0

    input_alias_list = [dataset.alias_key for dataset in dataset_list]

    alias_key = 'combo_' + ut.hashstr27(repr(input_alias_list), hashlen=8)
    training_dpath = ut.ensure_app_resource_dir('wbia_cnn', 'training', alias_key)
    data_fpath = ut.unixjoin(training_dpath, alias_key + '_data.hdf5')
    labels_fpath = ut.unixjoin(training_dpath, alias_key + '_labels.hdf5')

    try:
        # Try and short circut cached loading
        merged_dataset = DataSet.from_alias_key(alias_key)
        return merged_dataset
    except (Exception, AssertionError) as ex:
        ut.printex(
            ex,
            'alias definitions have changed. alias_key=%r' % (alias_key,),
            iswarning=True,
        )

    # Build the dataset
    consensus_check = consensus_check_factory()

    for dataset in dataset_list:
        print(ut.get_file_nBytes_str(dataset.data_fpath))
        print(dataset.data_fpath_dict['full'])
        print(dataset.num_labels)
        print(dataset.data_per_label)
        total_num_labels += dataset.num_labels
        total_num_data += dataset.data_per_label * dataset.num_labels
        # check that all data_dims agree
        data_shape = consensus_check(dataset.data_shape, 'data_shape')
        data_per_label = consensus_check(dataset.data_per_label, 'data_per_label')

    # hack record this
    import numpy as np

    data_dtype = np.uint8
    label_dtype = np.int32
    data = np.empty((total_num_data,) + data_shape, dtype=data_dtype)
    labels = np.empty(total_num_labels, dtype=label_dtype)

    # def iterable_assignment():
    #    pass
    data_left = 0
    data_right = None
    labels_left = 0
    labels_right = None
    for dataset in ut.ProgressIter(dataset_list, lbl='combining datasets', freq=1):
        X_all, y_all = dataset.subset('full')
        labels_right = labels_left + y_all.shape[0]
        data_right = data_left + X_all.shape[0]
        data[data_left:data_right] = X_all
        labels[labels_left:labels_right] = y_all
        data_left = data_right
        labels_left = labels_right

    ut.save_data(data_fpath, data)
    ut.save_data(labels_fpath, labels)

    labels = ut.load_data(labels_fpath)
    num_labels = len(labels)

    merged_dataset = DataSet.new_training_set(
        alias_key=alias_key,
        data_fpath=data_fpath,
        labels_fpath=labels_fpath,
        metadata_fpath=None,
        training_dpath=training_dpath,
        data_shape=data_shape,
        data_per_label=data_per_label,
        output_dims=1,
        num_labels=num_labels,
    )
    return merged_dataset


def grab_dataset(ds_tag=None, datatype='siam-patch'):
    if datatype == 'siam-patch':
        return grab_siam_dataset(ds_tag=ds_tag)
    elif datatype == 'siam-part':
        return get_wbia_part_siam_dataset()
    elif datatype == 'category':
        return grab_mnist_category_dataset()


def grab_siam_dataset(ds_tag=None):
    r"""
    Will build the dataset using the command line if it doesn't exist

    CommandLine:
        python -m wbia_cnn.ingest_data --test-grab_siam_dataset --db mnist --show
        python -m wbia_cnn.ingest_data --test-grab_siam_dataset --db liberty --show
        python -m wbia_cnn.ingest_data --test-grab_siam_dataset --db PZ_MTEST --show

        python -m wbia_cnn.ingest_data --test-grab_siam_dataset --db PZ_MTEST --show --nohud --nometa
        python -m wbia_cnn.ingest_data --test-grab_siam_dataset --db liberty --show --nohud --nometa

    Example:
        >>> # ENABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> ds_tag = None
        >>> dataset = grab_siam_dataset(ds_tag=ds_tag)
        >>> ut.quit_if_noshow()
        >>> from wbia_cnn import draw_results
        >>> dataset.interact(ibs=dataset.getprop('ibs', None), key='test', chunck_sizes=(8, 4))
        >>> ut.show_if_requested()

    """
    if ds_tag is not None:
        try:
            return DataSet.from_alias_key(ds_tag)
        except Exception as ex:
            ut.printex(
                ex, 'Could not resolve alias. Need to rebuild dataset', keys=['ds_tag']
            )
            raise

    dbname = ut.get_argval('--db')
    if dbname == 'liberty':
        pairs = 250000
        dataset = grab_liberty_siam_dataset(pairs)
    elif dbname == 'mnist':
        dataset = grab_mnist_siam_dataset()
    else:
        dataset = get_wbia_patch_siam_dataset()
    return dataset


def grab_mnist_category_dataset_float():
    r"""
    CommandLine:
        python -m wbia_cnn grab_mnist_category_dataset_float
        python -m wbia_cnn grab_mnist_category_dataset_float --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> dataset = grab_mnist_category_dataset_float()
        >>> dataset.print_subset_info()
        >>> dataset.print_dir_tree()
        >>> ut.quit_if_noshow()
        >>> inter = dataset.interact()
        >>> ut.show_if_requested()
    """
    import numpy as np

    training_dpath = ut.ensure_app_resource_dir('wbia_cnn', 'training')
    dataset = DataSet(
        name='mnist_float32', training_dpath=training_dpath, data_shape=(28, 28, 1)
    )
    try:
        dataset.load()
    except IOError:
        data, labels, metadata = ingest_helpers.grab_mnist2()
        # Get indicies of test / train split
        splitset = np.array(metadata['splitset'])
        train_idxs = np.where(splitset == 'train')[0]
        test_idxs = np.where(splitset == 'test')[0]
        # Give dataset the full data
        dataset.save(data, labels, metadata, data_per_label=1)
        # And the split sets
        dataset.add_split('train', train_idxs)
        dataset.add_split('test', test_idxs)
        dataset.clear_cache()
    dataset.ensure_symlinked()
    return dataset


def grab_mnist_category_dataset():
    r"""
    CommandLine:
        python -m wbia_cnn grab_mnist_category_dataset
        python -m wbia_cnn grab_mnist_category_dataset_float
        python -m wbia_cnn grab_mnist_category_dataset --show

    Example:
        >>> # DISABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> dataset = grab_mnist_category_dataset()
        >>> dataset.print_subset_info()
        >>> dataset.print_dir_tree()
        >>> ut.quit_if_noshow()
        >>> inter = dataset.interact()
        >>> ut.show_if_requested()
    """
    import numpy as np

    training_dpath = ut.ensure_app_resource_dir('wbia_cnn', 'training')
    dataset = DataSet(
        name='mnist_uint8', training_dpath=training_dpath, data_shape=(28, 28, 1)
    )
    try:
        dataset.load()
    except IOError:
        data, labels, metadata = ingest_helpers.grab_mnist1()
        # Get indicies of test / train split
        train_idxs = np.arange(60000)
        test_idxs = np.arange(10000) + 60000
        # Give dataset the full data
        dataset.save(data, labels, metadata, data_per_label=1)
        # And the split sets
        dataset.add_split('train', train_idxs)
        dataset.add_split('test', test_idxs)
        dataset.clear_cache()
    dataset.ensure_symlinked()
    return dataset


def grab_mnist_siam_dataset():
    r"""

    CommandLine:
        python -m wbia_cnn.ingest_data --test-grab_mnist_siam_dataset --show

    Example:
        >>> # ENABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> dataset = grab_mnist_siam_dataset()
        >>> ut.quit_if_noshow()
        >>> from wbia_cnn import draw_results
        >>> #ibsplugin.rrr()
        >>> flat_metadata = {}
        >>> data, labels = dataset.subset('full')
        >>> ut.quit_if_noshow()
        >>> dataset.interact()
        >>> ut.show_if_requested()
    """
    training_dpath = ut.ensure_app_resource_dir('wbia_cnn', 'training')
    dataset = DataSet(
        name='mnist_pairs',
        training_dpath=training_dpath,
        data_shape=(28, 28, 1),
    )
    try:
        dataset.load()
    except IOError:
        data_, labels_, metadata_ = ingest_helpers.grab_mnist2()
        data, labels = ingest_helpers.convert_category_to_siam_data(data_, labels_)
        dataset.save(data, labels, data_per_label=2)
    return dataset


def grab_liberty_siam_dataset(pairs=250000):
    """
    References:
        http://www.cs.ubc.ca/~mbrown/patchdata/patchdata.html
        https://github.com/osdf/datasets/blob/master/patchdata/dataset.py

    Notes:
        "info.txt" contains the match information Each row of info.txt
        corresponds corresponds to a separate patch, with the patches ordered
        from left to right and top to bottom in each bitmap image.

        3 types of metadata files

        info.txt - contains patch ids that correspond with the order of patches
          in the bmp images
          In the format:
              pointid, unused

        interest.txt -
            interest points corresponding to patches with patchids
            has same number of rows as info.txt
            In the format:
                reference image id, x, y, orientation, scale (in log2 units)

        m50_<d>_<d>_0.txt -
             matches files
             patchID1  3DpointID1  unused1  patchID2  3DpointID2  unused2

    CommandLine:
        python -m wbia_cnn.ingest_data --test-grab_liberty_siam_dataset --show

    Example:
        >>> # ENABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> pairs = 500
        >>> dataset = grab_liberty_siam_dataset(pairs)
        >>> ut.quit_if_noshow()
        >>> from wbia_cnn import draw_results
        >>> #ibsplugin.rrr()
        >>> flat_metadata = {}
        >>> data, labels = dataset.subset('full')
        >>> ut.quit_if_noshow()
        >>> warped_patch1_list = data[::2]
        >>> warped_patch2_list = data[1::2]
        >>> dataset.interact()
        >>> ut.show_if_requested()
    """
    datakw = {
        'detector': 'dog',
        'pairs': pairs,
    }

    assert datakw['detector'] in ['dog', 'harris']
    assert pairs in [500, 50000, 100000, 250000]

    liberty_urls = {
        'dog': 'http://www.cs.ubc.ca/~mbrown/patchdata/liberty.zip',
        'harris': 'http://www.cs.ubc.ca/~mbrown/patchdata/liberty_harris.zip',
    }
    url = liberty_urls[datakw['detector']]
    ds_path = ut.grab_zipped_url(url)

    ds_name = splitext(basename(ds_path))[0]
    alias_key = 'liberty;' + ut.dict_str(datakw, nl=False, explicit=True)
    cfgstr = ','.join([str(val) for key, val in ut.iteritems_sorted(datakw)])

    # TODO: allow a move of the base data prefix

    training_dpath = ut.ensure_app_resource_dir('wbia_cnn', 'training', ds_name)
    if ut.get_argflag('--vtd'):
        ut.vd(training_dpath)
    ut.ensuredir(training_dpath)

    data_fpath = join(training_dpath, 'liberty_data_' + cfgstr + '.pkl')
    labels_fpath = join(training_dpath, 'liberty_labels_' + cfgstr + '.pkl')

    if not ut.checkpath(data_fpath, verbose=True):
        data, labels = ingest_helpers.extract_liberty_style_patches(ds_path, pairs)
        ut.save_data(data_fpath, data)
        ut.save_data(labels_fpath, labels)

    # hack for caching num_labels
    labels = ut.load_data(labels_fpath)
    num_labels = len(labels)

    dataset = DataSet.new_training_set(
        alias_key=alias_key,
        data_fpath=data_fpath,
        labels_fpath=labels_fpath,
        metadata_fpath=None,
        training_dpath=training_dpath,
        data_shape=(64, 64, 1),
        data_per_label=2,
        output_dims=1,
        num_labels=num_labels,
    )
    return dataset


def get_wbia_patch_siam_dataset(**kwargs):
    """
    CommandLine:
        python -m wbia_cnn.ingest_data --test-get_wbia_patch_siam_dataset --show
        python -m wbia_cnn.ingest_data --test-get_wbia_patch_siam_dataset --show --db PZ_Master1 --acfg_name default
        python -m wbia_cnn.ingest_data --test-get_wbia_patch_siam_dataset --show --db PZ_Master1 --acfg_name timectrl
        python -m wbia_cnn.ingest_data --test-get_wbia_patch_siam_dataset --show --db PZ_MTEST --acfg_name unctrl --dryrun

    Example:
        >>> # ENABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> from wbia_cnn import draw_results
        >>> import wbia
        >>> kwargs = {}  # ut.argparse_dict({'max_examples': None, 'num_top': 3})
        >>> dataset = get_wbia_patch_siam_dataset(**kwargs)
        >>> ut.quit_if_noshow()
        >>> dataset.interact()
        >>> ut.show_if_requested()
    """
    datakw = ut.argparse_dict(
        {
            #'db': 'PZ_MTEST',
            'max_examples': None,
            #'num_top': 3,
            'num_top': None,
            'min_featweight': 0.8 if not ut.WIN32 else None,
            'controlled': True,
            'colorspace': 'gray',
            'acfg_name': None,
        },
        alias_dict={'acfg_name': ['acfg', 'a']},
        verbose=True,
    )

    datakw.update(kwargs)

    # ut.get_func_kwargs(ingest_wbia.get_aidpairs_and_matches)

    if datakw['acfg_name'] is not None:
        del datakw['controlled']
    if datakw['max_examples'] is None:
        del datakw['max_examples']
    if datakw['num_top'] is None:
        del datakw['num_top']

    with ut.Indenter('[LOAD IBEIS DB]'):
        import wbia

        dbname = ut.get_argval('--db', default='PZ_MTEST')
        ibs = wbia.opendb(dbname=dbname, defaultdb='PZ_MTEST')

    # Nets dir is the root dir for all training on this data
    training_dpath = ibs.get_neuralnet_dir()
    ut.ensuredir(training_dpath)
    print('\n\n[get_wbia_patch_siam_dataset] START')
    # log_dir = join(training_dpath, 'logs')
    # ut.start_logging(log_dir=log_dir)

    alias_key = ibs.get_dbname() + ';' + ut.dict_str(datakw, nl=False, explicit=True)
    try:
        if NOCACHE_DATASET:
            raise Exception('forced cache off')
        # Try and short circut cached loading
        dataset = DataSet.from_alias_key(alias_key)
        dataset.setprop('ibs', lambda: wbia.opendb(db=dbname))
        return dataset
    except Exception as ex:
        ut.printex(
            ex,
            'alias definitions have changed. alias_key=%r' % (alias_key,),
            iswarning=True,
        )

    with ut.Indenter('[BuildDS]'):
        # Get training data pairs
        colorspace = datakw.pop('colorspace')
        patchmatch_tup = ingest_wbia.get_aidpairs_and_matches(ibs, **datakw)
        (
            aid1_list,
            aid2_list,
            kpts1_m_list,
            kpts2_m_list,
            fm_list,
            metadata_lists,
        ) = patchmatch_tup
        # Extract and cache the data
        # TODO: metadata
        if ut.get_argflag('--dryrun'):
            print('exiting due to dry run')
            import sys

            sys.exit(0)
        tup = ingest_wbia.cached_patchmetric_training_data_fpaths(
            ibs,
            aid1_list,
            aid2_list,
            kpts1_m_list,
            kpts2_m_list,
            fm_list,
            metadata_lists,
            colorspace=colorspace,
        )
        data_fpath, labels_fpath, metadata_fpath, training_dpath, data_shape = tup
        print('\n[get_wbia_patch_siam_dataset] FINISH\n\n')

    # hack for caching num_labels
    labels = ut.load_data(labels_fpath)
    num_labels = len(labels)

    dataset = DataSet.new_training_set(
        alias_key=alias_key,
        data_fpath=data_fpath,
        labels_fpath=labels_fpath,
        metadata_fpath=metadata_fpath,
        training_dpath=training_dpath,
        data_shape=data_shape,
        data_per_label=2,
        output_dims=1,
        num_labels=num_labels,
    )
    dataset.setprop('ibs', ibs)
    return dataset


def get_wbia_part_siam_dataset(**kwargs):
    """
    PARTS based network data

    CommandLine:
        python -m wbia_cnn.ingest_data --test-get_wbia_part_siam_dataset --show
        python -m wbia_cnn.ingest_data --test-get_wbia_part_siam_dataset --show --db PZ_Master1 --acfg_name timectrl
        python -m wbia_cnn.ingest_data --test-get_wbia_part_siam_dataset --show --db PZ_MTEST --acfg_name unctrl --dryrun

    Example:
        >>> # ENABLE_DOCTEST
        >>> from wbia_cnn.ingest_data import *  # NOQA
        >>> from wbia_cnn import draw_results
        >>> import wbia
        >>> kwargs = {}  # ut.argparse_dict({'max_examples': None, 'num_top': 3})
        >>> dataset = get_wbia_part_siam_dataset(**kwargs)
        >>> ut.quit_if_noshow()
        >>> dataset.interact(ibs=dataset.getprop('ibs'))
        >>> ut.show_if_requested()
    """
    import wbia

    datakw = ut.argparse_dict(
        {
            'colorspace': 'gray',
            'acfg_name': 'ctrl',
            #'db': None,
            'db': 'PZ_MTEST',
        },
        alias_dict={'acfg_name': ['acfg']},
        verbose=True,
    )

    datakw.update(kwargs)
    print('\n\n[get_wbia_part_siam_dataset] START')

    alias_key = ut.dict_str(datakw, nl=False, explicit=True)

    dbname = datakw.pop('db')

    try:
        if NOCACHE_DATASET:
            raise Exception('forced cache off')
        # Try and short circut cached loading
        dataset = DataSet.from_alias_key(alias_key)
        dataset.setprop('ibs', lambda: wbia.opendb(db=dbname))
        return dataset
    except Exception as ex:
        ut.printex(
            ex,
            'alias definitions have changed. alias_key=%r' % (alias_key,),
            iswarning=True,
        )

    with ut.Indenter('[LOAD IBEIS DB]'):
        ibs = wbia.opendb(db=dbname)

    # Nets dir is the root dir for all training on this data
    training_dpath = ibs.get_neuralnet_dir()
    ut.ensuredir(training_dpath)

    with ut.Indenter('[BuildDS]'):
        # Get training data pairs
        colorspace = datakw.pop('colorspace')
        (aid_pairs, label_list, flat_metadata) = ingest_wbia.get_aidpairs_partmatch(
            ibs, **datakw
        )
        # Extract and cache the data, labels, and metadata
        if ut.get_argflag('--dryrun'):
            print('exiting due to dry run')
            import sys

            sys.exit(0)
        tup = ingest_wbia.cached_part_match_training_data_fpaths(
            ibs, aid_pairs, label_list, flat_metadata, colorspace=colorspace
        )
        data_fpath, labels_fpath, metadata_fpath, training_dpath, data_shape = tup
        print('\n[get_wbia_part_siam_dataset] FINISH\n\n')

    # hack for caching num_labels
    labels = ut.load_data(labels_fpath)
    num_labels = len(labels)

    dataset = DataSet.new_training_set(
        alias_key=alias_key,
        data_fpath=data_fpath,
        labels_fpath=labels_fpath,
        metadata_fpath=metadata_fpath,
        training_dpath=training_dpath,
        data_shape=data_shape,
        data_per_label=2,
        output_dims=1,
        num_labels=num_labels,
    )
    dataset.setprop('ibs', ibs)
    return dataset


def get_numpy_dataset(data_fpath, labels_fpath, training_dpath):
    """"""
    import numpy as np

    # hack for caching num_labels
    data = np.load(data_fpath)
    data_shape = data.shape[1:]
    labels = np.load(labels_fpath)
    num_labels = len(labels)

    alias_key = 'temp'
    ut.ensuredir(training_dpath)

    dataset = DataSet.new_training_set(
        alias_key=alias_key,
        data_fpath=data_fpath,
        labels_fpath=labels_fpath,
        metadata_fpath=None,
        training_dpath=training_dpath,
        data_shape=data_shape,
        data_per_label=1,
        output_dims=1,
        num_labels=num_labels,
    )
    return dataset


def get_numpy_dataset2(name, data_fpath, labels_fpath, training_dpath, cache=True):
    """"""
    import numpy as np

    # hack for caching num_labels
    data = np.load(data_fpath)
    data_shape = data.shape[1:]
    labels = np.load(labels_fpath)
    num_labels = len(labels)
    metadata = None

    dataset = DataSet(
        name=name,
        training_dpath=training_dpath,
        data_shape=data_shape,
    )
    error = False
    try:
        dataset.load()
    except IOError:
        error = True

    if error or not cache:
        import random

        # Get indicies of valid / train split
        idx_list = list(range(num_labels))
        random.shuffle(idx_list)

        split_idx = int(num_labels * 0.80)
        train_idxs = np.array(idx_list[:split_idx])
        valid_idxs = np.array(idx_list[split_idx:])
        # Give dataset the full data
        dataset.save(data, labels, metadata, data_per_label=1)
        # And the split sets
        dataset.add_split('train', train_idxs)
        dataset.add_split('valid', valid_idxs)
        dataset.clear_cache()
        print('LOADING FROM DATASET RAW')

    dataset.ensure_symlinked()
    return dataset


if __name__ == '__main__':
    """
    CommandLine:
        python -m wbia_cnn.ingest_data
        python -m wbia_cnn.ingest_data --allexamples
        python -m wbia_cnn.ingest_data --allexamples --noface --nosrc
    """
    import multiprocessing

    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA

    ut.doctest_funcs()
