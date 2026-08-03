# Mega Man 7 Archipelago World

Status: Playable pre-release

## Features

- Robot Master reward randomization
- All eight Robot Master stages available from the beginning
- Boss weakness logic option
- Rush Coil, Rush Search, and Rush Jet checks
- Rush Plate checks
- Super Adaptor granted after receiving all four Rush Plates
- Proto Man clue and Proto Shield checks
- Hyper Bolt, Exit Unit, Hyper Rocket Buster, and Energy Balancer checks
- Beat rescue check
- Mega Bolt and Mega Health Capsule checks
- Independent Wily 1, Wily 2, and Wily 3 Access Codes
- Wily 1, 2, and 3 can be completed in any order
- Configurable Wily 4 access requirement
- Wily boss reward checks
- Configurable starting resources
- Optional Intro Stage skip
- Configurable Robot Museum access requirement
- Optional Robot Museum skip
- Configurable Exit Unit behavior
- SNI client support

## Requirements

- Archipelago 0.6.7 or later
- A clean Mega Man 7 (USA) ROM
- An SNI-compatible SNES setup, such as BizHawk with Connector.lua

## Installation

1. Install `mm7.apworld` through the Archipelago Launcher.
2. Generate a game using a Mega Man 7 YAML.
3. Open the generated `.apmm7` patch through the Archipelago Launcher.
4. Run the patched ROM in your SNI-compatible emulator.
5. Connect through the Archipelago SNES Client.

See the included setup guide for detailed instructions.

## Current limitations

- The vanilla password system does not preserve Archipelago items, checks, or progression. Use emulator save states when stopping and resuming a game.
- On-screen item receive messages are not currently implemented.
- The Wily stage letter displayed on the stage-select screen may change color depending on the most recently displayed Robot Master name. This is cosmetic only.
- EnergyLink is not currently implemented.