import numpy as np
import dust_tools.extinction_tools
import os
from urllib3 import PoolManager


def download_file(file_path, url, unpack=False, reload=False):
    """

    Parameters
    ----------
    file_path : str or ``pathlib.Path``
    url : str
    unpack : bool
        In case the downloaded file is zipped, this function can unpack it and remove the downloaded file,
        leaving only the extracted file
    reload : bool
        If the file is corrupted, this removes the file and reloads it

    Returns
    -------

    """
    if reload:
        # if reload file the file will be removed to re download it
        os.remove(file_path)
    # check if file already exists
    if os.path.isfile(file_path):
        print(file_path, 'already exists')
        return True
    else:
        # download file
        http = PoolManager()
        r = http.request('GET', url, preload_content=False)

        if unpack:
            with open(file_path.with_suffix(".gz"), 'wb') as out:
                while True:
                    data = r.read()
                    if not data:
                        break
                    out.write(data)
            r.release_conn()
            # uncompress file
            from gzip import GzipFile
            # read compressed file
            compressed_file = GzipFile(file_path.with_suffix(".gz"), 'rb')
            s = compressed_file.read()
            compressed_file.close()
            # save compressed file
            uncompressed_file = open(file_path, 'wb')
            uncompressed_file.write(s)
            uncompressed_file.close()
            # delete compressed file
            os.remove(file_path.with_suffix(".gz"))
        else:
            with open(file_path, 'wb') as out:
                while True:
                    data = r.read()
                    if not data:
                        break
                    out.write(data)
            r.release_conn()


def plot_reddening_vect(ax,
                        x_wave_1=3366, x_wave_2=4339,  y_wave_1=5389, y_wave_2=8117,
                        init_x_color=0, init_y_color=0, av_value_mag=1,
                        arrow_line_width=2, arrow_line_color='k',
                        show_av_value=False, text_font_size=20, text_color='k', x_text_offset=0.1, y_text_offset=-0.3):
    """
    Function to plot reddening vector on color-color diagram based on reddening law described in
    Cardelli, Clayton, & Mathis (1989) Milky Way R(V) dependent model

    Parameters
    ----------
    ax : ``matplotlib.pylab.Axes``
        axis on which to plot
    x_wave_1, x_wave_2, y_wave_1, y_wave_2 : int or float
        Wavelengths in Angstrom for the 4 used colors. The colors are calculated as x_wave_1 - x_wave_2 and
        y_wave_1 - y_wave_2 on the X- and Y-axes, respectively.
    init_x_color , init_y_color : float
        initial x and Y color from where the reddening vector stars
    av_value_mag : float
        A_v value to determining the length of the reddening vector

    arrow_line_width : float or int
    arrow_line_color : str
    show_av_value : bool
        flag to show the A_v value as a text
    text_font_size : float or int
    text_color : str
    x_text_offset , y_text_offset : float
        in units of x and y colors the amount you need to offset the text from the arrow to avoid overlapping


    Returns
    -------
    None

    """
    # change wavelength unit from Angstrom into micron
    x_wave_1 *= 1e-4
    x_wave_2 *= 1e-4
    y_wave_1 *= 1e-4
    y_wave_2 *= 1e-4
    # calculate the color difference from reddening
    color_ext_x = dust_tools.extinction_tools.ExtinctionTools.color_ext_ccm89_av(wave1=x_wave_1, wave2=x_wave_2,
                                                                                 av=av_value_mag)
    color_ext_y = dust_tools.extinction_tools.ExtinctionTools.color_ext_ccm89_av(wave1=y_wave_1, wave2=y_wave_2,
                                                                                 av=av_value_mag)
    # plot arrow annotation with the calculated color differences
    ax.annotate('', xy=(init_x_color + color_ext_x, init_y_color + color_ext_y), xycoords='data',
                xytext=(init_x_color, init_y_color), fontsize=text_font_size,
                textcoords='data', arrowprops=dict(arrowstyle='-|>', color=arrow_line_color, lw=arrow_line_width, ls='-'))
    # add A_v value as text
    if show_av_value:
        if isinstance(av_value_mag, int):
            arrow_text = r'A$_{\rm V}$=%i mag' % av_value_mag
        else:
            arrow_text = r'A$_{\rm V}$=%.1f mag' % av_value_mag
        # calculate the angle of the reddening vector in order to annotate text parallel to it
        angle_av_vector = np.arctan(color_ext_y/color_ext_x) * 180/np.pi
        ax.text(init_x_color + x_text_offset, init_y_color + y_text_offset, arrow_text,
                horizontalalignment='left', verticalalignment='bottom',
                transform_rotates_text=True, rotation_mode='anchor',
                rotation=angle_av_vector, fontsize=text_font_size, color=text_color)
