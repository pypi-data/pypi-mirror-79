import os
import warnings
from .util import run_command


def fill_nodata(infile, outfile=None, inplace=True, max_distance=None):
    if outfile is not None and inplace:
        warnings.warn('inplace parameter is set to True, interpolation will be performed in place on the source file, '
                      'the specified outfile will be ignored and not generated. Set inplace=False to generate a '
                      'new file for the interpolated result')
    args = ['gdal_fillnodata.py']
    if max_distance is not None:
        args.extend(['-md', max_distance])
    args.append(infile)
    if not inplace:
        outfile = outfile or os.path.splitext(infile)[0] + '_filled' + os.path.splitext(infile)[1]
        args.append(outfile)
    run_command(args)
    return infile if inplace else outfile
