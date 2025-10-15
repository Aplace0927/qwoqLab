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

**2025-10-15 Update**:
Thanks to [@minsusun](https://github.com/minsusun) for pointing out necessary function to be patched!

Now we "manage" packages. Use `uv`.
*~~I didn't know what the package manager and why it is important when I first coded this 3 years ago~~*

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
