from uuid import UUID
from pathlib import Path

from nix_alien import helpers


def test_edit_file(monkeypatch):
    monkeypatch.setenv("EDITOR", "cat")
    assert helpers.edit_file(Path("/dev/null")).returncode == 0


def test_get_hash_for_program(monkeypatch):
    monkeypatch.setenv("HOME", "/home/nameless-shelter")
    assert helpers.get_hash_for_program("/home/nameless-shelter/abc") == UUID(
        "22e71c4d-8693-5b8e-867c-ccaf6d31389a"
    )
    assert helpers.get_hash_for_program("~/abc") == UUID(
        "22e71c4d-8693-5b8e-867c-ccaf6d31389a"
    )
    assert helpers.get_hash_for_program("/abc") == UUID(
        "24bdda4e-e28a-5a1c-92ff-6b988321616a"
    )
    assert helpers.get_hash_for_program("/./abc") == UUID(
        "24bdda4e-e28a-5a1c-92ff-6b988321616a"
    )
    assert helpers.get_hash_for_program("/xyz/../abc") == UUID(
        "24bdda4e-e28a-5a1c-92ff-6b988321616a"
    )


def test_get_cache_path(monkeypatch):
    monkeypatch.setenv("HOME", "/home/nameless-shelter")
    assert helpers.get_cache_path("/abc") == Path(
        "/home/nameless-shelter/.cache/nix-alien/24bdda4e-e28a-5a1c-92ff-6b988321616a"
    )

    monkeypatch.setenv("XDG_CACHE_HOME", "/")
    assert helpers.get_cache_path("/abc") == Path(
        "/nix-alien/24bdda4e-e28a-5a1c-92ff-6b988321616a"
    )


def test_get_dest_path(monkeypatch):
    monkeypatch.setenv("HOME", "/home/nameless-shelter")
    assert helpers.get_dest_path(
        destination=None,
        program="/abc",
        directory="bar",
        filename="foo.nix",
    ) == Path(
        "/home/nameless-shelter/.cache/nix-alien/24bdda4e-e28a-5a1c-92ff-6b988321616a/bar/foo.nix"
    )

    monkeypatch.setenv("XDG_CACHE_HOME", "/")
    assert helpers.get_dest_path(
        destination=None,
        program="/abc",
        directory="bar",
        filename="foo.nix",
    ) == Path("/nix-alien/24bdda4e-e28a-5a1c-92ff-6b988321616a/bar/foo.nix")

    assert helpers.get_dest_path(
        destination="/quux",
        program="/abc",
        directory="bar",
        filename="foo.nix",
    ) == Path("/quux/foo.nix")
