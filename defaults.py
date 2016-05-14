    #Copyright 2009-2016 Seyed Hessam Moosavi Mehr, Juergen Probst
    #This program is free software; you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation; either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, print_function

default_resolution = 32
default_mesh_size = 3
default_numbands = 2
default_k_interpolation = 3
default_initcode = (';load module for calculating local dos:\n'
                    '(define dosmodule (%search-load-path "dosv2.scm"))\n'
                    '(if dosmodule\n'
                    '    (include dosmodule)\n'
                    '    (throw \'error "dos.scm not found"))\n\n'
                    # remove the default filename-prefix:
                    # before MPB 1.5:
                    #'(set! filename-prefix "")\n')
                    # MPB 1.5 and newer:
                    '(set! filename-prefix #f)\n')
default_postcode = ''
default_runcode = '(run-tm)'

number_of_tiles_to_output = 3
# Field patterns transformed to PNG will be placed in subfolders named
# (field_output_folder_prefix + '_' + mode):
field_output_folder_prefix = 'pngs'

# poi: k-points of interest:
default_band_func_tm = lambda poi : (
        '\n    display-group-velocities' +
        ''.join([(
        '\n    (output-at-kpoint (vector3 %s) '
        'fix-efield-phase output-efield-z)') %
        ' '.join(str(c) for c in vec) for vec in poi]))
# poi: k-points of interest:
default_band_func_te = lambda poi : (
        '\n    display-group-velocities' +
        ''.join([(
        '\n    (output-at-kpoint (vector3 %s) '
        'fix-efield-phase output-hfield-z)') %
        ' '.join(str(c) for c in vec) for vec in poi]))


#mpb_call = 'mpb'
mpb_call = 'mpirun -np %(num_procs)s mpb-mpi'

# use -T if we run the simulation with mpb-mpi:
mpbdata_call = ('mpb-data -T -rn%(resolution)s '
                '-x%(number_of_tiles_to_output)s '
                '-y%(number_of_tiles_to_output)s '
                '-o%(output_file)s '
                '%(h5_file)s')
epsh5topng_call_2D = 'h5topng -S3 -Zrcbluered -oepsilon.png %(h5_file)s'
epsh5topng_call_3D = 'h5topng -0z0 -S3 -Zrcbluered -oepsilon.png %(h5_file)s'
epsh5topng_call_3D_cross_sect = ('h5topng -0x0 -S3 -Zrcbluered '
                              '-oepsilonslab.png %(h5_file)s')

fieldh5topng_call_2D = ('h5topng -S3 -Zcbluered -C%(eps_file)s '
                        '-o%(output_file)s %(h5_file)s')
fieldh5topng_call_2D_no_ovl = ('h5topng -S3 -Zcbluered '
                        '-o%(output_file_no_ovl)s %(h5_file)s')

fieldh5topng_call_3D = ('h5topng -0z0 -S3 -Zcbluered -C%(eps_file)s '
                        '-o%(output_file)s %(h5_file)s')
fieldh5topng_call_3D_no_ovl = ('h5topng -0z0 -S3 -Zcbluered '
                        '-o%(output_file_no_ovl)s %(h5_file)s')
display_png_call = 'display  %(files)s'

temporary_epsh5 = './temporary_eps.h5'
temporary_h5 = './temporary.h5'
temporary_h5_folder = './patterns~/'

isQuiet = False
template = '''%(initcode)s

(set! geometry-lattice %(lattice)s)

(set! resolution %(resolution)s)

(set! mesh-size %(meshsize)s)

(set! num-bands %(numbands)s)

(set! k-points %(kspace)s)

(set! geometry (list %(geometry)s))

%(runcode)s

%(postcode)s

(display-eigensolver-stats)'''



#####################################################
###          bandplotter defaults                 ###
#####################################################


log_format = "%(asctime)s %(levelname)s: %(message)s"
log_datefmt = "%d.%m.%Y %H:%M:%S"

fig_size = (12, 9)

# default kwargs for the tick labels for the k-vec-axis of band diagrams:
# (will be forwarded to underlying matplotlib.text.Text objects)
xticklabels_kwargs={'rotation':0, 'horizontalalignment':'center'}
# xticklabels_kwargs used when one of the labels strings is longer than
# long_xticklabels_when_longer_than:
long_xticklabels_kwargs={'rotation':45, 'horizontalalignment':'right'}
long_xticklabels_when_longer_than = 12

# Text added to gaps drawn in the band diagrams,
# formatted with default_gaptext.format(gapsize_in_percent):
default_gaptext='gap size: {0:.2f}%'
default_x_axis_hint = 4 # 4 equally spaced ticks, labeled with k-vector
default_y_axis_label = r'frequency $\omega a/2\pi c$'
default_x_axis_label = 'wave vector {0}'
# the x_axis_label used when showing high symmetry point labels on the k
# axis: Note: I am not entirely satisfied with this title. How do you
# really call it? 'Brilluoin zone symmetry points'? 'Wave vector
# direction'? (this last one is good, but we also see the magnitude,
# when e.g. going from Gamma to M etc.) 'Wave vector point in brilluoin
# zone'? (too long)
default_kspace_axis_label = 'wave vector k point'

default_kvecformatter_format_str = '({0:.2f}, {1:.2f}, {2:.2f})'
# other possibilities:
#default_kvecformatter_format_str = r'$\binom{{ {0} }}{{ {1} }}$'
# unfortunately, \stackrel[3]{}{}{} does not work, so it looks bad:
#default_kvecformatter_format_str = \
#    r'$\left(\stackrel{{ {0} }}{{ \stackrel{{ {1} }}{{ {2} }} }}\right)$'
#default_kvecformatter_format_str ='{0}\n{1}\n{2}'

# Show fractions in tick labels of k-axis instead of floating point values:
ticks_fractions = True
# Always show a floating point value if the resulting fraction's denominator
# is greater than:
tick_max_denominator = 1000


def default_onclick(event, bandplotter):
    """This is the default function called if the bands are plotted with a
    picker supplied and the user clicks on a vertex in the plot. It then just
    prints some information about the vertex(ices) clicked on to stdout,
    including the mode, the k-vector and -index and the frequency(ies).

    """
    try:
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        xaxisformatter = event.mouseevent.inaxes.xaxis.major.formatter
    except AttributeError:
        return
    
    print(thisline.get_label() + ' mode(s): ', end='')
    for i in ind:
        print('k_index={0:.0f}, k_vec={2}, freq={1}; '.format(
            xdata[i], ydata[i], xaxisformatter(xdata[i])), end='')
    print()

    # Other idea (not implemented): display mode pattern if it was exported
    # or even calculate it if not exported yet, e.g.:
    ## Start interactive mode:
    #plt.ion()
    ## create a new popup figure:
    #fig = plt.figure('mode pattern', figsize=(6, 2))
    #ax = fig.add_subplot(111) #put mode pattern image here

contour_lines = {'colors':'k',
                 'linestyles':['dashed','solid'],
                 'linewidths':1.0}
contour_plain = {'linewidths':1.0}
contour_filled = {}
colorbar_style = {'extend':'both','shrink':0.8}
