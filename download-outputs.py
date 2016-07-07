from jenkinsapi.jenkins import Jenkins
import sys
import getpass
import argparse
import re
import os

def isolate_matrix_configuration_from_url(url, matrix_scopes):
    """
    :param url: url to process
    :param matrix_scopes list of scopes which will be used
    :return: string which contains "SCOPE1-SCOPE2..."
    """
    name = ''
    for scope in matrix_scopes:
        scope_value = re.search(scope + '=(.+?)[^a-zA-Z0-9]', url).group(1)
        if scope_value:
            name += ('' if name == '' else '-') + scope_value
        else:
            raise NameError("Scope '" + scope + "' not found in url '" + url + "'!")
    return name

def check_if_folder_exists(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

def download_console_output_for_each_configuration(runs, build_number, matrix_scopes):
    check_if_folder_exists(build_number)
    for run in runs:
        console = run.get_console()
        path = build_number + os.path.sep + isolate_matrix_configuration_from_url(run.get_result_url(), matrix_scopes)
        print "Saving file to " + path
        f = open(path, 'w')
        f.write(console)
        f.close()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server-url', nargs='?', required=True, help="Url of jenkins frontend")
    parser.add_argument('-j', '--job-name', nargs='?', required=True, help="Name of master job")
    parser.add_argument('-b', '--build-number', nargs='?', required=True)
    parser.add_argument('-m', '--matrix-scopes', nargs='+', required=True, help="Scopes (dimensions) of configuration"
                                                                                "matrix")
    parser.add_argument('-u', '--username', nargs='?', required=True)
    parser.add_argument('-p', '--password', nargs='?', required=False, default='', help="If not defined, user will be"
                                                                                        "asked for password in "
                                                                                        "interactive mode")

    args = vars(parser.parse_args(argv[1:]))

    if args['password'] == '':
        password = getpass.getpass()
    else:
        password = args['password']

    server = Jenkins(args['server_url'], ssl_verify=False, username=args['username'], password=password)
    master_job = server.get_job(args['job_name'])
    build = master_job.get_build(int(args['build_number']))
    runs = build.get_matrix_runs()

    download_console_output_for_each_configuration(runs=runs, build_number=args['build_number'],
                                                   matrix_scopes=args['matrix_scopes'])

if __name__ == "__main__":
   main(sys.argv)
