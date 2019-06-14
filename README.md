# mks66-final

## Names
Aleks Koroza, Matthew Kendall

## Team Name
Team Malleks

## Core Features
- Texture Maps
  - Mapping an image file to a rectangular prism
  - Multiple textures allowed
  - Animation allowed

## Important Information
- Texture files MUST be .jpg or .jpeg files and MUST be located in the img directory
- All textures need to have nice pixel dimensions: (multiple of 50 x multiple of 50)

### Language
python3

### Required Packages
- numpy: used for inverse matrices.
- PIL (pillow): used for parsing image files and constructing the associated u,v dictionary necessary for mapping.

### Script Format
In the script, there must be the following line if there is a texture:
texture NAME 0 0 0 0 0 0 0 0 0 0 0 0

If you want to apply texture NAME to a box, add it as the second argument in the script, for example:
box NAME 0 0 0 200 200 200


## The mapping
The picture below shows the layout of a cube, where the six faces drawn in pen are the ones on the cube.
![](img/mapping.png)
Face 1: front,
Face 9: back,
Face 5: top,
Face 7: bottom,
Face 4: right,
Face 6: left
