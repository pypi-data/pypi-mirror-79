from .mutagenesis_visualization import *
import numpy as np
import os
import sys

__author__ = "Frank Hidalgo"
__version__ = "0.0.1"
__title__ = "Mutagenesis Visualization"
__license__ = "GPLv3"
__author_email__ = "fhidalgoruiz@berkeley.edu"


def demo(figure='heatmap'):
    """
    Performs a demonstration of the mutagenesis_visualization software.

    Parameters
    -----------
    figure : str, default 'heatmap'
        There are 5 example plots that can be displayed to test the package is working on your station.
        The 5 options are 'heatmap', 'miniheatmap', 'mean', 'kernel' and 'pca'. Check the documentation for more information.

    Returns
    -------
    None.
    """
    # Use relative file import to access the data folder
    location = os.path.dirname(os.path.realpath(__file__))
    my_file = os.path.join(location, 'data', 'HRas166_RBD.csv')

    # Load enrichment scores
    hras_enrichment_RBD = np.genfromtxt(my_file, delimiter=',')

    # Define protein sequence
    hras_sequence = 'MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHQYREQIKRVKDSDDVPMVLVGNKCDLAARTVESRQAQDLARSYGIPYIETSAKTRQGVEDAFYTLVREIRQHKLRKLNPPDESGPG'

    # Define secondary structure
    secondary = [['L0'], ['β1']*(9-1), ['L1']*(15-9), ['α1']*(25-15), ['L2']*(36-25), ['β2']*(46-36), ['L3']*(48-46), 
                 ['β3']*(58-48), ['L4'] * (64-58),['α2']*(74-64), ['L5']*(76-74), ['β4']*(83-76), 
                 ['L6']*(86-83), ['α3']*(103-86), ['L7']*(110-103), ['β5']*(116-110), ['L8']*(126-116), ['α4']*(137-126),
                 ['L9']*(140-137), ['β6']*(143-140), ['L10']*(151-143), ['α5']*(172-151), ['L11']*(190-172)]

    # Create object
    hras_RBD = Screen(dataset=hras_enrichment_RBD,
                      sequence=hras_sequence, secondary=secondary)

    if figure == 'heatmap':
        # Create heatmap plot
        hras_RBD.heatmap(title='H-Ras 2-166', show_cartoon=True)
    elif figure == 'miniheatmap':
        # Condensed heatmap
        hras_RBD.miniheatmap(title='Wt residue H-Ras')
    elif figure == 'mean':
        # Mean enrichment by position
        hras_RBD.mean(figsize=[6, 2.5], mode='mean',show_cartoon=True, yscale=[-2, 0.5], title = '')
    elif figure == 'kernel':
        # Plot kernel dist using sns.distplot.
        hras_RBD.kernel(histogram=True, title='H-Ras 2-166', xscale=[-2, 1])
    elif figure == 'pca':
        # PCA by amino acid substitution
        hras_RBD.pca(dimensions=[0, 1], figsize=(2, 2), adjustlabels=True, title = '')
    return
    
def demo_datasets():
    '''
    Loads example datasets so the user can play with it.
    
    Parameters
    -----------
    None
    
    Returns
    --------
    data_dict : dictionary
        Dictionary that contains the datasets used to create the plots on the documentation.
    '''
    
    # Use relative file import to access the data folder
    location = os.path.dirname(os.path.realpath(__file__))
    
    # Create dictionary where to store data
    data_dict = {}
    
    # Retrieve H-Ras dataset and store in dict
    my_file = os.path.join(location, 'data', 'HRas166_RBD.csv')
    hras_enrichment_RBD = np.genfromtxt(my_file, delimiter=',')
    data_dict['array_hras'] = hras_enrichment_RBD
    
    # Beta lactamase data
    my_file = os.path.join(location, 'data', 'df_bla_raw.pkl')
    df_bla_raw = pd.read_pickle(my_file)
    data_dict['df_bla'], sequence_bla = parse_pivot(df_bla_raw, col_data = 'DMS_amp_625_(b)')

    # Sumo
    my_file = os.path.join(location, 'data', 'df_sumo1_raw.pkl')
    df_sumo1_raw = pd.read_pickle(my_file)
    data_dict['df_sumo1'], sequence_sumo1 = parse_pivot(df_sumo1_raw, col_data = 'DMS')
   
    # MAPK1
    my_file = os.path.join(location, 'data', 'df_mapk1_raw.pkl')
    df_mapk1_raw = pd.read_pickle(my_file)
    data_dict['df_mapk1'], sequence_mapk1 = parse_pivot(df_mapk1_raw, col_data = 'DMS_DOX')
    
    #UBE2I
    my_file = os.path.join(location, 'data', 'df_ube2i_raw.pkl')
    df_ube2i_raw = pd.read_pickle(my_file)
    data_dict['df_ube2i'], sequence_ube2i = parse_pivot(df_ube2i_raw, col_data = 'DMS')

    #TAT
    my_file = os.path.join(location, 'data', 'df_tat.pkl')
    data_dict['df_tat'] = pd.read_pickle(my_file)

    #REV
    my_file = os.path.join(location, 'data', 'df_rev.pkl')
    data_dict['df_rev'] = pd.read_pickle(my_file)
    
    # asynuclein
    my_file = os.path.join(location, 'data', 'df_asynuclein.pkl')
    data_dict['df_asynuclein'] = pd.read_pickle(my_file)
    
    # APH
    my_file = os.path.join(location, 'data', 'df_aph.pkl')
    data_dict['df_aph'] = pd.read_pickle(my_file)

    # b11L5
    my_file = os.path.join(location, 'data', 'df_b11L5F_raw.pkl')
    df_b11L5F_raw = pd.read_pickle(my_file)
    data_dict['df_b11L5F'], sequence_b11L5F = parse_pivot(df_b11L5F_raw, col_data = 'relative_tryp_stability_score')
    
    return data_dict