def hypotheses_mean_comparison(control_group, treatment_group, test_type):
    if test_type == 'two-sided':
        h0 = 'Group "{}" and group "{}" have equal mean'.format(control_group, treatment_group)
        h1 = 'Group "{}" and group "{}" have different mean'.format(control_group, treatment_group)
    elif test_type == 'larger':
        h0 = 'Group "{}" has smaller or equal mean than group "{}"'.format(treatment_group, control_group)
        h1 = 'Group "{}" has larger mean than group "{}"'.format(treatment_group, control_group)
    elif test_type == 'smaller':
        h0 = 'Group "{}" has larger or equal mean than group "{}"'.format(treatment_group, control_group)
        h1 = 'Group "{}" has smaller mean than group "{}"'.format(treatment_group, control_group)
    else:
        raise ValueError('Incorrect test type. Must be one of "two-sided", "smaller" or "larger"')
    return {'H0': h0, 'H1': h1}

def hypotheses_variance_comparison(control_group, treatment_group, test_type):
    if test_type == 'two-sided':
        h0 = 'Group "{}" and group "{}" have equal variance'.format(control_group, treatment_group)
        h1 = 'Group "{}" and group "{}" have different variance'.format(control_group, treatment_group)
    elif test_type == 'larger':
        h0 = 'Group "{}" has smaller or equal variance than group "{}"'.format(treatment_group, control_group)
        h1 = 'Group "{}" has larger variance than group "{}"'.format(treatment_group, control_group)
    elif test_type == 'smaller':
        h0 = 'Group "{}" has larger or equal variance than group "{}"'.format(treatment_group, control_group)
        h1 = 'Group "{}" has smaller variance than group "{}"'.format(treatment_group, control_group)
    else:
        raise ValueError('Incorrect test type. Must be one of "two-sided", "smaller" or "larger"')
    return {'H0': h0, 'H1': h1}

def hypotheses_u_test(control_group, treatment_group, test_type):
    if test_type == 'two-sided':
        h0 = ('Group "{c}" and group "{t}" have the same distribution'
              ' (it is equally probable that a randomly selected value from'
              ' group "{c}" will be less than or greater'
              ' than a randomly selected value from group "{t}")').format(c=control_group, t=treatment_group)
        h1 = ('Group "{c}" and group "{t}" have different distributions'
              ' (it is not equally probable that a randomly selected value from'
              ' group "{c}" will be less than or greater'
              ' than a randomly selected value from group "{t}")').format(c=control_group, t=treatment_group)
    elif test_type == 'larger':
        h0 = ('Group "{t}" has a smaller or equal distribution than group "{c}"'
              ' (a randomly selected value from'
              ' group "{t}" is likely to be smaller or equal'
              ' than a randomly selected value from group "{c}")').format(c=control_group, t=treatment_group)
        h1 = ('Group "{t}" has a larger distribution than group "{c}"'
              ' (a randomly selected value from'
              ' group "{t}" is likely to be larger'
              ' than a randomly selected value from group "{c}")').format(c=control_group, t=treatment_group)
    elif test_type == 'smaller':
        h0 = ('Group "{t}" has a larger or equal distribution than group "{c}"'
              ' (a randomly selected value from'
              ' group "{t}" is likely to be larger or equal'
              ' than a randomly selected value from group "{c}")').format(c=control_group, t=treatment_group)
        h1 = ('Group "{t}" has a smaller distribution than group "{c}"'
              ' (a randomly selected value from'
              ' group "{t}" is likely to be smaller'
              ' than a randomly selected value from group "{c}")').format(c=control_group, t=treatment_group)
    else:
        raise ValueError('Incorrect test type. Must be one of "two-sided", "smaller" or "larger"')
    return {'H0': h0, 'H1': h1}


def hypotheses_normal_test(group):
    h0 = 'Group "{}" is a sample from a normal distribution'.format(group)
    h1 = 'Group "{}" is not a sample from a normal distribution'.format(group)
    return {'H0': h0, 'H1': h1}


def hypotheses_binomial_test(control_group, treatment_group, target_treatment_share):
    h0 = 'An observation is allocated to group "{}" (by opposition to group "{}") with probability {}'.format(treatment_group, control_group, target_treatment_share)
    h1 = 'An observation is not allocated to group "{}" (by opposition to group "{}") with probability {}'.format(treatment_group, control_group, target_treatment_share)
    return {'H0': h0, 'H1': h1}
