from picsellia import Client

from valeo_converter import ValeoConverter

api_token = ''

organization = ''

host = "https://app.picsellia.com"

client = Client(api_token=api_token, organization_name=organization, host=host)

dataset = client.get_dataset_version_by_id('')

converter = ValeoConverter(images_dir="", masks_dir="", labelmap={})

coco_annotations_object = converter.update_coco_annotations()

coco_annotations_path = "annotations/coco_annotations.json"
coco_annotations_object.save_coco_annotations_as_json(json_path=coco_annotations_path)

dataset.import_annotations_coco_file(file_path=coco_annotations_path, force_create_label=True,
                                     fail_on_asset_not_found=False)