{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.python311Packages; [ django ] ++ [ pkgs.docker-compose ] ;
  }