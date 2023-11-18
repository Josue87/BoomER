from multiprocessing.dummy import Pool
from os import walk

import extra_functions.custom_print as custom_print


class Search:
    def search(self, word):
        self.search_key = ' '.join(word).lower()
        custom_print.info(f"Searching: {self.search_key}")
        my_list = []
        for path, dirs, files in walk('modules'):
            my_list.extend(f'{path}/{f}' for f in files if "__" not in f'{path}/{f}')
        pool = Pool(2)
        results = pool.map(self.isIn, my_list)
        pool.close()
        pool.join()
        for result in results:
            if result:
                print(result.replace(".py", "").replace("modules/", ""))

    def isIn(self, arg):
        try:
            with open(arg, 'r') as fr:
                if self.search_key in fr.read().lower():
                    return arg
        except Exception as e:
            print(e)
            return None
