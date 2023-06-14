# picsellia-utils

This package aims at creating polygons annotation in COCO format from a pair of images and associated mask and uploading it to the Picsellia dataset previously created.

The script to execute is "convert_mask_to_polygon.py"

The prerequired packages are picsellia, fuzzywuzzy, orjson, numpy, typing, abc, and skimage.

Here are the steps to follow to execute the script properly:

1 - Upload the raw data to your Picsellia datalake (through UI or SDK) and create a dataset with all those raw data that will be annotated in the frame of this conversion mask to annotation

2 - Edit the "convert_mask_to_polygon.py" script.

    - line 5: Fill in the variable "api_token" with your Picsellia token, available in the personal settings of the Picsellia platform
    - line 7: Fill in the name of the organization you want to work in with the variable "organization"
    - line 9: Fill in the "host" variable with
        - "https://app.picsellia.com" if you are a Picsellia client 
        - "https://trial.picsellia.com" if you are currently in trial period

    - line 13: Fill in the argument of the method "get_dataset_version_by_id()" with the id of the dataset created at step one. This id can be retrieved on the dataset overview on the UI

3- Before inserting in the script the path to the raw images and the masks on your local machine, you need to make sure that those files/folders are properly structured in your files explorer. The images and masks directory needs to be organized by subfolders named as the label of the images/masks they are containing.

example: in case, we have two types of masks (car and bus), locally the images and masks folders must be organized like this
                                    image_directory/
                                         ├── car/
                                         │   ├── file1.jpg
                                         │   └── file2.png
                                         ├── bus/
                                         │   ├── file3.jpeg
                                         │   └── file4.jpg

                                    masks_directory/                
                                         ├── car/
                                         │   ├── file1.jpg
                                         │   └── file2.png
                                         ├── bus/
                                         │   ├── file3.jpeg
                                         │   └── file4.jpg

4 - Once files are well structured locally, you can go back to the script edition and fill in line 15 as explained below: 
         
            images_dir (str): path directory of your images with subdirectory as labels
  
            masks_dir (str): path directory of your masks with subdirectory as labels

            labelmap (Dict[str, str]): labelmap of your dataset,
                                example: {'0': 'car', '1': 'bus', '2': 'person'}

            conversion_tolerance (float): The tolerance on the approximation of the polygons extracted from the masks. The tolerance must be positive or zero. The smaller the tolerance, the closer the polygon points are to each other and therefore the more points there are to describe the polygon.

5 - Run the convert_mask_to_polygon.py

6 - At the end of script execution a file named "annotations.json" is created, this is the result of the conversion of the masks into COCO format annotations. Those annotations have also been uploaded through an API call to the Picsellia dataset you created at step one.