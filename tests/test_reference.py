"""Compile the C sketch extracted from the specification and verify output traces.
Requires Python 3 and a C11 compiler (CC, cc or clang); no Python packages.
"""
from pathlib import Path
import os, re, shutil, subprocess, tempfile, unittest
ROOT = Path(__file__).resolve().parents[1]

class ReferenceTests(unittest.TestCase):
    def test_traces(self):
        for remember in (False, True):
            with self.subTest(policy='remember' if remember else 'suppress'):
                self.check_traces(remember)

    def check_traces(self, remember):
        compiler = os.environ.get('CC') or shutil.which('cc') or shutil.which('clang')
        self.assertIsNotNone(compiler, 'A C11 compiler is required')
        doc = (ROOT/'docs/ULTIMATIC_MODE_SPECIFICATION_UNAMBIGUOUS.md').read_text()
        code = re.search(r'```c\n(.*?)```', doc, re.S).group(1)
        # (name, DIT closures, DAH closures, expected marks)
        cases = [
            ('T1 tap', [], [(0,40)], [('DAH',0,240)]),
            ('T2 hold', [], [(0,650)], [('DAH',0,240),('DAH',320,560),('DAH',640,880)]),
            ('T3 opposite', [(120,121)], [(0,40)], [('DAH',0,240),('DIT',320,400)]),
            ('T7 spacing', [(280,281)], [(0,40)], [('DAH',0,240),('DIT',320,400)]),
            ('T9 same mark', [], [(0,40),(120,160)], [('DAH',0,240)] + ([('DAH',320,560)] if remember else [])),
            ('T9 same space', [], [(0,40),(280,290)], [('DAH',0,240)] + ([('DAH',320,560)] if remember else [])),
            ('T10 held at boundary', [], [(0,40),(120,321)], [('DAH',0,240),('DAH',320,560)]),
            ('T11 coalescing', [(20,30),(120,130)], [(0,40)], [('DAH',0,240),('DIT',320,400)]),
            ('C1.1', [(10,80)], [(0,160)], [('DAH',0,240),('DIT',320,400)]),
            ('C1.2', [(200,210)], [(0,160)], [('DAH',0,240),('DIT',320,400)]),
            ('C1.3', [(250,260)], [(0,340)], [('DAH',0,240),('DIT',320,400)]),
            ('C1.4', [(300,410)], [(0,420)], [('DAH',0,240),('DIT',320,400)]),
            ('C1.5', [(300,470)], [(0,430)], [('DAH',0,240),('DIT',320,400)]),
            ('C2 D', [(300,520)], [(0,470)], [('DAH',0,240),('DIT',320,400),('DIT',480,560)]),
            ('C2a two taps', [(300,340),(380,420)], [(0,470)], [('DAH',0,240),('DIT',320,400)] + ([('DIT',480,560)] if remember else [])),
            ('T4 return', [(120,520)], [(0,900)], [('DAH',0,240),('DIT',320,400),('DIT',480,560),('DAH',640,880)]),
            ('T8 C3', [(10,160),(560,640)], [(20,1300)], [('DIT',10,90),('DAH',170,410),('DAH',490,730),('DIT',810,890),('DAH',970,1210),('DAH',1290,1530)]),
            ('T5 C2b', [(10,160),(560,640)], [(0,1250)], [('DAH',0,240),('DIT',320,400),('DAH',480,720),('DIT',800,880),('DAH',960,1200)]),
            ('T12 release boundary', [], [(0,320)], [('DAH',0,240)]),
            ('T12 press boundary', [], [(0,40),(320,321)], [('DAH',0,240),('DAH',320,560)]),
            ('T12 pending survives boundary release', [(280,320)], [(0,40)], [('DAH',0,240),('DIT',320,400)]),
        ]
        # Mirror timelines in unit coordinates using a separate small example:
        cases += [
            ('mirror T9 dit', [(0,20),(40,60)], [], [('DIT',0,80)] + ([('DIT',160,240)] if remember else [])),
            ('mirror T9 dit space', [(0,20),(120,130)], [], [('DIT',0,80)] + ([('DIT',160,240)] if remember else [])),
            ('mirror T10 dit', [(0,20),(120,161)], [], [('DIT',0,80),('DIT',160,240)]),
            ('mirror T11', [(0,20)], [(30,35),(50,55)], [('DIT',0,80),('DAH',160,400)]),
            ('mirror T7', [(0,20)], [(120,121)], [('DIT',0,80),('DAH',160,400)]),
        ]
        cases += [
            ('T11 same DAH coalesces', [], [(0,40),(120,140),(180,200)], [('DAH',0,240)] + ([('DAH',320,560)] if remember else [])),
            ('T11 same DIT coalesces', [(0,10),(20,30),(40,50)], [], [('DIT',0,80)] + ([('DIT',160,240)] if remember else [])),
            ('earlier opposite before same DAH', [(20,30)], [(0,40),(120,140)], [('DAH',0,240),('DIT',320,400)] + ([('DAH',480,720)] if remember else [])),
            ('earlier opposite before same DIT', [(0,10),(40,50)], [(20,30)], [('DIT',0,80),('DAH',160,400)] + ([('DIT',480,560)] if remember else [])),
            ('earlier same before opposite', [(180,190)], [(0,40),(120,140)], ([('DAH',0,240),('DAH',320,560),('DIT',640,720)] if remember else [('DAH',0,240),('DIT',320,400)])),
            ('C2a second tap in space', [(300,340),(440,450)], [(0,470)], [('DAH',0,240),('DIT',320,400)] + ([('DIT',480,560)] if remember else [])),
            ('mirror two DAH taps', [(0,450)], [(120,180),(240,280)], [('DIT',0,80),('DAH',160,400)] + ([('DAH',480,720)] if remember else [])),
        ]
        def expr(intervals):
            return ' || '.join(f'(now >= {a} && now < {b})' for a,b in intervals) or 'false'
        harness = '''\n#include <stdio.h>\nstatic unsigned nmarks;\nstatic uint64_t clock_now;\nvoid key_down(void) { printf("%u %llu %s\\n", nmarks++, (unsigned long long)clock_now, cycle_type == DIT ? "DIT" : "DAH"); }\nvoid key_up(void) { printf("end %llu\\n", (unsigned long long)clock_now); }\nstatic void reset(void) { state=IDLE;cycle_type=NONE;last_touched=NONE;pending_count=0;prev_dit=false;prev_dah=false;deadline=0;nmarks=0; }\nint main(void) {\n'''
        for i,(name,di,da,_) in enumerate(cases):
            policy = 'REMEMBER_CURRENT_TYPE' if remember else 'SUPPRESS_CURRENT_TYPE'
            harness += f'puts("CASE {i}"); reset(); reclosure_policy={policy}; for (uint64_t now=0;now<=1600;now++) {{clock_now=now;ultimatic_update(now,{expr(di)},{expr(da)});}}\n'
        # Test both pending flags before a decision, independent of current levels.
        for i,(first,second) in enumerate([('DIT','DAH'),('DAH','DIT')],len(cases)):
            harness += f'puts("CASE {i}");reset();accept_edge({first});accept_edge({first});accept_edge({second});for(uint64_t now=0;now<=800;now++){{clock_now=now;ultimatic_update(now,false,false);}}\n'
        harness += 'return 0;}\n'
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/'reference.c';binary=Path(td)/'reference'
            source.write_text('void key_down(void); void key_up(void);\n'+code+harness)
            subprocess.run([compiler,'-std=c11','-Wall','-Wextra','-Werror',str(source),'-o',str(binary)],check=True,capture_output=True,text=True)
            out=subprocess.run([str(binary)],check=True,capture_output=True,text=True).stdout
        actual={};current=None
        for row in out.splitlines():
            parts=row.split()
            if parts[0]=='CASE':current=int(parts[1]);actual[current]=[]
            elif parts[0]=='end':actual[current][-1].append(int(parts[1]))
            else:actual[current].append([parts[2],int(parts[1])])
        for i,(name,_,_,expected) in enumerate(cases):
            with self.subTest(name=name):self.assertEqual(actual[i],[list(x) for x in expected])
        self.assertEqual(actual[len(cases)],[['DIT',0,80],['DAH',160,400]])
        self.assertEqual(actual[len(cases)+1],[['DAH',0,240],['DIT',320,400]])
        print(f'Validated {len(cases)+2} timestamped traces with {"remember" if remember else "suppress"} current type.')

if __name__=='__main__':unittest.main()
