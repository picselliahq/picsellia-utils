from typing import List
from typing import Tuple

import numpy as np
import orjson
from fuzzywuzzy import fuzz
import tqdm
import cv2
import os
from picsellia import DatasetVersion
from picsellia.types.enums import InferenceType


def shift_x_and_y_coordinates(polygon: np.ndarray) -> np.ndarray:
    shifted_contours = np.zeros_like(polygon)
    shifted_contours[:, 0] = polygon[:, 1]
    shifted_contours[:, 1] = polygon[:, 0]
    return shifted_contours


def format_polygons(polygons: List[np.ndarray]) -> List[List[int]]:
    formatted_polygons = list(map(lambda polygon: list(polygon.ravel().astype(int)), polygons))
    return formatted_polygons


def find_most_similar_string(input_string: str, string_list: list) -> str:
    """
    Finds the most similar string in a list based on the input string.

    Parameters:
        input_string (str): The input string to compare against the strings in the list.
        string_list (dict): The list of strings to search for the most similar match.

    Returns:
        str: The most similar string from the list.
    """
    highest_similarity = 0
    most_similar_string = ""

    for string in string_list:
        similarity = fuzz.ratio(input_string, string)
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_string = string
    return most_similar_string


def find_similar_string(input_string: str, string_dict: dict) -> Tuple[int, str] or None:
    """
    Finds a similar string in a list, ignoring capital letters.

    Parameters:
        input_string (str): The input string to compare against the strings in the list.
        string_dict (list): The list of strings to search for a similar match.

    Returns:
        str or None: The similar string from the list, or None if no match is found.
    """
    input_string_lower = input_string.lower()
    for key_string, string in string_dict.items():
        if string.lower() == input_string_lower:
            return key_string, string
    return None


def save_dict_as_json_file(dictionary: dict,
                           json_path: str) -> None:
    """


    :param dictionary: coco_annotations_dict to save
    :param json_path: the path where to save the dictionary
    :return: None
    """
    with open(json_path, "wb") as out_file:
        out_file.write(orjson.dumps(dictionary, option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY))


def convert_seperated_multiclass_masks_to_polygons(data_path: str,
                                                   mask_root_path: str,
                                                   dataset_version: DatasetVersion):
    """

    Args:
        data_path: (str)  directory containing the images. Example: data_path = "archive/input"
        mask_root_path: (str) directory that contains the masks directories. Example: mask_root_path = "Archive"
        dataset_version: (DatasetVersion) the dataset version containing the assets

    Returns: None

    """

    dataset_version.set_type(InferenceType.SEGMENTATION)
    input_dir = os.listdir(data_path)
    labels = os.listdir(mask_root_path)
    labels.remove(os.path.basename(data_path))
    print(labels)
    for fname in tqdm.tqdm(input_dir[2:]):
        print(fname)
        asset = dataset_version.find_asset(filename=fname)
        polygons = []
        for l in labels:
            im = cv2.imread(os.path.join(mask_root_path, l, fname))
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            contours, _ = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            to_add = (
                contours[len(contours) - 1][::1]
                .reshape(
                    contours[len(contours) - 1][::1].shape[0],
                    contours[len(contours) - 1][::1].shape[2],
                )
                .tolist()
            )
            polygons.append((to_add, dataset_version.get_or_create_label(name=l)))
        if len(polygons) > 0:
            try:
                annotation = asset.create_annotation(duration=0)
                annotation.create_multiple_polygons(polygons)
            except Exception as e:
                print(e)
