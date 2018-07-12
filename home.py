from multiprocessing import Process
import antibody #direction in or out and volume to provide
import reagent #same as inject module but for reagent addition
import needle

#antibody.home()
#reagent.home()
#needle.home()

Process(target=antibody.home).start()
Process(target=reagent.home).start()
Process(target=needle.home).start()

