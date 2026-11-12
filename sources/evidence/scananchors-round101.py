"""基于函数锚点的引用扫描（避免线性反汇编失步）
用法: python scananchors.py <ver> <val>[:<span>] [val ...]
输出每条命中：函数起点、指令地址、指令、IMM/MEM 命中值
"""
import sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

from disasm import PATHS, load, va_to_off


def ranges(args):
    out = []
    for a in args:
        if ":" in a:
            b, s = a.split(":")
            out.append((int(b, 16), int(s, 16)))
        else:
            out.append((int(a, 16), 1))
    return out


def in_ranges(v, rr):
    return any(lo <= v < lo + span for lo, span in rr)


def main():
    ver = sys.argv[1]
    rr = ranges(sys.argv[2:])
    data, secs = load(PATHS[ver])
    starts = set()
    for vaddr, vsize, raddr, rsize in secs:
        if not (0x401000 <= vaddr < 0x800000):
            continue
        blob = data[raddr:raddr + rsize]
        for i in range(len(blob) - 2):
            if blob[i] == 0x55 and blob[i + 1] in (0x8B, 0x89) and blob[i + 2] in (0xEC, 0xE5):
                starts.add(vaddr + i)
    starts = sorted(starts)
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    print("=== %s === funcs=%d" % (ver, len(starts)))
    n = 0
    for idx, s in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else s + 0x400
        end = min(end, s + 0x2000)
        off = va_to_off(secs, s)
        if off is None:
            continue
        blob = data[off:off + (end - s)]
        for insn in md.disasm(blob, s):
            tags = []
            for op in insn.operands:
                if op.type == X86_OP_IMM and in_ranges(op.imm, rr):
                    tags.append("IMM=%08X" % op.imm)
                elif op.type == X86_OP_MEM and in_ranges(op.mem.disp, rr):
                    tags.append("MEM=%08X" % op.mem.disp)
            if tags:
                n += 1
                print("%08X [%08X]  %-8s %-30s  %s" % (
                    insn.address, s, insn.mnemonic, insn.op_str, " ".join(tags)))
    print("total", n)


if __name__ == "__main__":
    main()
