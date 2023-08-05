
from typing import List



def compute_sd(result_fix_issues: List):
    '''
    Compute the standard deviations of corrections applied to
    `result_fix_issues`, a return value of `ProvPopTable.fix_issues()`.

    Details
    -------
    For each correction applied to a problematic record, the user is able
    to get the log of all corrections applied to `ProvPopTable` via its
    `.fix_issues(return_all_mods = True)` method. This function is to
    compute the standard deviation of each correction.

    Usage
    -----
    `compute_sd(result_fix_issues)`

    Arguments
    ---------
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)`.

    Returns
    -------
    A `dict` with keys `(sex, age, comp)` where `sex` is a problematic 
    sex, `age` is a problematic age, and `comp` is the name of the
    problematic component, and values `sd` where `sd` are standard 
    deviation of each applied correction.
    '''

    pop_sex_age = result_fix_issues[0].get_pop_groups()

    result = {}
    for i in range(1, len(result_fix_issues)):
        problematic_sex_age = result_fix_issues[i]\
            .iloc[-1, :]\
            [pop_sex_age]\
            .values
        p_sex = problematic_sex_age[0]
        p_age = problematic_sex_age[1]
        comp_L_wo_0 = result_fix_issues[i]\
            .iloc[:, -1]\
            .loc[lambda x: x != 0]
        p_comp = comp_L_wo_0.name[:-2]
        sd_mod = comp_L_wo_0.std()
        result[(p_sex, p_age, p_comp)] = sd_mod

    return result

def diff(one, other):
    '''
    Return element(s) of `one` that is/are not an element of `other`.

    Usage
    -----
    `difference(one, other)`

    Examples
    --------
    >>> one = ['a', 'b']
    >>> other = ['a', 'c']
    >>> is_subset(one, other)
    False
    >>> diff(one, other)
    ['b']
    '''

    if not isinstance(one, set):
        one = set(one)
    if not isinstance(other, set):
        other = set(other)

    return list(one.difference(other))

def is_subset(one, other):
    '''
    Return True if `one` is the subset of the `other`.

    Usage
    -----
    `is_subset(one, other)`

    Examples
    --------
    >>> one = ['a']
    >>> other = ['a', 'b']
    >>> is_subset(one, other)
    True
    '''

    if not isinstance(one, set):
        one = set(one)
    if not isinstance(other, set):
        other = set(other)
    
    return one.issubset(other)

def raise_if_not_subset(
    one, other, one_name = "one", other_name = "other"
):
    '''
    Raise AssertionError if `one` is not the subset of the `other`, and
    display item(s) of `one` that is/are not an element of `other`. Provide
    names of `one` and `other` to `one_name` and `other_name` if one wishes
    to see the argument names displayed in the error message. By default,
    they are "one" and "other" respectively.

    Usage
    -----
    `raise_if_not_subset(one, other, one_name, other_name)`
    '''

    msg =\
        '"{0}" is not a subset of "{1}" since the following item(s) ' +\
        'of "{0}" does/do not exist in "{1}": {2}'
    msg = msg.format(one_name, other_name, diff(one, other))
    assert is_subset(one, other), msg

def return_op_if_None(op, argument):
    '''
    Return `op` if `argument` is None. Otherwise, return `argument`.

    Usage
    -----
    `return_op_if_None(op, argument)`
    '''

    return op if argument is None else argument



if __name__ == '__main__':
    import doctest
    doctest.testmod()
