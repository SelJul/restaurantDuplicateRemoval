import collections
import csv

from restaurant_audit import *
from fmt_methods import *
import os


class Duplicate(object):
    """
    This is a class for setting and getting duplicate id pairs

    Attributes
    ----------
    duplicate_id : list
        List of duplicate id pairs

    """

    def __init__(self):
        """ The constructor for Duplicate class. """

        self.duplicate_id = []

    def set_duplicate_id(self, duplicate_id):
        """
        Set the first or new duplicate_id

        Parameters
        ----------
        duplicate_id : list
            List of duplicate id pairs
        """

        self.duplicate_id = duplicate_id

    def get_duplicate_id(self):
        """ Return the current list of the duplicate id pairs """
        return self.duplicate_id


class DataSet(object):
    """
    This is a class for setting and getting duplicate id pairs

    Attributes
    ----------
    path : String
        Current path where the TSV file is located
    data : list
        List of all the restaurants with their name, street, city, phone and type
    """

    def __init__(self):
        """ The constructor for DataSet class. """
        self.path = 'data/restaurants.tsv'

        array = []
        with open(self.path) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                if row not in array:
                    array.append(row)

        self.data = array

    def get_restaurant_data(self):
        """ Return the current list of the restaurant data """

        return self.data

    def set_restaurant_data(self, data):
        """
        Set the new restaurant data

        Parameters
        ----------
        data : list
           List of restaurants with their name, street, city, phone and type
        """

        self.data = data

    def get_path(self):
        """ Return the current path of the restaurant data """

        return self.path


class Evaluation(object):
    """
    This is a class for the evaluation of the duplicate removal

    Attributes
    ----------
    tp : int
        True positives: number of duplicate pairs which where correctly guessed
    fp: int
        False positives: number of duplicate pairs which were actually non duplicates
    fn: int
        False negatives: number of non duplicate pairs which were actually duplicates
    precision: float
        Measure for the correctness of the result
    recall: float
        Measure for the completeness of the result
    f1_score: float
        Weighted average of Precision and Recall
    """

    def __init__(self, tp, fp, fn):
        """
        The constructor for Evaluation class.

        Parameters
        ----------
        tp : int
            Number of tp
        fp : int
            Number of fp
        fn : int
            Number of fn
        """

        self.tp = tp
        self.fp = fp
        self.fn = fn

        self.precision = self.tp / (self.tp + self.fp)
        self.recall = self.tp / (self.tp + self.fn)
        self.f1_score = (2 * self.precision * self.recall) / (self.precision + self.recall)

    def get_tp(self):
        """ Return the number of true positives"""

        return self.tp

    def get_fp(self):
        """ Return the number of false positives"""

        return self.fp

    def get_fn(self):
        """ Return the number of false negatives"""

        return self.fn

    def get_precision(self):
        """ Return the precision value"""

        return self.precision

    def get_recall(self):
        """ Return the recall value"""

        return self.recall

    def get_f1_score(self):
        """ Return the f1_score value"""

        return self.f1_score

    def print_evaluation(self):
        """ Print the recall, precision and f1 score"""

        print("Precision: {0:.8f}".format(self.get_precision()))
        print("Recall: {0:.8f}".format(self.get_recall()))
        print("F1 Score: {0:.8f}".format(self.get_f1_score()))


def get_gold_standard():
    """
    Gold standard regarding the duplicate pairs.

    Returns
    -------
    gold_duplicates: list
        List of duplicate id pairs
    """

    gold_duplicates = []

    with open('data/restaurants_DPL.tsv') as tsv_file:
        reader_n = csv.DictReader(tsv_file, dialect='excel-tab')
        for r in reader_n:
            info = {"id1": r["id1"], "id2": r["id2"]}
            gold_duplicates.append(info)

    return gold_duplicates


def get_eval_param(duplicate):
    """
    Get the evaluation params for the Evaluation

    Parameters
    ----------
    duplicate : Duplicate
        Object to save the id's of the duplicates in a list

    Returns
    -------
    tp : int
        Number of declared duplicates that are correct
    fp : int
        Number of declared duplicates that are actually non duplicates
    fn : int
        Number of declared non duplicates that are actually duplicates
    """

    duplicate_id = duplicate.get_duplicate_id()
    gs = get_gold_standard()

    index_d_list = []
    index_gs_list = []

    for index_d in range(len(duplicate_id)):
        for index_gs in range(len(gs)):
            if duplicate_id[index_d] == gs[index_gs]:
                index_d_list.append(index_d)
                index_gs_list.append(index_gs)

    # FP declared duplicate that is actually a non duplicate '
    fp_list = [duplicate_id[index] for index in range(len(duplicate_id)) if index not in index_d_list]
    # FN declared non duplicate that is actually a duplicate '''
    fn_list = [gs[index] for index in range(len(gs)) if index not in index_gs_list]

    fp = len(fp_list)
    fn = len(fn_list)
    tp = len(index_gs_list)
    return fp, fn, tp


def filter_by_name_and_location(duplicate, data_set):
    """
    Identify id pairs by comparing the values of the name, street and city amd saving them in Duplicate

    Parameters
    ----------
    duplicate : Duplicate
        Object to save the id's of the duplicates in a list
    data_set : DataSet
        Object to get the restaurant data
    """

    array = data_set.get_restaurant_data()

    duplicate_id = duplicate.get_duplicate_id()

    for index_d in range(len(array)):
        compare_list = array[index_d + 1:]
        for sub_list in compare_list:
            a_name = array[index_d]["name"]
            sub_name = sub_list["name"]
            a_adr = array[index_d]["address"]
            sub_adr = sub_list["address"]
            a_city = array[index_d]["city"]
            sub_city = sub_list["city"]

            if a_name == sub_name and a_adr == sub_adr and a_city == sub_city:
                info = {"id1": array[index_d]["id"], "id2": sub_list["id"]}
                duplicate_id.append(info)

    duplicate.set_duplicate_id(duplicate_id)


def filter_by_phone(duplicate, data_set):
    """
    Identify id pairs by comparing the values by the phone number and saving them in Duplicate

    Parameters
    ----------
    duplicate : Duplicate
        Object to save the id's of the duplicates in a list
    data_set : DataSet
        Object to get the restaurant data
    """

    duplicate_id = duplicate.get_duplicate_id()
    restaurant_data = data_set.get_restaurant_data()

    for index_d in range(len(restaurant_data)):
        compare_list = restaurant_data[index_d + 1:]
        for elem in compare_list:
            if restaurant_data[index_d]["phone"] == elem["phone"]:
                info = {"id1": restaurant_data[index_d]["id"], "id2": elem["id"]}
                duplicate_id.append(info)

    duplicate.set_duplicate_id(duplicate_id)


def filter_by_fmt(duplicate, data_set):
    """
    Identify the id pairs by using field matching techniques and saving them in Duplicate

    Parameters
    ----------
    duplicate : Duplicate
        Object to save the id's of the duplicates in a list
    data_set : DataSet
        Object to get the restaurant data
    """

    array = data_set.get_restaurant_data()
    duplicate_id = duplicate.get_duplicate_id()
    soundex_types = defaultdict(set)
    blocks = []

    for row in array:
        restaurant_name = row["name"]
        soundex_type = soundex(restaurant_name)
        soundex_types[soundex_type].add(int(row["id"]))

    for soundex_type, value in soundex_types.items():
        if len(value) >= 2:
            blocks.append(list(value))

    # Soundex typed blocking
    for block in blocks:
        block.sort()

        for index in range(len(block)):
            index_d = block[index] - 1
            compare_list = block[index + 1:]
            array_name = array[index_d]["name"]
            array_phone = array[index_d]["phone"]

            for c_index in range(len(compare_list)):
                index_c = compare_list[c_index] - 1
                sub_name = array[index_c]["name"]
                sub_phone = array[index_c]["phone"]

                # Check phone and character based similarity of name
                if array_phone == sub_phone and levenshtein(array_name, sub_name) < 9:
                    info = {"id1": array[index_d]["id"], "id2": array[index_c]["id"]}
                    duplicate_id.append(info)

    # Go trough data to find duplicates which could not be found by soundex blocking
    for index_d in range(len(array)):
        compare_list = array[index_d + 1:]
        array_name = array[index_d]["name"]
        array_phone = array[index_d]["phone"]

        for sub_list in compare_list:
            sub_name = sub_list["name"]
            sub_phone = sub_list["phone"]

            current_id_pair = {"id1": array[index_d]["id"], "id2": sub_list["id"]}

            # Skip ids found in the soundex blocking
            if current_id_pair in duplicate_id:
                continue

            # Check phone and token based similarity of name
            if array_phone == sub_phone and dice_coefficient(array_name, sub_name) > 0.92:
                info = {"id1": array[index_d]["id"], "id2": sub_list["id"]}
                duplicate_id.append(info)

    duplicate.set_duplicate_id(duplicate_id)


def remove_duplicates(duplicate, data_set):
    """
    Removes the duplicates from the DataSet object

    Parameters
    ----------
    data_set : DataSet
        Object to get data
    duplicate : Duplicate
        Object to get the duplicate id pairs
    """

    data = data_set.get_restaurant_data()
    duplicate_id = duplicate.get_duplicate_id()
    delete_id = []

    # Merge the two duplicates together and remember the duplicate id
    for row in duplicate_id:
        first_id = int(row["id1"])
        second_id = int(row["id2"])

        first_data = data[first_id - 1]
        second_data = data[second_id - 1]

        d = collections.OrderedDict()
        d["id"] = first_id
        d["name"] = max(first_data["name"], second_data["name"])
        d["address"] = max(first_data["address"], second_data["address"])
        d["city"] = max(first_data["city"], second_data["city"])
        d["phone"] = max(first_data["phone"], second_data["phone"])
        d["type"] = max(first_data["type"], second_data["type"])

        delete_id.append(second_id)
        data[first_id - 1] = d

    # Remove the duplicate ids
    data = [row for row in data if int(row["id"]) not in delete_id]
    data_set.set_restaurant_data(data)


def write_new_tsv_file(data_set):
    """
    Write the data with most of the duplicates removed into a new TSV file

    Parameters
    ----------
    data_set : DataSet
        Object to get restaurant data
    """

    data = data_set.get_restaurant_data()
    with open('data/restaurants_duplicates_removed.tsv', 'w') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["id", "name", "address", "city", "phone", "type"])
        for row in data:
            writer.writerow([int(row["id"]), row["name"], row["address"], row["city"], row["phone"], row["type"]])


def mongo_import_initial(data_set):
    """
    Import the original data set to a mongo db

    Parameters
    ----------
    data_set : DataSet
        Object to get the path String of the data set
    """

    stream = os.popen(
        'mongoimport --type tsv '
        '--headerline --db restaurant --collection restaurants_initial '
        '--host "restaurant-shard-0/'
        'restaurant-shard-00-01-pmqzx.mongodb.net:27017,'
        'restaurant-shard-00-02-pmqzx.mongodb.net:27017,'
        'restaurant-shard-00-00-pmqzx.mongodb.net:27017" '
        '--authenticationDatabase admin --ssl '
        '--username restaurant-admin '
        '--password restaurant-admin-password '
        '--file ' + data_set.get_path())
    output = stream.read()
    print(output)


if __name__ == "__main__":
    ds = DataSet()
    # mongo_import_initial(ds)

    # print_all_name_exceptions(ds)
    audit_name(ds)
    # print_all_street_types(ds)
    audit_street(ds)
    # print_all_cities(ds)
    audit_city(ds)
    # print_all_restaurant_types(ds)
    audit_restaurant_type(ds)
    # print_all_phone_formats(ds)
    audit_phone_format(ds)

    dup_sm = Duplicate()
    dup_p = Duplicate()
    dup_fmt = Duplicate()

    filter_by_name_and_location(dup_sm, ds)
    filter_by_phone(dup_p, ds)
    filter_by_fmt(dup_fmt, ds)

    # Evaluation from method filter by same value
    print("Exact same value: name, street and city")
    false_positive, false_negative, true_positive = get_eval_param(dup_sm)
    evaluation = Evaluation(true_positive, false_positive, false_negative)
    evaluation.print_evaluation()

    # Evaluation from method filter_by_phone
    print("\nExact same value: phone")
    false_positive, false_negative, true_positive = get_eval_param(dup_p)
    evaluation = Evaluation(true_positive, false_positive, false_negative)
    evaluation.print_evaluation()

    # Evaluation from method filter_by_fmt
    print("\nField matching techniques")
    false_positive, false_negative, true_positive = get_eval_param(dup_fmt)
    evaluation = Evaluation(true_positive, false_positive, false_negative)
    evaluation.print_evaluation()

    remove_duplicates(dup_fmt, ds)
    write_new_tsv_file(ds)
