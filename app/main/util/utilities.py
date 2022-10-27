class Utilities:
    @staticmethod
    def get_domain_name(url):
        url = url.rstrip('/')
        url = url.rstrip('#')
        url = url.rstrip('/')
        url = url.replace('http://', '')
        url = url.replace('https://', '')
        url = url.replace('www.', '')
        url = url.strip()
        url = url.lower()
        res = url.split('/')
        url = res[0].strip()
        url = url.split(":")[0].strip()
        return url

    @staticmethod
    def construct_where_clause_from_dict(query_dict):
        if len(query_dict) > 0:
            where = "where "
            for key, value in query_dict.items():
                if value.isdigit() or key.__contains__("date"):
                    where = where + str(key) + " like '" + str(value) + "' and "
                else:
                    where = where + str(key) + " like '%" + str(value) + "%' and "
            where = where.strip(" and ") + ";"
            return where
        else:
            return ""

    @staticmethod
    def validate_person_input(data):
        string_values = ["skills"]
        alpha_values = ["name", "employee role", "designation"]
        # int_values = ["id"]
        for key, value in data.items():
            # todo commentout below validation id is autoincrement
            # if key in int_values:
            #     if value is None or not str(value).isdigit() or str(value).startswith(" ") or str(value) == "":
            #         msg = str(key) + " should not be empty and should be of integer type"
            #         return False, msg
            # elif key in contact_values:
            #     pass  # todo add below validation when contact is mandatory again
            if key in string_values:
                if value is None or value.startswith(" ") or value == "":
                    msg = str(key) + " should not be empty or None"
                    return False, msg
            if key in alpha_values:
                if value is None or value.startswith(" ") or value == "":
                    msg = str(key) + " should not be empty or None"
                    return False, msg
                # else:
                #     value_list = value.split("")
                #     for val in value_list:
                #         if not val.isalpha():
                #             msg = str(key) + " should only contain alphabets, not numbers or special characters"
                #             return False, msg
            else:
                continue
        return True, ""

    @staticmethod
    def is_int_or_float(value):
        if type(value) == int:
            return True
        if type(value) == float:
            return True
        return False

    @staticmethod
    def create_update_set_from_dict(query_dict):
        # del query_dict['id']
        update_set = " set "
        for key, value in query_dict.items():
            update_set = update_set + str(key) + "=\"" + str(value) + "\", "
        update_set = update_set.strip(", ")

        return update_set

    @staticmethod
    def validate_update_input(data):
        dict_len = 0
        update_dict = {}
        for key, value in data.items():
            if value is not None and not str(value).startswith(" ") and value != "":
                update_dict[key] = value
                dict_len += 1
        return dict_len, update_dict
