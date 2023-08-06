import json
import logging
import sys

from faker import Faker

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def generate_text_log(seed, config={}, return_value=False):
    Faker.seed(seed)
    Factory = Faker()

    nb_words = config.get("TEXT_WORD_COUNT", 15)
    sentence = Factory.sentence(nb_words=nb_words)
    xid = config.get("TRANSACTION_ID", "")
    if return_value:
        return "{0} {1}".format(sentence, xid)
    else:
        logging.info("{0} {1}".format(sentence, xid))


def generate_kv_log(seed, config={}, return_value=False):
    Faker.seed(seed)
    Factory = Faker()
    profile = Factory.profile()
    profile["xid"] = config.get("TRANSACTION_ID", "")
    # The following fields aren't strings so we will remove them to avoid additional processing.
    del profile["current_location"]
    del profile["website"]
    if return_value:
        return " ".join(["{0}={1}".format(k, v) for k, v in profile.items()])
    else:
        logging.info(
            " ".join(["{0}={1}".format(k, v) for k, v in profile.items()])
        )


def generate_json_log(seed, config={}, return_value=False):
    def json_default(o):
        # Two of the values returned by Faker.profile fail to serialize into json. They are
        # decimal.Decimal and datetime.date.  They both have a __str__ function that we can use
        # to convert the values to a strings.
        return o.__str__()

    Faker.seed(seed)
    Factory = Faker()
    profile = Factory.profile()
    profile["xid"] = config.get("TRANSACTION_ID", "")
    if return_value:
        return json.dumps(profile, default=json_default)
    else:
        logging.info(json.dumps(profile, default=json_default))
