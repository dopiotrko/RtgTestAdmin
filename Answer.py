from database import CursorFromConnectionFromPool
from RTG import RTG


class Answer:
    def __init__(self, name, surname, email, time, rtg_id, answer, id_):
        self.id = id_
        self.name = name
        self.surname = surname
        self.email = email
        self.time = time
        self.rtg_id = rtg_id
        self.answer = answer
        self.rtg_url = RTG.open_from_db(rtg_id).rtg_url

    def __repr__(self):
        return '<Answer of {} {}>'.format(self.name, self.surname)

    @classmethod
    def open_from_db(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM answers')
            rtgs = cursor.fetchall()
            rtgs_table = []
            for rtg in rtgs:
                rtgs_table.append(cls(name=rtg[1],
                                      surname=rtg[2],
                                      email=rtg[3],
                                      time=rtg[4],
                                      rtg_id=rtg[5],
                                      answer=rtg[6],
                                      id_=rtg[0]))
        return rtgs_table
