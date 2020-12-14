# Yeast Tranformation Protocol
Automated yeast transformation using lithium acetate for Opentrons 2.
1) Automated pipetting of transformation mixture and yeast cells
2) User will move onto temperature module
3) Opentrons will carry out heat shock and then transfer contents to sterile plate
4) User will centrifuge plate and return to robot
5) Automated resuspend of cells and addition of calcium chlorides
6) Plate is now ready for incubation and plating

Download the folder from GitHub
-------------------

![Save GitHub folder on to your computer](https://i.postimg.cc/1t8HdhjY/Screenshot-2020-12-14-at-15-56-09.png)

Open terminal or command line and change the directory (‘cd’):

	$ YourFilePath/Yeast_Transformation_OT-main/Opentrons_scripts
 
Creating your customised protocol
-------------------

Run the script using python by typing the following on MacOS:

	$ python YeastTransformationProtocol_AP12.py
	
Or Windows:
  
	$ python YeastTransformationProtocol_AP12


Enter the values specific to your experiment.

![Save GitHub folder on to your computer](https://i.postimg.cc/cLFZ72tb/Screenshot-2020-12-14-at-16-23-20.png)

Ignore the following errors may appear:
  
	$ /.opentrons/deck_calibration.json not found. Loading defaults


	$ /.opentrons/robot_settings.json not found. Loading defaults


Enter new file name. 

The new file will be saved in the Opentrons_scripts folder.

You can now run this in the Opentrons app!





