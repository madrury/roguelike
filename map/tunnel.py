from random import randint

def random_tunnel_between_pinned_rooms(r1, r2):
    (p1x, p1y), (p2x, p2y) = r1.random_point(), r2.random_point()
    if randint(0, 1) == 1:
        return (
            Tunnel('horizontal', (p1x, p1y), (p2x, p1y)),
            Tunnel('vertical', (p2x, p1y), (p2x, p2y)))
    else:
        return (
            Tunnel('vertical', (p1x, p1y), (p1x, p2y)),
            Tunnel('horizontal', (p1x, p2y), (p2x, p2y)))


class Tunnel:

    def __init__(self, kind, p1, p2):
        if kind not in {'horizontal', 'vertical'}:
            raise ValueError(
                "kind of tunnel must be 'horizontal' or 'vertical'")
        self.kind = kind
        self.p1 = p1
        self.p2 = p2

    def __iter__(self):
        if self.kind == 'horizontal':
            yield from self._iter_horizontal()
        elif self.kind == 'vertical':
            yield from self._iter_vertical()
        else:
            raise ValueError("Unknown tunnel type")

    def _iter_horizontal(self):
        x1, x2 = self.p1[0], self.p2[0]
        x1, x2 = min(x1, x2), max(x1, x2)
        for x in range(x1, x2 + 1):
            yield (x, self.p1[1])
        
    def _iter_vertical(self):
        y1, y2 = self.p1[1], self.p2[1]
        y1, y2 = min(y1, y2), max(y1, y2)
        for y in range(y1, y2 + 1):
            yield (self.p1[0], y)
