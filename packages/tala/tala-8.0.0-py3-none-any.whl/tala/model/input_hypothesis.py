from typing import Text  # noqa: F401


class InputHypothesis(object):
    def __init__(self, utterance, confidence):
        # type: (Text, float) -> None
        self._utterance = utterance
        self._confidence = confidence

    @property
    def utterance(self):
        # type: () -> Text
        return self._utterance

    @property
    def confidence(self):
        # type: () -> float
        return self._confidence

    def __eq__(self, other):
        return self.utterance == other.utterance and self.confidence == other.confidence

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "InputHypothesis(%r, %r)" % (self._utterance, self._confidence)

    def __repr__(self):
        return str(self)
