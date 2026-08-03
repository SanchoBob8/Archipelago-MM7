# Mega Man 7

## Where is the options page?

The [player options page for this game](../player-options) contains all the options needed to configure and export a YAML file.

## What does randomization do to this game?

Mega Man 7 randomizes the following into the multiworld:

- Robot Master rewards
- Rush items
- Rush Plates
- Proto Man clues and the Proto Shield location
- Selected stage pickups and shop upgrades
- Wily Access Codes
- Wily boss rewards
- Consumable items

The game is completed by defeating Wily Capsule.

## How does Robot Master progression work?

All eight Robot Master stages are available from the beginning.

Defeating a Robot Master records the boss as defeated and sends the corresponding randomized reward location. The vanilla weapon is not awarded directly. Robot Master weapons are instead received through Archipelago.

When Boss Weakness Logic is enabled, the generated logic expects the player to possess an accepted weakness before defeating each boss. Exit Unit options may provide an alternate way to collect a stage check and leave without defeating the boss.

## How does Robot Museum work?

Robot Museum becomes available after defeating the configured number of Robot Masters. The default requirement is four.

When Skip Robot Museum is disabled, the player enters Robot Museum and must defeat Mash normally.

When Skip Robot Museum is enabled, Robot Museum is bypassed and the Mash location is checked automatically once the configured Robot Master requirement is reached.

When Boss Weakness Logic is enabled, Mash requires Danger Wrap unless Robot Museum is skipped.

## How do the Wily stages work?

Wily 1, Wily 2, and Wily 3 each have an independent Wily Access Code.

After receiving an access code, its corresponding Wily stage becomes selectable from the Wily box on the stage-select screen. **Available Wily stages can be cycled with L and R.**

Wily 1, Wily 2, and Wily 3 can be completed in any order.

Access to Wily 4 is configurable. It can require a selected number of:

- Cleared Wily stages
- Defeated Robot Masters
- Received Robot Master weapons

When Boss Weakness Logic is enabled, the Wily bosses and Wily Capsule also require their configured weaknesses.

## What Mega Man 7 items can appear in other players' worlds?

- Freeze Cracker
- Danger Wrap
- Thunder Bolt
- Junk Shield
- Slash Claw
- Wild Coil
- Noise Crush
- Scorch Wheel
- Rush Coil
- Rush Search
- Rush Jet
- Rush Plates
- Proto Man clues
- Proto Shield
- Hyper Bolt
- Exit Unit
- Hyper Rocket Buster
- Energy Balancer
- Beat
- Wily Access Codes
- 1-Ups
- E-Tanks
- W-Tanks
- S-Tanks

The Super Adaptor is not a randomized item. It is granted after receiving all four Rush Plates.

## What is considered a location check in Mega Man 7?

- Robot Master weapon rewards
- Proto Man meetings
- Proto Shield
- Rush item pickups
- Rush Plate pickups
- Hyper Bolt
- Exit Unit
- Hyper Rocket Buster
- Energy Balancer
- Beat rescue
- Mega Bolts
- Mega Health Capsule
- Intro Stage clear
- Mash / Robot Museum clear
- Wily 1, Wily 2, and Wily 3 boss rewards

Some items can be obtained either from an in-stage pickup or by purchasing them in Auto's shop. Both methods point to the same Archipelago location, so each location can only be checked once.

## When the player receives an item, what happens?

The effect of the item is applied immediately in-game.

Weapons and Rush items become usable as soon as they are received.

Rush Plates are tracked independently. Receiving all four Rush Plates grants the Super Adapter.

Consumables such as 1-Ups and tanks are added to the player's inventory.

Wily Access Codes unlock their corresponding Wily stages.

## What options are available?

### Boss Weakness Logic

When enabled, the generated logic expects the player to have an accepted weakness before defeating bosses.

### Starting Resources

The following starting resources are configurable:

- Lives
- Bolts
- E-Tanks
- W-Tanks
- S-Tanks

### Exit Unit Options

Exit Unit can optionally be used in stages that have not already been cleared.

Paid Exit Unit allows the player to use Exit Unit before receiving the actual item by spending the configured number of bolts.

Paid Exit Unit in Logic allows generated logic to consider that paid use as a valid method of leaving a stage.

### Wily 4 Requirement

Wily 4 can be configured to require:

- Cleared Wily stages
- Defeated Robot Masters
- Received Robot Master weapons

The required count for each requirement type is configurable.

### Skip Intro Stage

When enabled, the Intro Stage is skipped and its corresponding Archipelago location is checked automatically.

### Robot Museum Options

The number of Robot Masters required to access Robot Museum can be configured from one to eight.

When Skip Robot Museum is enabled, the stage and Mash fight are skipped, and the Mash location is checked automatically at the configured threshold.

## What is the goal?

The goal is to defeat Wily Capsule.

## Current limitations

This is a playable pre-release.

- The vanilla password system does not preserve Archipelago items, checks, or progression. Use emulator save states to resume a game after closing the emulator.
- On-screen item receive messages are not currently implemented.
- EnergyLink is not currently implemented.
- DeathLink is not currently implemented.
- The Wily stage letter on the stage-select screen may use a different color depending on the most recently displayed Robot Master name. This is a cosmetic issue.