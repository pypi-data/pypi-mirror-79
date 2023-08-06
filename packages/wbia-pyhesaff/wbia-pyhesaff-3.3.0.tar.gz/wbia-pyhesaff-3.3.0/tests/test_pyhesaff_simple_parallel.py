#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import numpy as np
from six.moves import zip
import utool as ut


def test_simple_parallel():
    r"""
    CommandLine:
        python -m tests.test_pyhesaff_simple_parallel --test-test_simple_parallel --show

    Example:
        >>> # ENABLE_DOCTEST
        >>> from tests.test_pyhesaff_simple_parallel import *  # NOQA
        >>> import matplotlib as mpl
        >>> from matplotlib import pyplot as plt
        >>> img_fpaths, kpts_array, desc_array = test_simple_parallel()
        >>> ut.quit_if_noshow()
        >>> # Do not plot by default
        >>> fig = plt.figure()
        >>> for count, (img_fpath, kpts, desc) in enumerate(zip(img_fpaths, kpts_array,
        >>>                                                     desc_array)):
        >>>     if count > 3:
        >>>         break
        >>>     ax = fig.add_subplot(2, 2, count + 1)
        >>>     img = mpl.image.imread(img_fpath)
        >>>     plt.imshow(img)
        >>>     _xs, _ys = kpts.T[0:2]
        >>>     ax.plot(_xs, _ys, 'ro', alpha=.5)
        >>> ut.show_if_requested()
    """
    import pyhesaff

    test_fnames = ['carl.jpg', 'lena.png', 'zebra.png', 'ada.jpg', 'star.png']
    img_fpaths = list(map(ut.grab_test_imgpath, test_fnames)) * 2

    # Time parallel computation
    with ut.Timer('Timing Parallel'):
        kpts_array, desc_array = pyhesaff.detect_feats_list(img_fpaths)

    # Time serial computation
    kpts_list2 = []
    desc_list2 = []
    with ut.Timer('Timing Iterative'):
        for img_fpath in img_fpaths:
            kpts_, desc_ = pyhesaff.detect_feats(img_fpath)
            kpts_list2.append(kpts_)
            desc_list2.append(desc_)

    print('Checking for errors')
    for (kpts_, desc_, kpts, desc) in zip(kpts_list2, desc_list2, kpts_array, desc_array):
        print(
            'shape(kpts, kpts_, desc, desc_) = %9r, %9r, %11r, %11r'
            % (kpts.shape, kpts_.shape, desc.shape, desc_.shape)
        )
        try:
            assert np.all(kpts_ == kpts), 'parallel computation inconsistent'
            assert np.all(desc_ == desc), 'parallel computation inconsistent'
            assert len(kpts_) > 0, 'no kpts detected'
            # assert False, 'deliberate triggering to see printouts'
        except Exception as ex:
            ut.printex(ex)
            raise
    print('Keypoints seem consistent')
    return img_fpaths, kpts_array, desc_array


if __name__ == '__main__':
    """
    CommandLine:
        python -m tests.test_pyhesaff_simple_parallel
        python -m tests.test_pyhesaff_simple_parallel --allexamples
        python -m tests.test_pyhesaff_simple_parallel --allexamples --noface --nosrc
    """
    import multiprocessing

    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA

    ut.doctest_funcs()
