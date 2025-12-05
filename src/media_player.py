'''
Docstring for media_player

Advanced OOP Architecture
•	Create media_player.py. Define a parent class Content.
•	Polymorphism: Create two classes, Movie and Series.
    Both must have a play() method.
    Movie should print "Starting Film...", while Series should print "Resuming S01E01...".
•	Encapsulation: Use a protected attribute _stream_key inside Content. 
    It should be accessible to subclasses but conceptually hidden from the public interface.
•	Magic Methods: Implement __repr__ to provide a developer-string for debugging \
    (e.g., Movie(id=101, title='SciFi')).

'''

class Content:
    """Parent class for all content types in StreamPy"""
    
    def __init__(self, content_id: int, title: str):
        self.content_id = content_id
        self.title = title
        self._stream_key = None  # Protected attribute

    def set_stream_key(self, key: str):
        """Setter for _stream_key"""
        self._stream_key = key

    def get_stream_key(self):
        """Getter for _stream_key"""
        return self._stream_key


class Movie(Content):
    def play(self):
        print("Starting Film...")

    def __repr__(self):
        return f"Movie(id={self.content_id}, title='{self.title}')"


class Series(Content):
    def play(self):
        print("Resuming S01E01...")

    def __repr__(self):
        return f"Series(id={self.content_id}, title='{self.title}')"


# Demo
if __name__ == "__main__":
    m = Movie(101, "Interstellar")
    s = Series(201, "Stranger Things")
    
    print(m)
    print(s)
    m.play()
    s.play()
