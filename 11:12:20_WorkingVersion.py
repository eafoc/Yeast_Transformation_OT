from opentrons import simulate
metadata = {'apiLevel': '2.8'}
protocol = simulate.get_protocol_api('2.8')

## Modules                                                  #### need to adjust where we will put these
# Keeping DNA at correct temperature
temp_mod_1 = protocol.load_module('temperature module gen2',6)
temp_mod_1.set_temperature(4)                               #sets tempertaure to 4°C. 

# Heat shock
temp_mod_2 = protocol.load_module('temperature module gen2',9)
temp_mod_2.set_temperature(42)                              

## Labware
# 96-well plates                                            #### need to adjust where we will put these
plate_OG = temp_mod_2.load_labware('corning_96_wellplate_360ul_flat', 4)
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

# Reagent reservoir -- I've left in the empty reservoirs for anyone to add to if they need
reservoir = temp_mod_1.load_labware('usascientific_12_reservoir_22ml', 3)
# = reservoir['A1']
LiAc_ssDNA = reservoir['A2']
# = reservoir['A3'] 
PEG = reservoir['A4']
# = reservoir['A5'] 
CaCl2 = reservoir['A6']
# = reservoir['A7'] 
yeast = reservoir['A8']
water = reservoir['A9'] 
# = reservoir['A10'] 
# = reservoir['A11'] 
waste = reservoir['A12']

## Pipettes
p300multi = protocol.load_instrument('p300_multi_gen2', 
                                   'right',
                                    tip_racks=[tiprack_1, tiprack_2])

p20single = protocol.load_instrument('p20_single_gen2', 
                                   'left',
                                    tip_racks=[tiprack_3])

#when you load an instrument you can only have one type of working pipette loaded at any one time. 
protocol.max_speeds['Z'] = 10

def DNATransfer(volH2O,volDNA):
    for i in range (12):
        p300multi.transfer(volH2O,reservoir['A9'], plate.columns[i],blow_out=True, new_tip='never') #transfer to daniella's code
    for i in range (eppendorfrack_1):
        p20single.transfer(volDNA,eppendorfrack_1[i],plate[0:24],blow_out=True, new_tip='always')
    for i in range (eppendorfrack_2):
        p20single.transfer(volDNA,eppendorfrack_2[i],plate[25:48],blow_out=True, new_tip='always')
    for i in range (eppendorfrack_3):
        p20single.transfer(volDNA,eppendorfrack_3[i],plate[49:72],blow_out=True, new_tip='always')
    for i in range (eppendorfrack_4):
        p20single.transfer(volDNA,eppendorfrack_4[i],plate[73:],blow_out=True, new_tip='always')
        
DNATransfer(5,5)
### Rough code for LiAc and PEG addition to 96 well plate --DANIELLA
## LiOac and ssDNA transfer
p300multi.distribute(23, LiAc_ssDNA,plate.columns()[:12],touch_tip=True, mix_before=(5,80),disposal_volume=24) # Mix the ssDNA and LioAC properly in reservoir

## PEG transfer                                               
p300multi.flow_rate.aspirate=50
p300multi.flow_rate.dispense=40

for i in range(12):                                  # note editable
    p300multi.transfer(120, PEG, plate.columns()[i], touch_tip=True, blow_out=True, blowout_location='destination well', new_tip='always',mix_after=(5,50))               
    # Mix the PEG, ssDNA, LioAC and plasmid DNA properly in 96-well plate

#This step entails:
#Pipette 175 ul of transformation mixture yeast into each well of the 96-well 
#PCR plate containing the DNA, aspirating gently several times to mix the DNA and
#yeast well.

##### Takes from the transformation mixture yeast with DNA well containg 
location_of_transformationmixture="A10"##unsure about location of transformation mixture. 
#This assumes the plate already has the DNA on it. 
#mix_after ensure it is well mixed with DNA. 
def transformationmixtureplusDNA(volume,column):
  for i in range(column):#Starting at zero means A1-A12 are being done. 
      p300multi.flow_rate.aspirate=50#to gently aspirate
      p300multi.flow_rate.dispense=50# and gently dispense.
      p300multi.transfer(volume,reservoir[location_of_transformationmixture],
                      plate.columns()[i],
                      touch_tip=True,
                       blow_out=True, blowout_location='destination well',
                       mix_after=(3,100),#mixing step afterwards
                       new_tip='always')#as DNA plasmid step being used,
                       #new tips all the time reccomended. 
	
# Step 11 - KIM

### Module for Heat shock
temp_mod_2 = protocol.load_module('Heat-Shock Module',4) #change the module position 
temp_mod_2.set_temperature(42) #sets tempertaure to 42°C. 

#this code is at Step 11 --> #Transfer the PCR plate to a 96-well thermocycler block set at 42°C for 40 mins

#User move the 96-well plate to the heat-block module at position X.  

temp_mod.temperature #confirm to the user that the heat block is at the right temperature
temp_mod.status #further confirm the status of the heat block - if it is steady at the target temp. good to go
temp_mod_2.set_block_temperature(42, hold_time_minutes=15, block_max_volume=355)

#User removes the 96-well plate from the heat block at the end of the desired time. 

#want this at the end of the protocol - the module wont turn off at the end of the protocol or if it is cancelled/reset by itself 
temp_mod.deactivate() 


#Transfers the transformed yeast cells from plate on heat block to new plate and centrifuge - EMILY

for i in range(1,11):
    p300multi.transfer(175, plate_OG.columns()[i],  ## plate on heat block name
                       plate.columns()[i],   ### new plate name
                       touch_tip=True, 
                       blow_out=True, blowout_location='destination well',
                       mix_after=(3,100),  ## Ensures mixture is homogenous
                       new_tip='always')
    
## User should centrifuge at 2000 rmp for 10 minutes and return to position ....

###Remove supernatant from the plate using multichannel pipette and add 200 ul of CaCl2 to each well - ELOISE

p300multi.flow_rate.aspirate = 25
p300multi.flow_rate.dispense = 150
p300multi.well_bottom_clearance.aspirate = 3
p300multi.pick_up_tip()
for i in range(12):
    p300multi.transfer(160, plate.columns()[i], waste, blow_out=True, blowout_location='destination well', new_tip='never')


p300multi.drop_tip()
p300multi.flow_rate.aspirate = 150
p300multi.flow_rate.dispense = 150
p300multi.well_bottom_clearance.dispense = 3
for x in range(12):
	p300multi.transfer(200, CaCl2, plate.columns()[x], blow_out=True, blowout_location='destination well', new_tip='always', mix_after=(7,100))
            


for line in protocol.commands(): 
        print(line)
