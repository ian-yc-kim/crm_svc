from .graph_objects import Figure

def _make_trace(x, y, **kwargs):
    # Represent trace as a simple dictionary with x and y sequences
    return {"x": list(x), "y": list(y)}


def bar(x, y, labels=None, title=None, **kwargs):
    fig = Figure()
    trace = _make_trace(x, y)
    fig.add_trace(trace)
    if title is not None:
        fig.layout.title = title
    return fig


def pie(names, values, title=None, **kwargs):
    fig = Figure()
    trace = {"labels": list(names), "values": list(values)}
    fig.add_trace(trace)
    if title is not None:
        fig.layout.title = title
    return fig


def line(x, y, labels=None, title=None, **kwargs):
    fig = Figure()
    trace = _make_trace(x, y)
    fig.add_trace(trace)
    if title is not None:
        fig.layout.title = title
    return fig
