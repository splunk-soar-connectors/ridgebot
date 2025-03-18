# RidgeBot

Publisher: RidgeSecurity \
Connector Version: 1.0.1 \
Product Vendor: RidgeSecurity \
Product Name: RidgeBot \
Minimum Product Version: 5.1.0

Support RidgeBot Task Creation and Result Retrieval

### Configuration variables

This table lists the configuration variables required to operate RidgeBot. These variables are specified when configuring a RidgeBot asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** | required | string | API Base URL |
**auth_token** | required | password | User Token for API execution |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[create task](#action-create-task) - Create Task \
[get data statistics](#action-get-data-statistics) - Get Task Result with Attack Surface, Vulnerablity and Risk Statistics \
[cancel task](#action-cancel-task) - Stop a unfinished task \
[get task info](#action-get-task-info) - Get Task Info for a Task \
[list tasks](#action-list-tasks) - Get Task Info Lists \
[create report](#action-create-report) - Generate and Download Report with Task ID

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

Check Asset Connectivity.

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'create task'

Create Task

Type: **generic** \
Read only: **False**

Create Penetration Task.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** | required | Task Name | string | |
**targets** | required | Task Target List | string | |
**template_id** | required | Template Id | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.name | string | | |
action_result.parameter.targets | string | | |
action_result.parameter.template_id | numeric | | |
action_result.status | string | | success failed |
action_result.data.\*.data.task_id | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get data statistics'

Get Task Result with Attack Surface, Vulnerablity and Risk Statistics

Type: **generic** \
Read only: **False**

Get Task Statistics.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task_id** | required | Task Id | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.task_id | string | | |
action_result.data.\*.data.risk.risk_number | string | | |
action_result.data.\*.data.vul.vul_number | string | | |
action_result.data.\*.data.vul.vul_high | string | | |
action_result.data.\*.data.vul.vul_middle | string | | |
action_result.data.\*.data.security_module.safety_index | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'cancel task'

Stop a unfinished task

Type: **generic** \
Read only: **False**

Stop a unfinished Task.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task_id** | required | Task Id | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.task_id | string | | |
action_result.data.\*.message.key | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get task info'

Get Task Info for a Task

Type: **generic** \
Read only: **False**

Get Task Info for a Task.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task_id** | required | Task Id | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.task_id | string | | |
action_result.status | string | | success failed |
action_result.data.\*.data.\*.task_id | string | | |
action_result.data.\*.data.\*.task_job_count | numeric | | |
action_result.data.\*.data.\*.task_job_total | numeric | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'list tasks'

Get Task Info Lists

Type: **generic** \
Read only: **False**

Get task info lists.

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.message.key | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create report'

Generate and Download Report with Task ID

Type: **generic** \
Read only: **False**

Generate and Download Report.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task_id** | required | Task Id | string | |
**type** | required | Report Type | string | |
**report_name** | required | Report Name | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.task_id | string | | |
action_result.parameter.type | string | | |
action_result.parameter.report_name | string | | |
action_result.data.\*.data.report | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
