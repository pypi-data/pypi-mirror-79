def hypotheses_multinormal_test(group):
    h0 = 'Group "{}" is a sample from a multinormal distribution'.format(group)
    h1 = 'Group "{}" is not a sample from a multinormal distribution'.format(group)
    return {'H0': h0, 'H1': h1}


def hypotheses_mean_comparison(control_group, treatment_group):
    h0 = 'Group "{}" and group "{}" have equal mean vector'.format(control_group, treatment_group)
    h1 = 'Group "{}" and group "{}" have different mean vector'.format(control_group, treatment_group)
    return {'H0': h0, 'H1': h1}