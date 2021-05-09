{
  description = "Python package for controlling an ElGato key light";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs }:
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;

    leglight = pkgs.python38Packages.buildPythonPackage rec {
      pname = "leglight";
      version = "0.2.0";

      src = pkgs.python38Packages.fetchPypi {
        inherit pname version;
        sha256 = "41ab462fe12e2ec3e02ff29a00316f822b078c331c70bd36a635568bd1c4204a";
      };

      propagatedBuildInputs = with pkgs.python38Packages; [
        zeroconf
        requests
      ];

      doCheck = false;
    };

    elgato = pkgs.python38Packages.buildPythonPackage rec {
      pname = "PyElgato";
      version = "1.2.0";

      src = pkgs.python38Packages.fetchPypi {
        inherit pname version;
        sha256 = "7834d4c6dac7a1646b5238dcec187645d6cd4d8dc4e2f3f9e0d789a3bddd369c";
      };

      buildInputs = with pkgs.python38Packages; [
        setuptools-scm
        wheel
      ];

      propagatedBuildInputs = [
        leglight
      ];

      doCheck = false;
    };

  in {
    pipenvDevShell = pkgs.mkShell {
      buildInputs = with pkgs; [
        python38
        pipenv
      ];
    };

    defaultPackage.x86_64-linux = elgato;
  };
}
