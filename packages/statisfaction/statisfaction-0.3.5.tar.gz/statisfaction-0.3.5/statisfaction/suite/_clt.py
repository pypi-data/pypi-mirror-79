from ..univariate import shapiro_test_from_observations
from ..utils.bucket import bucket
from ..utils.input import get_value_column_from_univariate
import pandas as pd
from ..core import ObservationSet
from .._constants import min_observations


def assess_convergence_to_normal_dist(observations, alpha=0.05, control='control', treatment='treatment',
                                      simulation_count=10, size_steps=50):
    """
    Runs multiple Shapiro normaltest at increasing levels of granularity of an ObservationSet in order to verify experimentally the central-limit theorem.
    Use this method when you need to prove that you can run a T-test on your sample.

    :param observations: The ObservationSet
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param control: The name of the control group
    :param treatment: The name of the treatment group
    :param simulation_count: The number of simulation to run at each granularity step
    :param size_steps: The size of the step of granularity between each iteration of the normaltest
    :type observations: ObservationSet
    :type alpha: float
    :type control: str
    :type treatment: str
    :type simulation_count: int
    :type size_steps: int
    :return: The dataframe containing the mean of the p-values observed at each granularity
    :rtype: DataFrame

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    norm_pvalues = []
    norm_gran = []
    query_results_ctrl = observations._get_series(control, value_column)
    query_results_treat = observations._get_series(treatment, value_column)
    control_size = len(query_results_ctrl)
    treatment_size = len(query_results_treat)
    max_range = min(control_size, treatment_size) // min_observations

    for i in range(1, max_range, size_steps):
        for j in range(1, simulation_count):
            obs_bucket = bucket(observations, i)
            normal_results = shapiro_test_from_observations(obs_bucket, alpha, control)
            norm_pvalues.append(normal_results['pvalue'])
            norm_gran.append(i)

    df = pd.DataFrame({'sample_size': norm_gran,
                        'p_value': norm_pvalues})
    df_mean = df.groupby(['sample_size'], as_index=False)['p_value'].mean()
    df_mean.columns = ['sample_size', 'average_p_value']

    return df_mean


