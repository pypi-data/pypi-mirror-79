import json
import traceback

EXECUTION_STATE_COMPLETED = 0
EXECUTION_STATE_INPROGRESS = 1
EXECUTION_STATE_FAILED = 2
EXECUTION_STATE_TIMEDOUT = 3


class ScriptResult:
    MAX_TOTAL_ATTACHMENT_SIZE = 5 * 1024 * 1024
    MAX_ATTACHMENT_SIZE = 3 * 1024 * 1024

    def __init__(self, entities):
        self._message = None
        self._result_value = None
        self._result_object = {}
        self._total_attachment_size = 0
        self._execution_state = EXECUTION_STATE_COMPLETED
        self._entities = entities

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def result_value(self):
        return self._result_value

    @result_value.setter
    def result_value(self, value):
        self._result_value = value

    @property
    def execution_state(self):
        return self._execution_state

    @execution_state.setter
    def execution_state(self, value):
        self._execution_state = value

    def add_entity_json(self, entity_identifier, json_data):
        """
        add json result with entity identifier as json title
        :param entity_identifier: {string} entity identifier
        :param json_data: {dict} json data
        """
        self.add_json(entity_identifier, json_data)

    def add_result_json(self, json_data):
        """
        add json result
        :param json_data: {dict} json data
        """
        # Must match Siemplify.Common.Consts.ScriptsDynamicResultFirstName
        # This is a prepation for dynamic results. In the begining, we have only one, called 'ResultJson'.
        # In the future, the names will come from the IDE Screen, like the "Output name", only dynamic
        self.add_json("JsonResult", json_data)

    def add_json(self, entity_identifier, json_data):
        """
        add json result
        :param entity_identifier: {string} entity identifier
        :param json_data: {string}/{dict}/{list} If input is json string object, it will be validated. If it's a dictionary or list, it will be json dumped
        """
        entity_data = self._get_entity_data(entity_identifier)
        if isinstance(json_data, dict) or isinstance(json_data, list):
            # In case we received a list or dict, turn it into json string
            try:
                json_data = json.dumps(json_data)
            except Exception as e:
                try:
                    # try a more lenient approach for serilization. This is not fool proof and may fail as well - str() can have errors
                    json_data = json.dumps(json_data, default=str)
                except Exception as e:
                    tb = traceback.format_exc()
                    msg = "Failed to dump json_data with default serilizier and str() as serilizier"
                    raise Exception(msg, e, tb)

        else:
            try:
                # In case we recevied a string, validate it's JSON serializable
                json.loads(json_data)
            except ValueError as err:
                raise Exception("Passed value is mot JSON serializable, Error: {0}".format(err.message))
            except TypeError as err:
                raise Exception(
                    "Expected dictionary, array or JSON serializable string, Error: {0}".format(err.message))
        entity_data["RawJson"] = json_data

    def add_entity_content(self, entity_identifier, content):
        """
        add content
        :param entity_identifier: {string} entity identifier
        :param content:
        """
        self.add_content(entity_identifier, content)

    def add_content(self, entity_identifier, content):
        """
        add content
        :param entity_identifier: {string} entity identifier
        :param content:
        """
        entity_data = self._get_entity_data(entity_identifier)
        entity_data["Content"] = content

    def add_entity_table(self, entity_identifier, data_table):
        """
        add data table with entity identifier as table title
        :param entity_identifier: {string} entity identifier
        :param data_table: {list} csv formatted list
        """
        self.add_data_table(entity_identifier, data_table)

    def add_data_table(self, title, data_table):
        """
        add data table
        :param title: {string} table title
        :param data_table: {list} csv formatted list
        """
        entity_data = self._get_entity_data(title)
        entity_data["CSVLines"] = data_table

    def add_entity_attachment(self, entity_identifier, filename, file_contents, additional_data=None):
        """
        add attachment with entity identifier as title
        :param entity_identifier: {string} entity identifier
        :param filename: {string} file name
        :param file_contents: {base64} file content
        :param additional_data:
        """
        self.add_attachment(entity_identifier, filename, file_contents, additional_data)

    def add_attachment(self, title, filename, file_contents, additional_data=None):
        """
        add attachment
        :param title: {string} attachment title
        :param filename: {string} file name
        :param file_contents: {base64} file content
        :param additional_data:
        :return:
        """
        self._validate_attachment_size(len(file_contents))

        file_dict = {}
        if additional_data is not None:
            file_dict.update(additional_data)

        file_dict["filename"] = filename
        file_dict["file_contents"] = file_contents

        entity_data = self._get_entity_data(title)
        entity_data["Attachments"][filename] = file_contents
        self._total_attachment_size += len(file_contents)

    def add_entity_html_report(self, entity_identifier, report_name, report_contents):
        """
        add html data with entity identifier as title
        :param entity_identifier: {string} entity identifier
        :param report_name:{string} html report name
        :param report_contents: html content
        :return:
        """
        self.add_html(entity_identifier, report_name, report_contents)

    def add_html(self, title, report_name, report_contents):
        """
        add html data
        :param title: {string} title
        :param report_name: {string} html report name
        :param report_contents: html content
        """
        self._validate_attachment_size(len(report_contents))

        entity_data = self._get_entity_data(title)
        entity_data["Htmls"][report_name] = report_contents

    def add_entity_link(self, entity_identifier, link):
        """
        add web link with entity identifier as title
        :param entity_identifier: {string} entity identifier
        :param link: {string} link
        """
        self.add_link(entity_identifier, link)

    def add_link(self, title, link):
        """
        add web link
        :param title: {string} link title
        :param link: {string} link
        """
        entity_data = self._get_entity_data(title)
        if "Links" not in entity_data:
            entity_data["Links"] = []
        entity_data["Links"].append(link)

    def _get_entity_data(self, title):
        """
        get entity data
        :param title: {string} entity identifier
        :return: entity data
        """
        if title not in self._result_object:
            is_entity = False
            if title in self._entities:
                is_entity = True
            self._result_object[title] = {"Title": title,
                                          "IsForEntity": is_entity,
                                          "Content": "",
                                          "RawJson": "",
                                          "CSVLines": "",
                                          "Attachments": {},
                                          "Htmls": {}}
        return self._result_object[title]

    def _validate_attachment_size(self, attachment_size):
        """
        Validate attachment size - limit to 5 MB.
        :param attachment_size: {int} attachment file size
        """
        if attachment_size > self.MAX_ATTACHMENT_SIZE:
            raise EnvironmentError(
                "Attachment cannot be larger than %d MB" % int(self.MAX_ATTACHMENT_SIZE / 1024 / 1024))
        if attachment_size + self._total_attachment_size > self.MAX_TOTAL_ATTACHMENT_SIZE:
            raise EnvironmentError("Total entity attachments cannot be larger than %d MB" % int(
                self.MAX_TOTAL_ATTACHMENT_SIZE / 1024 / 1024))
