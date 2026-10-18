{
  pkgs ? (import ./compat.nix).pkgs,
  self ? (import ./compat.nix).flake,
}:

let
  shortRev = self.shortRev or "dirty";
  version = "0.1.0+git_${shortRev}";

  lock = builtins.fromJSON (builtins.readFile ./flake.lock);
  nixpkgsLocked = lock.nodes.${lock.nodes.root.inputs.nixpkgs}.locked;
  nixpkgsRef =
    let
      l = nixpkgsLocked;
      storePath = "path:${self.inputs.nixpkgs.outPath}";
    in
    if (l.narHash or null) != (self.inputs.nixpkgs.narHash or null) then
      storePath
    else if l.type == "github" then
      "github:${l.owner}/${l.repo}/${l.rev}?narHash=${l.narHash}"
    else if l.type == "tarball" then
      "tarball+${l.url}?narHash=${l.narHash}"
    else if l.type == "git" then
      "git+${l.url}?rev=${l.rev}"
    else if l.type == "path" then
      "path:${l.path}"
    else
      storePath;
in
{
  nix-alien = pkgs.callPackage ./nix-alien.nix {
    inherit version nixpkgsRef;
    nix-index =
      self.inputs.nix-index-database.packages.${pkgs.stdenv.hostPlatform.system}.nix-index-with-db;
    nix-index-database-src = self.inputs.nix-index-database;
    nixpkgs-src = self.inputs.nixpkgs;
  };

  # For backwards compat, may be removed in the future
  nix-index-update = pkgs.callPackage ./nix-index-update.nix { };
}
