from typing import List, Any

class Figure:
    def __init__(self):
        # data is a list of trace-like dictionaries or objects
        self.data: List[Any] = []
        # minimal layout holder
        class Layout:
            pass

        self.layout = Layout()

    def add_trace(self, trace):
        self.data.append(trace)

    # allow index access like fig.data[0]["x"] if trace is dict

