# Functional Specification for blockchain quadratic voting system

- [Functional Specification for blockchain quadratic voting system](#functional-specification-for-blockchain-quadratic-voting-system)
  - [1. Introduction](#1-introduction)
    - [1.1 Overview](#11-overview)
    - [1.2 Business Context](#12-business-context)
    - [1.3 Glossary](#13-glossary)
  - [2. General description](#2-general-description)
    - [2.1 Product/system functions](#21-productsystem-functions)
    - [2.2 User Characteristics and Objectives](#22-user-characteristics-and-objectives)
    - [2.3 Operational Scenarios](#23-operational-scenarios)
      - [**Use case 1**](#use-case-1)
      - [**Description**](#description)
      - [**Extensions**](#extensions)
      - [**Use case 2**](#use-case-2)
      - [**Description**](#description-1)
      - [**Extensions**](#extensions-1)
      - [**Use case 3**](#use-case-3)
      - [**Description**](#description-2)
      - [**Extensions**](#extensions-2)
      - [**Use case 4**](#use-case-4)
      - [**Description**](#description-3)
      - [**Extensions**](#extensions-3)
  - [| 2a       | Blockchain query failure. The system displays an error message and retries the query.                     |](#-2a--------blockchain-query-failure-the-system-displays-an-error-message-and-retries-the-query---------------------)
      - [**Use case 5**](#use-case-5)
      - [**Description**](#description-4)
      - [**Extensions**](#extensions-4)
      - [**Use case 6**](#use-case-6)
      - [**Description**](#description-5)
      - [**Extensions**](#extensions-5)
      - [**Use case 7**](#use-case-7)
      - [**Description**](#description-6)
      - [**Extensions**](#extensions-6)
      - [**Use case 8**](#use-case-8)
      - [**Description**](#description-7)
      - [**Extensions**](#extensions-7)
      - [**Use case 9**](#use-case-9)
      - [**Description**](#description-8)
      - [**Extensions**](#extensions-8)
      - [**Use case 10**](#use-case-10)
      - [**Description**](#description-9)
      - [**Extensions**](#extensions-9)
    - [2.4 Constraints](#24-constraints)
  - [3. Requirements](#3-requirements)
    - [3.1 Register/Login](#31-registerlogin)
    - [3.2 Quadratic Voting](#32-quadratic-voting)
    - [3.3 Election Management](#33-election-management)
    - [3.4 Vote Casting and Authentication](#34-vote-casting-and-authentication)
    - [3.5 Vote Counting and Result Display](#35-vote-counting-and-result-display)
    - [3.6 Privacy and Security Mechanisms](#36-privacy-and-security-mechanisms)
    - [3.7 Blockchain Integration](#37-blockchain-integration)
    - [3.8 User Roles and Permissions](#38-user-roles-and-permissions)
    - [3.9 Proposal Management](#39-proposal-management)
    - [3.10 Election Results](#310-election-results)
    - [3.11 Incentive Mechanism for Miners](#311-incentive-mechanism-for-miners)
    - [3.12 Data Management](#312-data-management)
    - [3.13 Optional Features](#313-optional-features)
  - [4. System Architecture](#4-system-architecture)
    - [4.1 System Architecture Diagram](#41-system-architecture-diagram)
  - [5. High-Level Design](#5-high-level-design)
    - [5.1 Context Diagram](#51-context-diagram)
    - [5.2 Data Flow Diagram](#52-data-flow-diagram)
    - [5.3 Class Diagram Draft](#53-class-diagram-draft)
  - [6. Preliminary Schedule](#6-preliminary-schedule)
    - [6.1 Project Plan Tasks](#61-project-plan-tasks)
    - [6.2 Requirements](#62-requirements)
    - [6.3 Gantt Chart](#63-gantt-chart)
  - [7 Appendix](#7-appendix)
    - [7.1 Reference](#71-reference)

----------

## 1. Introduction

### 1.1 Overview

Our project goal is to create a  quadratic voting system based on a custom blockchain, it is designed to use a centralized authentication service (like estoniaid), and a decentralized mining system. This will ensure a safe and clear environment for voting.

The system includes three dashboards:
- User dashboard: allows user to authenticate, view active elections, and vote using a quadratic voting mechanism
- Admin dashboard: allows administrators to create and manage elections, configure candidates, and monitor progress.
- Miner dashboard: allows miners to mine directly from the browser, monitoring mining status and verify accumulated rewards

The blockchain records votes and miner-coins in blocks validated by miners. Miners can start and control the mining process only from their dashboard, which evaluates the solution to the PoW (Proof of Work) and sends the valid block to the blockchain. When a miner completes a PoW, they get an amount x of miner-coins.

An election server (that is our representation and simplification of the estoniaid), manages centralized authentication and provides data about the elections such as candidate names, start / end dates etc. Finally a centralized treasury server should convert the rewards accumulated by miners into real money or whatever the country thinks is a suitable reward.

This approach makes the system accessible, secure, and decentralized, balancing technical complexity of the block chain with a nice user-friendly interface.

### 1.2 Business Context 


This system can be utilised by many european governments such as Italy. Italy claims to spend around 400 million euro per election. This includes costs for logistics, voting materials, personnel such as scrutineers and election officials, and also infrastructure. (see 7.1.3)

If we do some basic maths, Italy has 60 million people, let suppose that only 50 million pays taxes and votes as (note this fifty million is very optimistic as Italys voting turnout for both european and general elections has been declining since the 70's hitting a record low 48% as of 2024.(see 7.1.4) This is a part of a global trend across many developing countries (see 7.1.5), (400 / 50) = 8 this means each person within in Italy pays on average 8 euros for each election.

In general, traditional elections are resource-intensive, because they require physical assets, a manual verification process, and a lot of people. by transitioning to an online voting system, a lot of tax payer money can be saved. For instance:
- Elimination of physical materials: ballots, voting booths, and other supplies.
- Reduced personal costs: automation of processes like voter registration and tallying.
- Simplified logistics: no need to organize physical polling stations or transport materials.

This blockchain-based system offers immutable and clear data that aligns with the requirements of a democratic system. the implementation of this system could save millions of euros per election cycle, while increasing accessibility for citizens, including those with mobility challenges. 


### 1.3 Glossary

- **Blockchain**: a decentralised, immutable ledger.
- **Quadratic voting**: voting method that allows users to cast multiple votes with a quadratic cost increase.
- **Estonian e-id system**: digital identification technology used for voter verification.
- **PoW**: proof of work, a consensus mechanism.
- **Miner-coins**: it is the reward for the mine that complete the pow, (this can can’t be exchanged with other users, but just with the country that decides how much it is worth)

## 2. General description

### 2.1 Product/system functions 

The systems general functions are as follows:

- **User management**
  - Voter auth: enables voters to use a centralised service (e.g. estoniaid) for authentication.
  - Administrator access: gives admin the possibility to oversee elections, choose candidates names, and review results.
  - Miner auth: provides a dashboard for miners to participate in pow and get rewards.

- **Election management**
  - Election creation: admin can create elections and define candidates information.
  - Election data management: stores and manages election data securely in a centralised database.

- **Voting process**
  - Quadratic voting: implements quadratic voting logic, allowing voters to vote their favourite candidates, with the cost of votes increasing quadratically.
  - Voter submission: submits votes to the blockchain for immutable recording.
  - Real-time validation: validates votes using the blockchain.

- **Mining**
  - Mining interface: provides miners their dashboard to start mine from the browser.
  - Block validation: checks validity of votes and adds new blocks to the blockchain.
  - Rewards system: handle the rewards for the miners.

- **Blockchain integration**
  - Immutable Record: stores a ledger of votes and transactions (miner-coins)
  - Decentralized Validation: check the integrity of the voting process
  - Reward payout: it should utilise another server (Treasury Server) that convert miner-coin into a rewards (i.e. real money)

- **Transparency and monitoring**
  - User Dashboard: allows users to see available elections and track voting history.
  - Admin Dashboard: provides tools to monitor elections in progress and check the results.
  - Miner Dashboard: shows mining activity, rewards, payment history

By using both centralized user management and decentralized blockchain validation, this system offers an efficient, secure and cheaper alternative to traditional voting.

### 2.2 User Characteristics and Objectives


The user community for this project can be split into three categories: voters, miners and administrators. Each group has different characteristics, objectives and requirements while interacting with our system.

- **Voters**
  - Characteristics
    - Citizens eligible to vote
    - No technical knowledge of blockchain
    - Expected to have a basic digital understanding, such as ability to sign on to a website and ability to cast a vote
  - Objective
    - Vote in a user-friendly environment
    - View elections and their voting history
  - Requirements
    - Intuitive interface that guides users through the voting process
    - Assurance of security and anonymity during the process of voting
- **Miners**
  - Characteristics
    - Individual that participate in the validation process of the votes
    - Basic knowledge of the blockchain concepts is preferred
    - Should have computational resources required for mining.
  - Objective
    - Validate blocks to get the rewards
    - Track payouts
  - Requirements
    - A dedicate Miner Dashboard
    - Clear instructions and documentation for non experts to understand mining
- **Administrators**
  - Characteristics
    - Responsible for managing elections and monitoring system performance
    - Understanding of election process and system configuration expected.
    - Technical expertise would be good
  - Objective
    - Create and mange elections
    - Monitor election results
  - Requirements
    - A dedicated AdminDashboard

By meeting the needs of all these categories, the whole system ensures an inclusive experience for the voters, a good efficiency for the miners, and a smooth management of the admins.

### 2.3 Operational Scenarios


#### **Use case 1**
| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | User registration/login                                                                                                                        |
| **Goal in Context**        | Allow voters and admins to securely access the system with proper authentication.                                                              |
| **Scope & Level**          | System-wide, high-level authentication process.                                                                                                |
| **Preconditions**          | - System is online and operational. <br> - User has a valid digital ID. <br> - 2FA is enabled.                                                |
| **Success End Condition**  | The user is logged in and redirected to their role-specific dashboard.                                                                         |
| **Failed End Condition**   | The system denies access due to incorrect credentials or failed 2FA.                                                                           |
| **Primary Actors**         | Voter, Admin                                                                                                                                   |
| **Secondary Actors**       | Authentication service, Digital ID verification system.                                                                                       |
| **Trigger**                | A user navigates to the system login page and initiates the login process.                                                                    |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | The user enters their username and password.                                                               |
| 2        | The system validates the credentials against the government's database.                                    |
| 3        | The government system prompts for 2FA verification (authentication app).                                  |
| 4        | User provides the 2FA code.                                                                                |
| 5        | The system verifies the code and logs the user in.                                                        |
| 6        | The user is redirected to their dashboard.                                                                |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 1a       | Invalid credentials prompt the user to re-enter their credentials and display an error message (e.g., forgotten password). |
| 3a       | Failed 2FA verification denies access and prompts the user to retry.                                      |


----------

#### **Use case 2**
| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Create Election                                                                                                                                |
| **Goal in Context**        | Enable admins to create and configure elections with proposals.                                                                                |
| **Scope & Level**          | System-level; focused on admin functionality.                                                                                                  |
| **Preconditions**          | - Admin is logged into the system. <br> - System is operational and capable of creating election objects.                                       |
| **Success End Condition**  | The election is successfully created with all necessary configurations.                                                                        |
| **Failed End Condition**   | The election creation fails due to missing or invalid data.                                                                                   |
| **Primary Actors**         | Admin                                                                                                                                          |
| **Secondary Actors**       | System                                                                                                                                         |
| **Trigger**                | The admin navigates to the “create election” page.                                                                                            |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Admin selects “create election.”                                                                           |
| 2        | Admin inputs election details, including (e.g., title, description).                                       |
| 3        | The system validates the input.                                                                            |
| 4        | Upon success, the system creates the election and assigns a unique ID.                                     |
| 5        | Admin is notified that the election was created.                                                           |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 2a       | Missing/invalid data. The system highlights invalid fields and prevents submission until corrected.        |
| 4a       | Database error. The system logs the issue and notifies the admin of the failure.                           |

----------


#### **Use case 3**
| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Vote Allocation                                                                                                                                |
| **Goal in Context**        | Allow voters to allocate votes to proposals using quadratic voting.                                                                            |
| **Scope & Level**          | System-wide; voter interaction with the voting mechanism.                                                                                      |
| **Preconditions**          | - Voter is logged into the system. <br> - Election is active and open for voting.                                                              |
| **Success End Condition**  | The vote is successfully cast, and credits are deducted accordingly.                                                                           |
| **Failed End Condition**   | The vote allocation fails due to insufficient credits or system errors.                                                                        |
| **Primary Actors**         | Voter                                                                                                                                          |
| **Secondary Actors**       | Blockchain                                                                                                                                    |
| **Trigger**                | Voter selects a proposal and initiates vote allocation.                                                                                       |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Voter selects a proposal.                                                                                  |
| 2        | Voter inputs the number of votes to allocate.                                                              |
| 3        | The system calculates the quadratic cost and checks available credits.                                     |
| 4        | The system deducts credits and records the vote on the blockchain.                                         |
| 5        | The system notifies the voter of a successful allocation.                                                  |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 3a       | Insufficient credits. The system notifies the voter and prevents the vote allocation.                     |
| 4a       | Blockchain error. The system retries the transaction and logs the issue if unresolved.                    |

----------

#### **Use case 4**

| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Display Election Results                                                                                                                       |
| **Goal in Context**        | Provide real-time access to election results for voters and admins.                                                                            |
| **Scope & Level**          | System-wide; read-only interaction with the blockchain.                                                                                        |
| **Preconditions**          | - The election has ended. <br> - Votes are tallied and recorded on the blockchain.                                                             |
| **Success End Condition**  | Results are displayed accurately on the dashboard.                                                                                            |
| **Failed End Condition**   | Results fail to display due to system or blockchain errors.                                                                                    |
| **Primary Actors**         | Voter, Admin                                                                                                                                   |
| **Secondary Actors**       | Blockchain                                                                                                                                     |
| **Trigger**                | A user selects the "View Results" option for a completed election.                                                                            |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | User navigates to the election results page.                                                               |
| 2        | System queries the blockchain for vote tallies.                                                            |
| 3        | System calculates results based on tallied votes.                                                         |
| 4        | Results are displayed on the dashboard, categorized by proposals.                                          |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 2a       | Blockchain query failure. The system displays an error message and retries the query.                     |
----------
#### **Use case 5**


| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Reward Miners                                                                                                                                   |
| **Goal in Context**        | Reward miners for validating and storing blocks on the blockchain.                                                                              |
| **Scope & Level**          | System-level; interaction with miners and blockchain.                                                                                          |
| **Preconditions**          | - Miners successfully validate a block.                                                                                                        |
| **Success End Condition**  | Miners are rewarded for their contribution.                                                                                                    |
| **Failed End Condition**   | The system fails to process the reward due to a validation or payment error.                                                                   |
| **Primary Actors**         | Miner                                                                                                                                          |
| **Secondary Actors**       | Blockchain                                                                                                                                     |
| **Trigger**                | A block is successfully validated and added to the blockchain.                                                                                |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Miner validates a block of votes.                                                                          |
| 2        | System verifies the block's validity.                                                                      |
| 3        | System processes the reward for the miner.                                                                 |
| 4        | Miner receives confirmation of payment.                                                                    |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 2a       | Block validation failure. System rejects the block and logs the reason.                                   |
| 3a       | Payment processing error. System retries the payment and notifies the miner of the delay.                 |

----------

#### **Use case 6**


| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Monitor Election Progress                                                                                                                       |
| **Goal in Context**        | Allow admins to view the ongoing status of an election, including voter turnout and votes per proposal.                                         |
| **Scope & Level**          | Admin-level; read-only access to the election's progress data.                                                                                  |
| **Preconditions**          | - The election is active. <br> - Votes are being cast.                                                                                         |
| **Success End Condition**  | Admin sees real-time updates of voter activity and proposal statistics.                                                                         |
| **Failed End Condition**   | The system fails to fetch progress data or displays incorrect information.                                                                      |
| **Primary Actors**         | Admin                                                                                                                                          |
| **Secondary Actors**       | Blockchain                                                                                                                                     |
| **Trigger**                | Admin selects "View Election Progress" from their dashboard.                                                                                   |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Admin navigates to the election progress page.                                                             |
| 2        | System queries the blockchain for the current state of votes.                                              |
| 3        | System displays voter turnout and proposal statistics.                                                     |
| 4        | Admin monitors the data.                                                                                   |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 2a       | Data query failure. System logs the error and retries fetching the data.                                   |

----------

#### **Use case 7**


| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Detect and Prevent Fraudulent Activity                                                                                                          |
| **Goal in Context**        | Ensure the system detects and blocks unauthorized access or duplicate voting attempts.                                                         |
| **Scope & Level**          | System-level; focused on security and integrity.                                                                                               |
| **Preconditions**          | - The system is actively monitoring for anomalies.                                                                                             |
| **Success End Condition**  | Fraudulent activity is detected and prevented.                                                                                                 |
| **Failed End Condition**   | A fraudulent attempt bypasses detection mechanisms.                                                                                            |
| **Primary Actors**         | System                                                                                                                                         |
| **Secondary Actors**       | Voter, Admin                                                                                                                                   |
| **Trigger**                | The system detects an anomaly, such as multiple votes from the same ID or unauthorized login attempts.                                         |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | The system monitors login attempts and voting behavior.                                                    |
| 2        | An anomaly (e.g., duplicate votes) triggers a fraud detection algorithm.                                   |
| 3        | The system logs the activity and flags the account.                                                        |
| 4        | Admins are notified for further investigation.                                                             |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 3a       | False positive. Admin reviews the flagged activity and clears the account if legitimate.                  |

----------

#### **Use case 8**


| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Auditing and Transparency Reporting                                                                                                             |
| **Goal in Context**        | Allow third-party auditors to verify election integrity and transparency.                                                                      |
| **Scope & Level**          | System-level; focused on compliance and auditing.                                                                                              |
| **Preconditions**          | - The election has concluded. <br> - Blockchain data is accessible for auditing.                                                              |
| **Success End Condition**  | Auditors successfully verify election results and process integrity.                                                                           |
| **Failed End Condition**   | Auditors encounter inconsistencies or cannot access data.                                                                                      |
| **Primary Actors**         | Auditor                                                                                                                                         |
| **Secondary Actors**       | System, Admin                                                                                                                                   |
| **Trigger**                | An auditor requests access to election data for verification.                                                                                 |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Auditor submits an access request to the admin.                                                            |
| 2        | Admin grants temporary access with specific permissions.                                                   |
| 3        | Auditor queries blockchain data for proposals, votes, and results.                                         |
| 4        | System provides requested data for analysis.                                                               |
| 5        | Auditor confirms data integrity and submits a report.                                                      |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 3a       | Data integrity failure. Auditor identifies inconsistencies and reports the issue to the admin.                                                |

----------

#### **Use case 9**


| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | Proposal Management                                                                                                                            |
| **Goal in Context**        | Enable admins to manage proposals for an election by adding, editing, or removing them.                                                        |
| **Scope & Level**          | Admin-level; focuses on managing proposal-related data.                                                                                        |
| **Preconditions**          | - Admin is logged into the system. <br> - The election is in the setup phase.                                                                  |
| **Success End Condition**  | Proposals are updated successfully without errors.                                                                                             |
| **Failed End Condition**   | Proposal updates fail due to validation errors or system issues.                                                                               |
| **Primary Actors**         | Admin                                                                                                                                          |
| **Secondary Actors**       | None                                                                                                                                           |
| **Trigger**                | Admin selects "Manage Proposals" for a specific election.                                                                                     |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Admin navigates to the proposals page for an election.                                                     |
| 2        | Admin adds, edits, or removes proposals.                                                                   |
| 3        | System validates the changes.                                                                              |
| 4        | System updates the blockchain with the new proposal data.                                                 |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 3a       | Validation error. System highlights the issue (e.g., missing title) and prevents submission.                                                   |

----------

#### **Use case 10**


| **Section**                | **Details**                                                                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **Use Case**               | System Monitoring and Performance Analytics                                                                                                    |
| **Goal in Context**        | Provide real-time insights into system performance, such as server load and blockchain activity.                                                |
| **Scope & Level**          | Admin-level; focused on system health and performance metrics.                                                                                  |
| **Preconditions**          | - The system is operational.                                                                                                                   |
| **Success End Condition**  | Admins access a dashboard with live system performance data.                                                                                   |
| **Failed End Condition**   | Performance metrics are unavailable due to monitoring failures.                                                                                |
| **Primary Actors**         | Admin                                                                                                                                          |
| **Secondary Actors**       | System                                                                                                                                         |
| **Trigger**                | Admin selects "System Monitoring" from the dashboard.                                                                                         |

#### **Description**
| **Step** | **Action**                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 1        | Admin navigates to the monitoring dashboard.                                                               |
| 2        | System displays performance metrics, including server uptime and transaction rates.                                                             |
| 3        | Admin reviews the metrics for anomalies.                                                                   |

#### **Extensions**
| **Step** | **Branching Action**                                                                                       |
|----------|-----------------------------------------------------------------------------------------------------------|
| 2a       | Metric not available. System displays a notification indicating that specific metrics are temporarily unavailable.                              |

### 2.4 Constraints

Below is a list of possible constraints, that the design and implementation of the system is subjected to:
- **Blockchain Processing Speed**: PoW validation may affect vote processing time.
- **Performance**: Will the system handle concurrent voting sessions efficiently.
- **Security Requirements**: Data encryption and system resilience are critical.
- **Privacy Regulations**: Compliant with privacy standards to protect voter anonymity.
- **Regulatory Compliance**: the system must meet legal requirements of the country.


## 3. Requirements

### 3.1 Register/Login
*Description:* The user authenticates their identity with their digital ID. This shall be based on two-factor authentication.  
*Technical Issues:* Shall securely handle and store user credentials and encrypt all user credentials to prevent unauthorized access.

### 3.2 Quadratic Voting
*Description:* Voters submit votes with quadratic costs to balance the power of majorities and minorities. Example: Voting 3 times costs 3<sup>2</sup> = 9 credits.  
*Criticality:* Ensures fair representation while balancing majority influence with minority interest.  
*Technical Issues:* Calculation of quadratic costs correctly and real-time deduction of voter credits.

### 3.3 Election Management
*Description:* The administrators create elections and manage them by assigning unique IDs to allow multiple voting events simultaneously.  
*Technical Issues:* Avoiding conflict between elections and handling parallel events robustly.

### 3.4 Vote Casting and Authentication
*Description:* The voter securely casts the vote using the Estonian e-ID-based system.  
*Technical Issues:* Avoid unauthorized access and duplicate voting.

### 3.5 Vote Counting and Result Display
*Description:* Government dashboard is updated in real time.  
*Technical Issues:* Requires high security and speed for correct display.

### 3.6 Privacy and Security Mechanisms
*Description:* Blind signatures ensure the privacy of the voter.  
*Technical Issues:* Keeps anonymity but confirms authenticity of voter.

### 3.7 Blockchain Integration
*Description:* All votes are recorded securely on the blockchain. One block holds up to 50 votes. Blockchain verifies blocks to keep the data integrity and unchangeable.  
*Technical Issues:* Real-time block validation and seamless integration with the voting mechanism.

### 3.8 User Roles and Permissions
*Description:* The system shall have three user roles:
  - **Voters:** Can view proposals, assign votes, and submit choices.
  - **Admins:** Can create/manage voting events, add and remove proposals, and publish results.
  - **Miners:** Shall validate blocks and store transactions on the blockchain.  

*Technical Issues:* The system should use role-based access control to prevent unauthorized actions.

### 3.9 Proposal Management
*Description:* Admins can manage proposals - add, update, and remove. Proposals shall include:
- Title
- Description
- Total vote count.

### 3.10 Election Results
*Description:* The results are computed and published after the end of the election, which is the outcome of the votes stored in blockchain.  
*Technical Issues:* Computation of results correctly and transparently.

### 3.11 Incentive Mechanism for Miners
*Description:* Miners are incentivized with a Miner coin for the validation and storage of blocks.  
*Technical Issues:* Transparency in reward distribution and an auditable mechanism for the payments.

### 3.12 Data Management
*Description:* The system should store all data about voting events, proposals, votes, and blockchain transactions.  
*Technical Issues:* Data should be kept confidential but at the same time auditable.

### 3.13 Optional Features
*Real-time Progress Tracking:* Show real-time statistics of the ongoing voting (for example, votes per proposal) during an election to increase transparency.


## 4. System Architecture

### 4.1 System Architecture Diagram
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc-Z4AyWSsaqJNta6UWw77oMBQ3Ez-CC2iBM-Uk9ft4vNjYJbpf2xZr_QzfSBVJ7h20ur4djilRSFZrYHf4MSnOI3vrxjc2txbExja3N8mqXUIt9tWZPsBzJKc2X3I5bUALrP-Sug?key=OPlPKb10dUxl9KW5gTOyK8ZK)
## 5. High-Level Design
Blow with these two diagram made by using PlantUML, we show the whole system and its external entities (context diagram) and also showing the system data processing with Data Flow diagram
### 5.1 Context Diagram
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXf61zwNxB4nnUelCT-h6CM75kctfM8MGFfFo7GnSkKrg1K8CMT_HVNFZ6WDBE7VcdSkWo0JOOzQ8tqXLr4vmBG9BLB-GFzsEyYKirbON25rfUh5HQ3YaGfaaLLJrDeoxg7h3LuGBA?key=OPlPKb10dUxl9KW5gTOyK8ZK)

### 5.2 Data Flow Diagram
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXejHh9RpOm3B4or05zq-aew8axoL-MYKlBwn8PNFP8aj7CSnlNoTX0nPYrYDNRv9nYxNVMs2buogX8X8vU_g-tVWrd9X3yMGrkLBajUAZeuabf89OZhex-5tJOw3ag7R49bevYF2w?key=OPlPKb10dUxl9KW5gTOyK8ZK)

### 5.3 Class Diagram Draft
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeYBRotXR18piVzH3RrbyVW-MgRjFZP0LNqnR1BgDv1jU7oQVhzNoj_xS-fzVaoMYPFZRjhcz2F0sAX1DsM0Hx08KLNXdA6GkFkG6RXWa7DSDb2sAJ2PkYaZhLot9j9HC6nmXgrsA?key=OPlPKb10dUxl9KW5gTOyK8ZK)

## 6. Preliminary Schedule

### 6.1 Project Plan Tasks


| **Task**                | **Start Date** | **End Date**   | **Dependencies**            | **Description**                                |
|--------------------------|---------------|----------------|-----------------------------|-----------------------------------------------|
| **Requirement Analysis**     | 01-11-2024    | 15-11-2024     | None                        | Define system objectives.                     |
| **System Design**            | 16-11-2024    | 25-11-2024     | Requirement Analysis        | Define high-level system architecture.        |
| **Frontend Development**     | 13-01-2025    | 20-01-2025     | System Design               | Implement React.js dashboards.               |
| **Blockchain Development**   | 21-01-2025    | 31-01-2025     | System Design               | Build the Python blockchain for vote recording and mining operations. |
| **Server Development**       | 01-02-2025    | 07-02-2025     | Blockchain & Frontend Dev   | Develop Flask-based Election Server with SQLite database. |
| **Integration Testing**      | 08-02-2025    | 15-02-2025     | All Development Tasks       | Test the integration of frontend, backend, and blockchain components. |
| **Final Deployment**         | 16-02-2025    | 20-02-2025     | Integration Testing         | Deploy the system.                            |


### 6.2 Requirements
- **Frontend**: React.js for all the dashboards.
- **Backend**: Flask for the Election server.
- **Blockchain**: Python for developing the custom blockchain.
- **Database**: SQLite for election and user data storage.
- **Testing Tools**: such as Postman


### 6.3 Gantt Chart 
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdm6iDzMih8FsfQTgr_XEquoKj_X5GkPyxaOlkY6T8uDE-CJ7ID7pfVlJjomyP06Erru6V-NeczYtNUtyp60aQ8x2fcvviOiqryIjFK73MXSS04iT9Xa2mFrJwVVZH7FOhkU33Uog?key=OPlPKb10dUxl9KW5gTOyK8ZK)

## 7 Appendix

### 7.1 Reference

1. A 501(c)(3) tax-exempt, charitable organization, 1100 13th Street, NW, Suite 800, Washington, DC 20005-857-0044. **"Cost of Election," OpenSecrets.**  
   Available at: [https://www.opensecrets.org/elections-overview/cost-of-election?display=T](https://www.opensecrets.org/elections-overview/cost-of-election?display=T)

2. **"Reducing Voter Registration Costs in France | The Abdul Latif Jameel Poverty Action Lab,"** The Abdul Latif Jameel Poverty Action Lab (J-PAL), 2016.  
   Available at: [https://www.povertyactionlab.org/evaluation/reducing-voter-registration-costs-france](https://www.povertyactionlab.org/evaluation/reducing-voter-registration-costs-france)

3. Giorgia Bonamoneta. **"Quanto ha speso lo Stato per le elezioni politiche?"** Money.it, September 26, 2022.  
   Available at: [https://www.money.it/quanto-ha-speso-stato-per-elezioni-politiche](https://www.money.it/quanto-ha-speso-stato-per-elezioni-politiche)

4. **"Share of registered Italian electors who voted in general and European elections from 1946 to 2024"** Statista data and intelligence platform, August 30, 2024.  
   Available at: [https://www.statista.com/statistics/581392/elections-turnout-italy/](https://www.statista.com/statistics/581392/elections-turnout-italy/)

5. **"The Generational and Institutional Sources of the Global Decline in Voter Turnout"** by Filip Kostelka and André Blais, published in World Politics (Volume 73, Issue 4, October 2021).  
   Available at: [https://www.cambridge.org/core/journals/world-politics/article/abs/generational-and-institutional-sources-of-the-global-decline-in-voter-turnout/B9EB23098C2A905FECA7072C384CD34F?form=MG0AV3](https://www.cambridge.org/core/journals/world-politics/article/abs/generational-and-institutional-sources-of-the-global-decline-in-voter-turnout/B9EB23098C2A905FECA7072C384CD34F?form=MG0AV3)
