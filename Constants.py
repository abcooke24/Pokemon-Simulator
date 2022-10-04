import pandas as pd

class Data:
    movelist = pd.read_csv('PokemonSimulator\Gen1_Moves_update.csv')
    pokedex = pd.read_csv("PokemonSimulator\Kanto_Pokemon_100.csv")

class Type:
    """ Establishes all 16 (including "None") Pokemon types.
        This includes their offensive relationships: super-effective,
        not very effective, and not effective."""

    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    FIGHTING = "Fighting"
    POISON = "Poison"
    GROUND = "Ground"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    BUG = "Bug"
    ROCK = "Rock"
    GHOST = "Ghost"
    DRAGON = "Dragon"
    NONE = "None"

    type_set = set([NORMAL, FIRE, WATER, GRASS, ELECTRIC, ICE, FIGHTING, 
    POISON, GROUND, FLYING, PSYCHIC, BUG, ROCK, GHOST, DRAGON, NONE])

    # The type initially referenced in each set is the offensive type
    super_effective = {
        NORMAL : {},
        FIRE: {GRASS, ICE, BUG},
        WATER: {FIRE, GROUND, ROCK},
        GRASS: {WATER, GROUND, ROCK},
        ELECTRIC: {WATER, FLYING},
        ICE: {GRASS, GROUND, FLYING, DRAGON},
        FIGHTING: {NORMAL, ICE, ROCK},
        POISON: {GRASS},
        GROUND: {FIRE, ELECTRIC, POISON},
        FLYING: {GRASS, FIGHTING, BUG},
        PSYCHIC: {FIGHTING, POISON},
        BUG: {GRASS, PSYCHIC},
        ROCK: {FIRE, ICE, FLYING, BUG},
        GHOST: {PSYCHIC, GHOST},
        DRAGON: {DRAGON},
        NONE: {}
    }

    not_very_effective = {
        NORMAL : {ROCK},
        FIRE: {WATER, FIRE, ROCK, DRAGON},
        WATER: {WATER, GRASS, DRAGON},
        GRASS: {FIRE, GRASS, POISON, FLYING, BUG, DRAGON},
        ELECTRIC: {ELECTRIC, GRASS, DRAGON},
        ICE: {FIRE, WATER, ICE},
        FIGHTING: {POISON, FLYING, PSYCHIC, BUG},
        POISON: {POISON, GROUND, ROCK, GHOST},
        GROUND: {GRASS, BUG},
        FLYING: {ELECTRIC, ROCK},
        PSYCHIC: {PSYCHIC},
        BUG: {FIRE, FIGHTING, POISON, FLYING, GHOST},
        ROCK: {FIGHTING, GROUND},
        GHOST: {},
        DRAGON: {},
        NONE: {}
    }

    no_effect = {
        NORMAL : {GHOST},
        FIRE: {},
        WATER: {},
        GRASS: {},
        ELECTRIC: {GROUND},
        ICE: {},
        FIGHTING: {GHOST},
        POISON: {},
        GROUND: {FLYING},
        FLYING: {},
        PSYCHIC: {},
        BUG: {},
        ROCK: {},
        GHOST: {NORMAL},
        DRAGON: {},
        NONE: {}
    }

class Stats:
    "List of each type of stat used for calculation of EVs and stats"
    stat_list = ["HP", "Attack", "Defense", "SpAtk", "SpDef", "Speed"] 

class Statuses:
    """Establishes each possible status condition as a constant and categorizes
    each status move accordingly."""
    HEALTHY = "Healthy"
    PRZ = "Paralysis"
    PSN = "Poisoned"
    TOX = "Badly Poisoned"
    BRN = "Burn"
    SLP = "Sleep"
    FRZ = "Freeze"
    CON = "Confuse"

    # Types of statuses
    IMMOBILIZERS = [PRZ, SLP, FRZ, CON]
    CHIP_DAMAGE = [PSN, BRN, TOX]

class Natures:
    """List of all 25 natures in the game. Each "+" signifies a 10% increase
    to a stat whereas each "-" signifies a 10% decrease to it. "." implies no
    change to a stat. Five natures are neutral (they include a + and - in the 
    same stat), so they will include a "." in all indexes. More about natures
    can be found in the link below:
    https://bulbapedia.bulbagarden.net/wiki/Nature
    
    Stat Indexes:
        0 - Attack
        1 - Defense
        2 - Special Attack
        3 - Special Defense
        4 - Speed
    """
    HARDY = [".", ".",".", ".", "."]
    LONELY = ["+", "-", ".", ".", "."]
    ADAMANT = ["+", ".", "-", ".", "."]
    NAUGHTY = ["+", ".", ".", "-", "."]
    BRAVE = ["+", ".", ".", ".", "-"]
    BOLD = ["-", "+",".", ".", "."]
    DOCILE = [".", ".",".", ".", "."]
    IMPISH = [".", "+", "-", ".", "."]
    LAX = [".", "+",".", "-", "."]
    RELAXED = [".", "+",".", ".", "-"]
    MODEST = ["-", ".","+", ".", "."]
    MILD = [".", "-","+", ".", "."]
    BASHFUL = [".", ".",".", ".", "."]
    RASH = [".", ".","+", "-", "."]
    QUIET = [".", ".","+", ".", "-"]
    CALM = ["-", ".",".", "+", "."]
    GENTLE = [".", "-",".", "+", "."]
    CAREFUL = [".", ".","-", "+", "."]
    QUIRKY = [".", ".",".", ".", "."]
    SASSY = [".", ".",".", "+", "-"]
    TIMID = ["-", ".",".", ".", "+"]
    HASTY = [".", "-",".", ".", "+"]
    JOLLY = [".", ".","-", ".", "+"] 
    NAIVE = [".", ".",".", "-", "+"]
    SERIOUS = [".", ".",".", ".", "."]

    nature_list = [HARDY, LONELY, ADAMANT, NAUGHTY, BRAVE, BOLD, DOCILE,
    IMPISH, LAX, RELAXED, MODEST, MILD, BASHFUL, RASH, QUIET, CALM, GENTLE,
    CAREFUL, QUIRKY, SASSY, TIMID, HASTY, JOLLY, NAIVE, SERIOUS]

