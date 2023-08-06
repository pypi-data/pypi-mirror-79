#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import numpy as np
import utool
import utool as ut


def TEST_ptool_find_kpts_direction(imgBGR, kpts):
    import vtool.patch as ptool

    hrint = utool.horiz_print
    print('[rotinvar] +---')
    print('[rotinvar] | 3) Find dominant orientation in histogram')
    hrint('[rotinvar] |  * kpts.shape = ', (kpts.shape,))
    hrint('[rotinvar] |  * kpts = ', kpts)
    kpts2 = ptool.find_kpts_direction(imgBGR, kpts)
    hrint('[rotinvar] |  * kpts2.shape = ', (kpts.shape,))
    hrint('[rotinvar] |  * kpts2 = ', kpts2)
    print('[rotinvar] L___')
    return kpts2


def TEST_figure1(wpatch, gradx, grady, gmag, gori, hist, centers):
    from wbia.plottool import draw_func2 as df2
    from wbia import plottool
    import vtool.patch as ptool

    print('[rotinvar] 4) Draw histogram with interpolation annotations')
    fnum = 1
    gorimag = plottool.color_orimag(gori, gmag, True)
    nRow, nCol = (2, 7)

    df2.figure(fnum=1, pnum=(nRow, 1, nRow), doclf=True, docla=True)
    plottool.draw_hist_subbin_maxima(hist, centers)
    df2.set_xlabel('grad orientation (radians)')
    df2.set_ylabel('grad magnitude')
    df2.set_title('dominant orientations')

    print('[rotinvar] 5) Show patch, gradients, magintude, and orientation')
    df2.imshow(wpatch, pnum=(nRow, nCol, 1), fnum=fnum, title='patch')
    df2.draw_vector_field(
        gradx, grady, pnum=(nRow, nCol, 2), fnum=fnum, title='gori (vec)'
    )
    df2.imshow(gorimag, pnum=(nRow, nCol, 3), fnum=fnum, title='gori (col)')
    df2.imshow(np.abs(gradx), pnum=(nRow, nCol, 4), fnum=fnum, title='gradx')
    df2.imshow(np.abs(grady), pnum=(nRow, nCol, 5), fnum=fnum, title='grady')
    df2.imshow(gmag, pnum=(nRow, nCol, 6), fnum=fnum, title='gmag')

    gpatch = ptool.gaussian_patch(shape=gori.shape)
    df2.imshow(
        gpatch * 255, pnum=(nRow, nCol, 7), fnum=fnum, title='gauss weights', cmap_='hot'
    )
    # gpatch3 = np.dstack((gpatch, gpatch, gpatch))
    # df2.draw_vector_field(gradx * gpatch, grady * gpatch, pnum=(nRow, nCol, 8), fnum=fnum, title='gori (vec)')
    # df2.imshow(gorimag * gpatch3, pnum=(nRow, nCol, 9), fnum=fnum, title='gori (col)')
    # df2.imshow(gradx * gpatch,   pnum=(nRow, nCol, 10), fnum=fnum, title='gradx')
    # df2.imshow(grady * gpatch,   pnum=(nRow, nCol, 11), fnum=fnum, title='grady')
    # df2.imshow(gmag * gpatch,    pnum=(nRow, nCol, 12), fnum=fnum, title='gmag')
    return locals()


def TEST_figure2(imgBGR, kpts, desc, sel, fnum=2):
    # df2.imshow(wpatch, fnum=2)
    from wbia.plottool import draw_func2 as df2
    from wbia.plottool.viz_keypoints import _annotate_kpts, show_keypoints
    from wbia.plottool.viz_featrow import draw_feat_row

    sift = desc[sel]
    viz_kwargs = dict(
        ell=True,
        eig=False,
        rect=True,
        ori_color=df2.DEEP_PINK,
        ell_alpha=1,
        fnum=fnum,
        pnum=(2, 1, 1),
    )
    show_keypoints(imgBGR, kpts, sifts=None, sel_fx=sel, ori=False, **viz_kwargs)
    _annotate_kpts(kpts, sel, ori=True, **viz_kwargs)
    draw_feat_row(imgBGR, sel, kpts[sel], sift, fnum=fnum, nRows=2, nCols=3, px=3)


def TEST_keypoint(imgBGR, img_fpath, kpts, desc, sel):
    import pyhesaff
    import vtool.patch as ptool
    from wbia.plottool import draw_func2 as df2

    # ----------------------#
    # --- Extract Data --- #
    # ----------------------#
    kp = kpts[sel]
    # Extract patches, gradients, and orientations
    print('[rotinvar] 1) Extract patch, gradients, and orientations')
    wpatch, wkp = ptool.get_warped_patch(imgBGR, kp, gray=True)
    gradx, grady = ptool.patch_gradient(wpatch, gaussian_weighted=False)
    gmag = ptool.patch_mag(gradx, grady)
    gori = ptool.patch_ori(gradx, grady)

    # Get orientation histogram
    print('[rotinvar] 2) Get orientation histogram')
    gori_weights = ptool.gaussian_weight_patch(gmag)
    hist, centers = ptool.get_orientation_histogram(gori, gori_weights)

    # Get dominant direction in radians
    kpts2 = TEST_ptool_find_kpts_direction(imgBGR, kpts)
    kpts2, desc2 = pyhesaff.vtool_adapt_rotation(img_fpath, kpts)

    # ----------------------#
    # --- Draw Results --- #
    # ----------------------#
    f1_loc = TEST_figure1(wpatch, gradx, grady, gmag, gori, hist, centers)
    df2.set_figtitle('Dominant Orienation Extraction')

    TEST_figure2(imgBGR, kpts, desc, sel, fnum=2)
    df2.set_figtitle('Gravity Vector')
    TEST_figure2(imgBGR, kpts2, desc2, sel, fnum=3)
    df2.set_figtitle('Rotation Invariant')

    # df2.draw_keypoint_gradient_orientations(imgBGR, kp=kpts2[sel],
    #                                        sift=desc[sel], mode='vec',
    #                                        fnum=4)

    # df2.draw_vector_field(gradx, grady, pnum=(1, 1, 1), fnum=4)
    # df2.draw_kpts2(np.array([wkp]), sifts=desc[sel:sel + 1], ori=True)
    return locals()


def test_patch_ori_main():
    r"""
    Returns:
        ?: locals_

    CommandLine:
        python -m tests.test_patch_orientation --test-test_patch_ori_main
        python -m tests.test_patch_orientation --test-test_patch_ori_main --show

    Example:
        >>> # xdoctest: +SKIP
        >>> from tests.test_patch_orientation import *  # NOQA
        >>> test_patch_ori_main()
        >>> ut.show_if_requested()
    """
    print('[rotinvar] loading test data')
    import pyhestest

    test_data = pyhestest.load_test_data(short=True, n=3)
    img_fpath = test_data['img_fpath']
    kpts = test_data['kpts']
    desc = test_data['desc']
    imgBGR = test_data['imgBGR']
    sel = min(len(kpts) - 1, 3)

    locals_ = TEST_keypoint(imgBGR, img_fpath, kpts, desc, sel)
    return locals_


if __name__ == '__main__':
    """
    CommandLine:
        python -m tests.test_patch_orientation
        python -m tests.test_patch_orientation --allexamples
        python -m tests.test_patch_orientation --allexamples --noface --nosrc
    """
    import multiprocessing

    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA

    ut.doctest_funcs()
