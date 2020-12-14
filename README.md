# Yeast_Transformation_OT
Automated yeast transformation protocol using Opentrons 2

1. Download the folder from GitHub
2. Open terminal or command line and change the directory (‘cd’) to 
  ~YourFilePath~/Yeast_Transformation_OT-main/Opentrons_scripts

  For an example, see screenshots.

3. Run the script using python by typing the following on /textbf{macs}:
   python YeastTransformationProtocol.py

   for /textbf{windows}:
   py YeastTransformationProtocol.py
      
4. Enter the values specific to your experiment.

5. Ignore the two error messages that appear:
/Users/eloiseoconnor/.opentrons/deck_calibration.json not found. Loading defaults
/Users/eloiseoconnor/.opentrons/robot_settings.json not found. Loading defaults

6. Name the new file your experiment name. e.g. 14122020_EloisesTransformation

7. The new file will be saved in the Opentrons_scripts folder. If you like, you can check this using list (‘ls’) which shows all the files in your current working directory.

8. You can now run your new file in the opentron and it will use values specific to your experiment 

