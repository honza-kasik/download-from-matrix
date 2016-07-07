Simple script for downloading console outputs from all jobs which are inside configuration matrix

```
Usage: download-outputs.py [-h] -s [SERVER_URL] -j [JOB_NAME] -b
                           [BUILD_NUMBER] -m MATRIX_SCOPES [MATRIX_SCOPES ...]
                           -u [USERNAME] [-p [PASSWORD]]

  -h, --help            show this help message and exit
  -s [SERVER_URL], --server-url [SERVER_URL]
                        Url of jenkins frontend
  -j [JOB_NAME], --job-name [JOB_NAME]
                        Name of master job
  -b [BUILD_NUMBER], --build-number [BUILD_NUMBER]
  -m MATRIX_SCOPES [MATRIX_SCOPES ...], --matrix-scopes MATRIX_SCOPES [MATRIX_SCOPES ...]
                        Scopes (dimensions) of configuration matrix
  -u [USERNAME], --username [USERNAME]
  -p [PASSWORD], --password [PASSWORD]
                        If not defined, user will be asked for password in
                        interactive mode
```
