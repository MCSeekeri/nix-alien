{ pkgs ? import
    (let p = "@nixpkgsPath@";
     in if builtins.pathExists p then builtins.storePath p
        else builtins.fetchTree "@nixpkgsRef@")
    { }
}:

let
  inherit (pkgs) buildFHSEnv;
in
buildFHSEnv {
  name = "${__name__}-fhs";
  targetPkgs = p: with p; [
    ${__packages__}
  ];
  runScript = "${__program__}";
}
