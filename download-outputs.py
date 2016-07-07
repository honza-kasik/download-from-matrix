from jenkinsapi.jenkins import Jenkins
import sys
import getopt
import getpass
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
        name += ('' if name == '' else '-') + scope_value
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
    use_string = argv[0] + " -b <number> -u <username> [-p <password>] -m <scope1,scope2...> -s <url> -j <job-name>"
    build_number = ''
    username = ''
    password = ''
    server_url = ''
    job_name = ''
    matrix_scopes = []
    try:
        opts, args = getopt.getopt(argv[1:], "hb:u:p:m:s:j:",["build=", "username=", "password=", "matrix-scopes=", "server-url=", "job-name="])
    except getopt.GetoptError:
        print use_string
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print use_string
            sys.exit()
        elif opt in ("-b", "--build"):
            build_number = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-m", "--matrix-scopes"):
            matrix_scopes = arg.split(',')
        elif opt in ("-s", "--server-url"):
            server_url = arg
        elif opt in ("-j", "--job-name"):
            job_name = arg

    # todo requested arguments checks!!

    if password == '':
        password = getpass.getpass()

    server = Jenkins(server_url, ssl_verify=False, username=username,
                     password=password)
    master_job = server.get_job(job_name)
    build = master_job.get_build(int(build_number))
    runs = build.get_matrix_runs()

    download_console_output_for_each_configuration(runs=runs, build_number=build_number, matrix_scopes=matrix_scopes)

if __name__ == "__main__":
   main(sys.argv)
