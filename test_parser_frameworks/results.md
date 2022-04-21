| parser          | method | current | peak   | total allocated |
|-----------------|--------|---------|--------|-----------------|
| lark            | LALR   | 672 KB  | 19MB   | 5.1MB           |
| lark-standalone | lalr   | 5.1MB   | 7.9MB  | 4.9MB           |   
| ply             | LALR   | 8.4MB   | 10.3MB | 8MB             |
|                 |        |         |        |                 |


# todo: 
    - check pegen - https://github.com/we-like-parsers/pegen_experiments/blob/master/Makefile
    - check pegen2 - 
    - check nom parser - https://github.com/progval/rust-python-parser