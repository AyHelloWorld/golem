import json
import os


def get_start_date_time_from_timestamp(timestamp):
    sp = timestamp.split('.')
    date_time_string = '{0}/{1}/{2} {3}:{4}'.format(sp[0], sp[1], sp[2],
                                                    sp[3], sp[4])
    return date_time_string


def get_last_executions(root_path, project, suite, limit):
    last_execution_data = {}

    path = os.path.join(root_path, 'projects')

    projects = []

    if project:
        projects.append(project)
    else:
        projects = os.walk(path).__next__()[1]
    for project in projects:
        last_execution_data[project] = {}
        report_path = os.path.join(path, project, 'reports')
        executed_suites = []
        if suite == '':
            executed_suites = os.walk(report_path).__next__()[1]
            if '__single__' in executed_suites:
                executed_suites.remove('__single__')
        else:
            executed_suites.append(suite)
        for su in executed_suites:
            last_execution_data[project][su] = []
            suite_executions = []
            suite_path = os.path.join(report_path, su)
            suite_executions = os.walk(suite_path).__next__()[1]
            #last_executions = sorted(suite_executions, reverse=True)
            for exe in suite_executions:
                print(exe)
            last_executions = sorted(suite_executions)
            limit = int(limit)
            if limit is not 0:
                last_executions = last_executions[-limit:]
            for execution in last_executions:
                last_execution_data[project][su].append(execution)

    return last_execution_data


def get_ejecucion_data(root_path, project, suite, execution):
    execution_data = {}
    total_cases_ok = 0
    total_cases = 0

    execution_dir = os.path.join(root_path, 'projects', project, 'reports',
                                 suite, execution)

    # ejecucion_data['modulo'] = modulo
    execution_data['test_cases'] = []

    print(execution_dir)
    
    test_cases = os.walk(execution_dir).__next__()[1]

    for test_case in test_cases:
        # each test case may have n >= 1 test sets
        
        test_case_path = os.path.join(execution_dir, test_case)
        test_sets = os.walk(test_case_path).__next__()[1]

        for test_set in test_sets:
            new_test_case = {}

            test_set_path = os.path.join(test_case_path, test_set)

            # if the suite is being executed, the report dir might exist,
            # but the report.json may still not be generated
            report_json_path = os.path.join(test_set_path, 'report.json')
            
            if not os.path.exists(report_json_path):
                continue

            with open(os.path.join(test_set_path, 'report.json'), 'r') as json_file:
                report_data = json.load(json_file)
                
            module = ''
            sub_modules = []
            test_case_splitted = test_case.split('.')
            if len(test_case_splitted) > 1:
                module = test_case_splitted[0]
                if len(test_case_splitted) > 2:
                    sub_modules = test_case_splitted[1:-1]
            new_test_case['module'] = module
            test_case_name = test_case_splitted[-1]
            new_test_case['sub_modules'] = sub_modules
            new_test_case['name'] = test_case_name
            new_test_case['test_set'] = test_set
            new_test_case['full_name'] = test_case
            new_test_case['result'] = report_data['result']
            total_cases += 1
            if report_data['result'] == 'pass':
                total_cases_ok += 1
            new_test_case['test_elapsed_time'] = report_data['test_elapsed_time']
            start_date_time = get_start_date_time_from_timestamp(
                report_data['test_timestamp']
            )
            new_test_case['start_date_time'] = start_date_time
            new_test_case['browser'] = report_data['browser']
            execution_data['test_cases'].append(new_test_case)
    execution_data['total_cases_ok'] = total_cases_ok
    execution_data['total_cases'] = total_cases

    return execution_data


def get_test_case_data(root_path, project, suite, execution, test_case, test_set):
    test_case_data = {}
    test_case_dir = os.path.join(root_path, 'projects', project, 'reports', 
                                 suite, execution, test_case, test_set)
    with open(os.path.join(test_case_dir, 'report.json'), 'r') as json_file:
        report_data = json.load(json_file)

        module = ''
        sub_modules = []
        test_case_splitted = test_case.split('.')
        if len(test_case_splitted) > 1:
            module = test_case_splitted[0]
            if len(test_case_splitted) > 2:
                sub_modules = test_case_splitted[1:-1]
        test_case_data['module'] = module
        test_case_name = test_case_splitted[-1]
        test_case_data['sub_modules'] = sub_modules
        test_case_data['name'] = test_case_name
        test_case_data['full_name'] = test_case
        test_case_data['description'] = report_data['description']
        test_case_data['result'] = report_data['result']
        test_case_data['test_elapsed_time'] = report_data['test_elapsed_time']
        start_date_time = get_start_date_time_from_timestamp(
            report_data['test_timestamp']
        )
        test_case_data['start_date_time'] = start_date_time
        test_case_data['error'] = report_data['error']
        test_case_data['browser'] = report_data['browser']
        steps = []
        for step in report_data['steps']:
            if '__' in step:
                this_step = (step.split('__')[0],
                             step.split('__')[1])
            else:
                this_step = (step.split('__')[0],)
            steps.append(this_step)
        test_case_data['steps'] = steps

    return test_case_data
