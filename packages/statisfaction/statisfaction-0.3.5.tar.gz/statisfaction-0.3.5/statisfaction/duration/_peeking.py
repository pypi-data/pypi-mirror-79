import math
import pandas as pd
from scipy.stats import norm
import os


alpha_table_path = os.path.join(os.path.dirname(__file__), 'alpha_refs.csv')


def peeking_alpha_boundaries(alpha=0.05, nb_peek=1, method='obrien'):
    """
    Returns the alpha boundaries sequence when testing hypothesis while experiment is still runing (alpha being the
    significance level i.e. the threshold that the p-value needs to be under for the test to be positive).

    When checking the results of the experiment while experiment is not over, you'll want to make sure that you are not
    increasing the type 1 error rate (=conclude that treatment has an effect while it's not actually the case).
    To control the type 1 error over the whole experiment, we will use an adjusted alpha for each interim analysis.
    
    Returns a pandas dataframe containing the alpha boudaries sequence that should be applied over the analysis.

    :param alpha: The significance level for the experiment.
                  Current implementation can only handle 0.05
    :param nb_peek: The number of interim analysis that you planned to run (including the final analysis).
                  Current implementation can handle from 1 to 5 peekings.
    :param method: The method chosen to run the interim analysis.
                  Current implementation handles 3 methodes:
                    - obrien: (default) slowly increase alpha boundaries over the experiment
                    - pocock: same alpha boundary for each peeking (better than bon-ferroni)
                    - haybittle–peto: keep the overall alpha for the last analysis, and run all interim analysis with a very low alpha boundary (0.001 or 0.002).
    :type alpha: float
    :type nb_peek: integer
    :type method: string
    :return: The pandas dataframe of alpha boundaries sequence that should be applied allong the experiment
             Columns:
                - method: method param
                - nb_peeking: nb_peek param
                - peeking_num: peeking number
                    (going from 1 to nb_peek)
                - information_fraction: the corresponding fraction of answers to be collected before running the interim analysis.
                    (goring from 1/nb_peek to 1)
                - alpha_boundary: the corresponding alpha boundary allowed for each peeking
    :rtype: pandas.DataFrame
    Sources: Values of alpha boundaries are sourced from this article (https://onlinecourses.science.psu.edu/stat509/node/80)
    """

    known_methods = ['haybittle–peto', 'obrien','pocock']
    # Check arguments
    if alpha!=0.05:
        raise ValueError('Please use 0.05 as overall alpha value. Peeking methode is not ready yet to support other alpha values.')
    elif method not in known_methods:
        raise ValueError('Unknown method {method}. Please select a valid method among {known_methods}'.format(method=method, known_methods=known_methods))
    elif (nb_peek < 1)|(nb_peek > 5):
        raise ValueError('Please use nb_peek between 1 and 5')
    # Compute
    alpha_refs = pd.read_csv(alpha_table_path, quotechar='"')
    alpha_boundaries = alpha_refs[(alpha_refs.nb_peeking==nb_peek) & (alpha_refs.method==method)]
    # Return
    return alpha_boundaries
