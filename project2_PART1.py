from astropy import units as u
from astropy.constants import sigma_sb, L_sun
import matplotlib as plt
import numpy as np
import matplotlib.pyplot as plt
 
def get_flux(temperature): 
    boltzmann_constant =  sigma_sb
    flux = boltzmann_constant * temperature**4
    return flux
def get_diameter_star(luminosity, temperature):
    flux = get_flux(temperature)
    diameter_of_star = (((luminosity)/(4*np.pi*flux))**(1/2))*2
    return diameter_of_star
def get_distance(diameter_of_aperature, wavelength, luminosity, temperature):
    diameter_star = get_diameter_star(luminosity,temperature)
    distance = ((diameter_star * diameter_of_aperature)/ (1.22*wavelength))
    return distance
def get_distance_in_pc(diameter_of_aperature,wavelength, luminosity,temperature):   
    return (get_distance(diameter_of_aperature,wavelength, luminosity,temperature)).to(u.parsec)

##### calculate the closest distance in parsecs that a supergiant luminosity class I, 
##### spectral type M star must be before it may be resolved by the WFIRST. 
temperature = 3400.0 *u.K #M
luminosity = 70000.0*L_sun #Class1
diameter_of_aperature = 2.4 * u.m
wavelength = 640*10**-9 *u.m

distance = get_distance_in_pc(diameter_of_aperature,wavelength,luminosity, temperature)

print('\n '+'#'*70 +'\n The closest distance in parsecs that a supergiant luminosity class I,\n',\
	'spectral type M star must be before it may be resolved by the WFIRST: \n \n',\
	distance,'\n','#'*70,'\n')
