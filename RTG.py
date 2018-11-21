from database import CursorFromConnectionFromPool


class RTG:
    def __init__(self, rtg_url, id_=None):
        self.id = id_
        self.rtg_url = rtg_url

    def __repr__(self):
        return '<RTG {}>'.format(self.rtg_url)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO rtgs(rtg_url) VALUES (%s)', (self.rtg_url,))

    @classmethod
    def open_from_db(cls, id_):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM rtgs WHERE rtgs.id = %s LIMIT 1', (id_,))
            data = cursor.fetchone()
            return cls(rtg_url=data[1], id_=data[0])
