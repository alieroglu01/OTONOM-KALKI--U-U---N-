# GEREKLİ KÜTÜPHANELERİ İMPORT ETTİM
from pymavlink import mavutil
import time




# UDP ÜZERİNDEN BAĞLANTI KURDUM
master = mavutil.mavlink_connection('127.0.0.1:14550')  
master.wait_heartbeat()  
print("Baglanti kuruldu")




# ARM ETTİK
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)
master.motors_armed_wait()
print("Arm gerceklesti")




# MODU TAKEOFF OLARAK DEĞİŞTİRDİK
master.set_mode("TAKEOFF")
print("Mod TAKEOFF olarak değistirildi")




# TAKEOFF İŞLEMİNİ GERÇEKLEŞTİRDİK
altitude = 50  
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0, 0, 0, altitude
)
print(f"{altitude} metreye otonom kalkis başlatildi!")

# Kalkış irtifasına ulaşıldığını kontrol et
while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    current_altitude = msg.relative_alt / 1000.0  # mm cinsinden geliyor, metreye çevirdik
    print(f"Güncel irtifa: {current_altitude}m")

    if current_altitude >= altitude - 2:  # İrtifaya ulaştığında
        print(f"{altitude}m irtifaya ulasildi, hedef waypoint'e gidiliyor!")
        break
    time.sleep(1)




# MODU AUTO OLARAK DEĞİŞTİR VE WAYPOINT'E GİT
master.set_mode("AUTO")
print("Mod AUTO olarak değiştirildi, Waypoint'e geçiliyor...")




# WAYPOINT KONUMU (-35.36134393, 149.16121519, 60m)
lat, lon, alt = -35.36134393, 149.16121519, 60
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    0,
    0, 0, 0, 0,  # Boş parametreler
    lat, lon, alt
)
print(f"Waypoint'e gidiliyor: {lat}, {lon}, {alt}m")
