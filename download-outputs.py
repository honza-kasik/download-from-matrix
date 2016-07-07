from jenkinsapi.jenkins import Jenkins
import sys
import getopt
import getpass
import re
import os

def isolate_matrix_configuration_from_url(url):
    """
    Isolates data from url, e.g.: 'https://eap-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/job/richfaces-4.5-metamer-smoke-ftest-eap70x-matrix-jkasik/SUITE=core,TEMPLATE=aRepeat,jdk=oracle-java-1.8,label=RHEL&&medium/25/testReport/api/python'
    :param url: url to process
    :return: string containg "TEMPLATE-SUITE"
    """
    template = re.search('TEMPLATE=(.+?)[^a-zA-Z0-9]', url).group()
    suite = re.search('SUITE=(.+?)[^a-zA-Z0-9]', url).group()
    return template + '-' + suite

def check_if_folder_exists(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

def download_console_output_for_each_configuration(runs, build_number):
    check_if_folder_exists(build_number)
    for run in runs:
        console = run.get_console()
        f = open(build_number + os.path.sep + isolate_matrix_configuration_from_url(run.get_result_url()), 'w')
        f.write(console)
        f.close()

def main(argv):
    print argv
    use_string = argv[0] + " -b <build-number> -u <username> -p <password>"
    build_number = ''
    username = ''
    password = ''
    try:
        opts, args = getopt.getopt(argv, "hb:u:p:",["build=", "username=", "password="])
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

    if username == '':
        print("Username is requested! \nUsage: " + use_string)
        sys.exit(2)

    if build_number == '':
        print("Build number is requested! \nUsage: " + use_string)
        sys.exit(2)

    if password == '':
        password = getpass.getpass()

    server = Jenkins('https://eap-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/', ssl_verify=False, username=username,
                     password=password)
    master_job = server.get_job('richfaces-4.5-metamer-smoke-ftest-eap70x-matrix-jkasik')
    build = master_job.get_build(int(build_number))
    runs = build.get_matrix_runs()

    download_console_output_for_each_configuration(runs=runs, build_number=build_number)

if __name__ == "__main__":
   main(sys.argv)
