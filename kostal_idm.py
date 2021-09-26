#!/usr/bin/env python

import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

#-----------------------------------------
# Routine to read a float    
def ReadFloat(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,2,unit=unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
    return(result_FloatRegister)   
#----------------------------------------- 
# Routine to write float
def WriteFloat(client,myadr_dec,feed_in,unitid):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    builder.add_32bit_float( feed_in )
    payload = builder.to_registers() 
    client.write_registers(myadr_dec, payload, unit=unitid)

if __name__ == "__main__":  
    print ("##### START #####")
    try:
        #change the IP address and port:
        inverter_ip="192.168.1.5"
        inverter_port="1502"
        idm_ip="192.168.1.3"
        idm_port="502"  
        feed_in_limit=1000  
        #feed_in_limit=1     
        #no more changes required
        
        print ("##### KOSTAL IP: ", inverter_ip)
        inverterclient = ModbusTcpClient(inverter_ip,port=inverter_port)            
        inverterclient.connect()       
        
        consumptionbat = ReadFloat(inverterclient,106,71)
        print ("##### consumption battery: ", consumptionbat)
        consumptiongrid = ReadFloat(inverterclient,108,71)
        print ("##### consumption grid: ", consumptiongrid)
        consumptionpv = ReadFloat(inverterclient,116,71)
        print ("##### consumption pv: ", consumptionpv)
        consumption_total = consumptionbat + consumptiongrid + consumptionpv
        print ("##### consumption: ", consumption_total)
        
        #inverter = ReadFloat(inverterclient,100,71)
        #print ("##### inverter: ", inverter) 
        #inverter_phase1 = ReadFloat(inverterclient,156,71)
        #print ("##### inverter_phase1: ", inverter_phase1)  
        #inverter_phase2 = ReadFloat(inverterclient,162,71)
        #print ("##### inverter_phase2: ", inverter_phase2)  
        #inverter_phase3 = ReadFloat(inverterclient,168,71)
        #print ("##### inverter_phase3: ", inverter_phase3)   
        #inverter = inverter_phase1 + inverter_phase2 + inverter_phase3
        #print ("##### inverter: ", inverter)
        inverter = ReadFloat(inverterclient,172,71)
        print ("##### inverter: ", inverter)         
        
        #this is not exact, but enough for us :-)
        powerToGrid = round(inverter - consumption_total,1)
        print ("##### powerToGrid: ", powerToGrid)   
        
        battery = ReadFloat(inverterclient,200,71)
        print ("##### battery: ", battery)
        if battery > 0.1:
            print ("##### battery: discharge")
            powerToGrid = -1    
        
        inverterclient.close()       
        
        #feed in must be above our limit
        feed_in = powerToGrid;
        if feed_in > feed_in_limit:
            print ("##### feed-in reached: ", feed_in)               
            feed_in = feed_in/1000
        else:
            print ("##### send ZERO: ", feed_in)  
            feed_in = 0
        
        print ("##### iDM IP: ", idm_ip)
        idmclient = ModbusTcpClient(idm_ip,port=idm_port)            
        idmclient.connect()        
       
        WriteFloat(idmclient,74,feed_in,1)
            
        #read from iDM
        idmvalue = ReadFloat(idmclient,74,1)
        print ("##### iDM: ", idmvalue)
            
        idmclient.close()   
        
        print ("##### END #####")
        
    except Exception as ex:
        print ("ERROR :", ex)    
        
    
