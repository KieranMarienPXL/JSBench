import subprocess
import sys
import json
import numpy as np
import inquirer
import datetime
import time
from scripts.WebSocketBench import *
from scripts.SQLiteBench import *
from scripts.FetchBench import *
from scripts.httpserver import *

if sys.platform.startswith("linux") or sys.platform == "darwin":
    Runtimes = [
        inquirer.Checkbox('runtimes',
                          message='What runtimes would you like to test?',
                          choices=['Node', 'Deno', 'Bun'], ), ]
else:
    Runtimes = [
        inquirer.Checkbox('runtimes',
                          message='What runtimes would you like to test?',
                          choices=['Node', 'Deno'], ), ]

Tests = [
    inquirer.Checkbox('tests',
                      message='What parts would you like to benchmark?',
                      choices=['Fetch', 'SQLiteRead', 'SQLiteWrite', 'Websocket', 'httpserver'], ), ]

if __name__ == '__main__':
    print('warning: BUN WEBSOCKET DOES NOT WORK')
    jsonserver = subprocess.Popen(['json-server', 'db.json'])
    start_time = time.time()

    print('bun sqlite write result')
    runtimesAnswers = inquirer.prompt(Runtimes)['runtimes']
    print(runtimesAnswers)
    benchAnswers = inquirer.prompt(Tests)['tests']
    print(benchAnswers)

    if len(runtimesAnswers) == 0:
        print('MIN 1 value for runtimes')
        runtimesAnswers = inquirer.prompt(Runtimes)

    if len(benchAnswers) == 0:
        print('MIN 1 value for benchmarks')
        runtimesAnswers = inquirer.prompt(Runtimes)
    print(globals())
    allResults = dict()
    for runtime in runtimesAnswers:
        for bench in benchAnswers:
            function = runtime + bench
            if function in globals() and callable(globals()[function]):
                res = globals()[function]()
                allResults.update({function: res})
    print(allResults)

    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d-%H-%M-%S.json")

    with open(filename, 'w') as fp:
        json.dump(allResults, fp, sort_keys=True, indent=4)

    jsonserver.kill()
    end = time.time() - start_time
    print("--- %s seconds ---" % end)

    '''
    df = FetchBench.DenoJSON()
    nf = FetchBench.NodeJSON()
    if (sys.platform.startswith("linux") or sys.platform == "darwin"):
        bf = FetchBench.BunJSON()
        print("--- %s seconds ---" % np.mean(bf))
        print('bun fetch json result')

    print("--- %s seconds ---" % np.mean(df))
    print('deno fetch json result')

    print("--- %s seconds ---" % np.mean(nf))
    print('node fetch json result')
    '''

"""
    dr = SQLiteBench.Deno_Read()
    dw = SQLiteBench.Deno_Write()
    nr = SQLiteBench.Node_Read()
    nw = SQLiteBench.Node_Write()

    if (sys.platform.startswith("linux") or sys.platform == "darwin"):
        br = SQLiteBench.Bun_Read()
        bw = SQLiteBench.Bun_Write()

        print("--- %s seconds ---" % np.mean(br))
        print('Bun sqlite read result')
        print("--- %s seconds ---" % np.mean(bw))
        print('Bun sqlite write result')

    print("--- %s seconds ---" % np.mean(dr))
    print('deno sqlite read result')

    print("--- %s seconds ---" % np.mean(dw))
    print('deno sqlite write result')

    print("--- %s seconds ---" % np.mean(nr))
    print('node sqlite read result')

    print("--- %s seconds ---" % np.mean(nw))
    print('node sqlite write result')
    """
