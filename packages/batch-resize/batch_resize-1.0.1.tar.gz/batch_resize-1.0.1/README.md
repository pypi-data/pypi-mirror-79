Resize and crop all images stored in the folder.

By designating a specific folder, resize and crop all images in the sub folders of the specified folder according to settings that you specify. Also save them in the other or the originally designated folder as you specified.

# Install
    pip install batch_resize

# Basic usage
1. The images to be converted are organized by folder as shown below.
    ~~~ 
    +- folder-a 
      +- subfolder-a
      |  +- image-1.jpg
      |  +- image-2.jpg
      +- subfolder-b
          +- image-3.jpg
          +- image-4.jpg
    ~~~

2. Create a config.json file under the destination folder as follows:
    ~~~
    {
        "dest": "../resized",
        "sizes": [
            {"size": [1000, 1500]},
            {"size": [960, 1280]}
        ]
    }
    ~~~

3. Execute the following command in the console environment.
    ~~~
    python -m batch_resize folder-a
    ~~~

4. As a result, you can see that the "resized" folder is created in the same path as the "folder-a" folder as shown below.
    ~~~
    +- folder-a
    +- resized 
      +- subfolder-a
      |  +- 1000x1500
      |  |  +- image-1.jpg
      |  |  +- image-2.jpg
      |  +- 960x1280
      |     +- image-1.jpg
      |     +- image-2.jpg
      +- subfolder-b
         +- 1000x1500
         |  +- image-3.jpg
         |  +- image-4.jpg
         +- 960x1280
            +- image-3.jpg
            +- image-4.jpg
    ~~~

# config.json
In the config.json file, you can specify the folder location where the converted images are to be saved, information on the size to be converted, and settings related to the center point when cropping.

config.json file is as follows:
  | | ||
  |---|---|---|
  | dest || The folder where the entire result will be saved. If it starts with "./" or "../", it is treated as a relative path from the source folder. |
  | sized || Array of target sizes |
  || size | (Required) Target size [width, height] |
  || count | The number of images to convert. The image files in the folder are sorted in ascending order and imported from the front. If it's 0, it gets all. |
  || path | The name of the folder in which to save the converted result to that size. If not specified, a folder in the form of {width}x{height} is created using the width and height values ​​specified in size by default. |
  || center | The ratio of the center point during crop processing. The default is [0.5, 0.5]. It represents the horizontal and vertical center points, respectively. The range is 0 to 1. The closer the number is to 1, the closer it is to the right and the bottom. |

# Command Line
You can also do it without writing config.json with a simple command like this:

    python -m batch_resize folder-a 960 1280

The output is created as follows under folder-a.

    +- folder-a
      +- subfolder-a
      | +- 960x1280
      | +- image-1.jpg
      | +- image-2.jpg
      +- subfolder-b
         +- 960x1280
            +- image-3.jpg
            +- image-4.jpg
