# qwoqLab
Automatic "bomblab" solver with symbolic executions.'

![Alt text](/img/image.png)
*Example bomb from [CS:APP official website](https://csapp.cs.cmu.edu/3e/bomb.tar)*

Executed: `python3 qwoqLab.py bomb -F`

---
qwoqLab is automatic solver of CSAPP 'bomblab', which learns basic assembly and reversing techniques.
(Rotate `bomb` 180˚ to get `qwoq` ;D)


Binary bomb can be simulated, and solutions could be found by [symbolic execution](https://en.wikipedia.org/wiki/Symbolic_execution).

We used [`angr`](https://angr.io/) - one of the powerful binary analysis tools - to track and solve for variables, simulate the status of bomb.

---
## Usage
`python qwoqLab.py [OPTIONS] bomb`
```text
arguments:
bomb    Path to Bomb

options:
-h                          Help
-L, -l, --local             Patch binary for local execution
-S, -s, --stage <N...>      Solve specific stage (Hidden = 7)
-D, -d, --defuse            Defuse every stage (-S 1 2 3 4 5 6 7)
-A, -a, --answer            Write answer to text file (Every phase should solved)
-F, -f, --full              Do everything! (-L -D -A)
```

## Requirements
```text
angr==9.2.54
archinfo==9.2.54
claripy==9.2.54
colorama==0.4.6
pwntools==4.10.0
```