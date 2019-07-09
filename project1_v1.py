import numpy as np

import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord, get_moon, solar_system_ephemeris, get_sun 
from pytz import timezone
from astropy.time import Time

from astroplan import Observer
from astroplan import FixedTarget
from astroplan.plots import plot_airmass, plot_sky

def observer_function(name_of_the_observatory, name_timezone):
    return Observer.at_site(name_of_the_observatory, timezone=name_timezone)

def target_wanted(RA, DEC, name_target='Target', frame='icrs'):
    coordinates = SkyCoord(RA, DEC, frame=frame)
    return FixedTarget(name=name_target, coord=coordinates)

def targeting_moon(observe_time):
    coordinates_moon = get_moon(observe_time)
    coordinates_moon = coordinates_moon.icrs      
    return FixedTarget(name='Moon', coord=coordinates_moon)      

def targeting_sun(observe_time):
    coordinates_sun = get_sun(observe_time)
    coordinates_sun = coordinates_sun.icrs      
    return FixedTarget(name='Sun', coord=coordinates_sun)  


def main():
    name_of_the_observatory = str(input("\nType the name of the observatory, e.g.: subaru : "))
    name_timezone = str(input("Type the timezone e.g. US/Hawaii : "))
    time_str = str(input("Type the date and the time of observation in UTC e.g. 2000-06-30 23:30:00 : "))

    see_moon = str(input("Would you like to target the moon? [yes/no] ")) 
    how_many_targets = int(input("How many objects would you like to observe? "))

    observe_time = Time(time_str)
    
    #time window
    time = observe_time + np.linspace(-12, 12, 100)*u.hour
    to_be_plot = time.plot_date
    #print (to_be_plot)
    #exit()
    observer = observer_function(name_of_the_observatory,name_timezone)
    
    fig = plt.figure(figsize=(11,7))
    fig.subplots_adjust(hspace=0.5)
    #fig.subplots_adjust(wspace=0.5)
    #fig.subplots_adjust(hspace=0.3)

    sun = targeting_sun(observe_time)

    ax = plt.subplot(1, 2, 1)
    plot_airmass(sun, observer, observe_time,brightness_shading=True,style_kwargs={'color': 'r'}, min_airmass=0.5, max_airmass=3.5)
    plt.text(0.5, 0.9, 'Observatory: '+name_of_the_observatory+'\n Timezone: '+name_timezone, horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes)
    ax.set_title('Airmass')
    plt.legend(shadow=True, loc=2)
    
    ax = plt.subplot(1, 2, 2, projection='polar')
    plot_sky(sun, observer, observe_time,style_kwargs={'color': 'r'}) 
    ax.set_title('Position at time: '+time_str+'[UTC]\n \n') 


    if see_moon == "yes": 
        moon = targeting_moon(observe_time)

        ax = plt.subplot(1, 2, 1)
        plot_airmass(moon, observer, observe_time,brightness_shading=True, min_airmass=0.5,max_airmass=3.5)
        ax.set_title('Airmass')
        plt.legend(shadow=True, loc=2)

        ax = plt.subplot(1, 2, 2, projection='polar')
        plot_sky(moon, observer, observe_time) 
        ax.set_title('Position at time: '+time_str+'[UTC]\n \n')   
    else:
        pass            
    while how_many_targets > 0 :
        RA = str(input("Type the RA of your target e.g. 06h45m08.9173s : "))
        DEC = str(input("Type the DEC of your target e.g. -16d42m58.017s : ")) 	
        NAME = str(input("Type the name of your target : "))
        frame = str(input("Type the frame of your target e.g. icrs: "))

        target = target_wanted(RA, DEC, NAME, frame)
        
        ax = plt.subplot(1, 2, 1)
        plot_airmass(target, observer, observe_time,brightness_shading=True, min_airmass=0.5,max_airmass=3.5)
        ax.set_title('Airmass')
        plt.legend(shadow=True, loc=2)

        ax = plt.subplot(1, 2, 2, projection='polar')        
        plot_sky(target, observer, observe_time) 
        ax.set_title('Position at time: '+time_str+'[UTC]\n \n') 

        print()
        how_many_targets -= 1 
    
    plt.legend(shadow=True, loc=2)
    #plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    #ax = plt.gca()
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.75, box.height * 0.75])


    plt.tight_layout()
    plt.show()
main()   