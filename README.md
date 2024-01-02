# PixelLightCookieGenerator
PLCG is a quick and customizable way to generate pixel style light cookie textures for your 2D games.

I couldn't find anything that could generate pixel light cookies easily, so I decided to write one for fun (crazy right?).

It uses [Pillow](https://pypi.org/project/Pillow/) to generate the images and Tkinter for the user interface.

![image](https://github.com/mkwozniak/PixelLightCookieGenerator/assets/51724102/1603b9f3-95fc-40c7-98f2-dd0cbd78503d)

##### <i>I'm not exactly an expert in UX. Forgive me.</i>

## Default Output Sample

![image](https://github.com/mkwozniak/PixelLightCookieGenerator/assets/51724102/ea77b7c6-0e00-4993-9792-c1497ac2c8c3)

<i>The white border and extra padding is not visible when exporting.</i>

# Usage
Enter your desired values into each entry and click Generate. You can view your generated image by clicking the Preview button.
This will open the preview window. Once you're satifisfied with your generated image, click the Save button to export it as a PNG image.

Note that generating with a Clear background won't be easily visible in the preview window. 

To prevent this, generate with a Black background first.

### Falloff
<b>Falloff Power</b> subtracts from each color channel for every <b>N</b> pixels <b>(Falloff Spread)</b>. This begins at the radius <b>Falloff Start</b>.

Use the <b>RGB</b> values to control the initial brightness.

### Half Point Mode
When calculating points inside the unit circle, Half Point Mode (enabled by default) will add 0.5 to each point. 
This is usually preferred as it tends to result in better looking circles.

# Building
* Use the command 'pyinstaller plcg.spec' to build the distributable.

# Light and Web Builds
* PLCG Light will be the barebones Python console version. Not yet available.
* PLCG Web will be the browser based Javascript version. Not yet available.

# Notes
* The executable was packaged with pyinstaller. Therefore it may trigger Windows Defender warnings.
* PLCG isn't dreadfully slow, but it is not efficient at generating very large images. You have been warned.

# Sins
* A few magic numbers need to move to config
* Tkinter layout is a bit messy
* Algorithm to generate falloff could use some optimization

# Future Improvements
* Saving/loading templates
* Support for angled cone shapes and sectors
* Support for noise generation
* Support for image masking
* Halo/border effects

  
