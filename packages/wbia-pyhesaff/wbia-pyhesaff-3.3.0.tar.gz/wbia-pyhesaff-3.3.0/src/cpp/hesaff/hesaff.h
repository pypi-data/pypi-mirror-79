#ifndef _HESAFF_DLLDEFINES_H
#define _HESAFF_DLLDEFINES_H

#ifdef WIN32
#ifndef snprintf
#define snprintf _snprintf
#endif // ndef sprintf
#endif // WIN32

#ifdef HESAFF_EXPORT
#undef HESAFF_EXPORT
#endif
#ifdef WIN32
/* win32 dll export/import directives */
 #ifdef HESAFF_EXPORTS
  #define HESAFF_EXPORT __declspec(dllexport)
 #elif defined(HESAFF_STATIC)
  #define HESAFF_EXPORT
 #else
  #define HESAFF_EXPORT __declspec(dllimport)
 #endif
#else
/* unix needs nothing */
 #define HESAFF_EXPORT
#endif

// TODO : use either adapt_rotation or rotation_invariance, but not both

struct HesaffParams
{
    float scale_min;     // minimum scale threshold
    float scale_max;     // maximum scale threshold
    float ori_maxima_thresh;  // threshold for orientation invariance
    bool rotation_invariance;  // are we assuming the gravity vector?
    bool adapt_rotation;
    bool adapt_scale;
    bool affine_invariance;
    bool augment_orientation;
    bool only_count;

    HesaffParams()
    {
        scale_min = -1;
        scale_max = -1;
        ori_maxima_thresh = .8;
        rotation_invariance = false; //remove in favor of adapt_rotation?
        augment_orientation = false; //remove in favor of adapt_rotation?
        adapt_rotation = false;
        adapt_scale = false;
        affine_invariance = true;  // if false uses circular keypoints
        only_count = false;
    }
};

#endif //_HESAFF_DLLDEFINES_H
