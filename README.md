# AI Flappy Bird

![Flappy Bird Demo](demo.gif)

Recreating the classic game Flappy Bird using Python and the Pygame library, along with the implementation of a bot that learns to play the game using the NeuroEvolution of Augmenting Topologies (NEAT) algorithm.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [NEAT Algorithm](#neat-algorithm)
- [Results](#results)

## Introduction

This project aims to recreate the iconic game Flappy Bird using Python and the Pygame library, while also integrating a bot that learns to navigate through the game using the NEAT algorithm. Flappy Bird is a simple yet addictive game where the player controls a bird, attempting to fly between pipes without hitting them.

## Installation

1. Clone this repository to your local machine
2. Install the required Python packages using: pip install pygame neat

## Usage

1. Run the main game script: python main.py
2. Watch the bot learn to play the game.

## NEAT Algorithm

We've employed the NEAT algorithm to train the AI bot in playing Flappy Bird. NEAT is a genetic algorithm designed to evolve artificial neural networks. It starts with a population of simple networks and iteratively generates new generations by combining and mutating the best-performing networks from the previous generation.

## Results

After training for 3 generations on average, the AI bot becomes optimized and capable of playing Flappy Bird with increasing proficiency. The learning curve and strategies adopted by the bot can be observed by running the provided demo.

---

