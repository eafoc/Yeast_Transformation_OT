#Python editing code (14/12/2020)

## DNA:water ratio
# user input
DNA_vol = int(input("Please enter the plasmid DNA volume per transformation (µl): "))

#this should change accordingly with the DNA volume 
H2O_vol = 10 - DNA_vol


## Changes to number of columns
# user input
transformants = int(input("Please enter the number of transformants that will be produced: "))

#change
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
        
## temperatrue 
# user input : temp
temp_block = int(input("Please enter the temperature for heat shock: "))

# user input : heat block time
time_block = int(input("Please enter the time for heat shock (mins): "))


##############################################################

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

## Functions

#######################Transformation mixture preperation
# LiOac and ssDNA transfer
def LiOAc_ssDNA_transfer(column):
  p300multi.distribute(23,
                    LiOAc_ssDNA, 
                    plate_OG.columns()[:column], 
                    touch_tip=True,
                    mix_before=(5,200),                # Mix the ssDNA and LioAC properly in reservoir
                    disposal_volume=24,
                    trash=True)

# PEG transfer 
def PEG_transfer(column):   
    p300multi.pick_up_tip(tiprack_1['A2'])          ## Not sure about which tips we were going to use here                           
    p300multi.flow_rate.aspirate=40
    p300multi.flow_rate.dispense=40
    p300multi.transfer(120,
                         PEG,
                         plate_OG.columns()[:column],
                         touch_tip=True,
                         blow_out=True,
                         blowout_location='destination well',
                         mix_after=(5,50),
                         new_tip='never')
    p300multi.drop_tip()                        ## Chuck these tips as PEG is annoying

##########################Plasmid DNA
#should find a way to let the user know somehow what wells on the 96 plate corresponds to what eppendorf!!!
# Transfers water and DNA from eppendorfs to the plate have to use block command for more control)
def DNA_transfer(DNAvolume, H2Ovolume, well):        
    for i in range(well):
        p20single.pick_up_tip()
        if i <= 23:
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_1.wells()[i])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        elif i <= 47:
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_2.wells()[i-24])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        elif i <= 71:
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_3.wells()[i-48])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        else:
            p20single.aspirate(H2Ovolume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_4.wells()[i-72])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
            
#Identify what eppendorf tube for the DNA tansfer is in what well
def eppen_welllocation(well):
    for i in range(well):
        plate_position = str(plate_OG.wells()[i])
        plate_well = plate_position.split()[0]
        if i <= 23:
            eppendorf_rack = "slot 7"
            eppendorf_position = str(eppendorfrack_1.wells()[i])
            eppendorf_well = eppendorf_position.split()[0]
        elif i <= 47:
            eppendorf_rack = "slot 8"
            eppendorf_position = str(eppendorfrack_2.wells()[i-24])
            eppendorf_well = eppendorf_position.split()[0]
        elif i <= 71:
            eppendorf_rack = "slot 10"
            eppendorf_position = str(eppendorfrack_3.wells()[i-48])
            eppendorf_well = eppendorf_position.split()[0]
        else:
            eppendorf_rack = "slot 11"
            eppendorf_position = str(eppendorfrack_4.wells()[i-72])
            eppendorf_well = eppendorf_position.split()[0]
        output = f"The eppenddorf in {eppendorf_well} of {eppendorf_rack} is in well {plate_well} of the 96 well plate"
        protocol.comment(output)

#save all strings in array 

##########################Yeast addition
def yeast_DNA(column):
    p300multi.flow_rate.aspirate=50           
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
        p300multi.return_tip()             

##########################Trasfer from from plate on heat block (9) to new plate(5)
def transfer_to_new(column):
    plate_OG = temp_mod_2.load_labware('corning_96_wellplate_360ul_flat', 9)   # Updates position of plate_OG
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0])
        p300multi.transfer(175, 
                            plate_OG.columns()[i],              # change to position on heat block name
                            plate_new.columns()[i],                      
                            touch_tip=True, 
                            blow_out=True, 
                            blowout_location='destination well',
                            mix_after=(3,100),
                            new_tip='never')                    
        p300multi.return_tip()                                 

##########################Remove supernatant
def supernatant(column):
    p300multi.flow_rate.aspirate = 25 #slowed aspiration rate to avoid disturbing the pellet
    p300multi.well_bottom_clearance.aspirate = 3 #this value would need to be optimised to avoid aspirating the pellet
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

##########################CaCl2 addition
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
                           mix_after=(7,100))
        p300multi.drop_tip()

############# PROTOCOL #########################
# 1
LiOAc_ssDNA_transfer(multichannel_column_number)

# 2
PEG_transfer(multichannel_column_number) 

# 3
DNA_transfer(DNA_vol, H2O_vol, transformants) 

eppen_welllocation(transformants)

# 4
yeast_DNA(multichannel_column_number)

# 5 - heat shock
temp_mod_2.status
temp_mod_2.temperature

protocol.pause('Move plate from cold block on 3 to heat block on 9 for 40 minute heat shock')
protocol.delay(minutes = time_block)

temp_mod_2.deactivate() 

# 6
transfer_to_new(multichannel_column_number)

# 7
protocol.pause('Centrifuge plate at 2000 rmp for 10 minutes and return to deck position 5')

# 8
supernatant(multichannel_column_number)

# 9
CaCl_addition(multichannel_column_number)

protocol.comment('Protocol complete!')


##############################################

#saving 
filename = str(input("Please enter the name for your new script: ")) 

## Checks file will be .py file
substring = ".py"
if substring in filename:   ## if filename ends with .py all is good
    pass
else:           ## If not, will add it automatically
    filename = filename + ".py"

from itertools import islice

with open(filename, "w") as new_file:
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
	
	with open("14:12:20.py") as f:     ## This needs to be the name of this file!
        	for num, line in enumerate(f, 1):
          		if num >= 50 and num <= 209:
            		new_file.write(line)
			
	new_file.write("\n")     
	new_file.write("for line in protocol.commands():\n")
	new_file.write("    print(line)\n")  
