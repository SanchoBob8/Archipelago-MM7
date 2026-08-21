# Mega Man 7 Archipelago World

Status: Playable pre-release

## Features

* Robot Master reward randomization

* All eight Robot Master stages available from the beginning

* Boss weakness logic option

* Optional Robot Master Access Codes
  * One random Robot Master Access Code is granted at the start
  * Remaining Access Codes are added to the item pool
  * If used with Boss Weakness Logic, the relevant weapon to complete the first stage will also be granted at the start

* Optional Pickupsanity
  * Adds 72 fixed stage pickups as Archipelago locations
  * Includes Health Energy, Weapon Energy, Bolts, 1-Ups, and Tanks
  * Enemy drops are not included
  * Each pickup placement can only be checked once; later respawns behave normally

* Checkpoint selection for Robot Master stages
  * Use L/R on the stage-select screen to choose between the stage entrance, midpoint, and pre-boss checkpoint
  * Can optionally be enabled for uncleared stages

* Rush Coil, Rush Search, and Rush Jet checks

* Rush Plate checks

* Super Adaptor granted after receiving all four Rush Plates

* Proto Man clue and Proto Shield checks

* Hyper Bolt, Exit Unit, Hyper Rocket Buster, and Energy Balancer checks

* Beat rescue check

* Mega Bolt and Mega Health Capsule checks

* Independent Wily 1, Wily 2, and Wily 3 Access Codes

* Wily 1, 2, and 3 can be completed in any order

* Cleared Wily stages remain selectable for re-entry

* Configurable Wily 4 access requirement

* Wily boss reward checks

* Configurable starting resources

* Optional Intro Stage skip

* Configurable Robot Museum access requirement

* Optional Robot Museum skip

* Configurable Exit Unit behavior

* DeathLink support

* SNI client support

## Requirements

* Archipelago 0.6.7 or later
* A clean Mega Man 7 (USA) ROM
* An SNI-compatible SNES setup, such as BizHawk with Connector.lua

## Installation

1. Install `mm7.apworld` through the Archipelago Launcher.
2. Generate a game using a Mega Man 7 YAML.
3. Open the generated `.apmm7` patch through the Archipelago Launcher.
4. Run the patched ROM in your SNI-compatible emulator.
5. Connect through the Archipelago SNES Client.

See the included setup guide for detailed instructions.

## Current limitations

* The vanilla password system does not preserve Archipelago items, checks, or progression. Use emulator save states when stopping and resuming a game.
* On-screen item receive messages are not currently implemented.
* The Wily stage letter displayed on the stage-select screen may change color depending on the most recently displayed Robot Master name. This is cosmetic only.
* EnergyLink is not currently implemented.