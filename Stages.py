import pygame
import sys

class Protostar:
    def __init__(self, screen):
        self.screen = screen
    def get_mass(self):
        return 1.989*10**30

    def get_radius(self):
        return 10**11


class MainSequence:
    def __init__(self, screen):
        self.screen = screen

    def get_mass(self):
        return 1.989*10**30

    def get_radius(self):
        return 7*10**8


class RedGiant:
    def __init__(self, screen):
        self.screen = screen

    def get_mass(self):
        return 1.293*10**30

    def get_radius(self):
        return 1.5*10**11


class PlanetaryNebula:
    def __init__(self,screen):
        self.screen = screen

    def get_mass(self):
        return 1.293*10**30

    def get_radius(self):
        return 5*10**15


class WhiteDwarf:
    def __init__(self, screen):
        self.screen = screen

    def get_mass(self):
        return 9.945*10**29

    def get_radius(self):
        return 6*10**6

