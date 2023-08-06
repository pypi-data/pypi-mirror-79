[![Downloads](https://pepy.tech/badge/saenews)](https://pepy.tech/project/saenews)

# For Quickstart go ![here](https://github.com/dheerajmpai/saenews/OLDREADME.md)


# Installing Python

The package runs on python3 (3.5+). It is recomended to use anaconda if you are on Windows or Ubuntu. Anaconda is a package distributer. It creates "Virtual Environments" and hence safer as it does not alter the core Python installation of the system. Miniconda, as the name says, is a minimal version of anaconda. If you are not a regular user of python use Miniconda.

## Installing Miniconda

![Official Release of Miniconda](https://docs.conda.io/en/latest/miniconda.html)

1. Download the relevant version (Windows, Linux or Mac, 64 or 32 bit)

2. For Windows : Execute the .exe file.

### For Linux :

1. Download the file 
2. Go to the folder you had downloaded
3. Open the terminal
4. Install it with the command `sh <the file name>.sh` (Should look something like `sh Miniconda3-latest-Linux-x86_64.sh`)
5. Accept the Terms and Conditions
6. In the final step when the command asks if you want to initialize. Press `Y` or `yes` (By default it will be `no`). This will prevent you from reinitializing the Miniconda everytime you boot up.
7. Exit the terminal and open it again (Or you can give the command `source ~/.bashrc`.)


# Installing Image editing library

- For Windows : Open the Anaconda Prompt.
- For Linux : Open Terminal

Install the package using `pip`. `pip` is a package installer (Kind of Software installer you can say). It will download the version that is compatible with your computer and installs it. Essentially it automates the installation process. The user need not care about the manual installation. 

Use the specific version number to get the particular version of the package

```
pip install saenews==<version_number>
```

As of now the latest version is `1.2.0` so use 

```
pip install saenews==1.2.0
```

(installation may take 5-10 mins)


# Editing Images

Once the package is installed you can use the package to edit images. (You need the image, obviously). 

With the package you can do the following edits.

1. Adding Logo, twitter, facebook handles etc.
2. Adding border
3. Adding Quotes
4. Adding focus (Shading out unimportant regions, also known as vignette effect)
5. Automatically focus on face.
6. Add Title.
7. Add Tagline.
8. And moreover, if you have `N` images you can just repeatedely do the work with just one additional `for` loop.

## Importing Library

First go to the directory wher you have the image that you want to edit. Then open Python with the command `python`. On Windows you need to do this on the Anaconda Command prompt. On Linux use the terminal.

```
python
```
Check of the package is installed properly. To do this import the library using

```python
import saenews
from saenews.utils import quote, put_quote
```
(The second command checks if the functions are imported or not)

## Putting Twitter and Facebook handles
For namesake I am considering the image name to be `image.jpg`. But change it accordingly.

```python
from saenews.utils import quote, put_quote
put_quote('image.jpg')
```
<img src="/ex/6.png" alt="drawing" width="400"/>

The final image would be saved in the directory in the format "Current Date and time".png . It will also be displayed on the terminal. There will be a lot of other intermediate images for references which you can delete.

The current version the default handles are of Awakened Indian. If you need to change them you need to pass additional arguments. Following is an example where I am using the code for sae.news. 

```python
from saenews.utils import put_quote
put_quote('image.jpg', fb_logo='www.sae.news', tw_logo='saenews_')
```
<img src="/ex/5.png" alt="drawing" width="400"/>

Note that it has also put a border. To remove the border use an argument `border_width=0`'

```python
from saenews.utils import quote, put_quote
put_quote('image.jpg', border_width=0)
```
<img src="/ex/4.png" alt="drawing" width="400"/>

## Repeating with a `for` loop

Suppose the name of the images are `image1.jpg` , `image2.jpg`, `image3.jpg`, `image4.jpg` we can do all the four at one shot.

```python
from saenews.utils import quote, put_quote

images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg' ]
for i in images:
    put_quote(i, border_width=0)
```
 (There will be 4 images with the date and time of editing with it. The names will also be displayed on terminal.)


## Adding black strip at the bottom 

You can add a black strip at the bottom so you can put an additional quote there.

There is an another argument to control the width of the blackstrip.

```
black_strip_dims=(left, top, right, bottom)
```
Where in the place of left, top etc. we need to pass the ratio by which the black strip should be extended out of image. (Examples will make it very clear). 

Suppose the image height is `H` and width is `W`. You can add a black strip at the bottom of with 50% of the height of the current image you will use `0.5` in the fourth place.

i.e 

```python
black_strip_dims=(0,0,0,0.5)
``` 

This will add an addition black strip at the bottom of height `0.5*H`. 

Example :

```python
from saenews.utils import quote, put_quote
put_quote('image.jpg',black_strip_dims=(0,0,0,0.5))
``` 
<img src="/ex/3.png" alt="drawing" width="400"/>


## Adding quotes or title/ tagline

You can add title and a tagline for the image. The nomenclature is title and tagline as the library was first build for News images. You can use the title for Quotes and tagline to mention the person who said it. Or any other purposes.


The title and tagline takes few arguments.

| arg    | Description | Datatype | Default Value| Example |
| ----------- | ----------- | -------- | ----------- | --- |
| title       | Title text | string | '' | 'Be the change you want to see' |
| title_cord   | Normalised cordinates of the beginning of the title | tupple (float,float)| (0.035,0.666) | (0.035,0.666) |
| title_font_size | Size of the font(Not normalised)| int/float| '' | 55 |
|title_width_ratio|Width of the title (Normalised)|Float|''|0.9||
|title_text_font|Font used in the text|string containing path to Font File|(Required only when you want to change to new font)|'./Arial.otf'|


## Example :

```python
from saenews.utils import quote, put_quote
title = "Be the change you want to see!"
put_quote(input_file='image.jpg', title=title, title_cord=(0.035, 0.666), title_font_size=80,  title_width_ratio=0.9)
```
<img src="/ex/2.png" alt="drawing" width="400"/>

## Adding Tagline. 

Tagline has exactly the same features but the font is different. You can infact put the title twice. Tagline is used just for convinience.


| arg    | Description | Datatype | Default Value| Example |
| ----------- | ----------- | -------- | ----------- | --- |
| tag_line      | Tagline text | string | '' | '-Mahatma Gandhi' |
| tag_cord   | Normalised cordinates of the beginning of the title | tupple (float,float)| Auto set based on the height and width of Title | (0.035,0.666) |
| tag_font_size | Size of the font(Not normalised)| int/float| '' | 55 |
|tag_width_ratio|Width of the tagline (Normalised)|Float|''|0.9||
|tag_text_font|Font used in the text|string containing path to Font File|(Required only when you want to change to new font)|'./Arial.otf'|

Example :

```python
from saenews.utils import quote, put_quote
title = "Be the change you want to see!"
tag_line = "-- Mahatma Gandhi"
put_quote(input_file='image.jpg', title=title, tag_line=tag_line, title_cord=(0.035, 0.666), title_font_size=80,  title_width_ratio=0.9)
```

<img src="/ex/7.png" alt="drawing" width="400"/>
# Other features

## Change Border Color, No Logo, Focussing etc.

| arg    | Description | Datatype | Default Value| Example |
| ----------- | ----------- | -------- | ----------- | --- |
|border_color|Change the color of border|string|red|orange|
|logo|Add logo or not|Boolean|True|logo=False|
|focus|Where to Focus?(Vignette)|string|''(Searches for face. If it does not get then focusses on center)|Other values : 'center'(focus on center),'false' (False will not focus)|

# Contribute

To contribute : please clone the repo. Make a branch and send a pull request.

If you find any bugs ask in the Issues sections ![here](https://github.com/dheerajmpai/saenews/issues)

If you think any new feature is to be added ask that too in the issues section ![here](https://github.com/dheerajmpai/saenews/issues)

### Updates

### Bugfixes


## Older verion of README 

![here](https://github.com/dheerajmpai/saenews/OLDREADME.md)

# Issues and feature requests

If you find any bug or if you find any feature missing. Raise an issue ![here](https://github.com/dheerajmpai/saenews/issues)


Do Visit our website <a href="https://sae.news"> SAE NEWS</a>



