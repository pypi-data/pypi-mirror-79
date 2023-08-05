import re
import json

from tala.testing.interactions.named_test import InteractionTest
from tala.testing.interactions.turn import UserPassivityTurn, UserInterpretationTurn, SystemUtteranceTurn, \
    RecognitionHypothesesTurn, NotifyStartedTurn, SystemMovesTurn
from tala.model.event_notification import EventNotification


class ParseException(Exception):
    pass


class InteractionTestCompiler(object):
    VALID_TURN_TYPES = ["U>", "S>", "Event>"]

    _turn_matcher = re.compile('^(%s) ?(.*)$' % "|".join(VALID_TURN_TYPES), re.MULTILINE | re.DOTALL)
    _moves_matcher = re.compile(r'([\[{].*[\]}])$')
    _utterance_string_and_confidence_matcher = re.compile(r'(.+) (\$\w+|\d*\.\d+)?$')
    _hypothesis_split_re = re.compile(r'\s*\|\s*')

    def compile_interaction_tests(self, filename, file_):
        self._filename = filename
        self._file = file_
        self._result = []
        self._line_number = 0
        self._test = None
        self._eof = False
        while not self._eof:
            line = self._read_multiline()
            if self._eof:
                self._add_current_test()
            else:
                self._process_line(line)
        return self._result

    def _read_multiline(self):
        multiline = ""
        while True:
            line = self._file.readline()
            if line == "":
                self._eof = True
                break
            self._line_number += 1
            if self._is_comment(line):
                continue
            line = line.rstrip(" \r\n")
            if line.endswith("\\"):
                line = line.rstrip("\\")
                multiline += line
                multiline += "\n"
                continue
            multiline += line
            if not line.endswith(";"):
                break
        return multiline

    def _process_line(self, line):
        if self._is_start_of_test(line):
            self._add_current_test()
            testname = self._get_testname(line)
            self._test = InteractionTest(self._filename, testname, [])
        elif self._is_turn(line):
            turn = self._parse_turn(line)
            self._test.turns.append(turn)
        elif line == "":
            pass
        else:
            raise ParseException(
                "Expected content in line %d of '%s' but got '%s'." %
                (self._line_number, self._filename, line.rstrip("\n"))
            )

    def _is_comment(self, line):
        return line.startswith("#")

    def _is_start_of_test(self, line):
        return line.startswith("--- ")

    @staticmethod
    def _is_turn(line):
        m = InteractionTestCompiler._turn_matcher.search(line)
        return m is not None

    def _add_current_test(self):
        if self._test:
            self._result.append(self._test)

    def _get_testname(self, line):
        return line[4:].rstrip("\n")

    def _parse_turn(self, line):
        match = self._turn_matcher.search(line)
        if match:
            turn_type_string, turn_content_as_string = match.groups()
            turn = self._parse_turn_by_type_string(turn_type_string, turn_content_as_string)
            return turn
        else:
            raise ParseException(
                "Expected one of %s on line %d in '%s' but got '%s'." %
                (self.VALID_TURN_TYPES, self._line_number, self._filename, line.rstrip("\n"))
            )

    def _parse_turn_by_type_string(self, type_string, turn_content_as_string):
        if type_string == "U>":
            return self._parse_user_input_turn(turn_content_as_string)
        elif type_string == "S>":
            return self._parse_system_output_turn(turn_content_as_string)
        elif type_string == "Event>":
            return self._parse_event_turn(turn_content_as_string)
        else:
            raise ParseException(
                "Expected one of %s on line %d in '%s' but got '%s'." %
                (self.VALID_TURN_TYPES, self._line_number, self._filename, turn_content_as_string)
            )

    def _parse_user_input_turn(self, turn_content_as_string):
        if not turn_content_as_string:
            return UserPassivityTurn(self._line_number)
        if self._is_moves_content_string(turn_content_as_string):
            moves, utterance, modality = self._parse_moves_content_string(turn_content_as_string)
            return UserInterpretationTurn(moves, self._line_number, utterance=utterance, modality=modality)
        hypothesis_list = self._get_hypothesis_list(turn_content_as_string)
        return RecognitionHypothesesTurn(hypothesis_list, self._line_number)

    def _parse_system_output_turn(self, turn_content_as_string):
        if self._is_moves_content_string(turn_content_as_string):
            moves, utterance, modality = self._parse_moves_content_string(turn_content_as_string)
            return SystemMovesTurn(moves, self._line_number)
        return SystemUtteranceTurn(turn_content_as_string, self._line_number)

    def _get_hypothesis_list(self, string):
        strings = self._hypothesis_split_re.split(string)
        return list(map(self._parse_hypothesis_as_string, strings))

    def _is_moves_content_string(self, string):
        return self._moves_matcher.search(string)

    def _parse_moves_content_string(self, string):
        def create_result(moves, utterance=None, modality=None):
            return moves, utterance, modality

        def extract(json_value):
            if isinstance(json_value, list):
                return create_result(moves=json_value)
            if isinstance(json_value, dict):
                interpretation = json_value
                return create_result(
                    interpretation["moves"],
                    interpretation.get("utterance"),
                    interpretation.get("modality")
                )  # yapf: disable
            raise RuntimeError(f"Expected a list or dict but got {json_value!r}")

        m = self._moves_matcher.search(string)
        if not m:
            raise ParseException(
                "Expected a list of moves or an interpretation object on line %d in '%s' but got '%s'." %
                (self._line_number, self._filename, string)
            )
        (string, ) = m.groups()
        try:
            json_value = json.loads(string)
        except json.decoder.JSONDecodeError as exception:
            raise ParseException(
                f"Expected valid JSON on line {self._line_number} of '{self._filename}' "
                f"but encountered a decoding error.\n\n"
                f"  Line {self._line_number}: {string}\n\n"
                f"  Error: '{exception}'"
            )
        return extract(json_value)

    def _parse_hypothesis_as_string(self, unicode_string):
        m = self._utterance_string_and_confidence_matcher.search(unicode_string)
        if m:
            (utterance_string_unicode, confidence) = m.groups()
            return (utterance_string_unicode, confidence)
        else:
            return (unicode_string, None)

    def _parse_event_turn(self, string):
        try:
            json_dict = json.loads(string)
        except Exception as json_exception:
            raise ParseException(
                "Expected a JSON parseable string on line %d in '%s' but got '%s'. JSON exception: %s" %
                (self._line_number, self._filename, string, json_exception)
            )
        if json_dict["status"] == EventNotification.STARTED:
            return NotifyStartedTurn(json_dict["name"], json_dict["parameters"], self._line_number)
        else:
            raise ParseException(
                f"Expected a supported event turn on line {self._line_number} in '{self._filename}' but got '{string}'."
            )

    @classmethod
    def pretty_passivity(cls):
        return "U>"

    @classmethod
    def pretty_system_utterance(cls, utterance):
        return "S> %s" % utterance

    @classmethod
    def pretty_hypotheses(cls, hypotheses):
        hypothesis_strings = [cls._pretty_hypothesis(hypothesis) for hypothesis in hypotheses]
        utterances_with_confidence = " | ".join(hypothesis_strings)
        return "U> %s" % utterances_with_confidence

    @classmethod
    def _pretty_hypothesis(cls, hypothesis):
        utterance, confidence = hypothesis
        if confidence == 1.0:
            return utterance
        return "%s %s" % (utterance, confidence)
