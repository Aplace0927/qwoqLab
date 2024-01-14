import angr
import claripy
import archinfo
from ctypes import c_int
from typing import Any

import logging

logging.getLogger("angr").setLevel("ERROR")

solve_targets = {
    1: "phase_1",
    2: "phase_2",
    3: "phase_3",
    4: "phase_4",
    5: "phase_5",
    6: "phase_6",
    7: "secret_phase",
}


class StringNotEqualHook(angr.SimProcedure):
    def run(self, s1, s2) -> int:
        i = 0
        while True:
            ch1 = self.state.memory.load(s1 + i, 1)
            ch2 = self.state.memory.load(s2 + i, 1)

            self.state.add_constraints(ch1 == ch2)
            if self.state.solver.eval(ch2) == 0:
                break
            i += 1

        return 0


class SscanfHook(angr.SimProcedure):
    def run(
        self,
        s,
        format_string,
    ) -> int:
 
        format_string = self.state.memory.load(format_string, 0x100)
        format_string = self.state.solver.eval(format_string, cast_to=bytes)
        format_string = format_string.split(b"\x00")[0].decode()

        formats = format_string.split(" ")

        ANSWER_STRING_MAXLEN = self.state.globals["ANSWER_STRING_MAXLEN"]

        answers = []
        for i, fmt in enumerate(formats):
            if fmt == "%d":
                answer = claripy.BVS(f"answer_sscanf_{i}", 32)
                addr = self.project.factory.cc().next_arg(self.arg_session, angr.types.parse_type("int*", arch=self.arch)).get_value(self.state)
                self.state.memory.store(addr, answer, endness=archinfo.Endness.LE)
            elif fmt == "%s":
                answer = claripy.BVS(f"answer_sscanf_{i}", 8 * ANSWER_STRING_MAXLEN)
                addr = self.project.factory.cc().next_arg(self.arg_session, angr.types.parse_type("char**", arch=self.arch)).get_value(self.state)
                self.state.memory.store(addr, answer)
            elif fmt == "%c":
                answer = claripy.BVS(f"answer_sscanf_{i}", 8)
                self.state.add_constraints(
                    claripy.Or(
                        claripy.And(
                            answer >= 0x20,
                            answer < 0x7F
                        ),
                        answer == 0x00
                    )
                )
                addr = self.project.factory.cc().next_arg(self.arg_session, angr.types.parse_type("char*", arch=self.arch)).get_value(self.state)
                self.state.memory.store(addr, answer)
            else:
                raise Exception(f"format not implemented: {fmt}")

            answers.append((answer, fmt))

        self.state.globals["sscanf_addr"] = self.state.solver.eval(s)
        self.state.globals["answer_sscanf"] = answers

        return len(formats)


class StrtolHook(angr.SimProcedure):
    def run(self) -> claripy.Bits:
        answer = claripy.BVS("answer_strtol", 64)
        self.state.globals["answer_strtol"] = (answer,)
        return answer


class NopHook(angr.SimProcedure):
    def run(self) -> None:
        return None


class QwoqSolver:
    RET_ADDR = 0xDEADBEEFCAFEBABE
    ANSWER_STRING_MAXLEN = 0x100

    def __init__(self, target_path):
        self.target_path = target_path

    def get_answer(self, phase) -> str | Any | None:
        proj = angr.Project(self.target_path, auto_load_libs=False)

        proj.hook_symbol("strings_not_equal", StringNotEqualHook())
        proj.hook_symbol("string_length", angr.SIM_PROCEDURES["libc"]["strlen"]())
        proj.hook_symbol("read_line", NopHook())
        proj.hook_symbol("phase_defused", NopHook())
        proj.hook_symbol("__isoc99_sscanf", SscanfHook())
        proj.hook_symbol("strtol", StrtolHook())

        answer_str = claripy.BVS("answer_string", 8 * self.ANSWER_STRING_MAXLEN)
        answer_str_addr = proj.loader.find_symbol("input_strings").rebased_addr

        initial_state = proj.factory.call_state(
            proj.loader.find_symbol(phase).rebased_addr,
            answer_str_addr,
            add_options={
                angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS,
                angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY,
            },
        )

        initial_state.memory.store(answer_str_addr, answer_str)

        for i in range(self.ANSWER_STRING_MAXLEN):
            answer_ch = initial_state.mem[answer_str_addr + i].byte.resolved
            initial_state.add_constraints(
                claripy.Or(
                    claripy.And(
                        answer_ch >= 0x20,
                        answer_ch < 0x7F
                    ),
                    answer_ch == 0x00
                )
            )

        initial_state.globals["answer_str"] = answer_str
        initial_state.globals["ANSWER_STRING_MAXLEN"] = self.ANSWER_STRING_MAXLEN

        initial_state.stack_push(self.RET_ADDR)

        simgr = proj.factory.simgr(initial_state)
        simgr.explore(
            find=self.RET_ADDR,
            avoid=proj.loader.find_symbol("explode_bomb").rebased_addr,
        )

        if len(simgr.found) == 0:
            return None

        state = simgr.found[0]

        if state.globals.get("answer_sscanf"):
            answer = state.globals["answer_sscanf"]
            _answer = []
            for x, fmt in answer:
                if fmt == "%d":
                    _answer.append(c_int(state.solver.eval(x)).value)
                elif fmt in ["%s", "%c"]:
                    _answer.append(
                        state.solver.eval(x, cast_to=bytes).split(b"\x00")[0].decode()
                    )
            answer = " ".join(map(str, _answer))

        elif state.globals.get("answer_strtol"):
            answer = state.globals["answer_strtol"]
            answer = state.solver.eval(answer[0])
        else:
            answer = state.globals["answer_str"]
            answer = state.solver.eval(answer, cast_to=bytes).split(b"\x00")[0].decode()

        return answer
