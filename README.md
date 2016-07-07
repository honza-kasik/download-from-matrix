Simple script for downloading console outputs from all Jenkins jobs which are inside configuration matrix

##Usage

```
usage: download-outputs.py [-h] -s SERVER_URL -j JOB_NAME -b BUILD_NUMBER -m
                           MATRIX_SCOPE [MATRIX_SCOPE ...] -u USERNAME
                           [-p PASSWORD]

arguments:
  -h, --help            show this help message and exit
  -s SERVER_URL, --server-url SERVER_URL
                        Url of jenkins frontend
  -j JOB_NAME, --job-name JOB_NAME
                        Name of master job
  -b BUILD_NUMBER, --build-number BUILD_NUMBER
  -m MATRIX_SCOPE [MATRIX_SCOPE ...], --matrix-scopes MATRIX_SCOPE [MATRIX_SCOPE ...]
                        Scopes (dimensions) of configuration matrix
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
                        If not defined, user will be asked for password in
                        interactive mode
```

##Example
`python download-outputs.py -b 23 -u myUser -m SCOPE1 SCOPE2 -s "https://localhost:7585/" -j myJob`