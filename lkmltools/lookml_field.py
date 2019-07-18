
class LookMLField():
    """A view field such a dimension, dimension_group, or measure"""

    def __init__(self, json_data):
        """instantiate a LookMLField with a chunk of JSON from lkml parser

        Args:
            json_data (JSON): chunk of JSON from lkml parser

        """
        self.json_data = json_data
        self.__dict__.update(json_data)

    def is_dimension(self):
        """is this a dimension?

        Returns:
            bool: whether this is a dimension

        """
        return self._type == 'dimension'

    def is_dimension_group(self):
        """is this a dimension_group?

        Returns:
            bool: whether this is a dimension_group

        """
        return self._type == 'dimension_group'

    def is_measure(self):
        """is this a measure?

        Returns:
            bool: whether this is a measure

        """
        return self._type == 'measure'

    def has_key(self, k):
        """does this have a key k?

        Returns:
            bool: whether this has key k

        """
        return k in self.json_data
