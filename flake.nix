{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let pkgs = import nixpkgs { system = "x86_64-linux"; };
    in {
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = with pkgs; [
          nil
          nixpkgs-fmt

          dhall-json

          (pkgs.python3.withPackages (p: with p;[
            openai
            telethon
            pandas
          ]))
        ];
      };
    };
}
