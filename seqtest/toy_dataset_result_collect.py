# coding=utf-8

"""
Given experiment results of toy data sets, convert the results into a format for publication。

Toy Dataset：Let A and B be two algorithms and mu is the difference of the generalization errors
            of A and B. Assume mu follows a multi-variant Gaussian distribution with mean vector of zero
            and covariance matrix of C. In C, the diagonal elements are 1, and the off-diagonal elements
            are e_{ij} with i\neq j。For odd i and j=i+1, e_{ij} is rho1, and the remainder elements are rho2.
"""


def convert_result_file_names(result_dir_path):
    """
    Rename the result files with regular names.

    The name convention is:
        [testname]_toy_[rho1]_[rho2】_[timestamp]
    where testname is the name of a test name, possibly taking three values, which are `bmx2_iv`, `bmx2_true` and
    `98paird`, rho1 and rho2 take values from 0.0 to 0.5 with step of 0.1.

    :param result_dir_path: the path of directory storing the experimental results.
    :return: none
    """
    import os
    assert os.path.exists(result_dir_path)
    file_names = os.listdir(result_dir_path)
    for file_name in file_names:
        file_name_tokens = file_name.split('_')
        token_counts = len(file_name_tokens)
        if token_counts <= 0:
            continue
        first_token = file_name_tokens[0]
        if first_token == "diet":
            if token_counts == 3:
                # it indicates rho1 = 0 and rho2 varies.
                rho1 = '%.1f' % 0.0
                rho2 = '0.%d' % (int(file_name_tokens[1].split('.')[1]) -2)
                destination_file_name = '98paired_toy_%s_%s_%s' % (rho1, rho2, file_name_tokens[-1])
                pass
            elif token_counts == 4:
                # it indicates rho1 and rho2 are all varying.
                rho1 = "0.%d" % int(file_name_tokens[1][-1])
                rho2 = "0.%d" % int(file_name_tokens[2])
                destination_file_name = '98paired_toy_%s_%s_%s' % (rho1, rho2, file_name_tokens[-1])
                pass
            else:
                continue
            pass
        elif first_token == 'bmx2':
            if token_counts == 4:
                # it indicates rho1 = 0 and rho2 varies.
                rho1 = '%.1f' % 0.0
                rho2 = '0.%d' % (int(file_name_tokens[1].split('.')[1]) - 2)
                destination_file_name = 'bmx2_%s_toy_%s_%s_%s' % (file_name_tokens[2][4:].lower(), rho1, rho2,
                                                                  file_name_tokens[-1])
                pass
            elif token_counts == 5:
                # it indicates rho1 and rho2 are all varies.
                rho1 = "0.%d" % int(file_name_tokens[1][-1])
                rho2 = "0.%d" % int(file_name_tokens[2])
                print(file_name_tokens)
                destination_file_name = 'bmx2_%s_toy_%s_%s_%s' % (file_name_tokens[3][4:].lower(), rho1, rho2,
                                                                  file_name_tokens[-1])
                pass
            else:
                continue
            pass
        else:
            continue
        abs_src_file_name = os.path.join(result_dir_path, file_name)
        abs_dest_file_name = os.path.join(result_dir_path, destination_file_name)
        os.rename(abs_src_file_name, abs_dest_file_name)
        pass
    pass


def format_power_function_values_for_a_result(result_file_abs_path):
    """
    Given a text file storing experimental results on a toy data set, retrieval and format the following information:
        - delta value
        - expected stoping time
        - power value
    and return these values in a CVS format with three columns.

    :param result_file_abs_path: the text file storing results.
    :return: list [[delta][expected stoping time][power value]].
    """
    import os
    assert os.path.exists(result_file_abs_path)
    f = open(result_file_abs_path)
    content = f.readlines()
    f.close()
    content.pop(0)
    results = {}
    max_type_1_error = 0
    for line in content:
        line = line.strip()
        if line == "":
            continue
        tokens = line.split(',')
        delta = float(tokens[1])
        stop_time_expected = int(tokens[33])
        acc_h0 = float(tokens[37])
        acc_h1 = float(tokens[38])
        acc_none = float(tokens[39])
        true_mu = 0
        if delta <= true_mu:
            # null hypothesis space
            type_1_error = acc_h1
            power_value = type_1_error
            if delta == true_mu:
                max_type_1_error = type_1_error
            pass
        else:
            # alternative hypothesis space
            type_2_error = acc_h0 + acc_none
            power_value = 1 - type_2_error
            pass
        if delta not in results:
            results[delta]= [stop_time_expected,power_value]
    return results, max_type_1_error
    pass


def merge_two_results(pop_result, ind_result):
    """
    Merge the individual result in result population.

    :param pop_result: result population
    :param ind_result: result individual
    :return: population result.
    """

    if pop_result is None or len(pop_result) == 0:
        return ind_result
    for key in pop_result:
        assert key in ind_result
        pop_result[key] = pop_result[key]+ind_result[key]
    return pop_result


def format_type_1_errors_to_a_latex_table(type_I_errors):
    test_methods = ['98paired', 'bmx2', 'ideal']
    content = ""
    for test_index in range(0, 3):
        line = "\multirow{6}{*}{%s}  " % test_methods[test_index]
        for rho_1 in range(0, 6):
            line += "& 0.%s & " % rho_1
            for rho_2 in range(0, 6):
                line += "%.3f" % type_I_errors[rho_1][rho_2][test_index]
                if rho_2 == 5:
                    line += "\\\\\n"
                else:
                    line += "&"
                pass
        content += line
    print(content)
    pass


def batch_all_results(result_file_abs_dir):
    """
    batch precess all results in the directory.

    :param result_file_abs_dir:
    :return:
    """
    import os
    assert os.path.exists(result_file_abs_dir)
    file_repo = {} # store all result files, key is prefix token without timestamp, value is file name.
    for file_name in os.listdir(result_file_abs_dir):
        file_repo[file_name[0:file_name.rfind('_')]] = file_name
        pass
    test_methods = ['98paired', 'bmx2_iv', 'bmx2_true']
    type_1_errors_all = []
    for rho_1 in range(0, 6):
        type_1_error_rho2 = []
        for rho_2 in range(0, 6):
            results = {}
            type_1_errors = []
            for test_method in test_methods:
                query_key = '%s_toy_0.%s_0.%s' % (test_method, rho_1, rho_2)
                file_name = file_repo[query_key]
                result, type_1_error = format_power_function_values_for_a_result(os.path.join(result_file_abs_dir, file_name))
                results = merge_two_results(results, result)
                type_1_errors.append(type_1_error)
                pass
            type_1_error_rho2.append(type_1_errors)
        type_1_errors_all.append(type_1_error_rho2)
    format_type_1_errors_to_a_latex_table(type_1_errors_all)
    pass


if __name__ == "__main__":
    toy_result_dir_abs_path = r"C:\Users\wangr\Desktop\m\manuscripts\PAPER-SEQTTEST\实验结果\toy"
    batch_all_results(toy_result_dir_abs_path)
    pass

