# Benchmarks

The benchmarks use TSP instances from [TSPLIB](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html), with the [tsplib95](https://github.com/rhgrant10/tsplib95) package for parsing problem data.  
To keep the repository lightweight, only 10 representative test cases are included.

## Structure
```text
benchmarks/
│
├── results/          # Benchmark results
│   ├── {problem-1}/  # Results for problem 1
│   ├── {problem-2}/  # Results for problem 2
│   ...
│   └── {problem-k}/  # Results for problem k
├── testcase/
│   ├── optimal/      # Optimal solutions for test cases
│   └── problems/     # TSPLIB problem instances
├── algos_bench.py    # Benchmark runner
└── Benchmarks.md
```

## Running benchmarks

After installing the required dependencies as described in the [README](../README.md), run:

```bash
# Run all algorithms 
$ python ./benchmarks/algos_bench.py all

## Run the specific algorithm
$ python ./benchmarks/algos_bench.py christofides
$ python ./benchmarks/algos_bench.py double_tree
$ python ./benchmarks/algos_bench.py nearest_addition
$ python ./benchmarks/algos_bench.py nearest_neighbor
$ python ./benchmarks/algos_bench.py nearest_insertion
$ python ./benchmarks/algos_bench.py cheapest_insertion
$ python ./benchmarks/algos_bench.py farthest_insertion
```

## Results

The benchmark results are printed to the command line:

```txt
Running ChristofidesAlgo on 10 problem(s)...
[   a280   ] distance =      2816.00, optimal =    2579.00, ratio = 1.0919, time =  0.5037s
[  att48   ] distance =     11441.00, optimal =   10628.00, ratio = 1.0765, time =  0.0211s
[  att532  ] distance =     30713.00, optimal =   27686.00, ratio = 1.1093, time =  6.6069s
[  bayg29  ] distance =      1737.00, optimal =    1610.00, ratio = 1.0789, time =  0.0059s
[ berlin52 ] distance =      8229.00, optimal =    7542.00, ratio = 1.0911, time =  0.0140s
[  brg180  ] SKIPPED (classified as TSP, not MetricTSP)
[ burma14  ] distance =      3448.00, optimal =    3323.00, ratio = 1.0376, time =  0.0011s
[  ch150   ] distance =      7075.00, optimal =    6528.00, ratio = 1.0838, time =  0.0890s
[   gr96   ] distance =     59403.00, optimal =   55209.00, ratio = 1.0760, time =  0.0343s
[ulysses22 ] distance =      7448.00, optimal =    7013.00, ratio = 1.0620, time =  0.0012s

Done. Reports saved under: C:\...\Python-Metric-TSP\benchmarks\results
```

After the benchmark completes, detailed reports for each problem and algorithm are saved in the `results/` folder.

For example:

```txt
┌─────────────────────────────────────────────────────────────┐
│ Problem   : bayg29                                          │
│ TSP_Type  : MetricTSP                                       │
│ Algorithm : ChristofidesAlgo                                │
│ Distance  : 1737.0000                                       │
│ Optimal   : 1610.0000                                       │
│ Ratio     : 1.0789                                          │
│ Time      : 0.0059s                                         │
├─────────────────────────────────────────────────────────────┤
│ Tour:                                                       │
│  1 —→ 28 —→  6 —→ 12 —→  5 —→  9 —→  3 —→ 29 —→ 26 —→ 21 —→ │
│  2 —→ 20 —→ 10 —→ 13 —→  4 —→ 15 —→ 18 —→ 14 —→ 22 —→ 17 —→ │
│ 11 —→ 19 —→ 25 —→  7 —→ 23 —→ 27 —→  8 —→ 16 —→ 24 —→ 1     │
└─────────────────────────────────────────────────────────────┘
```

## How to add a new test case

First, download the desired test case from [TSPLIB TSP](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/tspindex.html). This example uses `u159`.

<img src="../assets/images/Step1.png" width="50%">

After downloading and extracting the archive, place `u159.tsp` in `testcase/problems/`.

<img src="../assets/images/Step2.png" width="50%">


Remove the EOF line from `u159.tsp` so that it can be parsed correctly by `tsplib95`.

<img src="../assets/images/Step3.png" width="50%">

Next, create `u159.opt` in `testcase/optimal/`. Find the optimal solution for `u159` on [TSPLIB Optimal Solutions](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/TSP-BEST.html) and put it in `u159.opt`.

<img src="../assets/images/Step4.png" width="50%">


Finally, run the desired benchmark algorithm:

```bash
$ python ./benchmarks/algos_bench.py christofides
```

The new test case should then appear in the benchmark results:

```txt
Running ChristofidesAlgo on 11 problem(s)...
[   a280   ] distance =      2816.00, optimal =    2579.00, ratio = 1.0919, time =  0.5312s
[  att48   ] distance =     11441.00, optimal =   10628.00, ratio = 1.0765, time =  0.0219s
[  att532  ] distance =     30713.00, optimal =   27686.00, ratio = 1.1093, time =  6.1203s
[  bayg29  ] distance =      1737.00, optimal =    1610.00, ratio = 1.0789, time =  0.0029s
[ berlin52 ] distance =      8229.00, optimal =    7542.00, ratio = 1.0911, time =  0.0093s
[  brg180  ] SKIPPED (classified as TSP, not MetricTSP)
[ burma14  ] distance =      3448.00, optimal =    3323.00, ratio = 1.0376, time =  0.0006s
[  ch150   ] distance =      7075.00, optimal =    6528.00, ratio = 1.0838, time =  0.1303s
[   gr96   ] distance =     59403.00, optimal =   55209.00, ratio = 1.0760, time =  0.0426s
[   u159   ] distance =     45664.00, optimal =   42080.00, ratio = 1.0852, time =  0.1045s
[ulysses22 ] distance =      7448.00, optimal =    7013.00, ratio = 1.0620, time =  0.0015s

Done. Reports saved under: C:\...\Python-Metric-TSP\benchmarks\results
```

```
┌───────────────────────────────────────────────────────────────────────┐
│ Problem   : u159                                                      │
│ TSP_Type  : MetricTSP                                                 │
│ Algorithm : ChristofidesAlgo                                          │
│ Distance  : 45664.0000                                                │
│ Optimal   : 42080.0000                                                │
│ Ratio     : 1.0852                                                    │
│ Time      : 0.1045s                                                   │
├───────────────────────────────────────────────────────────────────────┤
│ Tour:                                                                 │
│   1 —→ 159 —→   2 —→   4 —→   5 —→ 153 —→ 152 —→   7 —→   8 —→   9 —→ │
│  10 —→  11 —→  13 —→  14 —→  15 —→  16 —→  17 —→  18 —→  19 —→  20 —→ │
│  21 —→  23 —→  22 —→  24 —→  25 —→  27 —→  26 —→  28 —→  29 —→  30 —→ │
│  31 —→  32 —→  33 —→  34 —→  35 —→  36 —→  38 —→  39 —→  40 —→  41 —→ │
│  42 —→  43 —→  44 —→  45 —→  46 —→  47 —→  48 —→  49 —→  50 —→  51 —→ │
│  52 —→  75 —→  74 —→  76 —→  77 —→  73 —→  71 —→  70 —→  69 —→  68 —→ │
│  67 —→  66 —→  65 —→  64 —→  62 —→  61 —→  60 —→  59 —→  58 —→  57 —→ │
│  56 —→  55 —→  53 —→  54 —→  63 —→  72 —→  78 —→  79 —→  80 —→  81 —→ │
│  82 —→  83 —→  84 —→  85 —→  86 —→  97 —→  98 —→  99 —→ 100 —→ 101 —→ │
│ 102 —→ 103 —→ 104 —→ 105 —→ 106 —→ 107 —→  95 —→  96 —→  87 —→  88 —→ │
│  89 —→  94 —→  90 —→  91 —→  92 —→  93 —→ 119 —→ 120 —→ 121 —→ 122 —→ │
│ 123 —→ 114 —→ 115 —→ 116 —→ 117 —→ 118 —→ 109 —→ 108 —→ 110 —→ 111 —→ │
│ 112 —→ 113 —→ 125 —→ 126 —→ 127 —→ 128 —→ 129 —→ 124 —→ 130 —→ 131 —→ │
│ 132 —→ 134 —→ 133 —→ 136 —→ 135 —→  37 —→ 138 —→ 137 —→ 139 —→ 140 —→ │
│ 141 —→ 142 —→ 143 —→ 144 —→ 145 —→  12 —→ 146 —→ 147 —→ 149 —→ 148 —→ │
│ 150 —→ 151 —→   6 —→ 154 —→ 155 —→ 158 —→ 157 —→ 156 —→   3 —→ 1      │
└───────────────────────────────────────────────────────────────────────┘
```

## Approximation ratios

|Problem | Nearest Neighbor | Nearest Addition | Nearest Insertion | Cheapest Insertion | Farthest Insertion | Double Tree | Christofides |
|:---------:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| a280      | 1.2520| 1.4118| 1.2001| 1.1660| 1.1644| 1.3823| 1.0919|
| att48     | 1.1775| 1.3385| 1.1201| 1.0700| 1.0636| 1.3102| 1.0765|
| att532    | 1.2560| 1.4077| 1.2285| 1.1704| 1.0885| 1.3420| 1.1093|
| bayg29    | 1.2547| 1.3758| 1.0807| 1.1466| 1.0391| 1.3727| 1.0789|
| berlin52  | 1.2096| 1.3526| 1.1990| 1.1900| 1.0764| 1.3410| 1.0911|
| brg180    | 9.1590|60.9436| 3.1897| 1.2410| 1.6718|     ✕|      ✕|
| burma14   | 1.2218| 1.2058| 1.0108| 1.0108| 1.0000| 1.1478| 1.0376|
| ch150     | 1.1605| 1.4104| 1.2384| 1.1857| 1.0515| 1.2888| 1.0838|
| gr96      | 1.2299| 1.3455| 1.2804| 1.2702| 1.0801| 1.3639| 1.0760|
| ulysses22 | 1.3090| 1.2072| 1.1072| 1.0719| 1.0000| 1.1979| 1.0620|


## Notes

Although `EUC_2D` represents Euclidean distances, TSPLIB rounding may cause some instances to violate the triangle inequality. These instances are still treated as Metric TSP instances in this project. For details about the TSPLIB data format, please refer to [`docs/tsp95.pdf`](../docs/tsp95.pdf).
