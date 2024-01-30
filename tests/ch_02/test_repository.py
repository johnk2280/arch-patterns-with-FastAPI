from sqlalchemy.orm import Session

from ch_02.repository import SQLAlchemyRepository


def test_repository_can_save_a_batch(session: Session):
    from ch_02.model import Batch
    batch = Batch('batch-1', 'RUSTY-SOAPDISH', 100)
    repo = SQLAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.query(Batch).all()

    assert len(rows) == 1
    assert rows == [batch]