from opentrons import simulate
metadata = {'apiLevel': '2.8'}
protocol = simulate.get_protocol_api('2.8')

## Modules                                                 
# Keeping DNA cool
temp_mod_1 = protocol.load_module('temperature module gen2',6)
temp_mod_1.set_temperature(4)                               

# Heat shock
temp_mod_2 = protocol.load_module('temperature module gen2',9)
temp_mod_2.set_temperature(42)                              

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
LiAc_ssDNA = reservoir['A2']
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

## Fucntions 

#######################Transformation mixture preperation
# LiOac and ssDNA transfer
def LiOAc_ssDNA_transfer(volume, column): 
    p300multi.pick_up_tip(tiprack_1['A1'])      ## Not sure about tips, are we reusing what we used for water?
    p300multi.mix(5,200,LiAc_ssDNA)
    p300multi.transfer(volume,
                         LiAc_ssDNA, 
                         plate_OG.columns()[:column], 
                         touch_tip=True,
                         blowout=True,
                         blowout_location='destination well',
                         new_tip='never') # Mix the ssDNA and LioAC properly in reservoir 
    p300multi.return_tip()

# PEG transfer 
def PEG_transfer(volume, column):   
    p300multi.pick_up_tip(tiprack_1['A1'])          ## Not sure about which tips we were going to use here                           
    p300multi.flow_rate.aspirate=40
    p300multi.flow_rate.dispense=40
    p300multi.transfer(volume,
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
# Transfers water and DNA from eppendorfs to the plate 9have to use block command for more control)
def DNA_transfer(DNAvolume, H20volume, well):        
    for i in range(well):
        p20single.pick_up_tip()
        if i <= 23:
            p20single.aspirate(H20volume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_1.wells()[i])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        elif i <= 47:
            p20single.aspirate(H20volume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_2.wells()[i-24])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        elif i <= 71:
            p20single.aspirate(H20volume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_3.wells()[i-48])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()
        else:
            p20single.aspirate(H20volume, water)
            p20single.aspirate(DNAvolume, eppendorfrack_4.wells()[i-72])
            p20single.blow_out(plate_OG.wells()[i])
            p20single.drop_tip()

##########################Yeast addition
def yeast_DNA(volume,column):
    p300multi.flow_rate.aspirate=50           
    p300multi.flow_rate.dispense=50      
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0])
        p300multi.transfer(volume,
                           yeast,
                           plate_OG.columns()[i],
                           trash=False,
                           touch_tip=True,
                           blow_out=True, 
                           blowout_location='destination well',
                           mix_after=(3,100),               
                           new_tip='never')    
        p300multi.return_tip()             

##########################User moves the plate from position 6 to the heat block (9)
#Heat shock step with user defined settings for temperature and duration 
        
##########################Trasfer contents of plate on the heat block (9) to a new plate(5)
def transfer_to_new(volume,column):
    plate_OG = temp_mod_2.load_labware('corning_96_wellplate_360ul_flat', 9)   # Updates position of plate_OG
    for i in range(column):
        p300multi.pick_up_tip(tiprack_2.columns()[i][0])
        p300multi.transfer(volume, 
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
    p300multi.well_bottom_clearance.aspirate = 3 #this value would need to be optimised (idk how high the pellet would go)
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
LiOAc_ssDNA_transfer(23, 12)

# 2
PEG_transfer(120, 12) 

# 3
DNA_transfer(5, 5, 45)

# 4
yeast_DNA(32,12)

# 5 - heat stuff
temp_mod_2.status
temp_mod_2.temperature

protocol.pause('Move plate from cold block on 6 to heat block on 9 for 40 minute heat shock')
protocol.delay(minutes=40)

#Opentron moves the contents of the plate from position 9 (heat shock) to the new plate at position 5. 

#want this at the end of the protocol - the module wont turn off at the end of the protocol or if it is cancelled/reset by itself 
temp_mod_2.deactivate() 

# 6
transfer_to_new(175,12)

# 7
protocol.pause('Centrifuge plate at 2000 rmp for 10 minutes and return to deck position 5')

# 8
supernatant(12)

# 9
CaCl_addition(12)

protocol.comment('Protocol complete!')

for line in protocol.commands(): 
        print(line)
