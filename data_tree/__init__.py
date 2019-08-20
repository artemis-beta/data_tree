import logging

logging.basicConfig()

class DataTree(object):
    '''
    The DataTree class is a complex form of a Python dictionary which allows only unique elements to
    be inserted. The dictionary by default has unlimited depth with each entry requiring only a parent.
    '''
    def __init__(self, max_depth=1E32):
        '''
        Create a new DataTree

        Optional Arguments
        ------------------

        max_depth    (int)         Maximum depth of tree

        '''
        self._logger = logging.getLogger('DataTree')
        self._logger.setLevel('ERROR')
        self._max_depth = max_depth
        self._data = {}
        self._all_keys = []

    def _find_item(self, label, dictionary, key_list=[], depth=0):
        self._logger.info(f'Scanning at Depth {depth}')
        if label in dictionary and label not in key_list:
            key_list.append(label)
            return True
        if depth+1 > self._max_depth:
            self._logger.error(f"Maximum depth of {self._max_depth} reached, failed to insert entry.")
            raise IndexError
        for i, j in dictionary.items():
            if isinstance(j, dict):
                key_list.append(i)
                item = self._find_item(label, j, key_list, depth+1)
                if label in key_list:
                    return True
                elif not item:
                    key_list.remove(i)
                
        return False

    def search(self, object):
        key_list = []
        self._find_item(object, self._data, key_list)
        if len(key_list) > 0:
            return key_list

    def flatten(self):
        return self._all_keys

    def add_data(self, parent, child):
        '''
        Add an entry to the data tree

        Arguments
        ---------

        parent   (string)         Parent key. If None the entry is root level.

        child    (string)         The entry to add.

        '''
        key_list = []
        self._find_item(child, self._data, key_list)
        if len(key_list) > 0:
            self._logger.error(f"Category '{child}' is already a member of this Data Tree")
            raise IndexError
        self._find_item(parent, self._data, key_list)
        if len(key_list) < 1:
            self._data[child] = {}
        else:
            _dict_pointer = self._data
            for i in range(len(key_list)-1):
                try:
                    _dict_pointer = _dict_pointer[key_list[i]]
                except KeyError:
                    key_list.remove(key_list[i])
            try:
                _dict_pointer[key_list[-1]][child] = {}
            except KeyError:
                _dict_pointer[key_list[-1]] = {child : {}}
        self._all_keys.append(child)
        #return key_list

    def _append_level_str(self, dictionary, depth=0):
        _out_str = ''
        for key in dictionary:
            _out_str += ' '*(depth-1)+f'{" "*depth if depth > 1 else ""}' +'`-'*(0 if depth == 0 else 1)+key+'\n'
            _out_str += self._append_level_str(dictionary[key], depth+1)
        return _out_str

    def __str__(self):
        out_str = self._append_level_str(self._data)
        return out_str


    def __add__(self, other):
        import copy
        _tmp = copy.deepcopy(self)
        for key in self._all_keys:
            if other.search(key):
                self._logger.error('Could not combine DataTree objects due to duplicates')
                raise IndexError
        _tmp._data.update(other._data)
        return _tmp