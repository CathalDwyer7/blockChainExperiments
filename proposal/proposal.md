# School of Computing CSC1049 Year 3 Project Proposal Form


Project Title: **Block-Chain Quadratic Voting System**

Student 1 Name: **Cathal Dwyer**
ID Number: 22391376

Student 2 Name: **Giuseppe Esposito**
ID Number: 22702705

Staff Member Consulted **Geoff Hamilton**

## Description

### Introduction
This project proposes a digital voting system utilising a custom blockchain to ensure transparency, security, and immutability. It implements a quadratic voting mechanism that balances voters' preferences with the intensity of their choices. The system manages multiple simultaneous votes and ensures voter authentication via Estonia's e-ID[^1] like system, verifying that only authorised users can vote.

### Project Goals
The main goals are to create a blockchain that records and verifies multiple votes as immutable transactions, implement quadratic voting to prevent minority domination, ensure secure authentication through a digital identity system, and manage multiple simultaneous elections accurately.

### Description of the System
The blockchain acts as the core infrastructure, with each block containing a hash of the previous block, anonymized voter IDs, the selected voting option, and the number of votes cast. It employs a Proof of Work (PoW) mechanism for decentralised validation of votes.
Quadratic voting allows voters to distribute their votes more flexibly, with the cost of votes increasing quadratically to discourage vote accumulation on a single option.
The authentication system uses a similar approach to that of Estonia's e-ID, including two-factor authentication (2FA), ensuring that only verified voters can access the system. Each vote is tagged with an ID to distinguish simultaneous elections, and all votes are stored immutably in the blockchain for final tallying.

### System Architecture
The government dashboard facilitates the creation, management, and monitoring of votes, displaying results in real-time. The voter dashboard allows users to view active elections, cast quadratic votes, and track their remaining credits. The system ensures high standards of security and privacy throughout the voting process.


## Division of Work
- Giuseppe: Focus on building the core blockchain, implementing the consensus mechanism (Proof of Work), managing transactions, and ensuring blockchain security. Giuseppe also handles the backend API for the blockchain.
- Cathal: Handle the authentication system, manage voter identity validation and security protocols, focus on data encryption, and ensure resilience against attacks. Cathal will also take care of any cryptographic signing of transactions and secure interaction with the blockchain.

By focusing on the deeper blockchain and security aspects, both of us will have substantial, challenging work that involves key aspects of both infrastructure and security.
We will work together on any task that proves to be especially difficult.

## Programming language(s)
- Python
- JS
- HTML-CSS

## Programming tools(s)
- Flask (web-tool)
- SQLite (data-base)
- unittest (testing)

## Learning Challenge 
- technology: Blockchain architecture, how decentralisation and consensus works,
- tools: restufullAPI with Flask, unittest module

## Hardware / software platform
- Linux

## Special hardware:
- None

[^1]: “ID-card,” e-Estonia, Jun. 10, 2024. https://e-estonia.com/solutions/estonian-e-identity/id-card/
