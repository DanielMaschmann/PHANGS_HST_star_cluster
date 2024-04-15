import numpy as np
import dust_tools.extinction_tools


def plot_reddening_vect(ax, x_color_1='v', x_color_2='i',  y_color_1='u', y_color_2='b',
                        x_color_int=0, y_color_int=0, av_val=1,
                        linewidth=2, line_color='k',
                        text=False, fontsize=20, text_color='k', x_text_offset=0.1, y_text_offset=-0.3):

    catalog_access = photometry_tools.data_access.CatalogAccess()

    nuv_wave = catalog_access.hst_wfc3_uvis1_bands_mean_wave['F275W']*1e-4
    u_wave = catalog_access.hst_wfc3_uvis1_bands_mean_wave['F336W']*1e-4
    b_wave = catalog_access.hst_wfc3_uvis1_bands_mean_wave['F438W']*1e-4
    v_wave = catalog_access.hst_wfc3_uvis1_bands_mean_wave['F555W']*1e-4
    i_wave = catalog_access.hst_wfc3_uvis1_bands_mean_wave['F814W']*1e-4

    x_wave_1 = locals()[x_color_1 + '_wave']
    x_wave_2 = locals()[x_color_2 + '_wave']
    y_wave_1 = locals()[y_color_1 + '_wave']
    y_wave_2 = locals()[y_color_2 + '_wave']

    color_ext_x = dust_tools.extinction_tools.ExtinctionTools.color_ext_ccm89_av(wave1=x_wave_1, wave2=x_wave_2, av=av_val)
    color_ext_y = dust_tools.extinction_tools.ExtinctionTools.color_ext_ccm89_av(wave1=y_wave_1, wave2=y_wave_2, av=av_val)

    slope_av_vector = ((y_color_int + color_ext_y) - y_color_int) / ((x_color_int + color_ext_x) - x_color_int)

    angle_av_vector = np.arctan(color_ext_y/color_ext_x) * 180/np.pi

    ax.annotate('', xy=(x_color_int + color_ext_x, y_color_int + color_ext_y), xycoords='data',
                xytext=(x_color_int, y_color_int), fontsize=fontsize,
                textcoords='data', arrowprops=dict(arrowstyle='-|>', color=line_color, lw=linewidth, ls='-'))

    if text:
        if isinstance(av_val, int):
            arrow_text = r'A$_{\rm V}$=%i mag' % av_val
        else:
            arrow_text = r'A$_{\rm V}$=%.1f mag' % av_val
        ax.text(x_color_int + x_text_offset, y_color_int + y_text_offset, arrow_text,
                horizontalalignment='left', verticalalignment='bottom',
                transform_rotates_text=True, rotation_mode='anchor',
                rotation=angle_av_vector, fontsize=fontsize, color=text_color)
