"""
tbot.common -- вспомогательные полезные функции.

Create at 29.12.2023 16:58:43
~/tbot/common.py
"""

__author__ = 'pavelmstu'
__copyright__ = 'KIB, 2023'
__license__ = 'KIB'
__credits__ = [
    'pavelmstu',
]
__version__ = "20231229"
__status__ = "Production"


from sqlalchemy import select, and_

from sqlalchemy.orm import Session

from models import engine

from models.sample import Sample, SampleStatus


def get_samples(user_id_owner, status: SampleStatus):
    samples = list()
    with Session(engine) as session:

        query = select(Sample).where(
            and_(Sample.user_id_owner == user_id_owner, Sample.status == status.value)
                 )

        result = session.execute(
            query
        ).all()

        for _samples in result:
            sample = _samples[0]
            # yield sample
            samples.append(sample)
    return samples


def count_samples(user_id_owner, status: SampleStatus) -> int:
    result = get_samples(user_id_owner, status)
    return len(result)

