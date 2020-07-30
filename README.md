# Malicious-Code
## Description
This web tool was created for the Duke Code+ program. It uses static analysis in order to detect malware in files.

## Python Libraries Used
  asgiref==3.2.10

  Django==3.0.7

  python-magic==0.4.18

  pytz==2020.1

  sqlparse==0.3.1

  yara-python==4.0.2

  requests==2.24.0

## Source for Yara Rules
https://github.com/Neo23x0/signature-base/blob/master/yara/gen_macro_ShellExecute_action.yar

https://github.com/Neo23x0/signature-base/blob/master/yara/gen_susp_office_dropper.yar

https://github.com/Neo23x0/signature-base/blob/master/yara/general_officemacros.yar

https://github.com/Neo23x0/signature-base/blob/master/yara/gen_dde_in_office_docs.yar

https://github.com/Yara-Rules/rules

## Other Sources
Virus Total API

## Installation
In order to run the website on your machine, you must install all of the python libraries listed above and in the requirements.txt file (We recommend installing these in a Python virtual environment).

## Authors
Joe Cusano
Luke Evans
Celine Murugi
Flora Shi
