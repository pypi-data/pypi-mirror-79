from reynir_correct.errtokenizer import TOK, CorrectToken, tokenize
from tokenizer import detokenize
from functools import partial


def reynir_correct(text):
    """
    Function that uses Reynir-correct library to correct a text string.
    It returns the corrected string without newlines.
    :param text: Text string
    :return corr_text: Corrected text
    """

    to_text = partial(detokenize, normalize=True)
    """ detokenize is a Utility function in Greynirs Tokenizer to convert an iterable of tokens back
                to a correctly spaced string. If normalize is True,
                punctuation is normalized before assembling the string. """
    # Initialize sentence accumulator list
    curr_sent = []  # type: List[CorrectToken]
    corr_text_lis = list()
    # Normal shallow parse, one line per sentence,
    # tokens separated by spaces

    # One problem with Reynir is trying to capitalize the first letter
    # So we prevent that here, but only if it is the beginning of a page
    f_islo = False
    if text[0].isalpha():
        if text[0].islower():
            f_islo = True

    for t in tokenize(text):
        if t.kind in TOK.END:
            # End of sentence/paragraph
            if curr_sent:
                corr_text_lis.append(to_text(curr_sent))
                curr_sent = []

        else:
            curr_sent.append(t)


    if f_islo:
        tmp_s = corr_text_lis[0][0].lower() + corr_text_lis[0][1:]
        corr_text_lis[0] = tmp_s
    corr_text = " ".join(corr_text_lis)
    corr_text += " ".join(to_text(curr_sent))




    return corr_text
