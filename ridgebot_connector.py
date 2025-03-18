# File: ridgebot_connector.py
#
# Copyright (c) RidgeSecurity, 2022-2025

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
# Python 3 Compatibility imports

import json
import os
import sys
import time
import uuid

# Phantom App imports
import phantom.app as phantom
import requests
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.vault import Vault


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class RidgebotConnector(BaseConnector):
    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        message = "Status Code: {}. Data from server:\n{}\n".format(status_code, "response with unexpected format")

        message = message.replace("{", "{{").replace("}", "}}")
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_pdf_response(self, response, action_result):
        return RetVal(phantom.APP_SUCCESS, response)

    def _process_zip_response(self, response, action_result):
        return RetVal(phantom.APP_SUCCESS, response)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Unable to parse JSON response. Error: {e!s}"), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {} Data from server: {}".format(r.status_code, r.text.replace("{", "{{").replace("}", "}}"))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately
        if "pdf" in r.headers.get("Content-Type", ""):
            return self._process_pdf_response(r, action_result)
        elif "zip" in r.headers.get("Content-Type", ""):
            return self._process_zip_response(r, action_result)
        # RidgeBot default is JSON
        else:
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {} Data from server: {}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", data=None, headers=None, params=None, stream=None):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        Auth_token = config.get("auth_token")
        headers = {"Authorization": str(Auth_token), "accept": "application/json"}
        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), resp_json)

        url = self._base_url + endpoint

        try:
            r = request_func(url, params=params, headers=headers, json=data, verify=False, stream=stream)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Error Connecting to server. Details: {e!s}"), resp_json)
        print(r.status_code)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress("Connecting to endpoint")
        # make rest call
        ret_val, response = self._make_rest_call("/test/connect", action_result, params=None, headers=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.send_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_createtask(self, param):
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        name = param["name"]
        targets = param["targets"]
        template_id = param["template_id"]
        # Required values can be accessed directly
        data = {"name": name, "targets": [targets], "template_id": int(template_id)}

        # make rest call
        ret_val, response = self._make_rest_call("/tasks", action_result, params=None, headers=None, data=data, method="post")

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        action_result.set_status(phantom.APP_SUCCESS)
        # Add a dictionary that is made up of the most important values from data into the summary
        action_result.update_summary({"task_id": response["data"]["task_id"]})

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.send_progress("Task Created Successfully")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_stoptask(self, param):
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        task_id = param.get("task_id")
        data = {"task_id": task_id}

        # make rest call
        ret_val, response = self._make_rest_call("/tasks/stop", action_result, params=None, headers=None, data=data, method="post")

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        action_result.set_status(phantom.APP_SUCCESS)
        # Add a dictionary that is made up of the most important values from data into the summary
        action_result.update_summary({"Stop Task": response["message"]["key"]})
        # Return success, no need to set the message, only the status

        self.send_progress("Task Stopped Successfully")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_gettaskinfo(self, param):
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        task_id = param["task_id"]

        # make rest call
        ret_val, response = self._make_rest_call("/tasks/info?task_id=" + task_id, action_result, params=None, headers=None, data=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        running_status_code = response["data"][0]["task_status"]
        if running_status_code == 0:
            running_status = "waiting"
        elif running_status_code == 1:
            running_status = "running"
        elif running_status_code == 2:
            running_status = "paused"
        elif running_status_code == 3:
            running_status = "canceled"
        elif running_status_code == 4:
            running_status = "finished"
        elif running_status_code == 5:
            running_status = "queueing"
        elif running_status_code == 6:
            running_status = "waiting ack"
        else:
            running_status = "undefined"
        # Add a dictionary that is made up of the most important values from data into the summary
        action_result.update_summary({"Task Running Status": running_status})

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.send_progress("Get Task Info Successfully")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_gettaskinfolists(self, param):
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        ret_val, response = self._make_rest_call("/tasks/info", action_result, params=None, headers=None, data=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({"Num of Tasks": len(response["data"])})
        summary["num_data"] = len(response["data"])

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.send_progress("Get Task List Successfully")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_gettaskstatistics(self, param):
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        task_id = param["task_id"]

        # make rest call
        ret_val, response = self._make_rest_call("/tasks/statistics?task_id=" + task_id, action_result, params=None, headers=None, data=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        # Add a dictionary that is made up of the most important values from data into the summary
        action_result.update_summary({"safety_index": response["data"]["security_module"]["safety_index"]})

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.send_progress("Get Task statistics Successfully")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_generatedownloadreport(self, param):
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        task_id = param["task_id"]
        report_type = param["type"]
        template = 0 if type == "pdf" else 3

        report_name = param["report_name"]
        data = {"custom_log": 0, "language": 1, "task_id": task_id, "type": report_type, "template": template}
        # Generate and download a CSV report from the task just created
        ret_val, response = self._make_rest_call("/report/generate", action_result, params=None, headers=None, data=data, method="post")

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            return action_result.get_status()

        # need wait a bit for generate done
        time.sleep(60)

        report_id = response["data"]["report_id"]
        data = {"ids": [int(report_id)], "password": ""}
        ret_val, response = self._make_rest_call(
            "/report/download", action_result, params=None, headers=None, data=data, method="post", stream=True
        )

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            return action_result.get_status()

        if report_type == "pdf":
            filename = report_name + "." + report_type
        else:
            filename = report_name + ".zip"

        # Creating temporary directory and file
        try:
            if hasattr(Vault, "get_vault_tmp_dir"):
                temp_dir = Vault.get_vault_tmp_dir()
            else:
                temp_dir = "/opt/phantom/vault/tmp/"

            temp_dir = f"{temp_dir}/{uuid.uuid4()}"

            os.makedirs(temp_dir)

            file_path = os.path.join(temp_dir, filename)

            with open(file_path, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=128):
                    file_obj.write(chunk)
        except Exception as e:
            print(e)
            return action_result.set_status(phantom.APP_ERROR, "Error while writing to temporary file"), None

        # Adding file to vault
        vault_ret_dict = Vault.add_attachment(file_path, self.get_container_id())

        # Removing temporary directory created to download file
        try:
            os.rmdir(temp_dir)
        except Exception as e:
            print(e)
            return action_result.set_status(phantom.APP_ERROR, "Unable to remove temporary directory"), None

        if vault_ret_dict["succeeded"]:
            self.send_progress("Generate Report Successfully")
            return action_result.set_status(phantom.APP_SUCCESS, "Write file to Vault"), None
        else:
            self.error_print("Generate Report Failed to write to Vault")
            return action_result.set_status(phantom.APP_ERROR, "Fail to Write file to Vault"), None

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)

        elif action_id == "createtask":
            ret_val = self._handle_createtask(param)

        elif action_id == "stoptask":
            ret_val = self._handle_stoptask(param)

        elif action_id == "gettaskinfo":
            ret_val = self._handle_gettaskinfo(param)

        elif action_id == "gettaskinfolists":
            ret_val = self._handle_gettaskinfolists(param)

        elif action_id == "gettaskstatistics":
            ret_val = self._handle_gettaskstatistics(param)

        elif action_id == "generatedownloadreport":
            ret_val = self._handle_generatedownloadreport(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions

        self._state = self.load_state()
        # get the asset config
        config = self.get_config()

        self._base_url = config.get("base_url")

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import argparse

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = RidgebotConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify, timeout=30)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=30)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = RidgebotConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)


if __name__ == "__main__":
    main()
