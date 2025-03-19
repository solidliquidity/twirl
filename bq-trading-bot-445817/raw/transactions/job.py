import uuid
from datetime import timedelta, datetime
import random

import pandas as pd

N_SAMPLES_TO_GENERATE = 10


def job() -> pd.DataFrame:
    data = []

    for _ in range(N_SAMPLES_TO_GENERATE):
        transaction_id = str(uuid.uuid4())
        user_id = str(random.randrange(1, 9, 1))
        created_at = datetime.utcnow() - timedelta(seconds=random.randrange(0, 3600 * 24))

        amount_eur_cents = 1000 + random.randrange(-200, 200)

        data.append((transaction_id, user_id, created_at, amount_eur_cents))

    df = pd.DataFrame(
        data, columns=["transaction_id", "user_id", "created_at", "amount_eur_cents"]
    )

    return df
