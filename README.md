[comment]: # "Auto-generated SOAR connector documentation"
# RidgeBot

Publisher: RidgeSecurity  
Connector Version: 1\.0\.1  
Product Vendor: RidgeSecurity  
Product Name: RidgeBot  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

Support RidgeBot Task Creation and Result Retrieval

# Splunk> Phantom

Welcome to the open-source repository for Splunk> Phantom's ridgebot App.

Please have a look at our [Contributing Guide](https://github.com/Splunk-SOAR-Apps/.github/blob/main/.github/CONTRIBUTING.md) if you are interested in contributing, raising issues, or learning more about open-source Phantom apps.

## Legal and License

This Phantom App is licensed under the Apache 2.0 license. Please see our [Contributing Guide](https://github.com/Splunk-SOAR-Apps/.github/blob/main/.github/CONTRIBUTING.md#legal-notice) for further details.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a RidgeBot asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | API Base URL
**auth\_token** |  required  | password | User Token for API execution

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[create task](#action-create-task) - Create Task  
[get data statistics](#action-get-data-statistics) - Get Task Result with Attack Surface, Vulnerablity and Risk Statistics  
[cancel task](#action-cancel-task) - Stop a unfinished task  
[get task info](#action-get-task-info) - Get Task Info for a Task  
[list tasks](#action-list-tasks) - Get Task Info Lists  
[create report](#action-create-report) - Generate and Download Report with Task ID  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

Check Asset Connectivity\.

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'create task'
Create Task

Type: **generic**  
Read only: **False**

Create Penetration Task\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Task Name | string | 
**targets** |  required  | Task Target List | string | 
**template\_id** |  required  | Template Id | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.name | string | 
action\_result\.parameter\.targets | string | 
action\_result\.parameter\.template\_id | numeric | 
action\_result\.status | string | 
action\_result\.data\.\*\.data\.task\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get data statistics'
Get Task Result with Attack Surface, Vulnerablity and Risk Statistics

Type: **generic**  
Read only: **False**

Get Task Statistics\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task\_id** |  required  | Task Id | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.task\_id | string | 
action\_result\.data\.\*\.data\.risk\.risk\_number | string | 
action\_result\.data\.\*\.data\.vul\.vul\_number | string | 
action\_result\.data\.\*\.data\.vul\.vul\_high | string | 
action\_result\.data\.\*\.data\.vul\.vul\_middle | string | 
action\_result\.data\.\*\.data\.security\_module\.safety\_index | string | 
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'cancel task'
Stop a unfinished task

Type: **generic**  
Read only: **False**

Stop a unfinished Task\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task\_id** |  required  | Task Id | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.task\_id | string | 
action\_result\.data\.\*\.message\.key | string | 
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get task info'
Get Task Info for a Task

Type: **generic**  
Read only: **False**

Get Task Info for a Task\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task\_id** |  required  | Task Id | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.task\_id | string | 
action\_result\.status | string | 
action\_result\.data\.\*\.data\.\*\.task\_id | string | 
action\_result\.data\.\*\.data\.\*\.task\_job\_count | numeric | 
action\_result\.data\.\*\.data\.\*\.task\_job\_total | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list tasks'
Get Task Info Lists

Type: **generic**  
Read only: **False**

Get task info lists\.

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.message\.key | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create report'
Generate and Download Report with Task ID

Type: **generic**  
Read only: **False**

Generate and Download Report\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task\_id** |  required  | Task Id | string | 
**type** |  required  | Report Type | string | 
**report\_name** |  required  | Report Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.task\_id | string | 
action\_result\.parameter\.type | string | 
action\_result\.parameter\.report\_name | string | 
action\_result\.data\.\*\.data\.report | string | 
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 