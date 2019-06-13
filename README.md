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
- Texture files MUST be .jpg files and MUST be located in the img directory
- All textures need to have nice pixel dimensions: (multiple of 50 x multiple of 50)

### Language
python3

### Required Packages
numpy: for inverse matrices
PIL: for parsing image files

### Script Format
In the script, there must be the following line if there is a texture:
texture NAME 0 0 0 0 0 0 0 0 0 0 0 0

If you want to apply texture NAME to a box, add it as the second argument in the script, for example:
box NAME 0 0 0 200 200 200
