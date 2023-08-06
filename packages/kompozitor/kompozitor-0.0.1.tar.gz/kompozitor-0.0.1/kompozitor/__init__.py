# import library ---------------------------------------------------------------
import pygame.midi
import time
import threading
from enum import Enum

# initize Pygame miDI ----------------------------------------------------------
pygame.midi.init()

players = []
def createPlayer():
    player = pygame.midi.Output( len(players) ) # device number in win10 laptop
    players.append(player)
    return player

# set the output device --------------------------------------------------------
defaultPlayer = createPlayer()
default_instrument = 0

def oktava(scale):
    global base
    base += scale

def p(duration = 1/4):
    time.sleep(tempo*duration)

class Note:
    def __init__(self, midi, instrument = None):
        self.midi = midi
        self.scale = 0
        self.duration = 1/4 if midi != -1 else 1 ## pauza je podrazumevano cela nota
        self.instrument = instrument
    def __call__(self, duration = None):
        global base
        global default_instrument
        if duration is None:
            duration = self.duration
        if self.midi != -1:
            defaultPlayer.set_instrument(default_instrument if self.instrument is None else self.instrument)
            defaultPlayer.note_on(scales[base+self.scale] + self.midi, volume)
        time.sleep(tempo*duration)
        if self.midi != -1:
            defaultPlayer.note_off(scales[base+self.scale] + self.midi, volume)
            defaultPlayer.set_instrument(default_instrument)
        ##play_note(self.midi, duration, default_instrument if self.instrument is None else self.instrument, self.scale)
    def __getitem__(self, scale):
        note = Note(self.midi)
        note.scale = self.scale
        note.duration = self.duration
        note.scale += scale
        return note
    def __getattr__(self, attr):
        note = Note(self.midi)
        note.scale = self.scale
        note.duration = self.duration
        
        if attr == "e" or attr == "eight" or attr == "osmina" or attr == "t8":
            note.duration = 1/8
        if attr == "q" or attr == "quarter" or attr == "cetvrt" or attr == "t4":
            note.duration = 1/2
        if attr == "h" or attr == "half" or attr == "pola" or attr == "t2":
            note.duration = 1/2
        if attr == "f" or attr == "full" or attr == "cela" or attr == "t1":
            note.duration = 1
        if attr == "o" or attr == "d" or attr == "dot":
            note.duration = self.duration * 3/2
        return note
    def __add__(self, other):
        note = Note(self.midi)
        note.scale = self.scale
        note.duration = self.duration
        #if(other is int)
        note.midi += other
        return note
    def __sub__(self, other):
        note = Note(self.midi)
        note.scale = self.scale
        note.duration = self.duration
        #if(other is int)
        note.midi -= other
        #if(other is Note)
        #    note.duration /= 2

        return note

# define all the constant values -----------------------------------------------

scales = [36, 48, 60, 72, 84, 96]
A = a = Note(-4)
As = Note(-3)
B = b = Note(-2)
C = do = Note(0)
Cs = Db = Note(1)
D = re = Note(2)
Ds = Eb = Note(3)
E = mi = Note(4)
F = fa = Note(5)
Fs = Gb = Note(6)
G = sol = Note(7)
Gs = Ab = Note(8)
A2 = la = Note(9)
As = Bb = Note(10)
B2 = si = Note(11)
C2 = do2 = Note(12)
D2 = re2 = Note(14)
E2 = mi2 = Note(16)
F2 = fa2 = Note(17)
G2 = sol2 = Note(19)
la2 = Note(21)
si2 = Note(23)
##p = P = Note(-1)

volume = 96
tempo = 1
base = 2

def kraj():
# close the device -------------------------------------------------------------
    global defaultPlayer
    defaultPlayer.close()
    del defaultPlayer
    pygame.midi.quit()

KLAVIR = Klavir = 1
EKLAVIR = 3
KSILOFON = Ksilofon = 14
HARMONIKA = Harmonika = 22
GITARA = Gitara = 25
EGITARA = EGitara = 29
ElektricnaGitara = elektricnaGitara = 28
VIOLINA = Violina = 41
VIOLA = Viola = 42
KONTRABAS = Kontrabas = 44
HARFA = Harfa = 47
TRUBA = Truba = 57
TROMBON = Trombon = 58
SAKSOFON = Saksofon = 66
OBOA = Oboa = 69
KLARINET = Klarinet = 72
Pikolo = PIKOLO = 73
Flauta = FLAUTA = 74

class Instrument():
    def __init__(self, value):
        self.player = value
        self.A = Note(-4, self.player)
        self.As = Note(-3, self.player)
        self.B = Note(-2, self.player)
        self.C = self.do = Note(0, self.player)
        self.Cs = self.Db = Note(1, self.player)
        self.D = self.re = Note(2, self.player)
        self.Ds = self.Eb = Note(3, self.player)
        self.E = self.mi = Note(4, self.player)
        self.F = self.fa = Note(5, self.player)
        self.Fs = self.Gb = Note(6, self.player)
        self.G = self.sol = Note(7, self.player)
        self.Gs = self.Ab = Note(8, self.player)
        self.A2 = self.la = Note(9, self.player)
        self.As = self.Bb = Note(10, self.player)
        self.B2 = self.si = Note(11, self.player)
        self.C2 = self.do2 = Note(12, self.player)
        self.D2 = self.re2 = Note(14, self.player)
        self.E2 = self.mi2 = Note(16, self.player)
        self.F2 = self.fa2 = Note(17, self.player)
        self.G2 = self.sol2 = Note(19, self.player)
        self.la2 = Note(21, self.player)
        self.si2 = Note(23, self.player)

def instrument(instrument):
    global default_instrument
    global defaultPlayer
    defaultPlayer.set_instrument(instrument)
    default_instrument = instrument
    
def napravi(instrument):
    instr = Instrument(instrument)
    return instr
