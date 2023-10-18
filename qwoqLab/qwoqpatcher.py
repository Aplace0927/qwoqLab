from pwn import *
import colorlog

from colorama import Fore, Back, Style

logging.getLogger("pwnlib").setLevel("ERROR")


class QwoqPatcher:
    def __init__(self, bomb_name: str, func_list: list[str]) -> None:
        self.__bomb = ELF(bomb_name)
        self.__func_list = func_list

    def __fetch_function_range(self, func_name: str) -> tuple[int, int]:
        """
        Fetch function's virtual address range.
        returns its starting address, and `ret` address as `tuple[int, int]`
        """
        vaddr_base = self.__bomb.symbols[func_name]

        init_size = 0x100
        disasm_str = ""

        if func_name != "explode_bomb":
            while "ret" not in disasm_str:
                disasm_str = self.__bomb.disasm(vaddr_base, init_size)
                init_size *= 2

            disasm_codes = disasm_str.splitlines()

            for code in disasm_codes:
                if "ret" in code:
                    vaddr_ret = int(code.split(":")[0].strip(), 16)

                    colorlog.log(
                        [Style.BRIGHT, Fore.YELLOW],
                        "[ ! ]",
                        f"Found function {func_name}",
                        f"{vaddr_base:#x} ~ {vaddr_ret:#x}",
                    )
                    return vaddr_base, vaddr_ret

        else:
            while f"{self.__bomb.symbols['exit']:x}" not in disasm_str:
                disasm_str = self.__bomb.disasm(vaddr_base, init_size)
                init_size *= 2

            disasm_codes = disasm_str.splitlines()

            for code in disasm_codes:
                if f"{self.__bomb.symbols['exit']:x}" in code:
                    vaddr_ret = int(code.split(":")[0].strip(), 16)

                    colorlog.log(
                        [Style.BRIGHT, Fore.YELLOW],
                        "[ ! ]",
                        f"Found function {func_name}",
                        f"{vaddr_base:#x} ~ {vaddr_ret:#x}",
                    )
                    return vaddr_base, vaddr_ret

    def patch(self, save_name: str) -> None:
        """
        Patch function with `nop`
        """
        for func in self.__func_list:
            vaddr_base, vaddr_ret = self.__fetch_function_range(func)
            self.__bomb.write(vaddr_base, asm("nop") * (vaddr_ret - vaddr_base))
            colorlog.log([Style.BRIGHT, Fore.CYAN], "[ + ]", f"Function {func} patched")

        self.__bomb.save(save_name)
