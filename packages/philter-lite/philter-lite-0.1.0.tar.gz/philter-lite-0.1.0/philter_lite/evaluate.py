import json
import os
import re

import nltk


def seq_eval(
    note_lst,
    anno_lst,
    text_matcher=re.compile(r"[a-zA-Z0-9]"),
    phi_matcher=re.compile(r"\*+"),
):
    """
        Compares two sequences item by item,
        returns generator which yields:
        classifcation, word

        classifications can be TP, FP, FN, TN
        corresponding to True Positive, False Positive, False Negative and True Negative
    """

    start_coordinate = 0
    for note_word, anno_word in list(zip(note_lst, anno_lst)):

        # Get coordinates
        note_word_stripped = re.sub(r"[^a-zA-Z0-9\*]+", "", note_word.strip())
        if len(note_word_stripped) == 0:
            # got a blank space or something without any characters or digits, move forward
            start_coordinate += len(note_word)
            continue

        if phi_matcher.search(anno_word):
            # this contains phi

            if note_word == anno_word:
                yield "TP", note_word, start_coordinate

            else:
                if text_matcher.search(anno_word):
                    # this is a complex edge case,
                    # the phi annotation has some characters *'ed, and some not,
                    # find the overlap and report any string of chars in anno as FP
                    # and any string of chars in note as FN
                    fn_words = []
                    fp_words = []

                    fn_chunk = []
                    fp_chunk = []
                    for n, a in list(zip(note_word, anno_word)):
                        if n == a:
                            # these characters match, clear our chunks
                            if len(fp_chunk) > 0:
                                fp_words.append("".join(fp_chunk))
                                fp_chunk = []
                            if len(fn_chunk) > 0:
                                fn_words.append("".join(fn_words))
                                fn_chunk = []

                            continue
                        if a == "*" and n != "*":
                            fn_chunk.append(n)
                        elif a != "*" and n == "*":
                            fp_chunk.append(a)

                    # clear any remaining chunks
                    if len(fp_chunk) > 0:
                        fp_words.append("".join(fp_chunk))
                    if len(fn_chunk) > 0:
                        fn_words.append("".join(fn_words))

                    # now drain the difference
                    for w in fn_words:
                        yield "FN", w, start_coordinate
                    for w in fp_words:
                        yield "FP", w, start_coordinate

                else:
                    # simpler case, anno word is completely blocked out except punctuation
                    yield "FN", note_word, start_coordinate

        else:
            if not note_word.isspace():
                # this isn't phi
                if note_word == anno_word:
                    yield "TN", note_word, start_coordinate
                else:
                    yield "FP", anno_word, start_coordinate

        # advance our start coordinate
        start_coordinate += len(note_word)


def eval(
    self,
    anno_path="data/i2b2_anno/",
    anno_suffix="_phi_reduced.ano",
    in_path="data/i2b2_results/",
    summary_output="data/phi/summary.json",
    fn_output="data/phi/fn.txt",
    fp_output="data/phi/fp.txt",
    punctuation_matcher=re.compile(r"[^a-zA-Z0-9\*]"),
):
    """ calculates the effectiveness of the philtering / extraction

        only_digits = <boolean> will constrain evaluation on philtering of only digit types
    """

    if not os.path.exists(anno_path):
        raise Exception("Anno Filepath does not exist", anno_path)
    if not os.path.exists(in_path):
        raise Exception("Input Filepath does not exist", in_path)

    summary = {
        "total_false_positives": 0,
        "total_false_negatives": 0,
        "total_true_positives": 0,
        "total_true_negatives": 0,
        "false_positives": [],  # non-phi words we think are phi
        "true_positives": [],  # phi words we correctly identify
        "false_negatives": [],  # phi words we think are non-phi
        "true_negatives": [],  # non-phi words we correctly identify
        "summary_by_file": {},
    }
    summary_coords = {"summary_by_file": {}}

    all_fn = []
    all_fp = []

    for root, dirs, files in os.walk(in_path):

        for f in files:
            # TODO: come up with something better to ensure one to one txt file comparisons with anno_path
            if not f.endswith(".txt"):
                continue

            # local values per file
            false_positives = []  # non-phi we think are phi
            false_positives_coords = []
            true_positives = []  # phi we correctly identify
            true_positives_coords = []
            false_negatives = []  # phi we think are non-phi
            false_negatives_coords = []
            true_negatives = []  # non-phi we correctly identify
            true_negatives_coords = []

            philtered_filename = root + f
            anno_filename = anno_path + "".join(f.split(".")[0]) + anno_suffix

            if not os.path.exists(philtered_filename):
                raise Exception("FILE DOESNT EXIST", philtered_filename)

            if not os.path.exists(anno_filename):
                continue

            philtered = open(philtered_filename, "r").read()
            philtered_words = re.split("(\s+)", philtered)
            philtered_words_cleaned = []
            for item in philtered_words:
                if len(item) > 0:
                    if item.isspace() == False:
                        split_item = re.split(
                            "(\s+)", re.sub(punctuation_matcher, " ", item)
                        )
                        for elem in split_item:
                            if len(elem) > 0:
                                philtered_words_cleaned.append(elem)
                    else:
                        philtered_words_cleaned.append(item)

            anno = open(anno_filename, "r").read()

            anno_words = re.split("(\s+)", anno)
            anno_words_cleaned = []
            for item in anno_words:
                if len(item) > 0:
                    if not item.isspace():
                        split_item = re.split(
                            "(\s+)", re.sub(punctuation_matcher, " ", item)
                        )
                        for elem in split_item:
                            if len(elem) > 0:
                                anno_words_cleaned.append(elem)
                    else:
                        anno_words_cleaned.append(item)
            for c, w, r in self.seq_eval(philtered_words_cleaned, anno_words_cleaned):

                # Double check that we aren't adding blank spaces or single punctionation characters to our lists
                if not w.isspace() and (re.sub(r"[^a-zA-Z0-9\*]+", "", w) != ""):

                    if c == "FP":
                        false_positives.append(w)
                        false_positives_coords.append([w, r])

                    elif c == "FN":
                        false_negatives.append(w)
                        false_negatives_coords.append([w, r])
                    elif c == "TP":
                        true_positives.append(w)
                        true_positives_coords.append([w, r])
                    elif c == "TN":
                        true_negatives.append(w)
                        true_negatives_coords.append([w, r])

            # update summary
            summary["summary_by_file"][philtered_filename] = {
                "false_positives": false_positives,
                "false_negatives": false_negatives,
                "num_false_negatives": len(false_negatives),
            }
            summary["total_true_positives"] = summary["total_true_positives"] + len(
                true_positives
            )
            summary["total_false_positives"] = summary["total_false_positives"] + len(
                false_positives
            )
            summary["total_false_negatives"] = summary["total_false_negatives"] + len(
                false_negatives
            )
            summary["total_true_negatives"] = summary["total_true_negatives"] + len(
                true_negatives
            )
            all_fp = all_fp + false_positives
            all_fn = all_fn + false_negatives

            # Create coordinate summaries
            summary_coords["summary_by_file"][philtered_filename] = {
                "false_positives": false_positives_coords,
                "false_negatives": false_negatives_coords,
                "true_positives": true_positives_coords,
            }

    if summary["total_true_positives"] + summary["total_false_negatives"] > 0:
        recall = summary["total_true_positives"] / (
            summary["total_true_positives"] + summary["total_false_negatives"]
        )
    elif summary["total_false_negatives"] == 0:
        recall = 1.0

    if summary["total_true_positives"] + summary["total_false_positives"] > 0:
        precision = summary["total_true_positives"] / (
            summary["total_true_positives"] + summary["total_false_positives"]
        )
    elif summary["total_true_positives"] == 0:
        precision = 0.0

    if summary["total_true_negatives"] + summary["total_false_positives"] > 0:
        retention = summary["total_true_negatives"] / (
            summary["total_true_negatives"] + summary["total_false_positives"]
        )
    else:
        retention = 0.0

    # DETAILED EVAL ##################
    # save the phi we missed
    json.dump(summary, open(summary_output, "w"), indent=4)
    json.dump(all_fn, open(fn_output, "w"), indent=4)
    json.dump(all_fp, open(fp_output, "w"), indent=4)

    if self.verbose:
        print("\n")
        print("Uncorrected Results:")
        print("\n")
        print(
            "TP:",
            summary["total_true_positives"],
            "FN:",
            summary["total_false_negatives"],
            "TN:",
            summary["total_true_negatives"],
            "FP:",
            summary["total_false_positives"],
        )
        print("Global Recall: {:.2%}".format(recall))
        print("Global Precision: {:.2%}".format(precision))
        print("Global Retention: {:.2%}".format(retention))

    # Get phi tags #####################
    # Get xml summary
    phi = self.xml
    # Create dictionary to hold fn tags
    fn_tags = {}
    fp_tags = {}

    # Keep track of recall and precision for each category
    phi_categories = ["Age", "Contact", "Date", "ID", "Location", "Name", "Other"]
    # i2b2:
    if not self.ucsf_format:
        # Define tag list
        i2b2_tags = [
            "DOCTOR",
            "PATIENT",
            "DATE",
            "MEDICALRECORD",
            "IDNUM",
            "DEVICE",
            "USERNAME",
            "PHONE",
            "EMAIL",
            "FAX",
            "CITY",
            "STATE",
            "ZIP",
            "STREET",
            "LOCATION-OTHER",
            "HOSPITAL",
            "AGE",
        ]

        i2b2_category_dict = {
            "DOCTOR": "Name",
            "PATIENT": "Name",
            "DATE": "Date",
            "MEDICALRECORD": "ID",
            "IDNUM": "ID",
            "DEVICE": "ID",
            "USERNAME": "Contact",
            "PHONE": "Contact",
            "EMAIL": "Contact",
            "FAX": "Contact",
            "CITY": "Location",
            "STATE": "Location",
            "ZIP": "Location",
            "STREET": "Location",
            "LOCATION-OTHER": "Location",
            "HOSPITAL": "Location",
            "AGE": "Age",
        }

        i2b2_include_tags = [
            "DOCTOR",
            "PATIENT",
            "DATE",
            "MEDICALRECORD",
            "IDNUM",
            "DEVICE",
            "USERNAME",
            "PHONE",
            "EMAIL",
            "FAX",
            "CITY",
            "STATE",
            "ZIP",
            "STREET",
            "LOCATION-OTHER",
            "HOSPITAL",
            "AGE",
        ]
        i2b2_patient_tags = [
            "PATIENT",
            "DATE",
            "MEDICALRECORD",
            "IDNUM",
            "DEVICE",
            "USERNAME",
            "PHONE",
            "EMAIL",
            "FAX",
            "CITY",
            "STATE",
            "ZIP",
            "STREET",
            "LOCATION-OTHER",
            "HOSPITAL",
            "AGE",
        ]
        i2b2_provider_tags = [
            "DOCTOR",
            "DATE",
            "USERNAME",
            "PHONE",
            "EMAIL",
            "FAX",
            "CITY",
            "STATE",
            "ZIP",
            "STREET",
            "LOCATION-OTHER",
            "HOSPITAL",
        ]

        rp_summaries = {}
        for i in range(0, len(i2b2_tags)):
            tag = i2b2_tags[i]
            fn_key = tag + "_fns"
            tp_key = tag + "_tps"
            rp_summaries[fn_key] = 0
            rp_summaries[tp_key] = 0

    # ucsf:
    if self.ucsf_format:
        # Define tag list
        ucsf_tags = [
            "Date",
            "Provider_Name",
            "Phone_Fax",
            "Age",
            "Patient_Name_or_Family_Member_Name",
            "Patient_Address",
            "Patient_Initials",
            "Provider_Address_or_Location",
            "Provider_Initials",
            "Provider_Certificate_or_License",
            "Patient_Medical_Record_Id",
            "Patient_Account_Number",
            "Patient_Social_Security_Number",
            "Patient_Vehicle_or_Device_Id",
            "Patient_Unique_Id",
            "Diagnosis_Code_ICD_or_International",
            "Procedure_or_Billing_Code",
            "Medical_Department_Name",
            "Email",
            "URL_IP",
            "Patient_Biometric_Id_or_Face_Photo",
            "Patient_Language_Spoken",
            "Patient_Place_Of_Work_or_Occupation",
            "Patient_Certificate_or_License",
            "Medical_Research_Study_Name_or_Number",
            "Teaching_Institution_Name",
            "Non_UCSF_Medical_Institution_Name",
            "Medical_Institution_Abbreviation",
            "Unclear",
        ]

        ucsf_category_dict = {
            "Date": "Date",
            "Provider_Name": "Name",
            "Phone_Fax": "Contact",
            "Age": "Age",
            "Patient_Name_or_Family_Member_Name": "Name",
            "Patient_Address": "Location",
            "Patient_Initials": "Name",
            "Provider_Address_or_Location": "Location",
            "Provider_Initials": "Name",
            "Provider_Certificate_or_License": "ID",
            "Patient_Medical_Record_Id": "ID",
            "Patient_Account_Number": "ID",
            "Patient_Social_Security_Number": "ID",
            "Patient_Vehicle_or_Device_Id": "ID",
            "Patient_Unique_Id": "ID",
            "Diagnosis_Code_ICD_or_International": "ID",
            "Procedure_or_Billing_Code": "ID",
            "Medical_Department_Name": "Location",
            "Email": "Contact",
            "URL_IP": "Contact",
            "Patient_Biometric_Id_or_Face_Photo": "ID",
            "Patient_Language_Spoken": "Other",
            "Patient_Place_Of_Work_or_Occupation": "Location",
            "Patient_Certificate_or_License": "ID",
            "Medical_Research_Study_Name_or_Number": "ID",
            "Teaching_Institution_Name": "Location",
            "Non_UCSF_Medical_Institution_Name": "Location",
            "Medical_Institution_Abbreviation": "Location",
            "Unclear": "Other",
        }

        if self.initials:
            ucsf_include_tags = [
                "Date",
                "Provider_Name",
                "Phone_Fax",
                "Patient_Name_or_Family_Member_Name",
                "Patient_Address",
                "Provider_Address_or_Location",
                "Provider_Certificate_or_License",
                "Patient_Medical_Record_Id",
                "Patient_Account_Number",
                "Patient_Social_Security_Number",
                "Patient_Vehicle_or_Device_Id",
                "Patient_Unique_Id",
                "Procedure_or_Billing_Code",
                "Email",
                "URL_IP",
                "Patient_Biometric_Id_or_Face_Photo",
                "Patient_Certificate_or_License",
                "Age",
                "Patient_Initials",
                "Provider_Initials",
            ]
            ucsf_patient_tags = [
                "Date",
                "Phone_Fax",
                "Age",
                "Patient_Name_or_Family_Member_Name",
                "Patient_Address",
                "Patient_Initials",
                "Patient_Medical_Record_Id",
                "Patient_Account_Number",
                "Patient_Social_Security_Number",
                "Patient_Vehicle_or_Device_Id",
                "Patient_Unique_Id",
                "Email",
                "URL_IP",
                "Patient_Biometric_Id_or_Face_Photo",
                "Patient_Certificate_or_License",
            ]
            ucsf_provider_tags = [
                "Provider_Name",
                "Phone_Fax",
                "Provider_Address_or_Location",
                "Provider_Initials",
                "Provider_Certificate_or_License",
                "Email",
                "URL_IP",
            ]

        else:
            ucsf_include_tags = [
                "Date",
                "Provider_Name",
                "Phone_Fax",
                "Patient_Name_or_Family_Member_Name",
                "Patient_Address",
                "Provider_Address_or_Location",
                "Provider_Certificate_or_License",
                "Patient_Medical_Record_Id",
                "Patient_Account_Number",
                "Patient_Social_Security_Number",
                "Patient_Vehicle_or_Device_Id",
                "Patient_Unique_Id",
                "Procedure_or_Billing_Code",
                "Email",
                "URL_IP",
                "Patient_Biometric_Id_or_Face_Photo",
                "Patient_Certificate_or_License",
                "Age",
            ]
            ucsf_patient_tags = [
                "Date",
                "Phone_Fax",
                "Age",
                "Patient_Name_or_Family_Member_Name",
                "Patient_Address",
                "Patient_Medical_Record_Id",
                "Patient_Account_Number",
                "Patient_Social_Security_Number",
                "Patient_Vehicle_or_Device_Id",
                "Patient_Unique_Id",
                "Email",
                "URL_IP",
                "Patient_Biometric_Id_or_Face_Photo",
                "Patient_Certificate_or_License",
            ]
            ucsf_provider_tags = [
                "Provider_Name",
                "Phone_Fax",
                "Provider_Address_or_Location",
                "Provider_Certificate_or_License",
                "Email",
                "URL_IP",
            ]

        rp_summaries = {}
        for i in range(0, len(ucsf_tags)):
            tag = ucsf_tags[i]
            fn_key = tag + "_fns"
            tp_key = tag + "_tps"
            rp_summaries[fn_key] = 0
            rp_summaries[tp_key] = 0

    # Create dictionaries for unigram and bigram PHI/non-PHI frequencies
    # Diciontary values look like: [phi_count, non-phi_count]
    unigram_dict = {}
    bigram_dict = {}
    corrected_age_fns = 0

    # Loop through all filenames in summary
    for fn in summary_coords["summary_by_file"]:
        # print(self.patterns)
        # get input notes filename (for filter analysis wit coordinatemap)
        input_filename = os.path.basename(fn)

        current_summary = summary_coords["summary_by_file"][fn]

        # Get corresponding info in phi_notes
        note_name = fn.split("/")[-1]

        try:
            anno_name = note_name.split(".")[0] + ".xml"
            text = phi[anno_name]["text"]
        except KeyError:
            anno_name = note_name.split(".")[0] + ".txt.xml"
            text = phi[anno_name]["text"]

        lst = re.split(r"(\s+)", text)
        cleaned = []
        for item in lst:
            if len(item) > 0:
                if not item.isspace():
                    split_item = re.split(r"(\s+)", re.sub(r"[^a-zA-Z0-9]", " ", item))
                    for elem in split_item:
                        if len(elem) > 0:
                            cleaned.append(elem)
                else:
                    cleaned.append(item)

        # Get coords for POS tags
        start_coordinate = 0
        pos_coords = []
        for item in cleaned:
            pos_coords.append(start_coordinate)
            start_coordinate += len(item)

        pos_list = nltk.pos_tag(cleaned)

        cleaned_with_pos = {}
        for i in range(0, len(pos_list)):
            cleaned_with_pos[str(pos_coords[i])] = [pos_list[i][0], pos_list[i][1]]

        # Get FN tags ##########
        phi_list = phi[anno_name]["phi"]

        # Create unigram and bigram frequency tables #######
        if self.freq_table:

            # Create separate cleaned list/coord list without spaces
            cleaned_nospaces = []
            coords_nospaces = []
            for i in range(0, len(cleaned)):
                if not cleaned[i].isspace():
                    cleaned_nospaces.append(cleaned[i])
                    coords_nospaces.append(pos_coords[i])

            # Loop through all single words and word pairs, and compare with PHI list
            for i in range(0, len(cleaned_nospaces) - 1):
                unigram_word = (
                    cleaned_nospaces[i]
                    .replace("\n", "")
                    .replace("\t", "")
                    .replace(" ", "")
                    .lower()
                )
                bigram_word = " ".join(
                    [
                        cleaned_nospaces[i]
                        .replace("\n", "")
                        .replace("\t", "")
                        .replace(" ", "")
                        .lower(),
                        cleaned_nospaces[i + 1]
                        .replace("\n", "")
                        .replace("\t", "")
                        .replace(" ", "")
                        .lower(),
                    ]
                )
                unigram_start = coords_nospaces[i]
                bigram_start1 = coords_nospaces[i]
                bigram_start2 = coords_nospaces[i + 1]

                # Loop through PHI list and compare ranges
                for phi_item in phi_list:
                    try:
                        phi_start = phi_item["start"]
                        phi_end = phi_item["end"]
                    except KeyError:
                        phi_start = phi_item["spans"].split("~")[0]
                        phi_end = phi_item["spans"].split("~")[1]
                    if unigram_start in range(int(phi_start), int(phi_end)):
                        # This word is PHI and hasn't been added to the dictionary yet
                        if unigram_word not in unigram_dict:
                            unigram_dict[unigram_word] = [1, 0]
                        # This word is PHI and has already been added to the dictionary
                        else:
                            unigram_dict[unigram_word][0] += 1
                    else:
                        # This word is not PHI and hasn't been aded to the dictionary yet
                        if unigram_word not in unigram_dict:
                            unigram_dict[unigram_word] = [0, 1]
                        # This word is not PHI and has already been added to the dictionary
                        else:
                            unigram_dict[unigram_word][1] += 1
                    if bigram_start1 in range(
                        int(phi_start), int(phi_end)
                    ) and bigram_start2 in range(int(phi_start), int(phi_end)):
                        # This word is PHI and hasn't been added to the dictionary yet
                        if bigram_word not in bigram_dict:
                            bigram_dict[bigram_word] = [1, 0]
                        # This word is PHI and has already been added to the dictionary
                        else:
                            bigram_dict[bigram_word][0] += 1
                    else:
                        # This word is not PHI and hasn't been aded to the dictionary yet
                        if bigram_word not in bigram_dict:
                            bigram_dict[bigram_word] = [0, 1]
                        # This word is not PHI and has already been added to the dictionary
                        else:
                            bigram_dict[bigram_word][1] += 1

        # Get tp counts per category
        current_tps = current_summary["true_positives"]
        # Initialize list to keep track of non-include tag FPs
        additional_fps = []

        for word in current_tps:
            start_coordinate_tp = word[1]
            for phi_item in phi_list:
                if self.ucsf_format:
                    phi_start = int(phi_item["spans"].split("~")[0])
                    phi_end = int(phi_item["spans"].split("~")[1])
                else:
                    phi_start = phi_item["start"]
                    phi_end = phi_item["end"]
                phi_type = phi_item["TYPE"]

                if not self.ucsf_format:
                    for i in range(0, len(i2b2_tags)):
                        tag = i2b2_tags[i]
                        tp_key = tag + "_tps"
                        if (
                            start_coordinate_tp in range(int(phi_start), int(phi_end))
                        ) and (tag == phi_type):
                            rp_summaries[tp_key] += 1
                    # Add these TPs to the FPs list of they are not in the include list
                    if phi_type not in i2b2_include_tags:
                        if start_coordinate_tp in range(int(phi_start), int(phi_end)):
                            additional_fps.append(
                                [
                                    text[
                                        start_coordinate_tp : start_coordinate_tp
                                        + len(word[0])
                                    ],
                                    start_coordinate_tp,
                                ]
                            )
                # ucsf
                if self.ucsf_format:
                    if phi_type not in ucsf_include_tags:
                        if start_coordinate_tp in range(int(phi_start), int(phi_end)):
                            additional_fps.append(
                                [
                                    text[
                                        start_coordinate_tp : start_coordinate_tp
                                        + len(word[0])
                                    ],
                                    start_coordinate_tp,
                                ]
                            )

                    for i in range(0, len(ucsf_tags)):
                        tag = ucsf_tags[i]
                        tp_key = tag + "_tps"
                        if (
                            start_coordinate_tp in range(int(phi_start), int(phi_end))
                        ) and (tag == phi_type):
                            rp_summaries[tp_key] += 1

        # i2b2
        if not self.ucsf_format:
            fn_counter_dict = {}
            for i in range(0, len(i2b2_tags)):
                tag = i2b2_tags[i]
                tag_fn_counter = tag + "_fn_counter"
                fn_counter_dict[tag_fn_counter] = 0
        # ucsf
        if self.ucsf_format:
            fn_counter_dict = {}
            for i in range(0, len(ucsf_tags)):
                tag = ucsf_tags[i]
                tag_fn_counter = tag + "_fn_counter"
                fn_counter_dict[tag_fn_counter] = 0

        fn_tag_summary = {}
        include_exclude_fns = ""

        if current_summary["false_negatives"] != [] and current_summary[
            "false_negatives"
        ] != [""]:
            counter = 0
            current_fns = current_summary["false_negatives"]

            for word in current_fns:
                counter += 1
                false_negative = word[0]
                start_coordinate_fn = word[1]

                # initialize list that will hold info on what matched what
                filter_file_list_exclude = []
                filter_file_list_include = []

                # if self.dependent:
                # Loop through coorinate map objects and match patterns with FPs
                for i, pattern in enumerate(self.patterns):
                    coord_map = pattern["coordinate_map"]
                    exclude_include = pattern["exclude"]
                    try:
                        filter_path = pattern["filepath"]
                    except KeyError:
                        filter_path = pattern["title"]
                    for start, stop in coord_map.filecoords(input_filename):
                        # Find intersection between ranges
                        word_range = set(
                            range(
                                start_coordinate_fn,
                                start_coordinate_fn + len(false_negative),
                            )
                        )
                        filter_range = set(range(start, stop))
                        intersection = word_range & filter_range
                        if intersection != set():
                            # Add this filter path to the list of things that filtered this word
                            if exclude_include:
                                filter_file_list_exclude.append(filter_path)
                            else:
                                filter_file_list_include.append(filter_path)

                for phi_item in phi_list:
                    phi_type = phi_item["TYPE"]
                    if self.ucsf_format:
                        phi_start = int(phi_item["spans"].split("~")[0])
                        phi_end = int(phi_item["spans"].split("~")[1])
                    else:
                        phi_start = phi_item["start"]
                        phi_end = phi_item["end"]

                    # i2b2
                    if not self.ucsf_format:
                        for i in range(0, len(i2b2_tags)):
                            tag = i2b2_tags[i]
                            fn_key = tag + "_fns"
                            tag_fn_counter = tag + "_fn_counter"
                            if (
                                start_coordinate_fn
                                in range(int(phi_start), int(phi_end))
                            ) and phi_type == tag:
                                rp_summaries[fn_key] += 1
                                fn_counter_dict[tag_fn_counter] += 1

                    # ucsf
                    if self.ucsf_format:
                        for i in range(0, len(ucsf_tags)):
                            tag = ucsf_tags[i]
                            fn_key = tag + "_fns"
                            tag_fn_counter = tag + "_fn_counter"
                            if (
                                start_coordinate_fn
                                in range(int(phi_start), int(phi_end))
                            ) and phi_type == tag:
                                if tag != "Age":
                                    rp_summaries[fn_key] += 1
                                    fn_counter_dict[tag_fn_counter] += 1

                    # Find PHI match: fn in text, coord in range
                    if start_coordinate_fn in range(int(phi_start), int(phi_end)):
                        # Get PHI tag
                        phi_tag = phi_type
                        # Get POS tag
                        pos_tag = cleaned_with_pos[str(start_coordinate_fn)][1]

                        # Get 25 characters surrounding FN on either side
                        context_start = start_coordinate_fn - 25
                        context_end = start_coordinate_fn + len(false_negative) + 25
                        if context_start >= 0 and context_end <= len(text) - 1:
                            fn_context = text[context_start:context_end]
                        elif context_start >= 0 and context_end > len(text) - 1:
                            fn_context = text[context_start:]
                        else:
                            fn_context = text[:context_end]

                        # Get fn id, to distinguish betweem multiple entries
                        fn_id = "N" + str(counter)

                        # Get include or exclude
                        if not self.ucsf_format:
                            if phi_tag in i2b2_include_tags:
                                include_exclude_fns = "include"
                            else:
                                include_exclude_fns = "exclude"
                        if self.ucsf_format:
                            if phi_tag in ucsf_include_tags:
                                if phi_tag != "Age":
                                    include_exclude_fns = "include"
                                # If age is over 90, include. Else, exclude
                                else:
                                    fn_stripped = false_negative.replace(".", "")
                                    # Is the age an integer?
                                    if fn_stripped.isdigit():
                                        if int(fn_stripped) >= 90:
                                            include_exclude_fns = "include"
                                            corrected_age_fns += 1
                                            # print('Include (int): ',fn_stripped)
                                        else:
                                            include_exclude_fns = "exclude"
                                    # Is the age a string?
                                    # Note that this won't catch all age FNs that are spelled ou
                                    # i.e., only the 'ninety' in 'ninety-five' will be marked as include
                                    # This won't affect our recall at all, but it will affect our precision a little
                                    # We will manually need to subtract theses from our FPs and add to our TPs
                                    else:
                                        if "ninety" in fn_stripped:
                                            include_exclude_fns = "include"
                                            corrected_age_fns += 1
                                        else:
                                            include_exclude_fns = "exclude"
                            else:
                                include_exclude_fns = "exclude"
                        # Create output dicitonary with id/word/pos/phi
                        fn_tag_summary[fn_id] = [
                            false_negative,
                            phi_tag,
                            pos_tag,
                            fn_context,
                            include_exclude_fns,
                            filter_file_list_exclude,
                            filter_file_list_include,
                        ]

        if fn_tag_summary != {}:
            fn_tags[fn] = fn_tag_summary

        # Get FP tags #########
        fp_tag_summary = {}
        current_fps = current_summary["false_positives"] + additional_fps
        if current_fps != [] and current_fps != [""]:
            counter = 0
            for word in current_fps:
                counter += 1
                false_positive = word[0]
                start_coordinate_fp = word[1]
                # print(word)

                # initialize list that will hold info on what matched what
                filter_file_list_exclude = []
                filter_file_list_include = []

                # if self.dependent:
                # Loop through coorinate map objects and match patterns with FPs
                for i, pattern in enumerate(self.patterns):
                    coord_map = pattern["coordinate_map"]
                    exclude_include = pattern["exclude"]
                    try:
                        filter_path = pattern["filepath"]
                    except KeyError:
                        filter_path = pattern["title"]
                    for start, stop in coord_map.filecoords(input_filename):
                        word_range = set(
                            range(
                                start_coordinate_fp,
                                start_coordinate_fp + len(false_positive),
                            )
                        )
                        filter_range = set(range(start, stop))
                        intersection = word_range & filter_range
                        if intersection != set():
                            # Add this filter path to the list of things that filtered this word
                            if exclude_include:
                                filter_file_list_exclude.append(filter_path)
                            else:
                                filter_file_list_include.append(filter_path)

                pos_entry = cleaned_with_pos[str(start_coordinate_fp)]

                pos_tag = pos_entry[1]

                # Get 25 characters surrounding FP on either side
                fp_context = ""
                context_start = start_coordinate_fp - 25
                context_end = start_coordinate_fp + len(false_positive) + 25
                if context_start >= 0 and context_end <= len(text) - 1:
                    fp_context = text[context_start:context_end]
                elif context_start >= 0 and context_end > len(text) - 1:
                    fp_context = text[context_start:]
                else:
                    fp_context = text[:context_end]

                fp_id = "P" + str(counter)

                fp_tag_summary[fp_id] = [
                    false_positive,
                    pos_tag,
                    fp_context,
                    filter_file_list_exclude,
                    filter_file_list_include,
                ]

        if fp_tag_summary != {}:
            fp_tags[fn] = fp_tag_summary

    # Create frequency table outputs
    if self.freq_table:
        # Unigram table
        with open("./data/phi/unigram_freq_table.csv", "w") as f:
            f.write("unigram,phi_count,non-phi_count\n")
            for key in unigram_dict:
                word = key
                phi_count = unigram_dict[key][0]
                non_phi_count = unigram_dict[key][1]
                f.write(word + "," + str(phi_count) + "," + str(non_phi_count) + "\n")
        with open("./data/phi/bigram_freq_table.csv", "w") as f:
            f.write("bigram,phi_count,non-phi_count\n")
            for key in bigram_dict:
                term = key
                phi_count = bigram_dict[key][0]
                non_phi_count = bigram_dict[key][1]
                f.write(term + "," + str(phi_count) + "," + str(non_phi_count) + "\n")

    # get specific recalls
    # i2b2
    overall_data = []
    if not self.ucsf_format:
        include_dict = {
            "fns": 0,
            "tps": 0,
            "fps": summary["total_false_positives"],
            "tns": summary["total_true_negatives"],
        }
        patient_phi_dict = {
            "fns": 0,
            "tps": 0,
            "fps": summary["total_false_positives"],
            "tns": summary["total_true_negatives"],
        }
        provider_phi_dict = {
            "fns": 0,
            "tps": 0,
            "fps": summary["total_false_positives"],
            "tns": summary["total_true_negatives"],
        }

        category_dict = {}
        for i in range(0, len(phi_categories)):
            category_tag = phi_categories[i]
            category_fns = category_tag + "_fns"
            category_tps = category_tag + "_tps"

            category_dict[category_fns] = 0
            category_dict[category_tps] = 0

        overall_recall_dict = {}

        for i in range(0, len(i2b2_tags)):
            tag = i2b2_tags[i]
            fn_key = tag + "_fns"
            tp_key = tag + "_tps"
            recall_key = tag + "_recall"

            # Get info for overall include dict and category dict
            if tag in i2b2_include_tags:
                include_dict["fns"] += rp_summaries[fn_key]
                include_dict["tps"] += rp_summaries[tp_key]

                if tag in i2b2_patient_tags:
                    patient_phi_dict["fns"] += rp_summaries[fn_key]
                    patient_phi_dict["tps"] += rp_summaries[tp_key]
                if tag in i2b2_provider_tags:
                    provider_phi_dict["fns"] += rp_summaries[fn_key]
                    provider_phi_dict["tps"] += rp_summaries[tp_key]

                tag_category = i2b2_category_dict[tag]
                category_fns = tag_category + "_fns"
                category_tps = tag_category + "_tps"

                category_dict[category_fns] += rp_summaries[fn_key]
                category_dict[category_tps] += rp_summaries[tp_key]

            # Get additional TNs and FPs
            if tag not in i2b2_include_tags:
                include_dict["tns"] += rp_summaries[fn_key]
                include_dict["fps"] += rp_summaries[tp_key]

                if tag in i2b2_patient_tags:
                    patient_phi_dict["tns"] += rp_summaries[fn_key]
                    patient_phi_dict["fps"] += rp_summaries[tp_key]
                if tag in i2b2_provider_tags:
                    provider_phi_dict["tns"] += rp_summaries[fn_key]
                    provider_phi_dict["fps"] += rp_summaries[tp_key]

            if rp_summaries[fn_key] != 0:
                overall_recall_dict[recall_key] = rp_summaries[tp_key] / (
                    rp_summaries[fn_key] + rp_summaries[tp_key]
                )
            else:
                overall_recall_dict[recall_key] = 1

            overall_data.append(
                [
                    tag,
                    "{:.2%}".format(overall_recall_dict[recall_key]),
                    str(rp_summaries[tp_key]),
                    str(rp_summaries[fn_key]),
                ]
            )

    # ucsf
    if self.ucsf_format:
        include_dict = {
            "fns": 0,
            "tps": 0,
            "fps": summary["total_false_positives"],
            "tns": summary["total_true_negatives"],
        }
        patient_phi_dict = {
            "fns": 0,
            "tps": 0,
            "fps": summary["total_false_positives"],
            "tns": summary["total_true_negatives"],
        }
        provider_phi_dict = {
            "fns": 0,
            "tps": 0,
            "fps": summary["total_false_positives"],
            "tns": summary["total_true_negatives"],
        }

        category_dict = {}
        for i in range(0, len(phi_categories)):
            category_tag = phi_categories[i]
            category_fns = category_tag + "_fns"
            category_tps = category_tag + "_tps"

            category_dict[category_fns] = 0
            category_dict[category_tps] = 0

        overall_recall_dict = {}

        for tag in ucsf_tags:
            fn_key = tag + "_fns"
            tp_key = tag + "_tps"
            recall_key = tag + "_recall"

            # Get info for overall include dict and category dict
            if tag in ucsf_include_tags:
                if tag != "Age":
                    include_dict["fns"] += rp_summaries[fn_key]
                    include_dict["tps"] += rp_summaries[tp_key]

                    if tag in ucsf_patient_tags:
                        patient_phi_dict["fns"] += rp_summaries[fn_key]
                        patient_phi_dict["tps"] += rp_summaries[tp_key]
                    if tag in ucsf_provider_tags:
                        provider_phi_dict["fns"] += rp_summaries[fn_key]
                        provider_phi_dict["tps"] += rp_summaries[tp_key]

                    tag_category = ucsf_category_dict[tag]
                    category_fns = tag_category + "_fns"
                    category_tps = tag_category + "_tps"

                    category_dict[category_fns] += rp_summaries[fn_key]
                    category_dict[category_tps] += rp_summaries[tp_key]
                else:
                    include_dict["fns"] += corrected_age_fns
                    include_dict["tps"] += rp_summaries[tp_key]
                    include_dict["tns"] += rp_summaries[fn_key] - corrected_age_fns

                    if tag in ucsf_patient_tags:
                        patient_phi_dict["fns"] += corrected_age_fns
                        patient_phi_dict["tps"] += rp_summaries[tp_key]
                        patient_phi_dict["tns"] += (
                            rp_summaries[fn_key] - corrected_age_fns
                        )
                    if tag in ucsf_provider_tags:
                        provider_phi_dict["fns"] += corrected_age_fns
                        provider_phi_dict["tps"] += rp_summaries[tp_key]
                        provider_phi_dict["tns"] += (
                            rp_summaries[fn_key] - corrected_age_fns
                        )

                    tag_category = ucsf_category_dict[tag]
                    category_fns = tag_category + "_fns"
                    category_tps = tag_category + "_tps"

                    category_dict[category_fns] += corrected_age_fns
                    category_dict[category_tps] += rp_summaries[tp_key]

            # Get additional TNs and FPs
            if tag not in ucsf_include_tags:
                include_dict["tns"] += rp_summaries[fn_key]
                include_dict["fps"] += rp_summaries[tp_key]

                if tag in ucsf_patient_tags:
                    patient_phi_dict["tns"] += rp_summaries[fn_key]
                    patient_phi_dict["fps"] += rp_summaries[tp_key]
                if tag in ucsf_provider_tags:
                    provider_phi_dict["tns"] += rp_summaries[fn_key]
                    provider_phi_dict["fps"] += rp_summaries[tp_key]

            if rp_summaries[fn_key] != 0:
                overall_recall_dict[recall_key] = rp_summaries[tp_key] / (
                    rp_summaries[fn_key] + rp_summaries[tp_key]
                )
            else:
                overall_recall_dict[recall_key] = 1
            if tag == "Age":
                overall_data.append(
                    [
                        tag,
                        "{:.2%}".format(overall_recall_dict[recall_key]),
                        str(rp_summaries[tp_key]),
                        str(corrected_age_fns),
                    ]
                )
            else:
                overall_data.append(
                    [
                        tag,
                        "{:.2%}".format(overall_recall_dict[recall_key]),
                        str(rp_summaries[tp_key]),
                        str(rp_summaries[fn_key]),
                    ]
                )

    # pretty print tag recalls
    overall_data.sort(key=lambda x: float(x[1][:-1]), reverse=True)
    sorted_overall_data = [["Tag", "Recall", "TPs", "FNs"]]
    for item in overall_data:
        sorted_overall_data.append(item)

    if self.verbose:
        print("\n")
        print("Recall by Tag:")
        col_width = (
            max(len(word) for row in sorted_overall_data for word in row) + 2
        )  # padding
        for row in sorted_overall_data:
            print("".join(word.ljust(col_width) for word in row))

    # Get category recall
    category_data = []
    for i in range(0, len(phi_categories)):
        category_tag = phi_categories[i]
        category_fns = category_tag + "_fns"
        category_tps = category_tag + "_tps"

        if category_dict[category_fns] != 0:
            category_recall = category_dict[category_tps] / (
                category_dict[category_fns] + category_dict[category_tps]
            )
        else:
            category_recall = 1
        category_data.append(
            [
                category_tag,
                "{:.2%}".format(category_recall),
                str(category_dict[category_tps]),
                str(category_dict[category_fns]),
            ]
        )

    # pretty print category recalls
    category_data.sort(key=lambda x: float(x[1][:-1]), reverse=True)
    sorted_category_data = [["Category", "Recall", "TPs", "FNs"]]
    for item in category_data:
        sorted_category_data.append(item)
    if self.verbose:
        print("\n")
        print("Recall by PHI Category:")
        col_width = (
            max(len(word) for row in category_data for word in row) + 2
        )  # padding
        for row in sorted_category_data:
            print("".join(word.ljust(col_width) for word in row))

    # Get corrected recall, precision ##########

    if include_dict["fns"] != 0:
        corrected_recall = include_dict["tps"] / (
            include_dict["fns"] + include_dict["tps"]
        )
    else:
        corrected_recall = 1

    if include_dict["fps"] != 0:
        corrected_precision = include_dict["tps"] / (
            include_dict["fps"] + include_dict["tps"]
        )
    else:
        corrected_precision = 1

    if include_dict["fps"] != 0:
        specificity = include_dict["tns"] / (include_dict["fps"] + include_dict["tns"])
    else:
        specificity = 1

    print("\n")
    print("Corrected Results:")
    print("\n")
    print(
        "cTP:",
        include_dict["tps"],
        "cFN:",
        include_dict["fns"],
        "cTN:",
        include_dict["tns"],
        "cFP:",
        include_dict["fps"],
    )
    print("Corrected Recall: " + "{:.2%}".format(corrected_recall))
    print("Corrected Precision: " + "{:.2%}".format(corrected_precision))
    print("Corrected Retention: " + "{:.2%}".format(specificity))
    print("\n")

    # Patient-only recall, precision ##########

    if patient_phi_dict["fns"] != 0:
        patient_recall = patient_phi_dict["tps"] / (
            patient_phi_dict["fns"] + patient_phi_dict["tps"]
        )
    else:
        patient_recall = 1

    if patient_phi_dict["fps"] != 0:
        patient_precision = patient_phi_dict["tps"] / (
            patient_phi_dict["fps"] + patient_phi_dict["tps"]
        )
    else:
        patient_precision = 1

    if patient_phi_dict["fps"] != 0:
        patient_specificity = patient_phi_dict["tns"] / (
            patient_phi_dict["fps"] + patient_phi_dict["tns"]
        )
    else:
        patient_specificity = 1

    print("\n")
    print("Patient-Only Results:")
    print("\n")
    print(
        "cTP:",
        patient_phi_dict["tps"],
        "cFN:",
        patient_phi_dict["fns"],
        "cTN:",
        patient_phi_dict["tns"],
        "cFP:",
        patient_phi_dict["fps"],
    )
    print("Patient PHI Recall: " + "{:.2%}".format(patient_recall))
    print("Precision: " + "{:.2%}".format(patient_precision))
    print("Retention: " + "{:.2%}".format(patient_specificity))
    print("\n")

    # Provider-only recall, precision ##########

    provider_recall = 0
    if provider_phi_dict["fns"] != 0:
        provider_recall = provider_phi_dict["tps"] / (
            provider_phi_dict["fns"] + provider_phi_dict["tps"]
        )

    provider_precision = 0
    if provider_phi_dict["fps"] != 0:
        provider_precision = provider_phi_dict["tps"] / (
            provider_phi_dict["fps"] + provider_phi_dict["tps"]
        )

    if provider_phi_dict["fps"] != 0:
        # if include_dict['tps'] != 0 and (include_dict['tps']-include_dict['fns']) > 0:
        provider_specificity = provider_phi_dict["tns"] / (
            provider_phi_dict["fps"] + provider_phi_dict["tns"]
        )
        # else:
        #     corrected_recall = 0
    else:
        provider_specificity = 1

    print("\n")
    print("Provider-Only Results:")
    print("\n")
    print(
        "cTP:",
        provider_phi_dict["tps"],
        "cFN:",
        provider_phi_dict["fns"],
        "cTN:",
        provider_phi_dict["tns"],
        "cFP:",
        provider_phi_dict["fps"],
    )
    print("Provider PHI Recall: " + "{:.2%}".format(provider_recall))
    print("Precision: " + "{:.2%}".format(provider_precision))
    print("Retention: " + "{:.2%}".format(provider_specificity))
    print("\n")

    # Summarize FN results #########

    # With and without context #####

    # With context:
    # Condensed tags will contain id, word, PHI tag, POS tag, occurrences
    fn_tags_condensed_context = {}
    # Stores lists that represent distinct groups of words, PHI and POS tags
    fn_tags_condensed_list_context = []

    # No context:
    # Condensed tags will contain id, word, PHI tag, POS tag, occurrences
    fn_tags_condensed = {}
    # Stores lists that represent distinct groups of words, PHI and POS tags
    fn_tags_condensed_list = []

    # Keep track of how many distinct combinations we've added to each list
    context_counter = 0
    nocontext_counter = 0
    for fn in fn_tags:
        file_dict = fn_tags[fn]
        for subfile in file_dict:
            current_list_context = file_dict[subfile]
            ##############################
            # print(current_list_context)
            current_list_nocontext = (
                current_list_context[:3]
                + [current_list_context[-3]]
                + [current_list_context[-2]]
                + [current_list_context[-1]]
            )
            ############################

            word = current_list_context[0]
            phi_tag = current_list_context[1]
            pos_tag = current_list_context[2]
            fn_context = current_list_context[3].replace("\n", " ")
            filter_matches_exclude = current_list_context[5]
            filter_matches_include = current_list_context[6]

            # Context: add each occurrence with corresponding filename
            fn_tags_condensed_list_context.append(current_list_context)
            key_name = "uniq" + str(context_counter)
            filename = fn.split("/")[-1]
            include_exclude = current_list_context[4]
            fn_tags_condensed_context[key_name] = [
                word,
                phi_tag,
                pos_tag,
                fn_context,
                filename,
                include_exclude,
                filter_matches_exclude,
                filter_matches_include,
            ]
            context_counter += 1

            # No context
            if current_list_nocontext not in fn_tags_condensed_list:
                fn_tags_condensed_list.append(current_list_nocontext)
                key_name = "uniq" + str(nocontext_counter)
                fn_tags_condensed[key_name] = [
                    word,
                    phi_tag,
                    pos_tag,
                    1,
                    include_exclude,
                    filter_matches_exclude,
                    filter_matches_include,
                ]
                nocontext_counter += 1
            else:
                uniq_id_index = fn_tags_condensed_list.index(current_list_nocontext)
                uniq_id = "uniq" + str(uniq_id_index)
                fn_tags_condensed[uniq_id][3] += 1

    # Summariz FP results

    # With context
    # Condensed tags will contain id, word, POS tag, occurrences
    fp_tags_condensed_context = {}
    # Stores lists that represent distinct groups of wordss and POS tags
    fp_tags_condensed_list_context = []

    # No context
    # Condensed tags will contain id, word, POS tag, occurrences
    fp_tags_condensed = {}
    # Stores lists that represent distinct groups of wordss and POS tags
    fp_tags_condensed_list = []

    # Keep track of how many distinct combinations we've added to each list
    nocontext_counter = 0
    context_counter = 0
    for fp in fp_tags:
        file_dict = fp_tags[fp]
        for subfile in file_dict:
            current_list_context = file_dict[subfile]
            current_list_nocontext = (
                current_list_context[:2]
                + [current_list_context[3]]
                + [current_list_context[4]]
            )

            word = current_list_context[0]
            pos_tag = current_list_context[1]
            fp_context = current_list_context[2].replace("\n", " ")
            filter_matches_exclude = current_list_context[3]
            filter_matches_include = current_list_context[4]

            # Context: add each occurrence with corresponding filename
            fp_tags_condensed_list_context.append(current_list_context)
            key_name = "uniq" + str(context_counter)
            filename = fp.split("/")[-1]
            fp_tags_condensed_context[key_name] = [
                word,
                pos_tag,
                fp_context,
                filename,
                filter_matches_exclude,
                filter_matches_include,
            ]
            context_counter += 1

            # No Context
            if current_list_nocontext not in fp_tags_condensed_list:
                fp_tags_condensed_list.append(current_list_nocontext)
                key_name = "uniq" + str(nocontext_counter)
                fp_tags_condensed[key_name] = [
                    word,
                    pos_tag,
                    1,
                    filter_matches_exclude,
                    filter_matches_include,
                ]
                nocontext_counter += 1
            else:
                uniq_id_index = fp_tags_condensed_list.index(current_list_nocontext)
                uniq_id = "uniq" + str(uniq_id_index)
                fp_tags_condensed[uniq_id][2] += 1

    # Write FN and FP results to outfolder
    # Conext
    with open(self.eval_outpath + "fn_tags_context.txt", "w") as fn_file:
        fn_file.write(
            "key"
            + "|"
            + "note_word"
            + "|"
            + "phi_tag"
            + "|"
            + "pos_tag"
            + "|"
            + "context"
            + "|"
            + "filename"
            + "|"
            + "include_exclude"
            + "|"
            + "exclude_filters"
            + "|"
            + "include_filters"
            + "\n"
        )
        # print(fn_tags_condensed_context)
        for key in fn_tags_condensed_context:
            current_list = fn_tags_condensed_context[key]
            fn_file.write(
                key
                + "|"
                + current_list[0]
                + "|"
                + current_list[1]
                + "|"
                + current_list[2]
                + "|"
                + current_list[3]
                + "|"
                + current_list[4]
                + "|"
                + current_list[5]
                + "|"
                + str(current_list[6])
                + "|"
                + str(current_list[7])
                + "\n"
            )

    with open(self.eval_outpath + "fp_tags_context.txt", "w") as fp_file:
        fp_file.write(
            "key"
            + "|"
            + "note_word"
            + "|"
            + "pos_tag"
            + "|"
            + "context"
            + "|"
            + "filename"
            + "|"
            + "exclude_filters"
            + "|"
            + "include_filters"
            + "\n"
        )
        for key in fp_tags_condensed_context:
            current_list = fp_tags_condensed_context[key]
            fp_file.write(
                key
                + "|"
                + current_list[0]
                + "|"
                + current_list[1]
                + "|"
                + current_list[2]
                + "|"
                + current_list[3]
                + "|"
                + str(current_list[4])
                + "|"
                + str(current_list[5])
                + "\n"
            )

    # No context
    with open(self.eval_outpath + "fn_tags.txt", "w") as fn_file:
        fn_file.write(
            "key"
            + "|"
            + "note_word"
            + "|"
            + "phi_tag"
            + "|"
            + "pos_tag"
            + "|"
            + "occurrences"
            + "|"
            + "include_exclude"
            + "|"
            + "exclude_filters"
            + "|"
            + "include_filters"
            + "\n"
        )
        for key in fn_tags_condensed:
            current_list = fn_tags_condensed[key]
            fn_file.write(
                key
                + "|"
                + current_list[0]
                + "|"
                + current_list[1]
                + "|"
                + current_list[2]
                + "|"
                + str(current_list[3])
                + "|"
                + current_list[4]
                + "|"
                + str(current_list[5])
                + "|"
                + str(current_list[6])
                + "\n"
            )

    with open(self.eval_outpath + "fp_tags.txt", "w") as fp_file:
        fp_file.write(
            "key"
            + "|"
            + "note_word"
            + "|"
            + "pos_tag"
            + "|"
            + "occurrences"
            + "|"
            + "exclude_filters"
            + "|"
            + "include_filters"
            + "\n"
        )
        for key in fp_tags_condensed:
            current_list = fp_tags_condensed[key]
            fp_file.write(
                key
                + "|"
                + current_list[0]
                + "|"
                + current_list[1]
                + "|"
                + str(current_list[2])
                + "|"
                + str(current_list[3])
                + "|"
                + str(current_list[4])
                + "\n"
            )


def getphi(
    self,
    anno_folder="data/i2b2_anno/",
    anno_suffix="_phi_reduced.ano",
    data_folder="data/i2b2_notes/",
    output_folder="i2b2_phi",
    filter_regex=None,
):
    """ get's phi from existing data to build up a data model
    data structure to hold our phi and classify phi we find
        {
            "foo.txt":[
                {
                    "phi":"1/1/2019",
                    "context":"The data was 1/1/2019 and the patient was happy",
                    "class":"numer" //number, string ...
                },...
            ],...
        }
    """
    if self.run_eval:
        print("getphi")

    # use config if exists
    if self.anno_folder is not None:
        anno_folder = self.anno_folder

    if self.anno_suffix != "":
        anno_suffix = self.anno_suffix

    phi = {}
    word_counts = {}
    not_phi = {}

    for root, dirs, files in os.walk(data_folder):

        for f in files:

            if not os.path.exists(root + f):
                raise Exception("FILE DOESNT EXIST", root + f)

            if len(anno_suffix) > 0:
                if not os.path.exists(anno_folder + f.split(".")[0] + anno_suffix):
                    print(
                        "FILE DOESNT EXIST",
                        anno_folder + f.split(".")[0] + anno_suffix,
                    )
                    continue
            else:
                if not os.path.exists(anno_folder + f):
                    print("FILE DOESNT EXIST", anno_folder + f)
                    continue

            orig_filename = root + f
            encoding1 = self.detect_encoding(orig_filename)
            orig = open(orig_filename, "r", encoding=encoding1["encoding"]).read()

            orig_words = re.split("\s+", orig)

            anno_filename = anno_folder + f.split(".")[0] + anno_suffix
            encoding2 = self.detect_encoding(anno_filename)
            anno = open(anno_filename, "r", encoding=encoding2["encoding"]).read()
            anno_words = re.split("\s+", anno)

            anno_dict = {}

            for w in anno_words:
                anno_dict[w] = 1

            for i, w in enumerate(orig_words):

                # check for edge cases that should not be "words"
                x = w.replace("_", "").strip()
                if len(x) == 0:
                    continue

                # add all words to our counts
                if w not in word_counts:
                    word_counts[w] = 0
                word_counts[w] += 1

                # check if this word is phi
                if w not in anno_dict:

                    left_index = i - 10
                    if left_index < 0:
                        left_index = 0

                    right_index = i + 10
                    if right_index >= len(orig_words):
                        right_index = len(orig_words) - 1
                    window = orig_words[left_index:right_index]
                    if f not in phi:
                        phi[f] = []

                    c = "string"
                    if re.search("\d+", w):
                        c = "number"

                    phi[f].append({"phi": w, "context": window, "class": c})
                else:
                    # add all words to our counts
                    if w not in not_phi:
                        not_phi[w] = 0
                    not_phi[w] += 1

    # save our phi with context
    json.dump(phi, open("data/phi/phi_context.json", "w"), indent=4)

    # save all phi word counts
    counts = {}
    num_phi = {}
    string_phi = {}

    for f in phi:
        for d in phi[f]:
            if d["phi"] not in counts:
                counts[d["phi"]] = 0
            counts[d["phi"]] += 1
            if d["class"] == "number":
                if d["phi"] not in num_phi:
                    num_phi[d["phi"]] = 0
                num_phi[d["phi"]] += 1
            else:
                if d["phi"] not in string_phi:
                    string_phi[d["phi"]] = 0
                string_phi[d["phi"]] += 1

    # save all phi counts
    json.dump(counts, open("data/phi/phi_counts.json", "w"), indent=4)
    # save phi number counts
    json.dump(num_phi, open("data/phi/phi_number_counts.json", "w"), indent=4)
    # save phi string counts
    json.dump(string_phi, open("data/phi/phi_string_counts.json", "w"), indent=4)
    # save our total word counts
    json.dump(word_counts, open("data/phi/word_counts.json", "w"), indent=4)
    # save our total non_phi counts
    json.dump(not_phi, open("data/phi/non_phi_counts.json", "w"), indent=4)

    # get all non_phi counts by number or string
    non_phi_number = {}
    non_phi_string = {}
    for w in word_counts:
        if re.search("\d+", w):
            if w not in non_phi_number:
                non_phi_number[w] = 0
            non_phi_number[w] += 1
        else:
            if w not in non_phi_string:
                non_phi_string[w] = 0
            non_phi_string[w] += 1

    # save all phi string counts
    json.dump(
        non_phi_number, open("data/phi/non_phi_number_counts.json", "w"), indent=4
    )

    # save all phi number counts
    json.dump(
        non_phi_string, open("data/phi/non_phi_string_counts.json", "w"), indent=4
    )


def mapphi(
    self,
    phi_path="data/phi/phi_counts.json",
    out_path="data/phi/phi_map.json",
    sorted_path="data/phi/phi_sorted.json",
    digit_char="`",
    string_char="?",
):
    """ given all examples of the phi, creates a general representation

        digit_char = this is what digits are replaced by
        string_char = this is what strings are replaced by
        any_char = this is what any random characters are replaced with
    """

    d = json.load(open(phi_path, "r"))

    phi_map = {}

    for phi in d:
        wordlst = []
        phi_word = phi["phi"]
        for c in phi_word:
            if re.match("\d+", c):
                wordlst.append(digit_char)
            elif re.match("[a-zA-Z]+", c):
                wordlst.append(string_char)
            else:
                wordlst.append(c)
        word = "".join(wordlst)
        if word not in phi_map:
            phi_map[word] = {"examples": {}}
        if phi_word not in phi_map[word]["examples"]:
            phi_map[word]["examples"][phi_word] = []
        phi_map[word]["examples"][phi_word].append(phi)

    # save the count of all representations
    for k in phi_map:
        phi_map[k]["count"] = len(phi_map[k]["examples"].keys())

    # save all representations
    json.dump(phi_map, open(out_path, "w"), indent=4)

    # save an ordered list of representations so we can prioritize regex building
    items = []
    for k in phi_map:
        items.append(
            {
                "pattern": k,
                "examples": phi_map[k]["examples"],
                "count": len(phi_map[k]["examples"].keys()),
            }
        )

    items.sort(key=lambda x: x["count"], reverse=True)
    json.dump(items, open(sorted_path, "w"), indent=4)
