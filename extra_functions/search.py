from os import walk
from multiprocessing.dummy import Pool
import extra_functions.custom_print as custom_print


class Search:
    def search(self, word):
        self.search_key = ' '.join(word).lower()
        custom_print.info("Searching: " + self.search_key)
        my_list = []
        for path, dirs, files in walk('modules'):
            for f in files:
                if not "__" in path+'/'+f:
                    my_list.append(path+'/'+f)
        pool = Pool(2)
        results = pool.map(self.isIn, my_list)
        pool.close()
        pool.join()
        for result in results:
            if result:
                print(result.replace(".py","").replace("modules/",""))

    def isIn(self, arg):
        try:
            fr = open(arg, 'r')
            if self.search_key in fr.read().lower():
                return arg
            fr.close()
        except Exception as e:
            print(e)
            return None 