from .tokenizer import encode, decode, ids_to_b64_uint16_buf, b64_uint16_buf_to_ids
from .api_client import api
import logging

logger = logging.getLogger("corpus.generators.novelai")

GENERATION_DEFAULT_PARAMETERS = {
    "temperature": 0.725,
    "tail_free_sampling": 1,
    "top_k": 69,
    "top_p": 0.85,
    "repetition_penalty": 1.1125,
    "repetition_penalty_range": 800,
    "repetition_penalty_slope": 2.52,
    "bad_words_ids": [[58],[60],[90],[92],[685],[1391],[1782],[2361],[3693],[4083],[4357],[4895],[5512],[5974],[7131],[8183],[8351],[8762],[8964],[8973],[9063],[11208],[11709],[11907],[11919],[12878],[12962],[13018],[13412],[14631],[14692],[14980],[15090],[15437],[16151],[16410],[16589],[17241],[17414],[17635],[17816],[17912],[18083],[18161],[18477],[19629],[19779],[19953],[20520],[20598],[20662],[20740],[21476],[21737],[22133],[22241],[22345],[22935],[23330],[23785],[23834],[23884],[25295],[25597],[25719],[25787],[25915],[26076],[26358],[26398],[26894],[26933],[27007],[27422],[28013],[29164],[29225],[29342],[29565],[29795],[30072],[30109],[30138],[30866],[31161],[31478],[32092],[32239],[32509],[33116],[33250],[33761],[34171],[34758],[34949],[35944],[36338],[36463],[36563],[36786],[36796],[36937],[37250],[37913],[37981],[38165],[38362],[38381],[38430],[38892],[39850],[39893],[41832],[41888],[42535],[42669],[42785],[42924],[43839],[44438],[44587],[44926],[45144],[45297],[46110],[46570],[46581],[46956],[47175],[47182],[47527],[47715],[48600],[48683],[48688],[48874],[48999],[49074],[49082],[49146],[49946],[10221],[4841],[1427],[2602,834],[29343],[37405],[35780],[2602]],
    "use_cache": False,
    "return_full_text": False,
}

MIN_GENERATED_TOKENS = 10
MAX_GENERATED_TOKENS = 60

subscription_data = api.subscription()

if not subscription_data["active"]:
    assert False, "Subscription is not active! Generator unavailable"

MAX_GENERATION_TOKENS = 2040 if subscription_data["perks"]["contextTokens"] == 2048 else subscription_data["perks"]["contextTokens"]
USED_GENERATION_MODEL = "6B"

logger.info("You have %i context tokens available" % MAX_GENERATION_TOKENS)
logger.info("%s generation model will be used" % USED_GENERATION_MODEL)

def generate(input: str, required_start_txt: str) -> str:
    if required_start_txt[-1] != "\n":
        required_start_txt += "\n"
    
    required_start_ids = encode(required_start_txt)
    max_input_tokens = MAX_GENERATION_TOKENS - len(required_start_ids) - MAX_GENERATED_TOKENS

    inputlines = input.splitlines()
    input_ids = encode("\n".join(inputlines))
    
    while len(input_ids) > max_input_tokens:
        inputlines.pop(0)
        input_ids = encode("\n".join(inputlines))

    final_sent_ids = required_start_ids + input_ids

    logger.debug("AI Input:\n'''\n%s\n'''\n" % decode(final_sent_ids))
    
    final_parameters = GENERATION_DEFAULT_PARAMETERS.copy()

    final_parameters["min_length"] = len(final_sent_ids) + MIN_GENERATED_TOKENS
    final_parameters["max_length"] = len(final_sent_ids) + MAX_GENERATED_TOKENS

    output = api.generate(ids_to_b64_uint16_buf(final_sent_ids), USED_GENERATION_MODEL, final_parameters)

    if "error" in output:
        raise ValueError("Generation model error", output["error"])
    else:
        return decode(b64_uint16_buf_to_ids(output["output"]))