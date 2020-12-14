# Yeast_Transformation_OT
Automated yeast transformation protocol using Opentrons 2

# Download the folder from GitHub

![Save GitHub folder on to your computer](https://i.postimg.cc/1t8HdhjY/Screenshot-2020-12-14-at-15-56-09.png)

Open terminal or command line and change the directory (‘cd’):n::

	$ YourFilePath/Yeast_Transformation_OT-main/Opentrons_scripts
 
3. Run the script using python by typing the following on either macs or windows
  on macs:
   python YeastTransformationProtocol.py

  on windows:
   python YeastTransformationProtocol
      
4. Enter the values specific to your experiment.

5. Ignore the two error messages that appear:

/Users/eloiseoconnor/.opentrons/deck_calibration.json not found. Loading defaults

/Users/eloiseoconnor/.opentrons/robot_settings.json not found. Loading defaults

6. Name the new file your experiment name. e.g. 14122020_EloisesTransformation

7. The new file will be saved in the Opentrons_scripts folder. If you like, you can check this using list (‘ls’) on mac, which shows all the files in your current working directory.
  on windows:
    Use dir to display a list of files.

8. You can now run your new file in the opentron and it will use values specific to your experiment 

![Mac terminal instructions](https://i.postimg.cc/wvNqF3gf/Picture2.png)


Then you can run::

	$ YourFilePath/Yeast_Transformation_OT-main/Opentrons_scripts
