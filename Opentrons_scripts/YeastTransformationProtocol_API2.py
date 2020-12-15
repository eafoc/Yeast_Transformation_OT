# Opentrons script for yeast transformation protocol changes

### User-input variables
## DNA:water ratio
# User input
DNA_vol = int(input("Please enter the plasmid DNA volume per transformation (max 10 µL) (µL): "))
if DNA_vol>10:
    raise Exception("Error: Cannot add more than 10 µL of plasmid DNA")
    
# H20 changes accordingly with the DNA volume 
H2O_vol = 10 - DNA_vol

## Changes to number of columns for p300multi
# User input
transformants = int(input("Please enter the number of transformants that will be produced (max 96): "))
if transformants>96:
    raise Exception("Error: Too many transformants")

# Column assignment for transformant number
if transformants <= 8:
    multichannel_column_number = 1
elif transformants <= 16:
      multichannel_column_number = 2
elif transformants <= 24:
      multichannel_column_number = 3  
elif transformants <= 32:
      multichannel_column_number = 4  
elif transformants <= 40:
      multichannel_column_number = 5  
elif transformants <= 48:
      multichannel_column_number = 6  
elif transformants <= 56:
      multichannel_column_number = 7  
elif transformants <= 64:
      multichannel_column_number = 8  
elif transformants <= 72:
      multichannel_column_number = 9  
elif transformants <= 80:
      multichannel_column_number = 10  
elif transformants <= 88:
      multichannel_column_number = 11 
elif transformants <= 96:
        multichannel_column_number = 12
        
## Heat shock changes 
# User input : temperature 
temp_block = int(input("Please enter the temperature for heat shock (recommend 45): "))

# User input : time on the heat block 
time_block = int(input("Please enter the time for heat shock (recommend 40) (mins): "))

########################### OUTPUT FILE STARTS HERE ###################################
### Set-up
## Initialisation
from opentrons import simulate
metadata = {'apiLevel': '2.8'}
protocol = simulate.get_protocol_api('2.8')

## Modules                                                 
# Keeping DNA cool
temp_mod_1 = protocol.load_module('temperature module gen2',6)
temp_mod_1.set_temperature(4)                               

# Heat shock
temp_mod_2 = protocol.load_module('temperature module gen2',9)
temp_mod_2.set_temperature(temp_block)                              

## Labware
# 96-well plates
plate_OG = temp_mod_1.load_labware('corning_96_wellplate_360ul_flat', 6)
plate_new = protocol.load_labware('corning_96_wellplate_360ul_flat', 5)

# Eppendorf racks
eppendorfrack_1 = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 7)
eppendorfrack_2 = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 8)
eppendorfrack_3 = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 10)
eppendorfrack_4 = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 11)

# Tip racks
tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
tiprack_3 = protocol.load_labware('opentrons_96_tiprack_20ul', 4)

# Reagent reservoir
reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 3)
LiOAc_ssDNA = reservoir['A2']
PEG = reservoir['A4']
CaCl2 = reservoir['A6']
yeast = reservoir['A8']
water = reservoir['A9'] 
waste = reservoir['A12']

## Pipettes
p300multi = protocol.load_instrument('p300_multi_gen2', 
                                   'right',
                                    tip_racks=[tiprack_1, tiprack_2])

p20single = protocol.load_instrument('p20_single_gen2', 
                                   'left',
                                    tip_racks=[tiprack_3])

protocol.max_speeds['Z'] = 10

### Functions
## Transformation mixture preperation
# LiOAc and ssDNA transfer
def LiOAc_ssDNA_transfer(column):
  p300multi.distribute(23,                             # Distribute function used to rapidly transfer to all wells with one aspiration
                    LiOAc_ssDNA, 
                    plate_OG.columns()[:column], 
                    touch_tip=True,
                    mix_before=(5,200),                # Mix the ssDNA and LiOAc in reservoir
                    disposal_volume=24,                # Maximum disposal volume used for tip to offset any inaccuracy caused by the distribute function
                    trash=True)

# PEG transfer 
def PEG_transfer(column):   
    p300multi.pick_up_tip(tiprack_1['A2'])                                
    p300multi.flow_rate.aspirate=40                    # Reduced speed as PEG is viscous
    p300multi.flow_rate.dispense=40
    p300multi.transfer(120,
                         PEG,
                         plate_OG.columns()[:column],
                         touch_tip=True,
                         blow_out=True,
                         blowout_location='destination well',
                         mix_after=(5,50),
                         new_tip='never')
    p300multi.drop_tip()                    

## Plasmid DNA and water transfer to 96 well plate (with robot comments linking the position of each eppendorf to each well in the plate)
def DNA_transfer(DNAvolume, H2Ovolume, well):        
    for i in range(well):
        plate_position = str(plate_OG.wells()[i])
        plate_well = plate_position.split()[0]
        
        p20single.pick_up_tip()
        if i <= 23:
            eppendorf_rack = "slot 7"
            eppendorf_position = str(eppendorfrack_1.wells()[i])
            eppendorf_well = eppendorf_position.split()[0]
            
            p20single.aspirate(H2Ovolume, water)                           # Block commands used for more control
            p20single.aspirate(DNAvolume, eppendorfrack_1.wells()[i])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        elif i <= 47:
            eppendorf_rack = "slot 8"
            eppendorf_position = str(eppendorfrack_2.wells()[i-24])
            eppendorf_well = eppendorf_position.split()[0]
            
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_2.wells()[i-24])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        elif i <= 71:
            eppendorf_rack = "slot 10"
            eppendorf_position = str(eppendorfrack_3.wells()[i-48])
            eppendorf_well = eppendorf_position.split()[0]
            
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_3.wells()[i-48])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        else:
            eppendorf_rack = "slot 11"
            eppendorf_position = str(eppendorfrack_4.wells()[i-72])
            eppendorf_well = eppendorf_position.split()[0]
            
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_4.wells()[i-72])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        output = f"The eppenddorf in {eppendorf_well} of {eppendorf_rack} is in well {plate_well} of the 96 well plate"
        protocol.comment(output)
        
## Yeast addition
def yeast_DNA(column):
    p300multi.flow_rate.aspirate=50                               # Reduced speed to account for sensitivity of living cells
    p300multi.flow_rate.dispense=50      
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0])
        p300multi.transfer(32,
                           yeast,
                           plate_OG.columns()[i],
                           trash=False,
                           touch_tip=True,
                           blow_out=True, 
                           blowout_location='destination well',
                           mix_after=(3,100),               
                           new_tip='never')    
        p300multi.drop_tip()             

## Trasfer content from original plate to new plate
def transfer_to_new(column):
    plate_OG = temp_mod_2.load_labware('corning_96_wellplate_360ul_flat', 9)   # Updates position of original plate (it is now on the tempaterature block)
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0])          
        p300multi.transfer(175,                                                # Transfer contents of original plate to a new, sterile plate
                            plate_OG.columns()[i],              
                            plate_new.columns()[i],                      
                            touch_tip=True,                                    # Extra steps ensures minimal loss of cells
                            blow_out=True, 
                            blowout_location='destination well',
                            mix_after=(3,100),                                 # Mixing step to ensure homogeneity 
                            new_tip='never')                                   
        p300multi.return_tip()                                                 # Returns tips to tip rack to be reused

## Remove supernatant
def supernatant(column):
    p300multi.flow_rate.aspirate = 25                                # Slowed aspiration rate to avoid disturbing the pellet
    p300multi.well_bottom_clearance.aspirate = 3                     # This value would need to be optimised to avoid aspirating the pellet
    p300multi.flow_rate.dispense = 150
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0])  
        p300multi.transfer(160,
                           plate_new.columns()[i],
                           waste,
                           blow_out=True,
                           blowout_location='destination well',
                           new_tip='never')
        p300multi.return_tip() 

## CaCl2 addition
def CaCl_addition(column):
    p300multi.flow_rate.aspirate = 150
    p300multi.flow_rate.dispense = 150
    p300multi.well_bottom_clearance.dispense = 3
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0]) 
        p300multi.transfer(200,
                           CaCl2,
                           plate_new.columns()[i],
                           blow_out=True,
                           blowout_location='destination well',
                           new_tip='never',
                           mix_after=(7,100))                       # Thorough mixing to resuspend the pellet
        p300multi.drop_tip()

### Protocol
## 1 - add lithium acetate and ssDNA mix
LiOAc_ssDNA_transfer(multichannel_column_number)

## 2 - add PEG
PEG_transfer(multichannel_column_number) 

## 3 - transfer the DNA constructs from eppendorf tubes to the plate
DNA_transfer(DNA_vol, H2O_vol, transformants) 

## 4 - add the yeast cells to the plate
yeast_DNA(multichannel_column_number)

## 5 - heat shock
temp_mod_2.status
temp_mod_2.temperature

protocol.pause('Move plate from cold block on 3 to heat block on 9 for 40 minute heat shock')       # User must confirm to continue protocol
protocol.delay(minutes = time_block)

temp_mod_2.deactivate()                                                                             # Automatically deactivates after heat shock and protocol continues

## 6 - transfer content of 96-well plate to fresh 96-well
transfer_to_new(multichannel_column_number)

protocol.pause('Centrifuge plate at 2000 rmp for 10 minutes and return to deck position 5')         # User must confirm to continue protocol

## 7 - remove supernatant
supernatant(multichannel_column_number)

## 8 - add calcium chloride to make cells competent  
CaCl_addition(multichannel_column_number)

protocol.comment('Protocol complete!')

########################### OUTPUT FILE ENDS HERE ###################################
### New custom script output
## User input
filename = str(input("Please enter the name for your new script: ")) 

## .py extension on file
substring = ".py"
if substring in filename:   
    pass
else:           
    filename = filename + ".py"

## File writing 
with open(filename, "w") as new_file:                                   # Writes out chosen parameters in new file as comments and defines variables
    new_file.write("#Opentrons protocol\n")
    new_file.write("\n")
    new_file.write("### DNA volumes a is set to: " + str(DNA_vol) + "\n")
    new_file.write("DNA_vol = " + str(DNA_vol) + "\n")
    new_file.write("H2O_vol = " + str(H2O_vol) + "\n")
    new_file.write("\n")
    new_file.write("###Transformants is set to: " + str(transformants) + "\n")
    new_file.write("transformants = " + str(transformants) + "\n")
    new_file.write("multichannel_column_number = " + str(multichannel_column_number) + "\n")
    new_file.write("\n")
    new_file.write("###Temperature for heat shock is set to: " + str(temp_block) + "\n")
    new_file.write("temp_block = " + str(temp_block) + "\n")
    new_file.write("\n")
    new_file.write("###Time for heat shock is set to: " + str(time_block) + "\n")
    new_file.write("time_block = " + str(time_block) + "\n")
    new_file.write("\n")
    
    with open("YeastTransformationProtocol_API2.py") as f:              # Copies protocol into new file 
        for num, line in enumerate(f, 1):
          if num >= 53 and num <= 274:
            new_file.write(line)
    
    new_file.write("\n")     
    new_file.write("for line in protocol.commands():\n")                # The customised file in Opentrons_scripts folder is ready to be used on the Opentrons app
    new_file.write("    print(line)\n")  

