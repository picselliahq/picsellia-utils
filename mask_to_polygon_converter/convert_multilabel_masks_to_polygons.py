from picsellia import Client
from picsellia.types.enums import InferenceType
from utils import prepare_mask_directories_for_multilabel, convert_seperated_multiclass_masks_to_polygons

api_token = ''

organization = ''

host = "https://app.picsellia.com"

client = Client(api_token=api_token, organization_name=organization, host=host)

dataset = client.get_dataset_version_by_id('')
dataset.set_type(InferenceType.SEGMENTATION)

prepare_mask_directories_for_multilabel(root_directory="", label_to_mask_dict={}, mask_directory="")

convert_seperated_multiclass_masks_to_polygons(data_path="", mask_root_path="", dataset_version=dataset)
