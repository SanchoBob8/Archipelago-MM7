# worlds/mm7/rom.py

from __future__ import annotations

import hashlib
import os
import pkgutil
from typing import Optional, TYPE_CHECKING

import settings
import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

if TYPE_CHECKING:
    from . import MegaMan7World


MM7_KNOWN_MD5: set[str] = set()
MM7_ROM_AUTH_TOKEN_OFFSET = 0x18FEC0
MM7_ROM_AUTH_TOKEN_SIZE = 32
MM7_ROM_AUTH_TOKEN_PREFIX = b"MM7AP"

def get_rom_auth_token(world: "MegaMan7World") -> bytes:
    player_name = world.multiworld.player_name[world.player]
    seed_name = world.multiworld.seed_name

    token_source = f"MM7|{seed_name}|{world.player}|{player_name}".encode("utf-8")
    digest = hashlib.sha256(token_source).digest()

    token = (
        MM7_ROM_AUTH_TOKEN_PREFIX
        + digest[: MM7_ROM_AUTH_TOKEN_SIZE - len(MM7_ROM_AUTH_TOKEN_PREFIX)]
    )

    assert len(token) == MM7_ROM_AUTH_TOKEN_SIZE
    return token


class MM7Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """Mega Man VII (USA) SNES ROM file."""

    rom_file: RomFile = RomFile("Megaman VII (USA).sfc")


class MM7ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man 7"
    patch_file_ending = ".apmm7"
    result_file_ending = ".sfc"

    hash = []

    procedure = [
        ("apply_bsdiff4", ["mm7_basepatch.bsdiff4"]),
        ("apply_tokens", ["mm7_tokens.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: "MegaMan7World", patch: MM7ProcedurePatch) -> None:
    basepatch = pkgutil.get_data(__name__, "data/mm7_basepatch.bsdiff4")
    if basepatch is None:
        raise FileNotFoundError(
            "Missing worlds/mm7/data/mm7_basepatch.bsdiff4. "
            "Build it from clean Mega Man 7 ROM -> ASM-patched ROM, then place it in data/."
        )

    patch.write_file("mm7_basepatch.bsdiff4", basepatch)

    auth_token = get_rom_auth_token(world)
    patch.write_token(APTokenTypes.WRITE, MM7_ROM_AUTH_TOKEN_OFFSET, auth_token)
    patch.write_file("mm7_tokens.bin", patch.get_token_binary())


def get_base_rom_path(file_name: str = "") -> str:
    if file_name:
        return file_name

    options = settings.get_settings()
    file_name = options["mm7_options"]["rom_file"]

    return Utils.user_path(file_name)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    cached_rom: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if cached_rom:
        return cached_rom

    path = get_base_rom_path(file_name)
    with open(path, "rb") as rom_file:
        rom = rom_file.read()

    rom = strip_snes_copier_header(rom)

    if MM7_KNOWN_MD5:
        md5 = hashlib.md5(rom).hexdigest()
        if md5 not in MM7_KNOWN_MD5:
            raise Exception(
                f"Supplied Mega Man 7 ROM does not match known MD5 hashes. Got {md5}."
            )

    setattr(get_base_rom_bytes, "base_rom_bytes", rom)
    return rom


def strip_snes_copier_header(rom: bytes) -> bytes:
    """Remove a 512-byte copier header if present.

    SNES ROM dumps are sometimes distributed with a 0x200-byte copier header.
    Most modern patch workflows expect headerless ROMs.
    """
    if len(rom) % 0x8000 == 0x200:
        return rom[0x200:]
    return rom
