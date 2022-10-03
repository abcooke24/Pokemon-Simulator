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

    # Moves that inflict status conditions based on movelist
    SLP_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'SLP Inflict']['Name'].tolist()
    PRZ_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ Inflict']['Name'].tolist()
    TOX_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'TOX Inflict']['Name'].tolist()
    PSN_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'PSN Inflict']['Name'].tolist()
    CON_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'Confuse Inflict']['Name'].tolist()

    # Moves that affect stats based on movelist
    ATK_DROP = Data.movelist.loc[Data.movelist['Effect'] == 'ATKdrop']['Name'].tolist() + ["Growth"]
    ATK_BOOST = Data.movelist.loc[Data.movelist['Effect'] == 'ATKboost']['Name'].tolist()
    DEF_DROP = Data.movelist.loc[Data.movelist['Effect'] == 'DEFdrop']['Name'].tolist()
    DEF_DROP_2 = Data.movelist.loc[Data.movelist['Effect'] == 'DEFdrop2']['Name'].tolist()
    DEF_BOOST = Data.movelist.loc[Data.movelist['Effect'] == 'DEFboost']['Name'].tolist()
    DEF_BOOST_2 = Data.movelist.loc[Data.movelist['Effect'] == 'DEFboost2']['Name'].tolist()
    SPATK_BOOST = ["Growth"]
    SPDEF_BOOST_2 = Data.movelist.loc[Data.movelist['Effect'] == 'SpdefBoost2']['Name'].tolist()
    SPEED_DROP = Data.movelist.loc[Data.movelist['Effect'] == 'Speed Drop']['Name'].tolist()
    SPEED_BOOST_2 = Data.movelist.loc[Data.movelist['Effect'] == 'SPEEDboost2']['Name'].tolist()
    CRIT_BOOST = ["Focus Energy"]

    STATUS_INFLICT = SLP_INFLICT + PRZ_INFLICT + PSN_INFLICT + TOX_INFLICT
    STAT_BOOST = ATK_BOOST + DEF_BOOST + DEF_BOOST_2 + SPATK_BOOST + SPDEF_BOOST_2 + SPEED_BOOST_2
    STAT_DROP = ATK_DROP + DEF_DROP + DEF_DROP_2 + SPEED_DROP

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

class SecondaryEffects:
    """ Establishes all of the moves with secondary effects. Many of these
    effects are the chance that something (stat drop, flinch, status, etc)
    will occur."""
    # moves w/chance to flinch
    FLINCH_10 = Data.movelist.loc[Data.movelist['Effect'] == 'Flinch10']['Name'].tolist()
    FLINCH_20 = Data.movelist.loc[Data.movelist['Effect'] == 'Flinch20']['Name'].tolist()
    FLINCH_30 = Data.movelist.loc[Data.movelist['Effect'] == 'Flinch30']['Name'].tolist()
    FLINCH_CHANCE = FLINCH_10 + FLINCH_20 + FLINCH_30

    # moves w/chance to inflict a status condition
    BRN_10 = Data.movelist.loc[Data.movelist['Effect'] == 'BRN10']['Name'].tolist() + ["Tri Attack"]
    FRZ_10 = Data.movelist.loc[Data.movelist['Effect'] == 'FRZ10']['Name'].tolist() + ["Tri Attack"]
    PRZ_10 = Data.movelist.loc[Data.movelist['Effect'] == 'BRN10']['Name'].tolist() + ["Tri Attack"]
    PRZ_30 = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ30']['Name'].tolist()
    PSN_30 = Data.movelist.loc[Data.movelist['Effect'] == 'PSN30']['Name'].tolist()
    PSN_40 = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ40']['Name'].tolist()
    CON_10 = Data.movelist.loc[Data.movelist['Effect'] == 'Confuse10']['Name'].tolist()
    CON_20 = Data.movelist.loc[Data.movelist['Effect'] == 'Confuse20']['Name'].tolist()
    STATUS_INFLICT_CHANCE = BRN_10 + FRZ_10 + PRZ_10 + PRZ_30 + PSN_30 + PSN_40

    # moves w/chance to drop the opponent's stats
    ATTACK_DROP_10 = Data.movelist.loc[Data.movelist['Effect'] == 'AttackDrop10']['Name'].tolist()
    SPDEF_DROP_10 = Data.movelist.loc[Data.movelist['Effect'] == 'SpdefDrop10']['Name'].tolist()
    SPEED_DROP_10 = Data.movelist.loc[Data.movelist['Effect'] == 'SpeedDrop10']['Name'].tolist()
    STAT_DROP_CHANCE = ATTACK_DROP_10 + SPDEF_DROP_10 + SPEED_DROP_10

    # moves that affect the user's HP in some way
    RECOIL = Data.movelist.loc[Data.movelist['Effect'] == 'Recoil']['Name'].tolist()
    ABSORB = Data.movelist.loc[Data.movelist['Effect'] == 'Absorb']['Name'].tolist()
    CRASH = Data.movelist.loc[Data.movelist['Effect'] == 'Crash']['Name'].tolist()

    # moves w/high chance to crit
    HIGH_CRIT = Data.movelist.loc[Data.movelist['Effect'] == 'High-Crit']['Name'].tolist()

    # moves that span multiple turns
    RECHARGE = Data.movelist.loc[Data.movelist['Effect'] == 'Recharge']['Name'].tolist()
    THRASH_LIKE = Data.movelist.loc[Data.movelist['Effect'] == 'Thrash-Like']['Name'].tolist()
    TWO_TURN = Data.movelist.loc[Data.movelist['Effect'] == '2Turn']['Name'].tolist()
    CONSECUTIVE = Data.movelist.loc[Data.movelist['Effect'] == 'SpeedDrop10']['Name'].tolist()

    # moves involving multiple hits or chip damage
    TWO_HIT = Data.movelist.loc[Data.movelist['Effect'] == '2Hit']['Name'].tolist()
    MULTI_HIT = Data.movelist.loc[Data.movelist['Effect'] == 'Multi-Hit']['Name'].tolist()
    TRAP = Data.movelist.loc[Data.movelist['Effect'] == 'Trap']['Name'].tolist()

    # move(s) with higher priority
    PRIORITY_1 = Data.movelist.loc[Data.movelist['Effect'] == 'Priority1']['Name'].tolist()