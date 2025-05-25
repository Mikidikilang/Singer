from typing import List, Tuple, Optional


class Singer:
    """
    Represents a singer with their name, genre, and upcoming performances.

    Provides a structured way to store and manage singer information, including
    adding/removing performances and comparing singers by performance count.

    Attributes:
        _name (str): The name of the singer (internal use). Must not be empty or whitespace.
        _genre (str): The music genre the singer performs (internal use). Must not be empty or whitespace.
        _performances (List[Tuple[str, str]]): List of (location, date) tuples
            for upcoming performances (internal use).
    """
    _name: str
    _genre: str
    _performances: List[Tuple[str, str]]

    def __init__(self, name: str, genre: str, performances: List[Tuple[str, str]]):
        """
        Initializes a Singer object.

        Args:
            name: The name of the singer. Cannot be empty or whitespace.
            genre: The music genre the singer performs. Cannot be empty or whitespace.
            performances: A list of tuples, where each tuple contains the
                location (str) and date (str) of a performance.

        Raises:
            TypeError: If input types are incorrect (name/genre not str, performances not list, etc.).
            ValueError: If name or genre is empty or whitespace, or if a performance tuple is malformed.
        """
        if not isinstance(name, str):
            raise TypeError("Singer name must be a string.")
        if not name.strip():
            raise ValueError("Singer name cannot be empty or whitespace.")

        if not isinstance(genre, str):
            raise TypeError("Singer's genre must be a string.")
        if not genre.strip():
            raise ValueError("Singer's genre cannot be empty or whitespace.")

        if not isinstance(performances, list):
            raise TypeError("Performances must be provided as a list.")

        for performance in performances:
            if not isinstance(performance, tuple) or len(performance) != 2:
                raise TypeError(
                    f"Each performance must be a tuple of (location, date). Found: {performance}"
                )
            if not all(isinstance(item, str) for item in performance):
                raise TypeError(
                    f"Both location and date in a performance tuple must be strings. Found: {performance}"
                 )

            if not performance[0].strip() or not performance[1].strip():
                raise ValueError(f"Location and date within a performance cannot be empty or whitespace. Found: {performance}")

        self._name = name
        self._genre = genre
        self._performances = list(performances)

    @property
    def name(self) -> str:
        """Gets the name of the singer."""
        return self._name

    @property
    def genre(self) -> str:
        """Gets the genre of music the singer performs."""
        return self._genre

    @property
    def performances(self) -> List[Tuple[str, str]]:
        """
        Gets a copy of the list of upcoming performances.

        Returns:
            A list of (location, date) tuples. Returning a copy ensures
            the internal list cannot be modified directly via the property.
        """
        return list(self._performances)

    @name.setter
    def name(self, value: str):
        """
        Sets the name of the singer.

        Args:
            value: The new name for the singer.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is an empty string or contains only whitespace.
        """
        if not isinstance(value, str):
            raise TypeError("Singer name must be a string.")
        if not value.strip():
            raise ValueError("Singer name cannot be empty or whitespace.")
        self._name = value

    @genre.setter
    def genre(self, value: str):
        """
        Sets the genre of music the singer performs.

        Args:
            value: The new genre for the singer.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is an empty string or contains only whitespace.
        """
        if not isinstance(value, str):
            raise TypeError("Singer's genre must be a string.")
        if not value.strip():
            raise ValueError("Singer's genre cannot be empty or whitespace.")
        self._genre = value

    def __str__(self) -> str:
        """
        Returns a string representation of the singer.

        Includes name, genre, and upcoming performances.
        """
        header = f"Singer: {self._name} (Genre: {self._genre})"
        if not self._performances:
            performances_str = " No scheduled performances."
        else:
            formatted_performances = [f"\n  - Location: {loc}, Date: {date}" for loc, date in self._performances]
            performances_str = "".join(formatted_performances)

        return f"{header}\nPerformances:{performances_str}"

    def __add__(self, performance: Tuple[str, str]) -> 'Singer':
        """
        Adds a new performance, returning a *new* Singer object.

        Args:
            performance: A tuple (location: str, date: str) for the new performance.

        Returns:
            A new Singer instance with the added performance.

        Raises:
            TypeError: If performance is not a tuple or its elements are not strings.
            ValueError: If performance tuple does not have exactly two elements,
                        or if location/date are empty/whitespace (optional check).
        """
        if not isinstance(performance, tuple):
            raise TypeError("Performance to add must be a tuple.")
        if len(performance) != 2:
            raise ValueError("Performance tuple must contain exactly (location, date).")
        if not all(isinstance(item, str) for item in performance):
            raise TypeError("Both location and date in the performance tuple must be strings.")
        if not performance[0].strip() or not performance[1].strip():
            raise ValueError(f"Location and date for the new performance cannot be empty or whitespace. Found: {performance}")

        new_performances = self._performances + [performance]
        return Singer(self._name, self._genre, new_performances)

    def __sub__(self, performance: Tuple[str, str]) -> 'Singer':
        """
        Removes a performance, returning a *new* Singer object.

        Args:
            performance: The (location: str, date: str) tuple of the performance to remove.

        Returns:
            A new Singer instance without the specified performance.

        Raises:
            TypeError: If performance is not a tuple.
            ValueError: If performance tuple is malformed or not found in the list.
        """
        if not isinstance(performance, tuple):
            raise TypeError("Performance to remove must be a tuple.")
        if len(performance) != 2:
            raise ValueError("Performance tuple must contain exactly (location, date).")

        temp_performances = self._performances[:]
        try:
            temp_performances.remove(performance)
        except ValueError:
            raise ValueError(f"Performance {performance} not found for singer {self._name}.") from None

        return Singer(self._name, self._genre, temp_performances)

    def __lt__(self, other: 'Singer') -> bool:
        """
        Compares singers based on the number of performances (less than).

        Args:
            other: Another Singer object to compare with.

        Returns:
            True if this singer has fewer performances than 'other', False otherwise.
            NotImplemented if 'other' is not a Singer instance.
        """
        if not isinstance(other, Singer):
            return NotImplemented
        return len(self._performances) < len(other._performances)

    def __gt__(self, other: 'Singer') -> bool:
        """
        Compares singers based on the number of performances (greater than).

        Args:
            other: Another Singer object to compare with.

        Returns:
            True if this singer has more performances than 'other', False otherwise.
            NotImplemented if 'other' is not a Singer instance.
        """
        if not isinstance(other, Singer):
            return NotImplemented
        return len(self._performances) > len(other._performances)

# =============================================================================


class ConcertOrganizer:
    """
    Manages a collection of Singer objects.

    Allows storing singers and finding the one with the most performances.

    Attributes:
        _singers (List[Singer]): A list of Singer objects managed by the organizer (internal use).
    """
    _singers: List[Singer]

    def __init__(self, singers: Optional[List[Singer]] = None):
        """
        Initializes the ConcertOrganizer.

        Args:
            singers: An optional initial list of Singer objects. If provided,
                     all elements must be Singer instances. A copy is stored.

        Raises:
            TypeError: If 'singers' is provided but is not a list or contains
                       non-Singer objects.
        """
        if singers is None:
            self._singers = []
        else:
            if not isinstance(singers, list):
                raise TypeError("Initial singers must be provided as a list.")
            if not all(isinstance(singer, Singer) for singer in singers):
                raise TypeError("All elements in the initial list must be Singer instances.")
            self._singers = list(singers)

    @property
    def singers(self) -> List[Singer]:
        """
        Gets a copy of the list of singers managed by the organizer.

        Returns:
            A list of Singer objects. Returning a copy prevents direct
            modification of the internal list.
        """
        return list(self._singers)

    def add_singer(self, singer: Singer):
        """Adds a singer to the organizer."""
        if not isinstance(singer, Singer):
            raise TypeError("Only Singer objects can be added.")
        if singer not in self._singers:
            self._singers.append(singer)

    def __str__(self) -> str:
        """Returns a string representation of the ConcertOrganizer."""
        count = len(self._singers)
        if count == 0:
            return "Concert Organizer (No singers registered)"
        else:
            singer_names = ", ".join(s.name for s in self._singers)
            return f"Concert Organizer ({count} singers registered): {singer_names}"

    def find_singers_with_most_performances(self) -> Singer:
        """
        Finds all singers with the highest number of scheduled performances.

        Returns:
            A list containing the Singer object(s) with the most performances.
            The list will contain multiple singers in case of a tie.

        Raises:
            ValueError: If no singers are registered with the organizer.
        """
        if not self._singers:
            raise ValueError("No singers registered to find the one with the most performances.")

        max_performances = max(len(singer.performances) for singer in self._singers)
        return [singer for singer in self._singers if len(singer.performances) == max_performances]