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

def DNATransfer(volH2O, volDNA):
#    p300multi.pick_up_tip()
#    for i in range (12):
#        p300multi.transfer(volH2O, reservoir['A9'], plate_OG.columns()[i], blow_out=True, new_tip='never') #transfer to daniella's code
    for i in range (24):
        p20single.transfer(volDNA, eppendorfrack_1('A1'), plate_OG.columns('A1'), blow_out=True, new_tip='always')
 #   for i in range (24):
 #       p20single.transfer(volDNA, eppendorfrack_2[i], plate_OG[25:48], blow_out=True, new_tip='always')
 #   for i in range (24):
 #       p20single.transfer(volDNA, eppendorfrack_3[i], plate_OG[49:72], blow_out=True, new_tip='always')
 #   for i in range (24):
 #       p20single.transfer(volDNA, eppendorfrack_4[i], plate_OG[73:], ablow_out=True, new_tip='always')
        
DNATransfer(5,5)

### LiOac, ssDNA and PEG addition to 96 well plate 
## LiOac and ssDNA transfer
def LiOAc_ssDNA_transfer(volume, column):
  p300multi.distribute(volume, LiAc_ssDNA, plate_OG.columns()[:column], touch_tip=True, mix_before=(5,80), disposal_volume=24) # Mix the ssDNA and LioAC properly in reservoir 

LiOAc_ssDNA_transfer(23, 12)

## PEG transfer   
def PEG_transfer(volume, column):                                          
  p300multi.flow_rate.aspirate=50
  p300multi.flow_rate.dispense=40
  p300multi.distribute(volume, PEG, plate_OG.columns()[:column], touch_tip=True, disposal_volume=20, mix_after=(5,50))
#p300multi.pick_up_tip()

PEG_transfer(120, 12) 

def mixing(column):
    for x in range(column):
        p300multi.pick_up_tip()
        p300multi.mix(5, 50, plate_OG.rows()[x])
      
mixing(12)



#this code is at Step 11 --> #Transfer the PCR plate to a 96-well thermocycler block set at 42°C for 40 mins

#User move the 96-well plate to the heat-block module at position X.  

temp_mod_2.temperature #confirm to the user that the heat block is at the right temperature
temp_mod_2.status #further confirm the status of the heat block - if it is steady at the target temp. good to go

protocol.pause('Move plate to Heat deck for Heat Shock')
protocol.delay(minutes=40)

#User removes the 96-well plate from the heat block at the end of the desired time. 

#want this at the end of the protocol - the module wont turn off at the end of the protocol or if it is cancelled/reset by itself 
temp_mod_2.deactivate() 


#Transfers the transformed yeast cells from plate on heat block to new plate and centrifuge - EMILY
def transfer_to_new(volume,column):
  plate_OG = temp_mod_2.load_labware('corning_96_wellplate_360ul_flat', 9)   # Updates position of plate_OG to temperature block
  for i in range(column):
    p300multi.pick_up_tip(tiprack_2.columns()[i][0])          # Picks up and iterates through columns of tiprack_2
    p300_multi.transfer(volume, plate_OG.columns()[i],              # plate on heat block name
                       plate_new.columns()[i],                      # new plate name
                       touch_tip=True, 
                       blow_out=True, 
                       blowout_location='destination well',
                       mix_after=(3,100),                       # Ensures mixture is homogenous
                       new_tip='never')                     # Allows tips to be reused in later steps
    p300_multi.return_tip()                                 # Returns tips to be reused
  
transfer_to_new(175,12)

## User should centrifuge at 2000 rmp for 10 minutes and return to deck position 5

###Remove supernatant from the plate using multichannel pipette and add 200 ul of CaCl2 to each well - ELOISE
def supernatant(column):
    p300multi.flow_rate.aspirate = 25 #slowed aspiration rate to avoid disturbing the pellet
    p300multi.well_bottom_clearance.aspirate = 3 #this value would need to be optimised (idk how high the pellet would go)
    p300multi.flow_rate.dispense = 150
    p300multi.pick_up_tip()
    for i in range(column):
        p300multi.transfer(160, plate_new.columns()[i], waste, blow_out=True, blowout_location='destination well', new_tip='never')

def CaCl_addition(column):
    p300multi.drop_tip()
    p300multi.flow_rate.aspirate = 150
    p300multi.flow_rate.dispense = 150
    p300multi.well_bottom_clearance.dispense = 3
    for i in range(column):
        p300multi.transfer(200, CaCl2, plate_new.columns()[x], blow_out=True, blowout_location='destination well', new_tip='always', mix_after=(7,100))

supernatant(12)
CaCl_addition(12)

protocol.comment('Protocol complete!')

for line in protocol.commands(): 
        print(line)
