{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          numpy
          networkx
          scipy
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          name = "forestcoll";
          buildInputs = [
            pythonEnv
          ];

          shellHook = ''
            echo "Envorinment $name"
            echo "$(python --version)"
          '';
        };
      }
    );
}
