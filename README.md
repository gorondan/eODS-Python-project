## eODS (enshrined Operator-Delegator Separation) - Python project

This project provides a minimal implementation of the core eODS concepts, including a 
simulation of delegation workflows — such as depositing, delegating, withdrawing, and updating 
the balances and quotas of delegators after applying rewards, penalties or slashing. Additionally, 
it includes mechanisms to validate the integrity and consistency of the generated data.

To address these requirements, a Simulator and a Tester were developed.

The Simulator operates in discrete 'ticks' over a defined number of iterations. During each tick, it generates new delegations, applies rewards, penalties, and slashings, and processes withdrawals.

The Tester evaluates the generated data to ensure its consistency and correctness.

### 1. Run the project

Source eODS/run.sh file to run the project:

`eODS/. run.sh`

### 2. Generate the project's documentation:

In `src`:
`pdoc --html --output-dir ../docs --force .`

### 3. Generate the project's class diagram:

In `src`:
`pyreverse --colorized -o jpg main.py simulator.py tester.py eods protocol`
