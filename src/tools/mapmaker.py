import numpy as np
import pip

from deprecated import deprecated

try:
    import spacy
except ImportError as e:
    print(e)
    pip.main(['install', 'spacy'])
    import spacy
import copy
import typing

import jsontools as jt


class ArrayLikeMap:

    def __init__(self, values=None):
        """
        Create an instance of an ArrayLikeMap that sequentially sets values in a map like a stack.

        Parameters
        ----------
        values : list or None, optional
            List containing the initial values. Defaults to None.

        Attributes
        ----------
        _mapping : dict
            A dictionary that maps unique string keys to corresponding input values.
        _counter : int
            A count of the number of values in the mapping.
        _vals : list
            List of the input values passed to the instance upon initialization.

        Returns
        -------
        None
        """
        if values is None or values == []:
            values = []
            self._mapping = {}
        else:
            indices: list = np.arange(len(values)).astype(str).tolist()
            self._mapping = dict(zip(indices, values))
        self._counter = len(values)
        self._vals = values

    def push(self, item):
        """
        Push a new item into the ArrayLikeMap.

        Parameter
        ---------
        self : object
            Instance of ArrayLikeMap class.
        item : any
            Object to be added to the ArrayLikeMap.

        Returns
        -------
        None
        """
        index = str(self._counter)
        self._mapping[index] = item
        self._vals.append(item)
        self._counter += 1

    def pull(self, index):
        """
        Returns a value from the ArrayLikeMap corresponding to the given index.

        Parameter
        ---------
        index : str
            A string representation of the index.

        Returns
        -------
        object
            Value from the ArrayLikeMap corresponding to the given index.
        """
        index = str(int(index))
        return self._mapping[index]

    def replace(self, index, new):
        """
        Replace the key-value pair in the ArrayLikeMap at the specified index with a new pair.

        Parameters
        ----------
        index : int or str
            The index indicating the key to be replaced.
        new : any
            The new value to be associated with the specified key.

        Returns
        -------
        None
            This method does not return any value, it simply updates the ArrayLikeMap.
        """
        self._mapping[index] = new

    def get_map(self) -> dict:
        """
        Return a deep copy of the current ArrayLikeMap's mapping attribute.

        Returns
        -------
        dict
            A dictionary representing the map.
        """
        return copy.deepcopy(self._mapping)

    def keys(self) -> list:
        """
        Return a list of all the keys in the ArrayLikeMap.

        Parameter
        ---------
        self : object
            The object calling the function.

        Returns
        -------
        list
            A list of all the keys present in the ArrayLikeMap.
        """
        return list(self._mapping.keys())

    def values(self) -> list:
        """
        Return a list with the values of the ArrayLikeMap.

        Returns
        -------
        list
            List containing the values of the class attribute '_vals'.

        Raises
        ------
        None
        """
        return self._vals

    @deprecated(version='0.8', reason="Replaced by self.values()")
    def get_values(self) -> list:
        """
        Return a list of values for the ArrayLikeMap.

        Returns
        -------
        list
            A list of values stored in the class instance.
        """
        return self._vals

    def show(self, indent=4):
        """
        Prints the mapping of the object with desired indentation.

        Parameters
        ---------
        indent : int, optional
            Number of spaces to indent the mapping. Default is 4.

        Returns
        -------
        None
        """
        mapping = self.get_map()
        jt.pprint(mapping, indent=indent)

    def copy(self):
        """
        Create a new instance of the current ArrayLikeMap object and return it.

        Returns
        -------
        ArrayLikeMap
            A copy of the current ArrayLikeMap object.
        """
        new_array_like_map = __class__(self._vals[:])
        return new_array_like_map

    def to_json(self, indent=4):
        """
        Return a JSON representation of the mapping obtained from get_map() method.

        Parameters
        ---------
        indent : int, optional
            Number of spaces for indentation (default is 4)

        Returns
        -------
        str
            A JSON-formatted string of the mapping obtained from get_map() method.
        """
        mapping = self.get_map()
        return jt.to_json(mapping, indent=indent)

    def __iter__(self):
        """
        Iterator for the ArrayLikeMap.

        Returns
        -------
        self
            Returns the iterator object.
        """
        self.itered_index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the collection until there are no more items left to return.

        The __next__() function allows you to iterate over a collection.

        Returns
        -------
        object
            The next item in the collection.

        Raises
        -------
        StopIteration
            If there are no more items to return, it raises StopIteration.
        """
        if self.itered_index < self._counter:
            index = str(self.itered_index)
            self.itered_index += 1
            item = self._mapping[index]
            return item
        else:
            raise StopIteration

    def reset(self):
        """
        Reset the internal state of the ArrayLikeMap by setting all attributes to their initial values.

        Attributes
        ----------
        self : object
            The instance on which the method is called.

        Returns
        -------
        NoneType
            This method does not return anything.
        """
        self._mapping = {}
        self._counter = 0
        self._vals = []


class MultiMap:
    def __init__(self):
        """
        Initialize a MultiMap, where keys can have multiple mapped values.

        Parameters
        ----------
        self : object
            The instance of the class being initialized.

        Attributes
        ----------
        _mapping : dict
            A dictionary that maps unique string keys to corresponding input values.

        Returns
        -------
        None
        """
        self._mapping = {}

    def add_key(self, k):
        """
        Add a new key to the MultiMap.

        Parameters
        ---------
        k : key type
            The new key to be added to the MultiMap.
        """
        if k in self._mapping.keys():
            return
        self._mapping[k] = ArrayLikeMap()

    def get(self, k):
        """
        Return the associated mappings for the given key from the MultiMap.

        Parameters
        ----------
        k : any hashable type
            Key for which the associated map is to be retrieved.

        Returns
        -------
        dict
            Associated map for the given key.
        """
        arr_like_map: ArrayLikeMap = self._mapping[k]
        return arr_like_map.get_map()

    def _set_mapping(self, k, v):
        """
        Create or update a key-value mapping in the MultiMap's internal dictionary.

        Parameters
        ----------
        k : any type
            Key to use for the mapping.
        v : any type
            Value to add to the mapping.

        Returns
        -------
        None
            This function does not return anything, but updates the mapping in-place.

        Notes
        -----
        This function is part of a class method. It first checks if the key is already present in the dictionary
        and adds it to the dictionary if it is not already present. Then, it appends the value to the corresponding key's value list.
        """
        if k not in self._mapping.keys():
            self.add_key(k)
        arr_like_map: ArrayLikeMap = self._mapping[k]
        arr_like_map.push(v)

    def put(self, k, *args):
        """
        Adds values to the MultiMap for the specified key.

        The values can be a single value or a list of values.

        Parameters
        ----------
        k : key
            Key for the dictionary.
        *args : tuple
            Tuple of values to be added to the dictionary.

        Returns
        -------
        None
            This function does not return any value, but updates the dictionary with the input values.
        """
        if isinstance(args[0], list):
            for v in args[0]:
                self._set_mapping(k, v)
        else:
            for v in args:
                self._set_mapping(k, v)

    def get_map(self):
        """
        Returns the MultiMap as a dictionary.

        This function returns a dictionary with the same keys as the mapping
        object and the values are ArrayLikeMap dictionaries.

        Parameters
        ----------
        self : object
            Mapping object.

        Returns
        -------
        dict
            A dictionary with the same keys as the mapping object and the values are also dictionaries representing
            the keys and values of inner ArrayLikeMap objects.
        """
        return_map = {}
        for key in self._mapping.keys():
            value: ArrayLikeMap = self._mapping[key]
            return_map[key] = value.get_map()
        return return_map

    def contains(self, k, v):
        """
        Check if a key-value pair exists.

        Parameters
        ----------
        k : hashable
            Key to be checked in the dictionary.
        v : Any
            Value associated with the key to be checked in the dictionary.
        Returns
        -------
        bool
            Returns True if the key-value pair exists, otherwise returns False.
        """
        array_like_map: ArrayLikeMap = self._mapping[k]
        return array_like_map.values().__contains__(v)

    def show(self, indent=4):
        """
        Print a formatted output of the MultiMap's mapping data.

        Parameters
        ----------
        indent : int, optional
            The number of spaces to indent the output. Default is 4.

        Returns
        -------
        None
            This function does not return any values, it only prints output.
        """
        mapping = self.get_map()
        jt.pprint(mapping, indent=indent)

    def copy(self):
        """
        Return a deep copy of the MultiMap object.

        Returns a new MultiMap object with the same key-value pairs as the original MultiMap.
        The new MultiMap is created as an instance of the same class as the original object.

        Returns
        -------
        MultiMap
            A deep copy of the MultiMap object.
        """
        new_multimap = __class__()
        for key in self._mapping.keys():
            array_like_map: ArrayLikeMap = self._mapping[key]
            vals = array_like_map.values()
            new_multimap.put(key, vals)
        return new_multimap

    def to_json(self, indent=4):
        """
        Serialize this MultiMap to a JSON formatted string.

        Parameters
        ---------
        self : instance
            The object instance that the method is being called on.
        indent : Optional[int], default=4
            The number of spaces to use for indentation when formatting the JSON string.

        Returns
        -------
        str
            A JSON formatted string that contains the values of the attributes in the MultiMap.
        """
        mapping = self.get_map()
        return jt.to_json(mapping, indent=indent)

    def reset(self):
        """
        Resets the keys and values of this MultiMap

        Parameters
        ---------
        self : Object
            The instance of the class calling the method.

        Returns
        -------
        NoneType
            The method does not return any value.
        """
        self._mapping = {}


class NestedMap:

    def __init__(self, input_map=None):
        """
        Initialize a NestedMap instance with an optional dictionary argument.

        Parameters
        ----------
        input_map : dict, optional
            Dictionary argument to initialize the NestedMap's mappings. Default is an empty dictionary.

        Attributes
        ----------
        _mapping: dict
            The NestedMap's internal dictionary

        Returns
        -------
        None
        """
        if not input_map:
            self._mapping = {}
        else:
            self._mapping = input_map

    def put(self, key, value, depth: list = None):
        """
        Puts a key-value pair within a nested dictionary structure, given a key, value, and the depth of the desired location within the structure.

        Examples
        -----------
        >>> example_map = NestedMap()
        >>> example_map.put("2", 2, depth=[])
        >>> print(example_map)
        {"2" : 2}
        >>> example_map.put("map", {})
        >>> print(example_map)
        {
            "2" : 2,
            "map" : {}
        }
        >>> example_map.put("two", {"2": 2}, depth=["map"])
        {
            "2" : 2,
            "map" : {
                "two" : {
                    "2" : 2
                }
            }
        }
        >>> example_map.put("4-2", 2, depth=["map", "two"])
        {
            "2" : 2,
            "map" : {
                "two" : {
                    "2" : 2,
                    "4-2" : 2
                }
            }
        }
        >>> example_map.put("2", "two")
        {
            "2" : "two",
            "map" : {
                "two" : {
                    "2" : 2,
                    "4-2" : 2
                }
            }
        }

        Parameters
        ----------
        key : varying types
            The key to be inserted into the nested dictionary structure.
        value : varying types
            The value to be paired with the key in the nested dictionary structure.
        depth : list
            (Optional) A list of key hierarchy, indicating the depth of the desired location within the dictionary structure.
            If depth is None, the key-value pair will be added to the root of the dictionary.

        Returns
        -------
        value : varying types
            The value that has been added to the dictionary structure.
        """
        if depth is None:
            depth = []
        if not depth:
            self._mapping[key] = value
        else:
            curr_map = None
            for k in depth:
                if curr_map is None:
                    curr_map = self._mapping[k]
                else:
                    curr_map = curr_map[k]
            curr_map[key] = value
        return value

    def get(self, key, depth: list = None):
        """
        Return the value of a key in a nested mapping (dictionary) at a specified depth, or at the top level if no depth is specified.

        Parameters
        ----------
        key : str
            Key to search for.
        depth : list, optional
            List of keys representing depth in the nested mapping. Default value is None.

        Returns
        -------
        Any
            Value stored under the key in the mapping.

        Note
        ----
        If depth is not None, function looks for the key in the nested mapping at the specified depth. Otherwise, it looks for the key at the top level (self._mapping[key]).

        Example
        -------
        >>> mapping = {
        >>>     'a': {
        >>>         'b': 1,
        >>>         'c': 2
        >>>     },
        >>>     'd': {
        >>>         'e': {
        >>>             'f': 3
        >>>         }
        >>>     }
        >>> }
        >>> x = NestedMap(mapping)
        >>> assert x.get('a', depth=['b']) == 1
        >>> assert x.get('f', depth=['d', 'e']) == 3
        >>> assert x.get('d') == {'e': {'f': 3}}
        """
        if depth is None:
            depth = []
        if not depth:
            value = self._mapping[key]
        else:
            curr_map = None
            for k in depth:
                if curr_map is None:
                    curr_map = self._mapping[k]
                else:
                    curr_map = curr_map[k]
            value = curr_map[key]
        return value

    def clear(self):
        """
        Clears all mappings from this NestedMap.

        Parameters
        ----------
        self: instance
            The instance of the class that the method is called on.

        Returns
        -------
        None
            This method returns nothing, it just clears the internal dictionary of the instance in place.
        """
        self._mapping.clear()

    def clone(self):
        """
        Returns a shallow copy of this data structure's dictionary: the keys and values themselves are not cloned.

        Returns
        -------
        dict
            A dictionary containing a copy of the current class instance.
        """
        copy = self._mapping.copy()
        return copy

    def __compute_helper(self, key, remapping_function,
                         depth: list = None,
                         mapping_condition=None,
                         map_to_use: dict = None,
                         return_type="value"):
        """
        Perform a helper function to compute and return either the value or dictionary based on the given parameters.

        Attempts to compute a mapping for the specified key and its current mapped value (or null if
        there is no current mapping), but only according to the mapping condition, which is
        a function that takes in the value associated with the passed in key and returns true if the
        condition is fulfilled. If a depth (i.e. a series of nested keys in a list)
        is not specified, then the remapping function is only applied to the first set of keys
        (i.e. the keys without any depth). Can either return the remapped value of the
        key or the updated dictionary. The only arguments that return_type will accept are
        'value' and 'dictionary'.

        Parameters
        ----------
        key : str
            Key mapped to the value.
        remapping_function : function
            Function to remap the given value.
        depth : list, optional
            A list of dictionary keys, by default None.
        mapping_condition : function, optional
            A condition to check if the value can be remapped, by default None.
        map_to_use : dict, optional
            The dictionary to use for mapping, by default None.
        return_type : str, optional
            The type of return value desired, either "value" or "dictionary", by default "value".

        Returns
        -------
        various
            Either the remapped value or the dictionary with the updated value.
        """
        assert_message = "You can only pass in 'value' or 'dictionary' into return_type"
        assert return_type.lower() == "value" or return_type.lower() == "dictionary", assert_message
        if not map_to_use:
            map_to_use = self._mapping
        else:
            map_to_use = map_to_use
        if depth is None:
            depth = []
        curr_map = None
        if not depth:
            value = map_to_use[key]
            curr_map = map_to_use
        else:
            for k in depth:
                if curr_map is None:
                    curr_map = map_to_use[k]
                else:
                    curr_map = curr_map[k]
            value = curr_map[key]
        if mapping_condition is None or mapping_condition(value) is True:
            remapped_value = remapping_function(value)
            curr_map[key] = remapped_value
            return remapped_value if return_type == "value" else map_to_use
        else:
            return value if return_type == "value" else map_to_use

    def compute(self, key, remapping_function,
                depth: list = None):
        """
        Attempts to compute a mapping for the specified
        key and its current mapped value (or null if
        there is no current mapping). If a depth
        (i.e. a series of nested keys in a list)
        is not specified, then the remapping function
        is only applied to the first set of keys
        (i.e. the keys without any depth).

        Parameters
        ---------
        key : str, int or tuple
            Key of the dictionary.
        remapping_function : function
            Function to apply to the value of the dictionary.
        depth : list, optional
            List of integers that represent the levels to go in the dictionary.

        Returns
        -------
        Any
            The computed value
        """
        return self.__compute_helper(key, remapping_function,
                                     depth=depth)

    def compute_if_absent(self, key, mapping_function,
                          depth: list = None):
        """
        If the specified key is not already associated with a value (or is mapped to null), attempts
        to compute its value using the given mapping function and enters it into this map unless null.

        Parameters
        ---------
        key : hashable
            The key to check in the dictionary.
        mapping_function : callable
            The function to call to compute and return a new value for the specified key, if the key is None.
        depth : list or None, optional
            A list of keys representing nested dictionaries to search for the specified key. If None, search the main dictionary.

        Returns
        -------
        Any
            The computed value for the specified key.
        """

        def value_is_absent(value):
            return value is None

        # Perform a helper function to compute and return the value based on the given parameters.
        return self.__compute_helper(key, mapping_function,
                                     depth=depth,
                                     mapping_condition=value_is_absent)

    def compute_if_present(self, key, mapping_function,
                           depth: list = None):
        """
        Return the value associated with the given key or compute a new value using the provided mapping function if it is absent.

        If the value for the specified key is present and non-null, attempts to compute a new mapping
        given the key and its current mapped value.

        Parameters
        ---------
        key : any hashable type
            Key to look up in the dictionary.
        mapping_function : function
            A function that computes a new value for the given key.
        depth : list, optional (default=None)
            A list of keys representing the path to the value in the structure.

        Returns
        -------
        any hashable type
            The value associated with the given key or the newly computed value.
        """

        def value_is_present(value):
            return value is not None

        return self.__compute_helper(key, mapping_function,
                                     depth=depth,
                                     mapping_condition=value_is_present)

    def __contains_key_helper(self, key, mapping) -> bool:
        """
        Recursively checks the mappings at each depth level to see if the specified key is
        present once in the main mapping. Returns a boolean to indicate whether a key exists in the NestedMap.

        Parameters
        ---------
        key : str
            The key to search for in the nested dictionary.
        mapping : dict
            The nested dictionary to search for the key in.

        Returns
        -------
        bool
            True if the key is found in the dictionary, False otherwise.

        Raises
        ------
        TypeError
            Raised when the input key is not hashable.
        """
        if not isinstance(key, typing.Hashable):
            raise TypeError("The input key is not hashable")

        keys = list(mapping.keys())
        if mapping is None:
            pass
        elif key in keys:
            return True
        else:
            for k in keys:
                curr_map = mapping[k]
                return self.__contains_key_helper(
                    key, curr_map
                )
            return False

    def contains_key(self, key):
        """
        Check if the input key exists in the current mapping of a dictionary.

        Returns true if this map contains a mapping for the specified key.

        Parameters
        ---------
        key : any hashable data type
            Key to be searched in the dictionary.

        Returns
        -------
        bool
            Returns True if the input key exists in the dictionary.

        Raises
        ------
        TypeError
            Raised when the input key is not hashable.
        """
        curr_map = self._mapping
        return self.__contains_key_helper(key, curr_map)

    def __contains_value_helper(self, value, mapping):
        """
        Checks if a value exists in a nested dictionary.

        Recursively checks the mappings at each depth level to see
        if the specified value is present once in the main mapping.

        Parameters
        ---------
        value : any
            The value to check in the nested dictionary.
        mapping : dict
            The nested dictionary to check the value against.

        Returns
        -------
        bool
            True if value exists in the nested dictionary, False otherwise.
        """
        keys = list(mapping.keys())
        values = list(mapping.values())
        if mapping is None:
            pass
        elif value in values:
            return True
        else:
            for k in keys:
                curr_map = mapping[k]
                return self.__contains_value_helper(
                    value, curr_map
                )
            return False

    def contains_value(self, value):
        """
        Return whether a given value is contained within the mapping.

        Parameters
        ----------
        value : any
            The value to be searched for in the mapping.

        Returns
        -------
        bool
            True if the value is found, False otherwise.
        """
        curr_map = self._mapping
        return self.__contains_value_helper(value,
                                            curr_map)

    def __for_each_helper(self, mapping,
                          bi_consumer_function):
        """
        Recursively iterates over a nested dictionary and applies the specified function to each key-value pair.

        This function finds key, value pairs where the values are not dictionaries, then uses each
        key, value pair as inputs for the specified BiConsumer function.

        Parameters
        ----------
        mapping : dict
            Input dictionary to be processed.
        bi_consumer_function : function
            Function to be applied to each key-value pair.
        Returns
        -------
        None
        """
        keys = list(mapping.keys())
        for key in keys:
            value = mapping[key]
            if type(value) == dict:
                return self.__for_each_helper(
                    value, bi_consumer_function
                )
            else:
                try:
                    bi_consumer_function(key, value)
                except Exception:
                    return

    def for_each(self, bi_consumer_function):
        """
        Invokes a specified consumer function on each key-value pair in a given map.

        Performs the given action for each entry in
        this map until all entries have been processed
        or the action throws an exception.

        Parameters
        ----------
        bi_consumer_function : function
            Custom function that accepts two parameters, key and value,
            and performs an action on each key-value pair in the map.

        Returns
        -------
        None
        """
        curr_map = self._mapping
        return self.__for_each_helper(
            curr_map, bi_consumer_function)

    def get_or_default(self, key, default_value,
                       depth=None):
        """
        Return the value associated with a given key or the default value if the key is not present in the NestedMap.

        Parameters
        ----------
        key : hashable
            The key to search for in the dictionary.
        default_value : any
            The value to return if the key is not present in the dictionary.
        depth : int or None
            The nesting depth of the dictionary, if applicable.

        Returns
        -------
        any
            The value associated with the given key if present in the dictionary, otherwise the default value.
        """
        value = self.get(key, depth)
        if value is not None:
            return value
        else:
            return default_value

    def is_empty(self):
        """
        Return True if the NestedMap is empty and False otherwise.

        Parameters
        ----------
        self : object
            This parameter represents the instance of the class.

        Returns
        -------
        bool
            True if the mapping is empty, False otherwise.
        """
        empty_map: bool = self._mapping == {}
        return empty_map

    @deprecated(version="0.8", reason="Replaced by self.keys()")
    def key_set(self, depth: list) -> set:
        """
        Return a set of keys from a dictionary based on the given depth.

        Parameters
        ----------
        depth : list
            List of keys to traverse through the dictionary.

        Returns
        -------
        set
            Set of keys obtained after traversing the dictionary at the given depth.
        """
        if depth is None:
            keyset = set(self._mapping.keys())
        else:
            curr_map = None
            for k in depth:
                if curr_map is None:
                    curr_map = self._mapping[k]
                else:
                    curr_map = curr_map[k]
            keyset = set(curr_map.keys())
        return keyset

    def keys(self, depth: list = None) -> set:
        """
        Return a set of keys from a dictionary based on the given depth.

        Parameters
        ----------
        depth : list
            List of keys to traverse through the dictionary.

        Returns
        -------
        set
            Set of keys obtained after traversing the dictionary at the given depth.
        """
        return self.key_set(depth=depth)

    def put_all(self, mapping: dict, depth: list = None):
        """
        Update a mapping by adding all key-value pairs in the provided dictionary.

        Copies all the mappings from the specified map to this map at the specified depth.

        Parameters
        ----------
        mapping : dict
            Dictionary of key-value pairs to add to the mapping.
        depth : list, Optional
            List of keys defining the depth of the nested dictionary to which the key-value pairs should be added.

        Returns
        -------
        None
        """
        if depth is None:
            depth = []
        if len(depth) > 0:
            curr_map = None
            index_offset = 1
            for i in range(len(depth)):
                k = depth[i]
                if curr_map is None:
                    curr_map = self._mapping[k]
                else:
                    prev_map = curr_map
                    curr_map = curr_map[k]
                    if i == len(depth) - index_offset:
                        prev_map[k] = {**curr_map, **mapping}
                        return
        else:
            return

    def remove_if(self, key, value, depth: list = None):
        """
        Remove a key-value pair at a specified depth in a dictionary if the key maps to a certain value.

        Parameters
        ----------
        key : hashable
            Key to be checked and removed.
        value : Any
            Value at which the key is to be removed.
        depth : List
            List of integers representing the path to the value. Default is None.

        Returns
        -------
        bool
            True if key-value pair is removed, False otherwise.
        """
        # remove the key if it is mapped to a certain value
        #   at the specified depth
        # if the key does not exist, do nothing
        # return true if the key was removed
        if depth is None:
            depth = []
        return True

    def remove(self, key, depth: list = None):
        """
        Removes the mapping for the specified key from this map if present.

        Parameters
        ---------
        key : str
            The key to remove from the dictionary.
        depth : list, optional
            List specifying the nested depth of the key to remove, default is None.

        Returns
        -------
        any
            Returns the value of the key removed from the dictionary.
            If the key does not exist, returns None.
        """
        if depth is None:
            depth = []
        # remove the key at the specified depth
        # if the key does not exist, do nothing
        # returns the value of the key removed
        old_value = ...
        return old_value

    def replace_if(self, key, old_value, new_value, depth: list = None):
        """
        Replaces the entry for the specified key only if currently mapped to the specified value.

        Parameters
        ----------
        key: str
            The key to be searched for and replaced if old_value is found.
        old_value: any
            The old value to be replaced if found.
        new_value: any
            The new value to be used as a replacement
        depth: list, optional
            A list of integers or keys that specify the depth in the dictionary where the key to be changed is located.
            Default is None.

        Returns
        -------
        bool
            Returns True if the specified key is found and the old_value is replaced otherwise False.
        """
        if depth is None:
            depth = []
        # replace the key only if it is currently
        #   mapped to a specified value
        #   at the specified depth
        # returns true if the value was replaced
        return True

    def replace(self, key, value, depth: list = None):
        """
        Replaces the entry for the specified key only if it is currently mapped to some value.

        Return the value associated with a key in a nested dictionary after replacing it with the given value.

        Parameters
        ----------
        key : Any hashable type
            The key in the dictionary whose value needs to be replaced.
        value : Any type
            The new value to be associated with the given key.
        depth : list, optional
            A list of keys representing the path to the nested dictionary where the value needs to be replaced. Default
            value is None, which means the value will be searched in the top level dictionary.

        Returns
        -------
        Any type
            The old value associated with the given key. None is returned if the key is not found in the dictionary.
        """
        if depth is None:
            depth = []
        old_value = self.get(key, depth=depth)
        if old_value is not None:
            self.replace_if(key, old_value, value, depth=depth)
        return old_value

    def replace_all(self, bi_function):
        """
        Perform a replacement operation on each entry's value by invoking the provided function on each entry until all
        entries have been processed or an exception is raised.

        Replaces each entry's value with the result of invoking the given function on that entry
        until all entries have been processed or the function throws an exception.

        Parameters
        ----------
        bi_function : function
            The function to be applied to each key-value pair.

        Returns
        -------
        None
        """
        # replace all values with the result
        #   yielded from applying the bi_function
        #   to each key, value pair
        pass

    def size(self, depth: list = None):
        """
        Return the number of key-value mappings with respect to the given depth.

        Parameters
        ---------
        depth : list, optional
            A list of keys used to navigate the mapping (default is None).

        Returns
        -------
        int64
            Integer size of the mapping with respect to the given depth.
        """
        if depth is None:
            depth = []
        map_size = None
        if not depth:
            map_size = len(list(self._mapping.keys()))
        else:
            curr_map = None
            index_offset = 1
            for i in range(len(depth)):
                k = depth[i]
                if curr_map is None:
                    curr_map = self._mapping[k]
                else:
                    curr_map = curr_map[k]
                    if i == len(depth) - index_offset:
                        map_size = len(list(curr_map.keys()))
        return map_size

    def get_all_keys(self, dictionary: dict, depth=None):
        """
        Return all keys and corresponding values of a given nested dictionary.

        Parameters
        ---------
        self : object
            The instance of the object class.
        dictionary : dict
            The nested dictionary to retrieve keys and values from.
        depth : list or None
            The list of keys representing the current depth of the nested
            dictionary. Default value is None.

        Returns
        -------
        generator
            A generator object yielding tuples of (key, value, depth) for
            each key-value pair in the given dictionary, including nested
            dictionaries and their respective depths.
        """
        if not depth:
            depth = []
        for key, value in dictionary.items():
            yield key, value, depth
            if isinstance(value, dict):
                new_depth = depth + [key]
                yield from self.get_all_keys(value, new_depth)

    def __expanded(self, map_to_use: dict) -> dict:
        """
        Return an expanded dictionary based on the input `map_to_use`.

        Parameters
        ---------
        map_to_use: dict
            A dictionary to be expanded.

        Returns
        -------
        dict
            An expanded dictionary.

        Raises
        ------
        TypeError
            If `map_to_use` is not a dictionary.
        TypeError
            If `value` is not an instance of `ArrayLikeMap` or `MultiMap`.

        Notes
        -----
        This function is a recursive function that computes the depth of the nested dictionary.
        """
        expanded_map = copy.deepcopy(map_to_use)
        for key, value, depth in self.get_all_keys(map_to_use):
            if isinstance(value, ArrayLikeMap) or isinstance(value, MultiMap):
                expanded_map = self.__compute_helper(key,
                                                     lambda mapping: mapping.get_map(),
                                                     depth=depth,
                                                     map_to_use=expanded_map,
                                                     return_type="dictionary")
        return expanded_map

    def get_map(self, expand=False):
        """
        Return the NestedMap as a dictionary.

        The NestedMap can be expanded, meaning all ArrayLikeMap and MultiMap objects are converted to dictionaries.

        Parameters
        ----------
        expand : bool, optional
            If True, returns the expanded version of the mapping.
            If False, returns the original mapping. Default is False.

        Returns
        -------
        dict
            The mapping with keys either in original format (if expand=False) or in dotted notation (if expand=True).
        """
        if expand:
            return self.__expanded(self._mapping.copy())
        else:
            return self._mapping

    def show(self, depth=None):
        """
        Prints the contents of a mapping object with optional depth limit.

        Parameters
        ----------
        depth : int or None
            Limit the depth of the printout to this number of levels. If set to None (default), prints all levels.

        Returns
        -------
        None
            This function only prints, it does not return a value.
        """
        map_to_use = self.__expanded(self._mapping.copy())
        if depth is None:
            depth = []
        if not depth:
            jt.pprint(map_to_use)
        else:
            curr_map = None
            for i in range(len(depth)):
                k = depth[i]
                if curr_map is None:
                    curr_map = map_to_use[k]
                else:
                    curr_map = curr_map[k]
            jt.pprint(curr_map)

    def to_json(self, indent=4):
        """
        Returns the NestedMap as a JSON string.

        Parameters
        ----------
        indent : int, optional
            Number of spaces to use for indentation (default is 4).

        Returns
        -------
        str
            JSON string representation of the object.
        """
        mapping = self.get_map(expand=True)
        return jt.to_json(mapping, indent=indent)

    def reset(self):
        """
        Reset the NestedMap to an empty state.

        Parameters
        ----------
        self : object
           Instance of the class.

        Returns
        -------
        None
           This function does not return a value.
        """
        self._mapping = {}