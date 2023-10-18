import os
import argparse

import qwoqhelper
import qwoqpatcher
import qwoqsolver
import colorlog

import time

from colorama import Fore, Back, Style

STAGE_CNT = 7

PATCH_PREFIX = "Patched_"
ANSWER_PREFIX = "Answer_"

if __name__ == "__main__":
    qwoqhelper.print_title()

    parser = argparse.ArgumentParser(
        prog="qwoqLab", description=qwoqhelper.qwoqLab_description
    )
    parser.add_argument("bomb", help="Path to bomb")
    parser.add_argument(
        "-L",
        "-l",
        "--local",
        dest="local",
        action="store_true",
        help="Defuse network functionalities to execute bomb locally",
    )
    parser.add_argument(
        "-S",
        "-s",
        "--stage",
        dest="stage",
        type=int,
        nargs="+",
        choices=range(1, STAGE_CNT + 1),
        help="Stage to be solved",
    )
    parser.add_argument(
        "-D",
        "-d",
        "--defuse",
        dest="defuse",
        action="store_true",
        help="Defuse every stages (Same as -S 1 2 3 4 5 6 7)",
    )
    parser.add_argument(
        "-A",
        "-a",
        "--answer",
        dest="answer",
        action="store_true",
        help="Export answer text file - Should solve every stage",
    )
    parser.add_argument(
        "-F",
        "-f",
        "--full",
        dest="full",
        action="store_true",
        help="Generate local bomb, and solve all, and save the answers (Same as -L -D -A)",
    )

    parse = parser.parse_args()

    """
    Binary Patcher
    """
    if parse.full or parse.local:
        colorlog.log([Style.BRIGHT, Fore.GREEN], f"[***] Patching Binary...", "")

        patcher = qwoqpatcher.QwoqPatcher(
            parse.bomb,
            [
                "initialize_bomb",
                "explode_bomb",
            ],
        )

        patcher.patch(PATCH_PREFIX + parse.bomb)
        colorlog.log([Style.BRIGHT, Fore.GREEN], f"[***] Patched!", "")
    """
    Solver targets
    """
    solve_target = set()
    solve_answer = {}

    if parse.full or parse.defuse or parse.stage:
        if parse.full or parse.defuse:
            solve_target = set(range(1, STAGE_CNT + 1))
        else:
            solve_target = set(parse.stage)

        colorlog.log([Style.BRIGHT, Fore.GREEN], f"[***] Solving Bomb...", "")
        solver = qwoqsolver.QwoqSolver(parse.bomb)

        for stage in range(1, STAGE_CNT + 1):
            if stage in solve_target:
                start = time.time()
                solution = solver.get_answer(qwoqsolver.solve_targets[stage])

                if solution != None:
                    colorlog.log(
                        [Style.BRIGHT, Fore.BLUE],
                        f"[+ {stage}]",
                        solution,
                        f"{time.time() - start:.4f} s",
                    )
                    solve_answer[stage] = solution
                else:
                    colorlog.log(
                        [Style.BRIGHT, Fore.RED],
                        f"[- {stage}]",
                        "Answer NOT FOUND",
                        f"{time.time() - start:.4f} s",
                    )
                    solve_answer[stage] = ""
        colorlog.log([Style.BRIGHT, Fore.GREEN], f"[***] Solved!", "")
    """
    Answer Saving
    """
    if parse.full or (parse.answer and solve_target == set(range(1, STAGE_CNT + 1))):
        colorlog.log([Style.BRIGHT, Fore.GREEN], f"[***] Saving Answer...", "")
        with open(ANSWER_PREFIX + parse.bomb + ".txt", "w") as ans:
            for stage in range(1, STAGE_CNT + 1):
                if stage == 4:
                    ans.write(f"{solve_answer[stage]} DrEvil\n")
                else:
                    ans.write(f"{solve_answer[stage]}\n")
        colorlog.log([Style.BRIGHT, Fore.GREEN], f"[***] Saved!", "")
